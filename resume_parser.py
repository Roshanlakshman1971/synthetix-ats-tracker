"""
Resume Parser & Structural ATS Audit Module.
Scans PDF, DOCX, TXT, or Markdown resumes, extracts structured sections,
and audits for ATS parser blockers (tables, placeholders, missing headers, contact gaps).
"""

import io
import os
import re
from typing import Dict, List, Any, Tuple

try:
    from pypdf import PdfReader
except ImportError:
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        PdfReader = None

try:
    import docx
except ImportError:
    docx = None


STANDARD_SECTION_PATTERNS = {
    "summary": r"^(?:professional\s+summary|executive\s+summary|summary|profile|objective|about\s+me)\b",
    "experience": r"^(?:work\s+experience|professional\s+experience|experience|employment\s+history|career\s+history)\b",
    "skills": r"^(?:technical\s+skills|core\s+competencies|skills|key\s+skills|technologies|tools\s*&\s*technologies)\b",
    "education": r"^(?:education|academic\s+background|educational\s+qualifications|academics)\b",
    "achievements": r"^(?:key\s+achievements|achievements|accomplishments|awards|highlights)\b",
    "certifications": r"^(?:certifications|courses|licenses\s*&\s*certifications|training|courses\s*&\s*certifications)\b",
    "projects": r"^(?:projects|key\s+projects|academic\s+projects)\b",
    "languages": r"^(?:languages|language\s+proficiency)\b",
}

PLACEHOLDER_REGEX = re.compile(
    r"(\[\s*insert[^\]]*\]|\[\s*xx+[^\]]*\]|\[\s*tbd[^\]]*\]|<\s*insert[^>]*>|\bTBD\b|\bTODO\b)",
    re.IGNORECASE,
)

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
PHONE_REGEX = re.compile(r"(?:\+?\d{1,3}[\s-]?)?(?:\d{10}|\d{3}[\s-]\d{3}[\s-]\d{4}|\d{5}[\s-]\d{5})")
LINKEDIN_REGEX = re.compile(r"(?:linkedin\.com/in/[a-zA-Z0-9_-]+)", re.IGNORECASE)


def extract_text_from_file(file_obj_or_path: Any, filename: str = "") -> Tuple[str, Dict[str, Any]]:
    """
    Extracts raw text and formatting metadata from PDF, DOCX, TXT, or MD files.
    Returns (extracted_text, metadata_dict).
    """
    meta = {
        "filename": filename or ( file_obj_or_path if isinstance(file_obj_or_path, str) else "uploaded_resume" ),
        "file_type": "unknown",
        "has_tables": False,
        "table_count": 0,
        "has_headers_footers": False,
        "page_count": 1,
        "parser_warnings": [],
    }

    ext = os.path.splitext(meta["filename"])[1].lower()
    if isinstance(file_obj_or_path, str) and os.path.exists(file_obj_or_path):
        with open(file_obj_or_path, "rb") as f:
            raw_bytes = f.read()
    elif hasattr(file_obj_or_path, "read"):
        raw_bytes = file_obj_or_path.read()
        if hasattr(file_obj_or_path, "seek"):
            file_obj_or_path.seek(0)
    elif isinstance(file_obj_or_path, bytes):
        raw_bytes = file_obj_or_path
    else:
        raise ValueError("Unsupported file input provided to extract_text_from_file")

    if ext == ".pdf":
        meta["file_type"] = "PDF"
        if PdfReader is None:
            raise RuntimeError("pypdf is required to parse PDF resumes. Run: pip install pypdf")
        reader = PdfReader(io.BytesIO(raw_bytes))
        meta["page_count"] = len(reader.pages)
        pages_text = []
        for idx, page in enumerate(reader.pages):
            txt = page.extract_text() or ""
            pages_text.append(txt)
        full_text = "\n".join(pages_text)
        if len(full_text.strip()) < 80:
            meta["parser_warnings"].append(
                "PDF contains very little selectable text. It may be a scanned image PDF, which enterprise ATS parsers cannot read."
            )
        return full_text, meta

    elif ext == ".docx":
        meta["file_type"] = "DOCX"
        if docx is None:
            raise RuntimeError("python-docx is required to parse DOCX resumes. Run: pip install python-docx")
        doc = docx.Document(io.BytesIO(raw_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        table_texts = []
        if len(doc.tables) > 0:
            meta["has_tables"] = True
            meta["table_count"] = len(doc.tables)
            meta["parser_warnings"].append(
                f"Detected {len(doc.tables)} table(s) in DOCX. Legacy ATS systems (Taleo, older Workday parsers) often scramble or drop text inside tables."
            )
            for table in doc.tables:
                for row in table.rows:
                    row_cells = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                    if row_cells:
                        table_texts.append(" | ".join(dict.fromkeys(row_cells)))

        for section in doc.sections:
            header_txt = " ".join(p.text.strip() for p in section.header.paragraphs if p.text.strip())
            footer_txt = " ".join(p.text.strip() for p in section.footer.paragraphs if p.text.strip())
            if header_txt or footer_txt:
                meta["has_headers_footers"] = True
                if EMAIL_REGEX.search(header_txt) or PHONE_REGEX.search(header_txt):
                    meta["parser_warnings"].append(
                        "Contact details detected inside the Word Header/Footer. Many ATS parsers ignore headers and footers—keep name, email, and phone in the main document body."
                    )

        full_text = "\n".join(paragraphs)
        if table_texts:
            full_text += "\n" + "\n".join(table_texts)
        return full_text, meta

    else:
        meta["file_type"] = ext.upper().lstrip(".") or "TEXT"
        full_text = raw_bytes.decode("utf-8", errors="replace")
        if "|" in full_text and "---" in full_text:
            meta["has_tables"] = True
            meta["parser_warnings"].append(
                "Detected Markdown tables in resume text. Convert tables to clean bullet points or inline lines for maximum ATS compatibility."
            )
        return full_text, meta


def parse_resume_structure(raw_text: str, file_meta: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Parses raw resume text into structured sections, contact details,
    quantified metrics, and structural ATS audit findings.
    """
    file_meta = file_meta or {}
    lines = [line.strip() for line in raw_text.splitlines()]
    non_empty_lines = [l for l in lines if l]

    # 1. Extract Contact Details
    emails = EMAIL_REGEX.findall(raw_text)
    phones = PHONE_REGEX.findall(raw_text)
    linkedins = LINKEDIN_REGEX.findall(raw_text)

    # Candidate name heuristic: first non-empty line stripped of markdown #
    candidate_name = "Candidate"
    target_headline = ""
    for i, line in enumerate(non_empty_lines[:5]):
        clean_line = re.sub(r"^[#*\s-]+|[#*\s-]+$", "", line).strip()
        if clean_line and not EMAIL_REGEX.search(clean_line) and not PHONE_REGEX.search(clean_line):
            if len(clean_line.split()) <= 5 and not any(ch.isdigit() for ch in clean_line):
                candidate_name = clean_line
                if i + 1 < len(non_empty_lines):
                    next_clean = re.sub(r"^[#*\s-]+|[#*\s-]+$", "", non_empty_lines[i + 1]).strip()
                    if len(next_clean.split()) <= 8 and not EMAIL_REGEX.search(next_clean) and not PHONE_REGEX.search(next_clean):
                        target_headline = next_clean
                break

    # Location heuristic
    location = ""
    loc_match = re.search(
        r"\b(Bangalore|Bengaluru|Hyderabad|Mumbai|Pune|Chennai|Delhi|Gurgaon|Noida|India|Remote)\b",
        raw_text[:600],
        re.IGNORECASE,
    )
    if loc_match:
        location = loc_match.group(1)

    # 2. Segment Sections
    sections: Dict[str, List[str]] = {k: [] for k in STANDARD_SECTION_PATTERNS}
    sections["header"] = []
    current_section = "header"

    for line in non_empty_lines:
        clean_header = re.sub(r"^[#*\s:-]+|[#*\s:-]+$", "", line).strip()
        matched_section = None
        if len(clean_header.split()) <= 5:
            for sec_key, pattern in STANDARD_SECTION_PATTERNS.items():
                if re.match(pattern, clean_header, re.IGNORECASE):
                    matched_section = sec_key
                    break
        if matched_section:
            current_section = matched_section
        else:
            sections[current_section].append(line)

    # 3. Detect Unfilled Placeholders (e.g., [Insert %], [TBD])
    placeholders_found = PLACEHOLDER_REGEX.findall(raw_text)

    # 4. Extract Quantified Impact Bullets (%, $, ₹, numbers with time/scale units)
    metric_pattern = re.compile(
        r"(\b\d+(?:\.\d+)?%|\b\d+\+?\s*(?:years?|months?|hrs?|hours?|mins?|minutes?|days?|clients?|users?|tickets?|incidents?|team|members?|engineers?|projects?|SLAs?|P1|P2)\b|(?:₹|\$|USD|INR)\s*\d+)",
        re.IGNORECASE,
    )
    experience_lines = sections.get("experience", []) + sections.get("achievements", [])
    quantified_bullets = [
        line for line in experience_lines if metric_pattern.search(line) and len(line.split()) >= 6
    ]

    # 5. Build Structural Audit Warnings
    audit_issues = list(file_meta.get("parser_warnings", []))
    if placeholders_found:
        audit_issues.append(
            f"CRITICAL BLOCKER: Unfilled placeholder text detected ({', '.join(set(placeholders_found))}). Instant rejection trigger for recruiters and ATS screening."
        )
    if not emails:
        audit_issues.append("Missing email address in main body text.")
    if not phones:
        audit_issues.append("Missing phone number in main body text.")
    if not sections["summary"]:
        audit_issues.append("Missing dedicated Summary / Profile section heading.")
    if not sections["experience"]:
        audit_issues.append("Missing clearly labeled Experience / Work History section heading.")
    if not sections["skills"]:
        audit_issues.append("Missing dedicated Skills section heading.")
    if not sections["education"]:
        audit_issues.append("Missing dedicated Education section heading.")
    if len(quantified_bullets) < 3:
        audit_issues.append(
            f"Low quantified metric density: Only {len(quantified_bullets)} bullet(s) contain measurable numbers/percentages. Aim for at least 5–8 quantified impact statements."
        )

    return {
        "candidate_name": candidate_name,
        "target_headline": target_headline,
        "contact": {
            "email": emails[0] if emails else "",
            "phone": phones[0] if phones else "",
            "location": location or "Bangalore, India",
            "linkedin": linkedins[0] if linkedins else "",
        },
        "sections": {k: "\n".join(v) for k, v in sections.items() if v},
        "raw_text": raw_text,
        "word_count": len(raw_text.split()),
        "placeholders_found": list(set(placeholders_found)),
        "quantified_bullets_count": len(quantified_bullets),
        "quantified_bullets": quantified_bullets,
        "file_meta": file_meta,
        "audit_issues": audit_issues,
    }

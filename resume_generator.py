"""
ATS-Compliant Resume File Generator.
Exports the rewritten structured resume into clean, single-column,
zero-table DOCX, Markdown (.md), and Plain Text (.txt) files that pass
Workday, Taleo, Greenhouse, Lever, iCIMS, and Naukri parsers without formatting loss.
Includes a zero-dependency native OpenXML (.docx) builder so DOCX generation works
even if python-docx is not installed in the active Python environment.
"""

import io
import os
import re
import zipfile
from datetime import datetime
from typing import Dict, Any
from xml.sax.saxutils import escape

try:
    import docx
    from docx.shared import Pt, Inches, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
except ImportError:
    docx = None


def generate_ats_docx_bytes(resume_data: Dict[str, Any]) -> bytes:
    """
    Builds a clean, single-column, ATS-friendly Word Document (.docx) in memory
    and returns raw bytes. Uses python-docx if installed, or falls back to a
    native OpenXML (.docx) builder using Python's standard library.
    """
    if docx is not None:
        return _generate_docx_with_python_docx(resume_data)
    return _generate_docx_native_openxml(resume_data)


def _generate_docx_with_python_docx(resume_data: Dict[str, Any]) -> bytes:
    doc = docx.Document()

    for section in doc.sections:
        section.top_margin = Inches(0.6)
        section.bottom_margin = Inches(0.6)
        section.left_margin = Inches(0.65)
        section.right_margin = Inches(0.65)

    style = doc.styles["Normal"]
    font = style.font
    font.name = "Calibri"
    font.size = Pt(10.5)
    font.color.rgb = RGBColor(0x1F, 0x29, 0x37)

    name_p = doc.add_paragraph()
    name_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    name_p.paragraph_format.space_after = Pt(2)
    name_run = name_p.add_run(resume_data.get("name", "ROSHAN L").upper())
    name_run.bold = True
    name_run.font.size = Pt(18)
    name_run.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    headline_p = doc.add_paragraph()
    headline_p.paragraph_format.space_after = Pt(2)
    headline_run = headline_p.add_run(resume_data.get("headline", ""))
    headline_run.bold = True
    headline_run.font.size = Pt(11.5)
    headline_run.font.color.rgb = RGBColor(0x1D, 0x4E, 0xD8)

    contact_p = doc.add_paragraph()
    contact_p.paragraph_format.space_after = Pt(8)
    contact_run = contact_p.add_run(resume_data.get("contact_line", ""))
    contact_run.font.size = Pt(10)
    contact_run.font.color.rgb = RGBColor(0x4B, 0x55, 0x63)

    def add_section_heading(title: str):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        run = p.add_run(title.upper())
        run.bold = True
        run.font.size = Pt(11.5)
        run.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    add_section_heading("PROFESSIONAL SUMMARY")
    sum_p = doc.add_paragraph(resume_data.get("summary", ""))
    sum_p.paragraph_format.space_after = Pt(6)

    add_section_heading("CORE SKILLS & TECHNICAL COMPETENCIES")
    for category, skills in resume_data.get("core_skills", {}).items():
        sp = doc.add_paragraph()
        sp.paragraph_format.space_after = Pt(2)
        cat_run = sp.add_run(f"{category}: ")
        cat_run.bold = True
        skill_str = ", ".join(skills) if isinstance(skills, list) else str(skills)
        sp.add_run(skill_str)

    add_section_heading("PROFESSIONAL EXPERIENCE")
    for exp in resume_data.get("experience", []):
        role_p = doc.add_paragraph()
        role_p.paragraph_format.space_before = Pt(5)
        role_p.paragraph_format.space_after = Pt(1)
        r_run = role_p.add_run(f"{exp.get('role', '')} | {exp.get('company', '')}")
        r_run.bold = True
        r_run.font.size = Pt(11)

        meta_p = doc.add_paragraph()
        meta_p.paragraph_format.space_after = Pt(3)
        m_run = meta_p.add_run(f"{exp.get('dates', '')} | {exp.get('location', '')}")
        m_run.italic = True
        m_run.font.size = Pt(9.5)
        m_run.font.color.rgb = RGBColor(0x4B, 0x55, 0x63)

        for bullet in exp.get("bullets", []):
            bp = doc.add_paragraph(style="List Bullet")
            bp.paragraph_format.space_after = Pt(2)
            bp.add_run(bullet)

    if resume_data.get("achievements"):
        add_section_heading("KEY ACHIEVEMENTS")
        for ach in resume_data["achievements"]:
            ap = doc.add_paragraph(style="List Bullet")
            ap.paragraph_format.space_after = Pt(2)
            if ":" in ach:
                lead, rest = ach.split(":", 1)
                lead_run = ap.add_run(f"{lead}:")
                lead_run.bold = True
                ap.add_run(rest)
            else:
                ap.add_run(ach)

    if resume_data.get("education"):
        add_section_heading("EDUCATION")
        for edu in resume_data["education"]:
            ep = doc.add_paragraph(style="List Bullet")
            ep.paragraph_format.space_after = Pt(2)
            ep.add_run(edu)

    if resume_data.get("certifications"):
        add_section_heading("CERTIFICATIONS & COURSES")
        for cert in resume_data["certifications"]:
            cp = doc.add_paragraph(style="List Bullet")
            cp.paragraph_format.space_after = Pt(2)
            cp.add_run(cert)

    if resume_data.get("languages"):
        add_section_heading("LANGUAGES")
        lp = doc.add_paragraph(resume_data["languages"])
        lp.paragraph_format.space_after = Pt(4)

    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()


def _generate_docx_native_openxml(resume_data: Dict[str, Any]) -> bytes:
    """
    Zero-dependency OpenXML (.docx) generator using standard library zipfile.
    Produces a valid, ATS-compliant Word document with clean Calibri formatting.
    """
    paragraphs_xml = []

    def add_p(text: str, bold: bool = False, italic: bool = False, size_half_pt: int = 21, color: str = "1F2937", space_before: int = 0, space_after: int = 80):
        rpr = f'<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="{size_half_pt}"/><w:color w:val="{color}"/>'
        if bold:
            rpr += "<w:b/>"
        if italic:
            rpr += "<w:i/>"
        ppr = f'<w:spacing w:before="{space_before}" w:after="{space_after}"/>'
        paragraphs_xml.append(
            f'<w:p><w:pPr>{ppr}</w:pPr><w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>'
        )

    add_p(resume_data.get("name", "ROSHAN L").upper(), bold=True, size_half_pt=36, color="0F172A", space_after=40)
    add_p(resume_data.get("headline", ""), bold=True, size_half_pt=23, color="1D4ED8", space_after=40)
    add_p(resume_data.get("contact_line", ""), size_half_pt=20, color="4B5563", space_after=140)

    add_p("PROFESSIONAL SUMMARY", bold=True, size_half_pt=23, color="0F172A", space_before=120, space_after=60)
    add_p(resume_data.get("summary", ""), size_half_pt=21, space_after=120)

    add_p("CORE SKILLS & TECHNICAL COMPETENCIES", bold=True, size_half_pt=23, color="0F172A", space_before=120, space_after=60)
    for category, skills in resume_data.get("core_skills", {}).items():
        skill_str = ", ".join(skills) if isinstance(skills, list) else str(skills)
        add_p(f"• {category}: {skill_str}", size_half_pt=21, space_after=40)

    add_p("PROFESSIONAL EXPERIENCE", bold=True, size_half_pt=23, color="0F172A", space_before=120, space_after=60)
    for exp in resume_data.get("experience", []):
        add_p(f"{exp.get('role', '')} | {exp.get('company', '')}", bold=True, size_half_pt=22, space_before=100, space_after=20)
        add_p(f"{exp.get('dates', '')} | {exp.get('location', '')}", italic=True, size_half_pt=19, color="4B5563", space_after=60)
        for bullet in exp.get("bullets", []):
            add_p(f"• {bullet}", size_half_pt=21, space_after=40)

    if resume_data.get("achievements"):
        add_p("KEY ACHIEVEMENTS", bold=True, size_half_pt=23, color="0F172A", space_before=120, space_after=60)
        for ach in resume_data["achievements"]:
            add_p(f"• {ach}", size_half_pt=21, space_after=40)

    if resume_data.get("education"):
        add_p("EDUCATION", bold=True, size_half_pt=23, color="0F172A", space_before=120, space_after=60)
        for edu in resume_data["education"]:
            add_p(f"• {edu}", size_half_pt=21, space_after=40)

    if resume_data.get("certifications"):
        add_p("CERTIFICATIONS & COURSES", bold=True, size_half_pt=23, color="0F172A", space_before=120, space_after=60)
        for cert in resume_data["certifications"]:
            add_p(f"• {cert}", size_half_pt=21, space_after=40)

    if resume_data.get("languages"):
        add_p("LANGUAGES", bold=True, size_half_pt=23, color="0F172A", space_before=120, space_after=60)
        add_p(resume_data["languages"], size_half_pt=21, space_after=80)

    document_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        "<w:body>"
        + "".join(paragraphs_xml)
        + '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="864" w:right="936" w:bottom="864" w:left="936"/></w:sectPr>'
        "</w:body></w:document>"
    )

    content_types_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        "</Types>"
    )

    rels_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        "</Relationships>"
    )

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types_xml)
        zf.writestr("_rels/.rels", rels_xml)
        zf.writestr("word/document.xml", document_xml)
    return buf.getvalue()


def save_tailored_resume_files(
    resume_data: Dict[str, Any],
    output_dir: str,
    target_role_title: str = "",
    company_name: str = "",
) -> Dict[str, str]:
    """
    Saves tailored resume files (.docx, .md, .txt) into output_dir and returns their file paths.
    """
    os.makedirs(output_dir, exist_ok=True)
    slug_parts = [
        re.sub(r"[^a-zA-Z0-9]+", "_", resume_data.get("name", "Roshan_L")).strip("_"),
    ]
    if company_name.strip():
        slug_parts.append(re.sub(r"[^a-zA-Z0-9]+", "_", company_name.strip()).strip("_"))
    if target_role_title.strip():
        slug_parts.append(re.sub(r"[^a-zA-Z0-9]+", "_", target_role_title.strip()).strip("_"))
    else:
        slug_parts.append("ATS_Tailored_Resume")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    base_name = "_".join(slug_parts) + f"_{timestamp}"

    paths = {}
    md_text = resume_data.get("markdown_text", "")

    # Save DOCX (Always works via python-docx or native OpenXML fallback)
    docx_bytes = generate_ats_docx_bytes(resume_data)
    docx_path = os.path.join(output_dir, f"{base_name}.docx")
    with open(docx_path, "wb") as f:
        f.write(docx_bytes)
    paths["docx"] = docx_path

    # Save Markdown
    md_path = os.path.join(output_dir, f"{base_name}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_text)
    paths["markdown"] = md_path

    # Save Plain Text
    txt_path = os.path.join(output_dir, f"{base_name}.txt")
    plain_text = re.sub(r"[#*]", "", md_text)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(plain_text)
    paths["txt"] = txt_path

    return paths

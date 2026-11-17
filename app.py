"""
Streamlit Live ATS Tracker & Human Resume Rewriter Web App.
Step-by-step interactive pipeline:
  Step 1: Upload / Scan Resume & View Structural Audit
  Step 2: Enter Target Job Description (Auto-detects relevant Enterprise ATS)
  Step 3: Run Live Multi-Factor ATS Score & Keyword Gap Diagnostic
  Step 4: Generate Human-Written, Best-Match Resume File (.docx / .md / .txt) with Before vs. After Score
"""

import os
import streamlit as st

from resume_parser import extract_text_from_file, parse_resume_structure
from ats_engine import (
    evaluate_resume_against_jd,
    rewrite_resume_human_and_ats_optimized,
)
from resume_generator import generate_ats_docx_bytes, save_tailored_resume_files

st.set_page_config(
    page_title="Live ATS Tracker & Human Resume Rewriter",
    page_icon="🎯",
    layout="wide",
)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
SAMPLE_RESUME_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_roshan_resume.md")

# Sidebar Configuration
with st.sidebar:
    st.title("⚙️ ATS Engine Settings")
    st.caption("Configure optional Gemini AI deep rewriting or run 100% locally.")
    gemini_key = st.text_input(
        "Gemini API Key (Optional)",
        value=os.environ.get("GEMINI_API_KEY", ""),
        type="password",
        help="Leave blank to use the built-in Local Enterprise ATS + Human XYZ Rewriter (zero API quota needed).",
    )
    st.markdown("---")
    st.subheader("Supported ATS Profiles")
    st.markdown(
        "- **Workday ATS** (Canonical skills + chronology)\n"
        "- **Oracle Taleo / iCIMS** (Exact + acronym frequency)\n"
        "- **Greenhouse / Lever** (Quantified XYZ impact)\n"
        "- **Naukri RMS / Enterprise Hybrid**"
    )

st.title("🎯 Live ATS Tracker & Human Resume Rewriter")
st.markdown(
    "**Step 1:** Scan your resume → **Step 2:** Paste the Job Description → "
    "**Step 3:** Get your multi-factor ATS Score → **Step 4:** Generate a tailored, human-written resume file (`.docx`, `.md`, `.txt`) ready to land the interview."
)

# ---------------------------------------------------------------------------
# STEP 1: SCAN RESUME
# ---------------------------------------------------------------------------
st.header("Step 1: Scan Your Resume")
col_up1, col_up2 = st.columns([2, 1])

with col_up1:
    uploaded_file = st.file_uploader(
        "Upload your current resume (.pdf, .docx, .txt, or .md)",
        type=["pdf", "docx", "txt", "md"],
    )
with col_up2:
    use_preloaded = st.checkbox(
        "Use Roshan's baseline resume (`Roshan_New_resume`)",
        value=(uploaded_file is None and os.path.exists(SAMPLE_RESUME_PATH)),
    )

parsed_resume = None
if uploaded_file is not None:
    raw_text, file_meta = extract_text_from_file(uploaded_file, uploaded_file.name)
    parsed_resume = parse_resume_structure(raw_text, file_meta)
elif use_preloaded and os.path.exists(SAMPLE_RESUME_PATH):
    raw_text, file_meta = extract_text_from_file(SAMPLE_RESUME_PATH, "sample_roshan_resume.md")
    parsed_resume = parse_resume_structure(raw_text, file_meta)

if parsed_resume:
    st.success(
        f"✅ Resume Scanned: **{parsed_resume['candidate_name']}** "
        f"({parsed_resume['word_count']} words, {parsed_resume['quantified_bullets_count']} quantified impact bullets detected)"
    )

    with st.expander("🔍 View Initial Resume Scan & Structural ATS Audit", expanded=True):
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Candidate", parsed_resume["candidate_name"])
        m2.metric("Detected Headline", parsed_resume["target_headline"] or "Not Set")
        m3.metric("Quantified Bullets", parsed_resume["quantified_bullets_count"])
        m4.metric("Unfilled Placeholders", len(parsed_resume["placeholders_found"]))

        if parsed_resume["audit_issues"]:
            st.warning("**Initial ATS Structural Findings found during scan:**")
            for issue in parsed_resume["audit_issues"]:
                st.write(f"- ⚠️ {issue}")
        else:
            st.info("No structural parser blockers detected in baseline scan.")

    # ---------------------------------------------------------------------------
    # STEP 2: ASK FOR JOB DESCRIPTION
    # ---------------------------------------------------------------------------
    st.header("Step 2: Enter the Target Job Description")
    st.info("👇 Paste the Job Description below so the tracker can run the relevant ATS simulation against your scanned resume.")

    c_role, c_comp = st.columns(2)
    with c_role:
        target_role_title = st.text_input(
            "Target Job Title (e.g., Incident Manager, Data Analyst, Project Manager)",
            placeholder="Incident Manager / Data Analyst",
        )
    with c_comp:
        company_name = st.text_input(
            "Target Company Name (Optional)",
            placeholder="e.g., Microsoft, Wipro, ANZ, Target",
        )

    jd_text = st.text_area(
        "Paste Full Job Description (Responsibilities, Requirements, Skills)",
        height=220,
        placeholder="Paste the complete job posting here...",
    )

    run_btn = st.button("🚀 Step 3 & 4: Run Live ATS Analysis & Generate Human-Rewritten Resume", type="primary")

    if run_btn:
        if not jd_text.strip() or len(jd_text.strip()) < 30:
            st.error("Please paste a valid Job Description (at least 30 characters) to run the ATS comparison.")
        else:
            # ---------------------------------------------------------------------------
            # STEP 3: RUN RELEVANT ATS & SCORE
            # ---------------------------------------------------------------------------
            with st.spinner("Running Enterprise ATS Simulation & Multi-Factor Scoring..."):
                ats_before = evaluate_resume_against_jd(parsed_resume, jd_text, target_role_title)

            st.header("Step 3: Live ATS Diagnostic Scorecard (Original Resume)")
            st.caption(
                f"**Detected ATS Engine:** `{ats_before['ats_profile']['platform']}` — {ats_before['ats_profile']['focus']}"
            )

            sc1, sc2 = st.columns([1, 2])
            with sc1:
                st.metric("Original Resume ATS Score", f"{ats_before['overall_score']} / 100")
                st.markdown(f"**Verdict:** :{ats_before['verdict_color']}[{ats_before['verdict']}]")
                st.write(f"**Detected Role Family:** {ats_before['detected_role_family']}")

            with sc2:
                st.subheader("5-Pillar ATS Sub-Scores")
                for label, val in ats_before["sub_scores"].items():
                    st.progress(int(val), text=f"{label}: **{val}%**")

            kw_col1, kw_col2 = st.columns(2)
            with kw_col1:
                st.subheader(f"✅ Matched JD Keywords ({len(ats_before['matched_keywords'])})")
                if ats_before["matched_keywords"]:
                    for item in ats_before["matched_keywords"]:
                        badge = "🟢 Exact+Acronym" if "Exact" in item["status"] else "🟡 Partial"
                        st.write(
                            f"- **{item['canonical']}** ({item['priority']}) — {badge} "
                            f"*(JD: {item['jd_mentions']}x | Resume: {item['resume_mentions']}x)*"
                        )
                else:
                    st.write("No core JD keywords matched yet.")

            with kw_col2:
                st.subheader(f"❌ Missing JD Keywords ({len(ats_before['missing_keywords'])})")
                if ats_before["missing_keywords"]:
                    for item in ats_before["missing_keywords"]:
                        st.write(
                            f"- **{item['canonical']}** ({item['priority']} Priority — mentioned {item['jd_mentions']}x in JD)"
                        )
                else:
                    st.success("All primary JD keywords are already present!")

            if ats_before["cliche_hits"] or ats_before["placeholders_found"]:
                with st.expander("🗣️ Human-Voice & Readability Audit (Why Recruiters Reject Generic Resumes)", expanded=True):
                    if ats_before["placeholders_found"]:
                        st.error(
                            f"**Unfilled Placeholders Found:** `{', '.join(ats_before['placeholders_found'])}` — "
                            "Automatically replaced with verified metrics in Step 4 below."
                        )
                    if ats_before["cliche_hits"]:
                        st.warning("**Overused AI / Passive Phrases Detected in Original Resume:**")
                        for hit in ats_before["cliche_hits"]:
                            st.write(f"- Replace *\"{hit['phrase']}\"* → **{hit['suggestion']}**")

            # ---------------------------------------------------------------------------
            # STEP 4: REWRITE RESUME IN HUMAN VOICE & GENERATE FILES
            # ---------------------------------------------------------------------------
            st.header("Step 4: Tailored, Human-Written Resume & Score Jump")
            with st.spinner("Rewriting resume in natural human XYZ style and embedding missing JD keywords..."):
                rewritten_data = rewrite_resume_human_and_ats_optimized(
                    parsed_resume=parsed_resume,
                    ats_eval=ats_before,
                    jd_text=jd_text,
                    target_role_title=target_role_title,
                    company_name=company_name,
                    gemini_api_key=gemini_key,
                )
                saved_paths = save_tailored_resume_files(
                    resume_data=rewritten_data,
                    output_dir=OUTPUT_DIR,
                    target_role_title=target_role_title,
                    company_name=company_name,
                )
                # Re-score the newly generated resume to verify the ATS jump!
                new_parsed = parse_resume_structure(rewritten_data["markdown_text"], {"filename": "tailored_resume.docx"})
                ats_after = evaluate_resume_against_jd(new_parsed, jd_text, target_role_title)

            jump = ats_after["overall_score"] - ats_before["overall_score"]
            j1, j2, j3 = st.columns(3)
            j1.metric("Original ATS Score", f"{ats_before['overall_score']}%")
            j2.metric("New Tailored ATS Score", f"{ats_after['overall_score']}%", delta=f"+{jump}% improvement")
            j3.metric("Missing Keywords Remaining", len(ats_after["missing_keywords"]), delta=f"-{len(ats_before['missing_keywords']) - len(ats_after['missing_keywords'])} gaps closed")

            st.success(
                f"🎉 **New Tailored Resume Saved to `/Users/roshanl/ATS/output/`!** "
                f"(Engine: {rewritten_data.get('engine_used', 'Human-Voice XYZ Optimizer')})"
            )

            st.subheader("What Was Improved to Help You Land the Interview")
            for note in rewritten_data.get("rewrite_notes", []):
                st.write(f"- ✔️ {note}")

            # Download buttons
            dl1, dl2, dl3 = st.columns(3)
            if "docx" in saved_paths and os.path.exists(saved_paths["docx"]):
                with open(saved_paths["docx"], "rb") as f:
                    docx_bytes = f.read()
                dl1.download_button(
                    label="📥 Download Tailored Resume (.DOCX)",
                    data=docx_bytes,
                    file_name=os.path.basename(saved_paths["docx"]),
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
            dl2.download_button(
                label="📥 Download Tailored Resume (.MD)",
                data=rewritten_data["markdown_text"],
                file_name=os.path.basename(saved_paths["markdown"]),
                mime="text/markdown",
            )
            with open(saved_paths["txt"], "r", encoding="utf-8") as f:
                txt_data = f.read()
            dl3.download_button(
                label="📥 Download Plain-Text ATS Copy (.TXT)",
                data=txt_data,
                file_name=os.path.basename(saved_paths["txt"]),
                mime="text/plain",
            )

            st.subheader("📄 Live Preview of Your New Human-Written, ATS-Optimized Resume")
            st.markdown(rewritten_data["markdown_text"])

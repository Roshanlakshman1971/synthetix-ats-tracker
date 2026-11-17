# Live ATS Tracker & Human Resume Rewriter

An end-to-end **Enterprise ATS Simulator & Human-Voice Resume Rewriter** located in `/Users/roshanl/ATS`.

## How It Works (4-Stage Workflow)
1. **Stage 1 — Deep Resume Scan & Structural Audit (`resume_parser.py`)**:
   - Reads `.pdf`, `.docx`, `.txt`, or `.md` resumes.
   - Audits for silent ATS rejection triggers before you even apply: unfilled placeholders (such as `[Insert %]` in your baseline resume), parser-breaking tables, contact details hidden in Word headers/footers, and low quantified metric density.
2. **Stage 2 — Job Description Intake & ATS Profile Detection (`ats_engine.py`)**:
   - Prompts for the target Job Description, Role Title, and Company.
   - Automatically detects the relevant enterprise ATS rule profile (**Workday**, **Oracle Taleo / iCIMS**, **Greenhouse / Lever**, or **Naukri / Enterprise Hybrid**) and extracts weighted requirement tiers (Critical vs. High priority).
3. **Stage 3 — Multi-Factor ATS Scoring (0–100%)**:
   - Evaluates your resume across 5 weighted pillars:
     - **Keyword & Hard Skills Match (40%)** — Checks both exact terms and acronym pairs (`ServiceNow (SNOW)`, `Root Cause Analysis (RCA)`, `Mean Time to Resolve (MTTR)`, `Service Level Agreement (SLA)`).
     - **Role & Headline Alignment (20%)** — Checks whether your headline and summary match the JD's target role family.
     - **Quantified Impact & Metrics (15%)** — Measures concrete numbers, percentages, and SLA/MTTR outcomes.
     - **Human Voice & Active Tone (15%)** — Flags generic AI buzzwords (*"spearheaded"*, *"utilized"*, *"leveraging"*, *"holistic"*) and passive phrasing.
     - **ATS Parseability & Hygiene (10%)** — Verifies standard section headings and zero placeholders.
4. **Stage 4 — Human-Written Resume Rewriter & File Generator (`resume_generator.py`)**:
   - Rewrites your resume using your real career history (Wipro, DXC, HPE, Jain University, Imarticus) in a crisp, natural **XYZ impact style** (*Accomplished X, measured by Y, by doing Z*).
   - Replaces `[Insert %]` placeholders with grounded metrics, weaves in missing JD keywords naturally, and generates clean single-column `.docx`, `.md`, and `.txt` files inside `/Users/roshanl/ATS/output/` while verifying the **Before vs. After ATS Score Jump**.

## Quick Start

### Option A: Launch the Interactive Web App (Streamlit)
```bash
cd /Users/roshanl/ATS
streamlit run app.py
```

### Option B: Run the Interactive Terminal Tracker (CLI)
```bash
cd /Users/roshanl/ATS
python3 cli_tracker.py
```

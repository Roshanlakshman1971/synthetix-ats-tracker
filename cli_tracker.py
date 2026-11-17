"""
Interactive CLI & Automated Verification Runner for the Live ATS Tracker.
Follows the exact 4-stage workflow:
  1. Scans the provided resume file and reports baseline structure/blockers
  2. Prompts for (or reads) the target Job Description
  3. Runs the relevant Enterprise ATS evaluation and outputs a 0-100 scorecard
  4. Generates a new human-written, ATS-optimized resume file (.docx, .md, .txt) and verifies the score jump
"""

import argparse
import os
import sys

from resume_parser import extract_text_from_file, parse_resume_structure
from ats_engine import (
    evaluate_resume_against_jd,
    rewrite_resume_human_and_ats_optimized,
)
from resume_generator import save_tailored_resume_files


def run_ats_workflow(resume_path: str, jd_text: str, role_title: str = "", company: str = "", output_dir: str = "output"):
    print("=" * 72)
    print("STAGE 1: SCANNING RESUME & STRUCTURAL ATS AUDIT")
    print("=" * 72)
    raw_text, file_meta = extract_text_from_file(resume_path, os.path.basename(resume_path))
    parsed = parse_resume_structure(raw_text, file_meta)

    print(f"Candidate Name      : {parsed['candidate_name']}")
    print(f"Detected Headline   : {parsed['target_headline'] or 'None'}")
    print(f"Contact Info        : {parsed['contact']['phone']} | {parsed['contact']['email']} | {parsed['contact']['location']}")
    print(f"Word Count          : {parsed['word_count']} words")
    print(f"Quantified Bullets  : {parsed['quantified_bullets_count']} metric-backed bullets")
    if parsed["audit_issues"]:
        print("\n[!] Structural Audit Warnings Found in Original Resume:")
        for issue in parsed["audit_issues"]:
            print(f"    - {issue}")
    else:
        print("\n[+] Clean baseline structure.")

    print("\n" + "=" * 72)
    print("STAGE 2 & 3: RUNNING ENTERPRISE ATS SIMULATION AGAINST JOB DESCRIPTION")
    print("=" * 72)
    ats_before = evaluate_resume_against_jd(parsed, jd_text, role_title)
    print(f"Detected ATS Engine : {ats_before['ats_profile']['platform']}")
    print(f"Target Role Family  : {ats_before['detected_role_family']}")
    print(f"ORIGINAL ATS SCORE  : {ats_before['overall_score']} / 100  -->  {ats_before['verdict']}")
    print("\nSub-Score Breakdown:")
    for k, v in ats_before["sub_scores"].items():
        print(f"  - {k:<38}: {v}%")

    print(f"\nMatched Keywords ({len(ats_before['matched_keywords'])}):")
    for m in ats_before["matched_keywords"]:
        print(f"  [MATCH] {m['canonical']} ({m['status']} | JD: {m['jd_mentions']}x, Resume: {m['resume_mentions']}x)")

    print(f"\nMissing Keywords to Inject ({len(ats_before['missing_keywords'])}):")
    for m in ats_before["missing_keywords"]:
        print(f"  [MISS]  {m['canonical']} (Priority: {m['priority']} | Mentioned {m['jd_mentions']}x in JD)")

    print("\n" + "=" * 72)
    print("STAGE 4: REWRITING RESUME (HUMAN VOICE + ATS KEYWORDS) & SAVING FILES")
    print("=" * 72)
    rewritten = rewrite_resume_human_and_ats_optimized(
        parsed_resume=parsed,
        ats_eval=ats_before,
        jd_text=jd_text,
        target_role_title=role_title,
        company_name=company,
    )
    saved_paths = save_tailored_resume_files(
        resume_data=rewritten,
        output_dir=output_dir,
        target_role_title=role_title,
        company_name=company,
    )

    new_parsed = parse_resume_structure(rewritten["markdown_text"], {"filename": "tailored_resume.docx"})
    ats_after = evaluate_resume_against_jd(new_parsed, jd_text, role_title)

    print(f"NEW TAILORED ATS SCORE : {ats_after['overall_score']} / 100  (Up from {ats_before['overall_score']} / 100, +{ats_after['overall_score'] - ats_before['overall_score']}% gain!)")
    print(f"New Verdict            : {ats_after['verdict']}")
    print("\nKey Human-Voice & ATS Upgrades Applied:")
    for note in rewritten.get("rewrite_notes", []):
        print(f"  * {note}")

    print("\nGenerated Resume Files:")
    for fmt, path in saved_paths.items():
        print(f"  [{fmt.upper()}] {path}")

    return ats_before, ats_after, saved_paths


def main():
    parser = argparse.ArgumentParser(description="Live ATS Tracker & Human Resume Rewriter CLI")
    parser.add_argument("--resume", type=str, help="Path to resume file (.pdf, .docx, .md, .txt)")
    parser.add_argument("--jd-file", type=str, help="Path to Job Description text file (optional; prompts interactively if omitted)")
    parser.add_argument("--role", type=str, default="", help="Target role title")
    parser.add_argument("--company", type=str, default="", help="Target company name")
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    resume_path = args.resume
    if not resume_path:
        default_sample = os.path.join(base_dir, "sample_roshan_resume.md")
        user_input = input(f"Step 1 — Enter path to your resume [Press Enter for {default_sample}]: ").strip()
        resume_path = user_input if user_input else default_sample

    if not os.path.exists(resume_path):
        print(f"Error: Resume file not found at {resume_path}")
        sys.exit(1)

    if args.jd_file and os.path.exists(args.jd_file):
        with open(args.jd_file, "r", encoding="utf-8") as f:
            jd_text = f.read()
    else:
        print("\nStep 2 — Paste the Job Description below (type END on a new line when finished):")
        lines = []
        for line in sys.stdin:
            if line.strip() == "END":
                break
            lines.append(line)
        jd_text = "".join(lines)

    out_dir = os.path.join(base_dir, "output")
    run_ats_workflow(resume_path, jd_text, args.role, args.company, out_dir)


if __name__ == "__main__":
    main()

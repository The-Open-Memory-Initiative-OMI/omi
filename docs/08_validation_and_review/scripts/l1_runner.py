#!/usr/bin/env python3
"""
OMI L1 Bench Electrical — Master Orchestrator

Runs generate_probe_sequence.py and validate_continuity_log.py in sequence,
captures git commit SHA, computes file hashes, and produces the unified
L1 evidence package per the "Credible L1" standard.

Usage:
    python l1_runner.py \\
        --reference path/to/ddr4_udimm_288_pinmap.csv \\
        --measurements path/to/measurement_log.csv
    python l1_runner.py \\
        --reference path/to/csv \\
        --measurements path/to/log.csv \\
        --output-dir path/to/evidence

Exit codes:
    0 = L1 PASS (all checks passed)
    1 = L1 FAIL (one or more checks failed)
    2 = Input/environment error
"""

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent


def compute_sha256(path: Path) -> str:
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def get_git_commit_sha() -> str:
    """Get current git HEAD commit SHA, or 'unknown' if not in a git repo."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return "unknown"


def run_script(script_name: str, args: list[str]) -> tuple[int, str, str]:
    """Run a verification script and capture output."""
    script_path = SCRIPT_DIR / script_name
    cmd = [sys.executable, str(script_path)] + args

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=120,
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 2, "", f"Script {script_name} timed out after 120 seconds"
    except FileNotFoundError:
        return 2, "", f"Script not found: {script_path}"


def main():
    parser = argparse.ArgumentParser(
        description="OMI L1 Bench Electrical — Master Orchestrator"
    )
    parser.add_argument(
        "--reference",
        required=True,
        type=Path,
        help="Path to ddr4_udimm_288_pinmap.csv",
    )
    parser.add_argument(
        "--measurements",
        required=True,
        type=Path,
        help="Path to tester's measurement CSV",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("evidence"),
        help="Directory for evidence output (default: evidence/)",
    )
    args = parser.parse_args()

    # Validate inputs
    if not args.reference.exists():
        print(f"ERROR: Reference CSV not found: {args.reference}", file=sys.stderr)
        sys.exit(2)
    if not args.measurements.exists():
        print(f"ERROR: Measurements CSV not found: {args.measurements}", file=sys.stderr)
        sys.exit(2)

    # Prepare output directory
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    # Capture environment
    timestamp = datetime.now(timezone.utc)
    git_sha = get_git_commit_sha()
    csv_hash = compute_sha256(args.reference)
    meas_hash = compute_sha256(args.measurements)

    print("=" * 70)
    print("  OMI L1 Bench Electrical — Full Validation Suite")
    print("=" * 70)
    print()
    print(f"  Timestamp:       {timestamp.isoformat()}")
    print(f"  Git commit:      {git_sha}")
    print(f"  Reference:       {args.reference}")
    print(f"  CSV SHA-256:     {csv_hash}")
    print(f"  Measurements:    {args.measurements}")
    print(f"  Meas SHA-256:    {meas_hash}")
    print(f"  Output dir:      {output_dir}")
    print()

    # -------------------------------------------------------------------
    # Run generate_probe_sequence.py
    # -------------------------------------------------------------------
    print("-" * 70)
    print("  [1/3] Generating Probe Sequence (generate_probe_sequence.py)")
    print("-" * 70)

    probe_csv = output_dir / "probe_sequence.csv"
    probe_md = output_dir / "probe_checklist.md"

    # CSV output
    rc_probe_csv, out_probe_csv, err_probe_csv = run_script(
        "generate_probe_sequence.py",
        ["--reference", str(args.reference), "--output", str(probe_csv)],
    )
    print(out_probe_csv)
    if err_probe_csv:
        print(err_probe_csv, file=sys.stderr)

    # Markdown output
    rc_probe_md, out_probe_md, err_probe_md = run_script(
        "generate_probe_sequence.py",
        [
            "--reference", str(args.reference),
            "--format", "markdown",
            "--output", str(probe_md),
        ],
    )
    if err_probe_md:
        print(err_probe_md, file=sys.stderr)

    rc_probe = 0 if (rc_probe_csv == 0 and rc_probe_md == 0) else 1

    # -------------------------------------------------------------------
    # Run validate_continuity_log.py
    # -------------------------------------------------------------------
    print("-" * 70)
    print("  [2/3] Validating Continuity Log (validate_continuity_log.py)")
    print("-" * 70)

    validate_args = [
        "--reference", str(args.reference),
        "--measurements", str(args.measurements),
        "--output", str(output_dir / "continuity_report.json"),
    ]

    rc_validate, out_validate, err_validate = run_script(
        "validate_continuity_log.py", validate_args
    )
    print(out_validate)
    if err_validate:
        print(err_validate, file=sys.stderr)

    # -------------------------------------------------------------------
    # Generate unified L1 summary
    # -------------------------------------------------------------------
    print("-" * 70)
    print("  [3/3] Generating L1 Summary")
    print("-" * 70)

    all_passed = (rc_probe == 0 and rc_validate == 0)

    summary = {
        "tool": "l1_runner.py",
        "version": "1.0.0",
        "timestamp": timestamp.isoformat(),
        "git_commit_sha": git_sha,
        "overall_status": "PASS" if all_passed else "FAIL",
        "input_files": {
            "reference_csv": str(args.reference),
            "reference_csv_sha256": csv_hash,
            "measurements_csv": str(args.measurements),
            "measurements_csv_sha256": meas_hash,
        },
        "sub_checks": {
            "generate_probe_sequence": {
                "exit_code": rc_probe,
                "status": "PASS" if rc_probe == 0 else "FAIL",
                "probe_csv": str(probe_csv),
                "probe_checklist": str(probe_md),
            },
            "validate_continuity_log": {
                "exit_code": rc_validate,
                "status": "PASS" if rc_validate == 0 else "FAIL",
                "report_file": str(output_dir / "continuity_report.json"),
            },
        },
        "evidence_files": [],
    }

    # List all generated evidence files
    for f in sorted(output_dir.iterdir()):
        if f.is_file():
            summary["evidence_files"].append({
                "name": f.name,
                "sha256": compute_sha256(f),
            })

    # Write unified summary (JSON)
    summary_path = output_dir / "l1_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # Write human-readable markdown summary
    md_path = output_dir / "l1_summary.md"
    with open(md_path, "w", encoding="utf-8") as f:
        status_str = "PASS" if all_passed else "FAIL"
        f.write("# OMI L1 Bench Electrical — Summary\n\n")
        f.write(f"**Status:** {status_str}\n\n")
        f.write("| Field | Value |\n")
        f.write("|-------|-------|\n")
        f.write(f"| Timestamp | {timestamp.isoformat()} |\n")
        f.write(f"| Git Commit | `{git_sha}` |\n")
        f.write(f"| Reference CSV | `{args.reference}` |\n")
        f.write(f"| CSV SHA-256 | `{csv_hash}` |\n")
        f.write(f"| Measurements | `{args.measurements}` |\n")
        f.write(f"| Meas SHA-256 | `{meas_hash}` |\n\n")
        f.write("## Check Results\n\n")
        f.write("| Check | Status |\n")
        f.write("|-------|--------|\n")
        ps = "PASS" if rc_probe == 0 else "FAIL"
        vs = "PASS" if rc_validate == 0 else "FAIL"
        f.write(f"| Probe Sequence Generation | {ps} |\n")
        f.write(f"| Continuity Log Validation | {vs} |\n\n")
        f.write("## Evidence Files\n\n")
        for ev in summary["evidence_files"]:
            f.write(f"- `{ev['name']}` — SHA-256: `{ev['sha256']}`\n")
        f.write("\n---\n\n")
        f.write("*Generated by l1_runner.py v1.0.0*\n")

    # Final output
    print()
    print("=" * 70)
    if all_passed:
        print("  L1 BENCH ELECTRICAL: PASS")
        print()
        print("  All continuity, isolation, and bus integrity checks passed.")
    else:
        print("  L1 BENCH ELECTRICAL: FAIL")
        print()
        if rc_probe != 0:
            print("  [X] Probe Sequence Generation: FAIL")
        if rc_validate != 0:
            print("  [X] Continuity Log Validation: FAIL")
    print()
    print(f"  Evidence directory: {output_dir}")
    print(f"  Summary (JSON):    {summary_path}")
    print(f"  Summary (MD):      {md_path}")
    print("=" * 70)

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
OMI L0 Artifact Integrity — Master Orchestrator

Runs both verify_pinmap.py and verify_naming.py in sequence,
captures git commit SHA, computes file hashes, and produces
the unified L0 evidence package per the "Credible L0" standard.

Usage:
    python l0_runner.py --reference path/to/ddr4_udimm_288_pinmap.csv
    python l0_runner.py --reference path/to/csv --manifest path/to/net_manifest.md
    python l0_runner.py --reference path/to/csv --output-dir path/to/evidence

Exit codes:
    0 = L0 PASS (all checks passed)
    1 = L0 FAIL (one or more checks failed)
    2 = Input/environment error
"""

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Import the verification modules directly
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
        description="OMI L0 Artifact Integrity — Master Orchestrator"
    )
    parser.add_argument(
        "--reference",
        required=True,
        type=Path,
        help="Path to ddr4_udimm_288_pinmap.csv",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help="Path to Stage 7.5 net manifest markdown (optional)",
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

    # Prepare output directory
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    # Capture environment
    timestamp = datetime.now(timezone.utc)
    git_sha = get_git_commit_sha()
    csv_hash = compute_sha256(args.reference)

    print("=" * 70)
    print("  OMI L0 Artifact Integrity — Full Validation Suite")
    print("=" * 70)
    print()
    print(f"  Timestamp:   {timestamp.isoformat()}")
    print(f"  Git commit:  {git_sha}")
    print(f"  Reference:   {args.reference}")
    print(f"  CSV SHA-256: {csv_hash}")
    print(f"  Output dir:  {output_dir}")
    print()

    # -----------------------------------------------------------------------
    # Run verify_pinmap.py
    # -----------------------------------------------------------------------
    print("-" * 70)
    print("  [1/2] Running Pin Map Verification (verify_pinmap.py)")
    print("-" * 70)

    pinmap_args = [
        "--reference", str(args.reference),
        "--output", str(output_dir / "pinmap_report.json"),
    ]
    if args.manifest:
        pinmap_args += ["--manifest", str(args.manifest)]

    rc_pinmap, out_pinmap, err_pinmap = run_script("verify_pinmap.py", pinmap_args)
    print(out_pinmap)
    if err_pinmap:
        print(err_pinmap, file=sys.stderr)

    # -----------------------------------------------------------------------
    # Run verify_naming.py
    # -----------------------------------------------------------------------
    print("-" * 70)
    print("  [2/2] Running Naming Consistency Audit (verify_naming.py)")
    print("-" * 70)

    naming_args = [
        "--reference", str(args.reference),
        "--output", str(output_dir / "naming_report.json"),
        "--matrix", str(output_dir / "lane_matrix.csv"),
    ]

    rc_naming, out_naming, err_naming = run_script("verify_naming.py", naming_args)
    print(out_naming)
    if err_naming:
        print(err_naming, file=sys.stderr)

    # -----------------------------------------------------------------------
    # Generate unified L0 summary
    # -----------------------------------------------------------------------
    all_passed = (rc_pinmap == 0 and rc_naming == 0)

    summary = {
        "tool": "l0_runner.py",
        "version": "1.0.0",
        "timestamp": timestamp.isoformat(),
        "git_commit_sha": git_sha,
        "overall_status": "PASS" if all_passed else "FAIL",
        "input_files": {
            "reference_csv": str(args.reference),
            "reference_csv_sha256": csv_hash,
        },
        "sub_checks": {
            "verify_pinmap": {
                "exit_code": rc_pinmap,
                "status": "PASS" if rc_pinmap == 0 else "FAIL",
                "report_file": str(output_dir / "pinmap_report.json"),
            },
            "verify_naming": {
                "exit_code": rc_naming,
                "status": "PASS" if rc_naming == 0 else "FAIL",
                "report_file": str(output_dir / "naming_report.json"),
                "matrix_file": str(output_dir / "lane_matrix.csv"),
            },
        },
        "evidence_files": [],
    }

    if args.manifest:
        summary["input_files"]["manifest"] = str(args.manifest)
        summary["input_files"]["manifest_sha256"] = compute_sha256(args.manifest)

    # List all generated evidence files
    for f in sorted(output_dir.iterdir()):
        if f.is_file():
            summary["evidence_files"].append({
                "name": f.name,
                "sha256": compute_sha256(f),
            })

    # Write unified summary
    summary_path = output_dir / "l0_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # Write human-readable markdown summary
    md_path = output_dir / "l0_summary.md"
    with open(md_path, "w", encoding="utf-8") as f:
        status_str = "PASS" if all_passed else "FAIL"
        f.write(f"# OMI L0 Artifact Integrity — Summary\n\n")
        f.write(f"**Status:** {status_str}\n\n")
        f.write(f"| Field | Value |\n")
        f.write(f"|-------|-------|\n")
        f.write(f"| Timestamp | {timestamp.isoformat()} |\n")
        f.write(f"| Git Commit | `{git_sha}` |\n")
        f.write(f"| Reference CSV | `{args.reference}` |\n")
        f.write(f"| CSV SHA-256 | `{csv_hash}` |\n\n")
        f.write(f"## Check Results\n\n")
        f.write(f"| Check | Status |\n")
        f.write(f"|-------|--------|\n")
        pm_s = "PASS" if rc_pinmap == 0 else "FAIL"
        nm_s = "PASS" if rc_naming == 0 else "FAIL"
        f.write(f"| Pin Map Verification | {pm_s} |\n")
        f.write(f"| Naming Consistency Audit | {nm_s} |\n\n")
        f.write(f"## Evidence Files\n\n")
        for ev in summary["evidence_files"]:
            f.write(f"- `{ev['name']}` — SHA-256: `{ev['sha256']}`\n")
        f.write(f"\n---\n\n")
        f.write(f"*Generated by l0_runner.py v1.0.0*\n")

    # Final output
    print()
    print("=" * 70)
    if all_passed:
        print("  L0 ARTIFACT INTEGRITY: PASS")
        print()
        print("  All structural, mapping, and naming checks passed.")
    else:
        print("  L0 ARTIFACT INTEGRITY: FAIL")
        print()
        if rc_pinmap != 0:
            print("  [X] Pin Map Verification: FAIL")
        if rc_naming != 0:
            print("  [X] Naming Consistency Audit: FAIL")
    print()
    print(f"  Evidence directory: {output_dir}")
    print(f"  Summary (JSON):    {summary_path}")
    print(f"  Summary (MD):      {md_path}")
    print("=" * 70)

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()

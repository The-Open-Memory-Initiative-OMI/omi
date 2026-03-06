# L0 — Artifact Integrity

## Purpose

L0 is the foundational level of the OMI Validation Ladder.
It proves that the frozen Stage 7 schematic artifacts are internally consistent
before any physical manufacturing or bench validation occurs.

L0 demands machine-verifiable evidence across three pillars:

1. **ERC Sanity** — zero unintended electrical rule violations
2. **Pin Map Integrity (288/288)** — all edge connector pins correctly mapped
3. **Naming Consistency** — byte-lane isolation and per-device net naming verified

## Quick Start

**Prerequisites:** Python 3.8+, access to the frozen pin map CSV.

```bash
# From the repository root:

# Run pin map verification
python docs/08_validation_and_review/scripts/verify_pinmap.py \
  --reference design/connector/ddr4_udimm_288_pinmap.csv

# Run naming consistency audit
python docs/08_validation_and_review/scripts/verify_naming.py \
  --reference design/connector/ddr4_udimm_288_pinmap.csv

# Run the full L0 suite with evidence generation
python docs/08_validation_and_review/scripts/l0_runner.py \
  --reference design/connector/ddr4_udimm_288_pinmap.csv \
  --output-dir validation/evidence
```

## Directory Contents

| File | Purpose |
|------|---------|
| `naming_rules.md` | Regex patterns and naming conventions for all net groups |

## Related Files

| File | Location |
|------|----------|
| Verification scripts | `docs/08_validation_and_review/scripts/` |
| Report templates | `docs/08_validation_and_review/templates/` |
| Canonical pin map CSV | `design/connector/ddr4_udimm_288_pinmap.csv` |
| Net manifest | `docs/07_schematic_capture/stage-7-5-net-manifest.md` |
| Full L0 playbook | `docs/08_validation_and_review/OMI Stage 8 L0 Playbook Development.md` |
| Bringup ladder | `docs/08_validation_and_review/08-2_bringup_ladder.md` |

## "Credible L0" Standard

L0 is only achieved when the evidence package includes:

1. The specific Git commit SHA of the frozen schematic
2. The SHA-256 hash of the input CSV
3. The exact script used and its version
4. The raw output log

An independent engineer must be able to reproduce the exact same results
by checking out the same commit and running the same scripts.

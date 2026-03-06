# OMI Stage 8 Validation: L0 Artifact Integrity Report

**Run ID:** `RUN-YYYYMMDD-LOCAL-L0-001`
**Executing Engineer:** [GitHub Handle / Name]
**Date:** YYYY-MM-DD
**Target Commit Hash:** [insert git SHA]

---

## 1. Executive Summary

This report presents the evidence required to fulfill Level 0 (L0) validation
for the OMI v1 target (DDR4 UDIMM, 8 GB, 1R, x8, Non-ECC).

All structural, mapping, and naming integrity checks have been executed
against the frozen Stage 7 schematic and are documented below.

---

## 2. Environment

| Field | Value |
|-------|-------|
| Git commit SHA | `[insert]` |
| EDA tool + version | KiCad [version] |
| Python version | [insert] |
| OS | [insert] |
| Script versions | verify_pinmap.py v1.0.0, verify_naming.py v1.0.0 |

---

## 3. Check Results & Evidence

| Check Category | Criteria | Status | SHA-256 Hash | Evidence File |
|----------------|----------|--------|--------------|---------------|
| **BOM Sanity** | 8x DRAM (x8), 1x SPD EEPROM | PASS / FAIL | `[hash]` | `evidence/session1_bom.csv` |
| **ERC Sanity** | 0 Errors, 0 Unwaived Warnings | PASS / FAIL | `[hash]` | `evidence/session2_erc_clean.rpt` |
| **Pin Map** | 288/288 Edge Connector match | PASS / FAIL | `[hash]` | `evidence/pinmap_report.json` |
| **Naming** | Byte-lane isolation, per-device nets | PASS / FAIL | `[hash]` | `evidence/naming_report.json` |

**Overall L0 Status:** PASS / FAIL

---

## 4. Deviations & Documented Waivers

> List all ERC waivers applied during Session 2.
> Each waiver must include an engineering justification.

- **Waiver 1:** [Signal/Net name] — [Warning description]
  - **Justification:** [Why this is a false positive for DDR4 1R x8 architecture]

- *(Add additional waivers as needed, or write "None" if no waivers applied)*

---

## 5. Evidence Package

### Automated Script Outputs

| File | Description | SHA-256 |
|------|-------------|---------|
| `pinmap_report.json` | Pin map verification results | `[hash]` |
| `naming_report.json` | Naming consistency audit results | `[hash]` |
| `lane_matrix.csv` | Byte-lane-to-pin mapping matrix | `[hash]` |
| `l0_summary.json` | Unified L0 summary | `[hash]` |

### Manual Evidence (ERC + BOM)

| File | Description | SHA-256 |
|------|-------------|---------|
| `session1_bom.csv` | BOM export from EDA tool | `[hash]` |
| `session2_erc_clean.rpt` | ERC report from EDA tool | `[hash]` |

---

## 6. Reproduction Instructions

```bash
# Clone and checkout the exact commit
git clone https://github.com/The-Open-Memory-Initiative-OMI/omi.git
git checkout [commit-hash]

# Run L0 verification suite
python docs/08_validation_and_review/scripts/l0_runner.py \
  --reference design/connector/ddr4_udimm_288_pinmap.csv \
  --output-dir validation/evidence
```

---

## 7. Sign-Off

| Field | Value |
|-------|-------|
| Reported by | [Name / Handle] |
| Date | YYYY-MM-DD |
| Run ID | `RUN-YYYYMMDD-LOCAL-L0-001` |
| Result | PASS / FAIL |
| Linked PR / Issue | [link] |

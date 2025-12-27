# OMI v1 — Stage 6 Block Interface Summary & Closure

## Status
Proposed (Stage 6.7)

## Scope
OMI Version 1 only

## Authority
OMI Maintainers

---

## 1. Purpose

This document formally summarizes the **Stage 6 technical decomposition** for OMI v1 and declares **Stage 6 complete**.

It exists to:
- Integrate all block-level definitions
- Make interfaces explicit
- Confirm internal consistency
- Authorize transition to **Stage 7 — Schematic Capture**

---

## 2. Stage 6 Block Summary

| Block | Responsibility | Key Assumptions |
|-----|---------------|----------------|
| Power Delivery & PDN | Defines required rails and sourcing | JEDEC-only, host-supplied rails |
| Address / Command / Clock | Defines CA topology and loading | Single-rank, fly-by topology |
| Data Byte-Lanes & DQS | Defines data grouping and timing | x8 devices, symmetric lanes |
| SPD & Configuration | Defines module identity and timing | Single JEDEC profile |
| Mechanical & Connector | Defines physical interface | JEDEC UDIMM compliance |
| Validation & Bring-Up | Defines success and failure model | Observability over coverage |

---

## 3. Interface Mapping

### 3.1 Power ↔ Signal Blocks
- Power stability (VDDQ, VREF) directly affects CA and data training
- PDN margins are assumed by signal blocks

### 3.2 CA ↔ Data Blocks
- Training coordination depends on consistent topology assumptions
- No rank interleaving simplifies interaction

### 3.3 SPD ↔ Platform Interaction
- SPD defines how the platform configures CA and data timing
- Incorrect SPD data propagates into training behavior

### 3.4 Mechanical ↔ Electrical Blocks
- Connector geometry constrains pin access and routing
- Mechanical keep-outs affect PDN and signal placement

### 3.5 Validation ↔ All Blocks
- Validation strategy defines how assumptions are tested
- Failures feed back into documentation, not silent fixes

---

## 4. Consistency Verification

The following consistency checks have been performed:

- All blocks assume **DDR4 UDIMM, 8 GB, 1R, x8, non-ECC**
- No block introduces unsupported features (ECC, multi-rank, XMP)
- All assumptions are JEDEC-aligned and publicly documentable
- No block relies on NDA-protected behavior

No unresolved contradictions have been identified.

---

## 5. Accepted Residual Risks

The following risks are acknowledged and carried into Stage 7:

- Platform-dependent training behavior
- Sensitivity to power and reference noise
- BIOS variability affecting initialization

These risks are **explicitly accepted** and will be documented during validation.

---

## 6. Stage 6 Closure Statement

With this document, **Stage 6 (Technical Decomposition) is declared complete**.

All core assumptions, interfaces, and dependencies for OMI v1 are documented and internally consistent.

Implementation may now proceed to:

➡ **Stage 7 — Schematic Capture**

---

## 7. Final Note

Stage 6 ensures that OMI v1 is **fully defined in thought** before being defined in hardware.

From this point onward, progress is measured in **schematics, layouts, and measurements**, not decisions.

---

*End of document*

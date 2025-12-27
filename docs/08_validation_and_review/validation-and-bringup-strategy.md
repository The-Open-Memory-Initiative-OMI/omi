# OMI v1 — Validation & Bring-Up Strategy  
*(DDR4 UDIMM, 8 GB, 1R, x8, non-ECC)*

## Status
Draft (Stage 6.6)

## Scope
OMI Version 1 only

## Authority
OMI Maintainers

## Related
- Stage 6.6 — Validation & Bring-Up Strategy
- Stage 6.5 — Mechanical & Connector Interface
- Stage 6.4 — SPD & Configuration Block
- Stage 6.3 — Data Byte-Lanes & DQS Block
- Stage 6.2 — Address / Command / Clock Block
- Stage 6.1 — Power Delivery & PDN

---

## 1. Purpose

This document defines the **strategy for bringing up and validating** the OMI v1 DDR4 UDIMM.

It establishes:
- How bring-up is sequenced
- What constitutes success
- How failures are interpreted
- What observability is required
- How results are documented

This document does **not** define detailed test procedures or acceptance testing. Those belong to later stages.

---

## 2. Design Philosophy

Validation in OMI v1 follows these principles:

- **Reproducibility over coverage**
- **Observability over automation**
- **Failure treated as engineering data**
- **Platform variability acknowledged, not hidden**
- **Completion over perfection**

The goal is to learn and document behavior, not to certify a commercial product.

---

## 3. Bring-Up Phases

Bring-up is expected to proceed in the following high-level phases.

### 3.1 Power Application

- Module is inserted into a compatible DDR4 UDIMM socket
- Platform supplies required power rails
- Rails are verified to be within JEDEC tolerance

Failure at this stage indicates **power delivery or mechanical issues**.

---

### 3.2 SPD Detection

- Platform successfully reads SPD contents
- Module organization and timing are recognized

Failure at this stage indicates **SPD or I²C interface issues**.

---

### 3.3 Training & Initialization

- Memory controller initiates DDR4 training
- CA and data-path training completes or fails visibly

Failure here indicates **signal integrity, timing, or reference stability issues**.

---

### 3.4 Basic Functional Validation

- Memory is visible to the operating system
- Basic read/write functionality is exercised

This stage confirms **end-to-end correctness**, not performance.

---

## 4. Success Criteria

For OMI v1, **successful bring-up** is defined as:

- SPD is readable
- Training completes on at least one reference platform
- Memory is enumerated by the system
- Basic read/write tests pass

Partial success is acceptable and includes:
- Platform-specific failures
- Reduced operating frequency
- Intermittent behavior under certain conditions

---

## 5. Expected Failure Modes

The following failures are considered **expected and documentable**:

- Training failure on certain platforms
- Sensitivity to power or reference noise
- Behavior differences across BIOS versions
- Failures that resolve under reduced speed

Such failures are **engineering results**, not project failures.

---

## 6. Observability & Measurement Assumptions

Validation assumes access to:

- Basic lab equipment (multimeter, oscilloscope)
- Ability to probe power rails
- Ability to read SPD contents

Advanced tools are beneficial but **not required**.

---

## 7. Platform Variability

OMI v1 explicitly acknowledges:

- BIOS and firmware variability
- Differences in memory controller behavior
- Non-deterministic training outcomes

Results are documented **per platform**, without forced normalization.

---

## 8. Documentation Philosophy

Validation results must be:

- Reproducible where possible
- Accompanied by platform context
- Explicit about limitations and uncertainty

Failure is documented with the same rigor as success.

---

## 9. Explicit Non-Goals

This strategy explicitly excludes:

- Performance benchmarking
- Long-term reliability testing
- Compliance certification
- Commercial qualification workflows

---

## 10. Interface With Other Blocks

Validation outcomes inform:

- Signal topology assumptions
- Power delivery margins
- SPD configuration correctness

Findings may result in **document revisions**, not silent fixes.

---

## 11. Locking Statement

This document defines the **validation and bring-up strategy** for OMI v1.

All validation and review work MUST follow the philosophy and constraints stated herein unless this document is explicitly revised.

---

*End of document*

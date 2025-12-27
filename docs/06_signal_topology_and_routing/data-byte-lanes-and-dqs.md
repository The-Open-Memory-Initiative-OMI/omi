# OMI v1 — Data Byte-Lanes & DQS Block Definition  
*(DDR4 UDIMM, 8 GB, 1R, x8, non-ECC)*

## Status
Draft (Stage 6.3)

## Scope
OMI Version 1 only

## Authority
OMI Maintainers

## Related
- Stage 6.3 — Data Byte-Lanes & DQS Block
- Stage 6.2 — Address / Command / Clock Block
- Stage 6.1 — Power Delivery & PDN
- OMI v1 — DDR4 Acceptance Conditions
- OMI v1 — Capacity & Organization

---

## 1. Purpose

This document defines the **data-path topology** for the OMI v1 DDR4 UDIMM.

It specifies:
- How data signals are grouped into byte lanes
- The relationship between DQ, DQS, and DM
- Symmetry and matching philosophy
- Timing sensitivity and training interaction
- Observability and expected failure modes

This document intentionally **does not define routing rules or schematic details**. Those belong to later stages.

---

## 2. Design Philosophy

The data-path design for OMI v1 follows these principles:

- **Byte-lane symmetry over optimization**
- **JEDEC-compliant signaling only**
- **Single-rank simplicity**
- **Margin-first timing assumptions**
- **Explicit documentation of failure behavior**

The goal is **predictable training and diagnosable errors**, not maximum bandwidth.

---

## 3. Data Signal Groups

Each x8 DRAM device corresponds to **one byte lane**.

Per byte lane, the following signals exist:

- DQ\[7:0\] — Data bits  
- DQS / DQS# — Differential data strobe  
- DM — Data mask (if used per JEDEC DDR4 expectations)

A full 64-bit non-ECC data bus therefore consists of **8 byte lanes**.

---

## 4. Byte-Lane Organization

### 4.1 Device-to-Lane Mapping

- Each DRAM device maps to exactly one byte lane
- Byte lanes are treated as **logically equivalent**
- No byte lane is optimized or treated specially

---

### 4.2 Symmetry Assumptions

OMI v1 assumes:

- Identical topology intent across all byte lanes
- Similar electrical environments per lane
- No intentional skewing between lanes

Differences introduced by physical layout are treated as **implementation artifacts**, not architectural intent.

---

## 5. DQ–DQS Relationship

### 5.1 Data Strobe Role

- DQS/DQS# acts as the timing reference for its associated DQ signals
- Read and write timing is trained relative to DQS

---

### 5.2 Timing Sensitivity

The data path is sensitive to:

- DQ–DQS skew within a byte lane
- Inter-lane skew (second-order)
- VDDQ and VREF stability

These sensitivities directly influence training success.

---

## 6. Training Interaction

The data path participates in:

- Write leveling
- Read training
- Read/write timing centering

Failures in these steps are expected to correlate with:
- Poor DQ–DQS alignment
- Excessive skew or noise
- PDN or reference instability

Such failures are **valid engineering outcomes** and must be documented.

---

## 7. Observability & Validation Considerations

Validation expectations include:

- Ability to probe representative DQS and DQ signals
- Correlation of data errors with training results
- Documentation of platform-dependent behavior

Data-path issues are expected to manifest as:
- Read/write training failures
- Data corruption under load
- Errors that improve at reduced speed

---

## 8. Expected Failure Modes

The following are considered expected and documentable:

- Lane-specific training instability
- Intermittent read/write errors
- Platform-dependent sensitivity to noise or skew

These are treated as **engineering data**, not defects to be hidden.

---

## 9. Explicit Non-Goals

This block definition explicitly excludes:

- Optimization for maximum data rate
- Multi-rank or ECC data complexity
- Vendor-specific or proprietary tuning
- NDA-restricted behavior

---

## 10. Interface With Other Blocks

The data block interfaces directly with:

- Address / Command / Clock Block (training coordination)
- Power Delivery & PDN (VDDQ, VREF quality)
- Validation & Bring-Up Strategy

Any change in these blocks requires re-evaluation of data-path assumptions.

---

## 11. Locking Statement

This document defines the **data byte-lane and DQS assumptions** for OMI v1.

All schematic capture, layout, and validation work MUST conform to the constraints and assumptions stated herein unless this document is explicitly revised.

---

*End of document*

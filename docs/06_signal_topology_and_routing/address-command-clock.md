# OMI v1 — Address / Command / Clock Block Definition  
*(DDR4 UDIMM, 8 GB, 1R, x8, non-ECC)*

## Status
Draft (Stage 6.2)

## Scope
OMI Version 1 only

## Authority
OMI Maintainers

## Related
- Stage 6.2 — Address / Command / Clock Block
- Stage 6.1 — Power Delivery & PDN
- OMI v1 — DDR4 Acceptance Conditions
- OMI v1 — Form Factor (DDR4 UDIMM)
- OMI v1 — Capacity & Organization

---

## 1. Purpose

This document defines the **Address / Command / Clock (CA) block** for the OMI v1 DDR4 UDIMM.

It specifies:
- Which CA and control signals exist
- Clocking assumptions and topology
- Loading and rank assumptions
- Conceptual termination philosophy
- Timing sensitivity and training interactions
- Observability and validation expectations

This document intentionally **does not define pin-level implementation or routing details**. Those belong to **Stage 7 — Schematic Capture**.

---

## 2. Design Philosophy

The CA block for OMI v1 follows these principles:

- **JEDEC-compliant signaling only**
- **Single-rank simplicity**
- **Topology clarity over optimization**
- **Explicit loading assumptions**
- **Margin-first timing philosophy**
- **Documented platform variability**

The objective is to ensure **predictable training behavior and diagnosable failures**, not maximum frequency operation.

---

## 3. Signal Groups Covered

The CA block includes the following signal categories:

### 3.1 Address Signals
- A\[0:N\]
- Used for row, column, and mode register addressing

### 3.2 Bank and Bank Group Signals
- BA\[x\]
- BG\[x\]

### 3.3 Command Signals
- RAS#
- CAS#
- WE#

### 3.4 Control Signals
- CS# (single rank)
- CKE
- RESET#
- ODT (as applicable)

### 3.5 Clock Signals
- CK
- CK#

---

## 4. Rank and Loading Assumptions

OMI v1 uses a **single-rank (1R)** organization.

Assumptions:
- One CS# line active
- Uniform loading across all DRAM devices
- No rank interleaving complexity
- Reduced address/command loading relative to multi-rank modules

These assumptions directly influence topology, termination expectations, and training behavior.

---

## 5. Clocking Model

### 5.1 Differential Clock

- CK/CK# are treated as a differential pair
- Clock signals are assumed to be sourced by the host memory controller
- No on-DIMM clock regeneration or conditioning is assumed

### 5.2 Topology Assumptions

- Clock topology follows standard DDR4 UDIMM expectations
- Symmetry across DRAM devices is prioritized
- Skew minimization is treated as a first-order constraint

Clock jitter and skew are considered **platform variables**, not DIMM-controlled parameters.

---

## 6. Topology Philosophy

### 6.1 Address / Command Topology

The CA bus is assumed to follow a **fly-by style topology**, consistent with DDR4 UDIMM practice.

Conceptual expectations:
- Signals traverse devices sequentially
- Controlled impedance routing
- Termination strategy consistent with JEDEC recommendations

Exact routing and termination implementation is deferred to Stage 7.

---

### 6.2 Termination Assumptions

- On-die termination (ODT) behavior is relied upon as defined by DDR4
- No exotic or vendor-specific termination schemes are assumed
- Termination strategy must remain explainable using public documentation

---

## 7. Timing Sensitivity & Training Interaction

The CA block directly affects:

- Command decoding reliability
- Mode register programming
- Training convergence behavior

Expected sensitivities:
- Skew between CK and CA signals
- Inter-signal skew within CA group
- Interaction with VDDQ and VREF stability

Training failures related to CA timing are considered **valid and documentable outcomes**.

---

## 8. Observability & Validation Considerations

The CA block must remain **observable and debuggable**.

Validation expectations:
- Ability to probe CK/CK# and representative CA signals
- Correlation of training success/failure with CA integrity
- Documentation of platform-specific sensitivity

CA-related issues are expected to manifest as:
- Training failures
- Inconsistent initialization
- Mode register access failures

---

## 9. Expected Failure Modes

The following are considered expected and documentable:

- Training instability caused by marginal CA timing
- Platform-dependent sensitivity to CA skew
- Failures that resolve under reduced frequency or relaxed timing

Such failures are treated as **engineering data**, not defects to be hidden.

---

## 10. Explicit Non-Goals

This block definition explicitly excludes:

- Optimization for high-frequency operation
- Multi-rank address complexity
- Custom or proprietary training mechanisms
- NDA-protected platform behavior

---

## 11. Interface With Other Blocks

The CA block interfaces directly with:

- Power Delivery & PDN (rail stability and reference quality)
- Data Byte-Lane & DQS Block (training coordination)
- Validation & Bring-Up Strategy

Any change to CA assumptions requires re-evaluation of these blocks.

---

## 12. Locking Statement

This document defines the **address, command, and clock assumptions** for OMI v1.

All schematic capture, layout, and validation work MUST conform to the constraints and assumptions stated herein unless this document is explicitly revised.

---

*End of document*

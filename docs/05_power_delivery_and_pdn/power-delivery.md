# OMI v1 — Power Delivery & Rails Definition  
*(DDR4 UDIMM, 8 GB, 1R, x8, non-ECC)*

## Status
Draft (Stage 6.1)

## Scope
OMI Version 1 only

## Authority
OMI Maintainers

## Related
- Stage 6.1 — Power Delivery Block
- OMI v1 — DDR4 Acceptance Conditions
- OMI v1 — Form Factor (DDR4 UDIMM)
- OMI v1 — Capacity & Organization

---

## 1. Purpose

This document defines the **power delivery model** for the OMI v1 DDR4 UDIMM.

It specifies:
- Which power rails are required
- Nominal voltages and tolerances
- Rail sourcing assumptions
- Conceptual PDN and decoupling philosophy
- Power-up and dependency assumptions
- Observability and validation expectations

This document intentionally **does not define implementation details** such as regulator selection, capacitor values, or PCB placement. Those belong to **Stage 7 — Schematic Capture**.

---

## 2. Design Philosophy

Power delivery decisions for OMI v1 follow these principles:

- **Conservatism over optimization**  
- **JEDEC-aligned behavior only**  
- **Explicit assumptions, no implicit platform magic**  
- **Margin-first PDN philosophy**  
- **Observable and debuggable rails**  

The goal is not performance leadership, but **predictable, reproducible operation** on commodity desktop platforms.

---

## 3. Required Power Rails

A DDR4 UDIMM requires the following power rails:

### 3.1 VDD  
**Function:** Core DRAM array power  
**Nominal Voltage:** 1.20 V  
**Tolerance:** JEDEC-defined  

VDD supplies the internal memory cell arrays and associated logic within each DRAM device.

---

### 3.2 VDDQ  
**Function:** I/O buffer power for DQ, DQS, CA signals  
**Nominal Voltage:** 1.20 V  
**Tolerance:** JEDEC-defined  

VDDQ directly impacts signal integrity and timing margins and must be tightly controlled.

---

### 3.3 VPP  
**Function:** Wordline boost voltage  
**Nominal Voltage:** 2.50 V  
**Tolerance:** JEDEC-defined  

VPP is required for internal wordline activation and is typically sourced externally to the DRAM core.

---

### 3.4 VREF  
**Function:** Reference voltage for input comparators  
**Nominal Voltage:** ~0.50 × VDDQ  
**Tolerance:** JEDEC-defined  

VREF stability directly affects read margin and training behavior.

---

### 3.5 Ground (GND)

A low-impedance ground reference is required for all rails and signal return paths. Ground integrity is treated as part of the PDN, not a passive assumption.

---

## 4. Rail Sourcing Assumptions

### 4.1 Host-Supplied Rails

For OMI v1, the following rails are assumed to be **supplied by the host platform via the DIMM connector**, consistent with standard DDR4 UDIMM behavior:

- VDD  
- VDDQ  
- VPP  
- GND  

No on-DIMM generation of these rails is assumed or required.

---

### 4.2 VREF Generation

VREF handling follows a **conservative, platform-aligned approach**:

- VREF is assumed to be generated in accordance with JEDEC DDR4 UDIMM expectations  
- Exact generation (on-DIMM vs host-provided) will be documented explicitly during schematic capture  
- VREF must be locally decoupled and treated as a noise-sensitive rail  

---

### 4.3 Explicit Non-Assumptions

OMI v1 does **not** assume:

- Vendor-specific power sequencing behavior  
- Proprietary platform power conditioning  
- Hidden margin compensation by the memory controller  

All behavior must be explainable using public documentation.

---

## 5. PDN & Decoupling Philosophy (Conceptual)

The OMI v1 PDN strategy is **margin-first**.

Key principles:

- Combination of **bulk decoupling** (low-frequency stability) and **local decoupling** (high-frequency current demand)  
- Symmetry across DRAM devices where feasible  
- Conservative assumptions on current transients  
- Avoidance of aggressive or exotic PDN techniques  

Final capacitor selection, placement, and values are deferred to Stage 7.

---

## 6. Power Sequencing & Dependencies

OMI v1 assumes **JEDEC-compliant power-up behavior**.

Key assumptions:

- No custom or non-standard sequencing requirements  
- Rails are considered valid only once within JEDEC tolerance  
- DRAM behavior outside defined sequencing is considered undefined  

Platform-specific sequencing variations are treated as **validation variables**, not design dependencies.

---

## 7. Observability & Validation Considerations

Power rails must be **observable and debuggable**.

Validation expectations:

- Physical access to measure VDD, VDDQ, VPP, and VREF  
- Ability to correlate rail behavior with training success or failure  
- Voltage instability or noise is considered a valid failure mode  

Power integrity issues must be documentable using standard lab equipment.

---

## 8. Expected Failure Modes

The following are considered **expected and documentable** failure modes:

- Training failures due to marginal VDDQ or VREF stability  
- Intermittent errors correlated with load transients  
- Platform-dependent sensitivity to rail noise  

Such failures are not hidden; they are **engineering data**.

---

## 9. Explicit Non-Goals

This power delivery definition explicitly excludes:

- Performance-driven PDN optimization  
- Cost-minimized capacitor selection  
- Vendor-proprietary power techniques  
- NDA-protected platform behavior  

---

## 10. Interface With Other Blocks

This block constrains and informs:

- Signal Integrity & Routing Constraints  
- Data Byte-Lane Design  
- Validation & Bring-Up Strategy  

Any change to power delivery assumptions requires re-evaluation of these blocks.

---

## 11. Locking Statement

This document defines the **power delivery assumptions** for OMI v1.

All schematic, layout, and validation work MUST conform to the constraints and assumptions stated herein unless this document is explicitly revised.

---

*End of document*

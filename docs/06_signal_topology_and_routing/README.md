# 06 — Signal Topology & Routing

## Purpose

This directory defines the **signal topology, loading assumptions, and routing philosophy** for the OMI v1 DDR4 UDIMM.

It captures **how signals are conceptually organized and expected to behave**, before any schematic capture or PCB routing begins. The intent is to eliminate hidden assumptions and ensure that all signal-related design work proceeds from a shared, documented understanding.

This directory exists to bridge **architectural intent (Stage 6)** and **implementation (Stage 7)**.

---

## Scope

The content in this directory focuses on **signal definition and topology**, not implementation.

Included:

- Address, command, and control signal definitions  
- Clocking assumptions and topology  
- Data byte-lane and DQS group concepts  
- Loading and rank assumptions  
- Conceptual termination and margin philosophy  
- Timing sensitivity and training interactions  
- Observability and validation considerations  

Explicitly excluded:

- Pin-level schematic decisions  
- Trace length targets or routing rules  
- Impedance calculations or stack-up specifics  
- Resistor values, placement, or component footprints  
- Vendor- or platform-specific tuning  

Implementation details belong to **Stage 7 — Schematic Capture** and **Stage 10 — Layout, SI & PI Guidelines**.

---

## Files in This Directory

### `address-command-clock.md`

Defines the **Address / Command / Clock (CA) block** for OMI v1.

This document specifies:
- CA and control signal groups  
- Clocking model and topology assumptions  
- Rank and loading behavior  
- Termination philosophy  
- Timing sensitivity and training interactions  
- Expected failure modes and validation observability  

This file establishes how the memory controller communicates with the DRAM devices at a conceptual level.

---

### *(Future)* `data-byte-lanes-and-dqs.md`

Will define the **data path block**, including:
- DQ, DQS, and DM signal grouping  
- Byte-lane organization for x8 devices  
- Symmetry and matching philosophy  
- Data-related timing sensitivities  
- Failure modes related to read/write training  

---

## Relationship to Other Stages

This directory directly depends on:

- `05_power_delivery_and_pdn` — rail stability and reference assumptions  

And directly informs:

- `07_schematic_capture` — pin-level and circuit implementation  
- `08_validation_and_review` — bring-up and training analysis  
- `10_layout_si_pi_guidelines` — detailed routing constraints  

No schematic or routing work should begin until the assumptions in this directory are understood and accepted.

---

## Design Philosophy

Signal topology decisions in OMI v1 are guided by:

- JEDEC-compliant behavior only  
- Single-rank simplicity  
- Margin-first assumptions  
- Explicit loading and topology documentation  
- Failure treated as engineering data  

This directory prioritizes **clarity and diagnosability** over performance optimization.

---

## Contribution Guidelines

Contributions to this directory should:

- Clarify assumptions or signal roles  
- Identify risks, ambiguities, or missing constraints  
- Improve documentation precision  

Contributions that introduce schematic-level detail, routing rules, or platform-specific tuning will be deferred to later stages.

---

## Status

- Stage: **6 — Technical Decomposition**
- Current focus: **6.2 Address / Command / Clock Block**
- Maturity: **Definition in progress**
- Scope: **OMI v1 only**

---

*Signal topology defines how intent becomes connectivity. Clarity here prevents silent failure later.*

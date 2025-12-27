# 05 — Power Delivery & PDN

## Purpose

This directory defines the **power delivery and power distribution network (PDN) assumptions** for **OMI v1**.

It documents **what power rails exist, how they are sourced, and what constraints apply**, before any schematic capture or layout work begins.

Power delivery is treated as a **first-class architectural block**, because mistakes or ambiguity at this level propagate into signal integrity, training behavior, validation complexity, and bring-up risk.

---

## Scope

The content in this directory focuses on **definition and intent**, not implementation.

Included:

- Required DDR4 power rails for an OMI v1 UDIMM  
- Nominal voltages and JEDEC-aligned tolerances  
- Rail sourcing assumptions (host-supplied vs on-DIMM)  
- Conceptual PDN and decoupling philosophy  
- Power-up, sequencing, and dependency assumptions  
- Observability and validation considerations  

Explicitly excluded:

- Regulator or LDO part selection  
- Capacitor values, footprints, or placement  
- PCB routing or schematic symbols  
- Performance or cost optimization  

Implementation details belong to **Stage 7 — Schematic Capture**.

---

## Files in This Directory

### `power-delivery.md`

The primary **Stage 6.1 block definition** for power delivery.

This document specifies:
- Required power rails (VDD, VDDQ, VPP, VREF, GND)  
- Voltage assumptions and tolerances  
- PDN philosophy and non-goals  
- Expected failure modes and validation observability  

All downstream design work must conform to the assumptions defined here.

---

## Relationship to Other Stages

This directory sits at the boundary between **scope locking (Stage 5)** and **schematic capture (Stage 7)**.

It directly informs:

- `06_signal_topology_and_routing` — signal integrity and routing constraints  
- `07_schematic_capture` — actual circuit implementation  
- `08_validation_and_review` — bring-up and power-related failure analysis  

No schematic or layout work should begin until the assumptions in this directory are understood and accepted.

---

## Design Philosophy

Power delivery in OMI v1 follows these principles:

- Conservative, margin-first design  
- JEDEC-compliant behavior only  
- Explicit assumptions, no implicit platform behavior  
- Failure treated as engineering data  
- Observability over optimization  

This directory exists to ensure those principles are enforced consistently.

---

## Contribution Guidelines

Contributions to this directory should:

- Improve clarity of assumptions  
- Identify risks, ambiguities, or missing constraints  
- Propose documentation improvements (not implementation shortcuts)  

Contributions that introduce schematic-level detail or vendor-specific behavior will be deferred to later stages.

---

## Status

- Stage: **6.1 — Power Delivery Block**
- Maturity: **Definition complete / implementation pending**
- Scope: **OMI v1 only**

---

*Power delivery defines the electrical floor every other block stands on.*

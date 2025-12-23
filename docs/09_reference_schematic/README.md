# Stage 9 — Minimal Reference Schematic

Stage 9 defines the **Minimal Reference Schematic** for the OMI v1 DIMM design.

This schematic is:
- Intentionally minimal
- Architecturally faithful
- Correctness-first
- Fully reviewable using Stage 8 validation rules

Its purpose is not to be production-ready, but to be **unambiguously correct**.

---

## Purpose of the Minimal Reference Schematic

The Minimal Reference Schematic exists to:

- Prove that the architecture can be implemented cleanly
- Demonstrate correct signal grouping and topology
- Make all constraints visible in a real schematic
- Serve as a canonical reference for contributors

If this schematic is correct, more complex versions can be derived safely.

---

## What "Minimal" Means (Very Important)

Minimal does **not** mean incomplete.

Minimal means:
- No optional features
- No optimizations
- No speculative enhancements
- No performance-driven complexity

Everything present must exist **because the architecture requires it**, not because it might be useful later.

---

## What the Reference Schematic Includes

The Minimal Reference Schematic includes:

- One DIMM connector (conceptual or standard-aligned)
- One rank of DRAM devices
- The minimum number of byte lanes required by the chosen DDR width
- One SPD device
- Explicit power rails
- Explicit decoupling placeholders
- Explicit clock, command, and data grouping

Nothing more.

---

## What the Reference Schematic Explicitly Excludes

The schematic must **not** include:

- Multiple ranks
- Optional ECC (unless explicitly scoped)
- Register or buffer logic
- Power regulation circuitry
- Performance tuning components
- Vendor-specific enhancements

Exclusions are intentional and must remain so.

---

## Required Schematic Sheet Structure

The reference schematic must follow the Stage 7 guide exactly.

Recommended sheet set:



01_dimm_connector.sch
02_power_distribution.sch
03_dram_array_overview.sch
04_byte_lane_0.sch
05_byte_lane_1.sch
...
NN_spd_and_aux.sch


Each sheet must have a single, clear responsibility.

---

## DRAM Devices in the Reference Schematic

Rules:

- Use generic DRAM symbols
- Do not assume a specific vendor
- Show only architecturally relevant pins
- Power, ground, DQ, DQS, address, command, clock only

Unused pins must be:
- Explicitly marked
- Justified

No hidden behavior is allowed.

---

## Data Path Requirements

For each byte lane:

- Exactly one DQ bundle
- Exactly one DQS (and complement if applicable)
- Clear point-to-point connectivity
- No stubs
- No shared nets between lanes

Each lane must be independently traceable.

---

## Address, Command, and Clock Requirements

- Address and command must appear as shared buses
- Clock must appear as a shared differential pair
- Rank select must be explicit (even if only one rank)
- No local buffering or regeneration

Topology must be obvious from the schematic alone.

---

## Power and Decoupling Requirements

- VDD, VDDQ, Vref, VTT, and auxiliary rails must be separate
- Decoupling placeholders must exist per rail
- Decoupling must be rail-specific (not generic)
- Vref must not power logic
- VTT must only serve termination-related pins

Power intent must be visible, not implied.

---

## SPD and Auxiliary Logic Requirements

- SPD must be powered only from auxiliary/standby rail
- SPD must connect only to the low-speed management bus
- No DDR signals allowed on the SPD sheet
- Clear isolation from high-speed domains

SPD failure must not electrically affect DRAM operation.

---

## Validation Requirements

The reference schematic must pass **all Stage 8 validation layers**:

- Architecture compliance
- Schematic structure review
- Constraint adherence
- Power integrity sanity
- Failure containment

If any checklist item fails, the schematic is not acceptable.

---

## What Makes This a "Reference"

This schematic is a reference because:

- It is readable without tribal knowledge
- It encodes architectural intent structurally
- It can be reviewed by independent engineers
- It can be reimplemented consistently

A reference schematic teaches by example.

---

## How Contributors Should Use This Schematic

Contributors may:
- Extend it cautiously
- Optimize it knowingly
- Specialize it for platforms

But they must:
- Preserve architectural intent
- Revalidate using Stage 8
- Document deviations explicitly

The reference is a baseline, not a ceiling.

---

## Takeaway

Stage 9 turns intent into reality — carefully.

The Minimal Reference Schematic proves that:
- The architecture is implementable
- The constraints are enforceable
- The design is reviewable
- The project is real

Complexity can come later.
Correctness must come first.

---

Next stages:
- Stage 10 — Layout Guidelines
- Stage 10 — Signal Integrity Validation
- Stage 10 — Power Integrity Validation

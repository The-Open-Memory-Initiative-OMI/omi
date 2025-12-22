# Design Assumptions and Non-Goals

This document defines the **explicit assumptions, constraints, and non-goals** for the OMI v1 DIMM design.

Its purpose is to:

- Prevent scope creep
- Make design intent unambiguous
- Clarify what the design does *not* attempt to solve
- Enable fair technical review

Any design decision must be interpreted in the context of these assumptions.

---

## Scope Definition

OMI v1 is a **reference-grade, correctness-first DIMM design**.

It is intended to:

- Demonstrate a complete, understandable DDR memory module architecture
- Prioritize correctness, margin, and reproducibility
- Serve as an educational and foundational open design

It is **not** intended to be a competitive commercial product.

---

## Assumptions About the Target System

The OMI v1 DIMM assumes:

- A standards-compliant DDR memory controller
- A single, known DDR generation (defined elsewhere)
- Controller-managed training and calibration
- Conservative operating conditions

The design does not attempt to compensate for:

- Non-compliant controllers
- Undefined platform behavior
- Broken training algorithms

Correctness is a shared contract.

---

## Performance Assumptions

OMI v1 assumes:

- JEDEC-compliant operating speeds
- No overclocking
- No aggressive timing margins
- No performance binning

The design explicitly avoids:

- Extreme frequency targets
- Margin-free operation
- Performance-driven tradeoffs

Performance is secondary to stability.

---

## Signal Integrity Assumptions

The design assumes:

- Proper PCB stack-up selection
- Continuous reference planes
- Controlled impedance routing
- Respect for documented constraints

OMI v1 does not attempt to:

- Compensate for poor layout
- Mask signal integrity violations
- Rely on calibration to fix physical mistakes

Physics is not optional.

---

## Power Integrity Assumptions

OMI v1 assumes:

- Proper external power regulation
- Adequate upstream supply stability
- Clean power delivery to the DIMM connector

The design does not attempt to:

- Fix unstable system power
- Replace platform-level regulation
- Operate under marginal power conditions

Power integrity is a system-level responsibility.

---

## Environmental Assumptions

The design assumes:

- Operation within standard temperature ranges
- Reasonable airflow and cooling
- Normal aging behavior

OMI v1 does not attempt to:

- Guarantee operation under extreme environments
- Compensate for thermal abuse
- Optimize for extended lifetime beyond standards

Environmental stress testing is out of scope.

---

## Manufacturing Assumptions

OMI v1 assumes:

- Standard PCB manufacturing tolerances
- Typical assembly quality
- No exotic fabrication techniques

The design avoids:

- Unmanufacturable geometries
- Ultra-tight tolerances
- Vendor-specific tricks

Reproducibility matters more than novelty.

---

## Validation Assumptions

OMI v1 assumes validation will include:

- Bring-up testing
- Basic functional testing
- Margin-aware evaluation

The design does not claim:

- Zero-defect operation
- Exhaustive corner-case coverage
- Field-ready qualification

OMI v1 is a **reference**, not a certified product.

---

## Explicit Non-Goals

OMI v1 explicitly does **not** attempt to:

- Maximize bandwidth
- Minimize cost
- Minimize PCB area
- Compete with commercial DIMMs
- Support every platform
- Hide design tradeoffs

These goals may exist in future versions, but not here.

---

## Why These Assumptions Matter

Without explicit assumptions:

- Designs become unreviewable
- Failures become ambiguous
- Responsibility becomes unclear

OMI documents assumptions so that:

- Success is measurable
- Failure is explainable
- Improvements are intentional

---

## Takeaway

OMI v1 is designed to be:

- Correct
- Understandable
- Reproducible
- Conservative

It is not designed to be everything.

These assumptions are not limitations.
They are **design boundaries**.

---

This document closes Stage 5.

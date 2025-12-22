# Learning Roadmap
**Open Memory Initiative (OMI)**

This document defines a technical learning path for contributors who are starting from scratch but want to meaningfully participate in the Open Memory Initiative.

> OMI is not optimized for speed.  
> It is optimized for understanding, correctness, and reproducibility.

This roadmap reflects that philosophy.

---

## How to Use This Roadmap

- You do not need prior DDR or PCB experience to start.
- Each stage builds the mental model required for the next.
- Contributors are encouraged to learn and document simultaneously.
- Reaching later stages is not required to contribute value.
- **Skipping stages is discouraged.**

---

## Stage 0 — System Context: Why Memory Matters

**Goal**: Understand why DRAM must behave correctly before learning how it works.

### Learn:
- What happens on a cache miss
- Why latency consistency matters
- Why memory errors are catastrophic
- How CPUs assume memory correctness

### Key questions:
- What assumptions does the CPU make about DRAM?
- What breaks if those assumptions are violated?

### Suggested OMI contribution:
- `docs/memory_hierarchy.md`
- `docs/why_dram_is_critical.md`

**Outcome:**  
You understand why memory is foundational, not peripheral.

---

## Stage 1 — DRAM Fundamentals (Device-Level)

**Goal**: Understand DRAM as a physical memory device.

### Learn:
- DRAM cell structure (capacitor + transistor)
- Charge leakage and refresh
- Row activation and precharge
- Destructive reads
- Banks and arrays

### Key questions:
- Why must DRAM be refreshed?
- Why do rows and columns exist?
- Why is timing unavoidable?

### Suggested OMI contribution:
- `docs/dram_fundamentals.md`

**Outcome:**  
DDR timing parameters stop feeling arbitrary.

---

## Stage 2 — DDR as a Protocol

**Goal**: Understand DDR as a structured command and data protocol layered on top of DRAM.

### Learn:
- Command bus vs data bus
- ACT / READ / WRITE / PRE commands
- CAS latency (CL)
- tRCD, tRP, tRAS
- Burst length
- Banks and bank groups

### Key questions:
- Why can't commands be issued back-to-back?
- Why is burst-based access used?
- How does DDR trade latency for bandwidth?

### Suggested OMI contribution:
- `docs/ddr_protocol.md`
- `docs/ddr_timing_overview.md`

**Outcome:**  
You can read a DDR datasheet without guessing.

---

## Stage 3 — DIMM Anatomy (Module-Level)

**Goal**: Understand the memory module as a system, not just DRAM chips.

**This is where OMI's core scope begins.**

### Learn:
- What components exist on a DIMM
- DRAM chips vs module behavior
- Power rails (VDD, VTT, Vref)
- Termination strategies
- SPD EEPROM and configuration data
- Why routing matters at the module level

### Key questions:
- Why is termination placed on the module?
- Why does Vref stability matter?
- What does SPD actually configure?

### Suggested OMI contribution:
- `docs/dimm_anatomy.md`
- `docs/spd_overview.md`

**Outcome:**  
You understand what OMI is actually building.

---

## Stage 4 — Signal Integrity (DDR-Focused)

**Goal**: Learn only the signal integrity concepts required for DDR reliability.

**This is not RF engineering. It is applied discipline.**

### Learn:
- Transmission lines
- Reflections and impedance mismatch
- Length matching
- Stubs and vias
- Why DDR margins are small

### Key questions:
- Why does trace length matter?
- Why are stubs dangerous?
- Why does DDR fail silently?

### Suggested OMI contribution:
- `docs/signal_integrity_basics.md`
- `docs/ddr_routing_principles.md`

**Outcome:**  
DDR routing rules become logical instead of restrictive.

---

## Stage 5 — Power Integrity (Often Ignored, Always Critical)

**Goal**: Understand why power quality directly affects memory correctness.

### Learn:
- Decoupling strategy
- Bulk vs ceramic capacitors
- Power noise and transient response
- Vref sensitivity
- Ground integrity

### Key questions:
- Why do power issues cause random memory errors?
- Why does Vref noise corrupt data?
- Why is decoupling placement critical?

### Suggested OMI contribution:
- `docs/power_integrity.md`

**Outcome:**  
Memory errors stop looking like "software bugs".

---

## Stage 6 — Reference Designs and Interpretation

**Goal**: Learn how to interpret vendor reference designs without copying blindly.

### Learn:
- What vendors document
- What vendors omit
- How assumptions are embedded
- Where design freedom exists

### Key questions:
- What is required vs conventional?
- What is vendor-specific?
- What can be simplified or clarified?

### Suggested OMI contribution:
- `docs/reference_design_analysis.md`

**Outcome:**  
You can critique designs instead of replicating them.

---

## Stage 7 — Validation and Bring-Up Philosophy

**Goal**: Understand how memory designs are validated and tested.

### Learn:
- Platform dependency
- BIOS and firmware interaction
- Stress testing vs functional testing
- Failure modes
- Reproducibility

### Key questions:
- What does "working" actually mean?
- Why are memory failures hard to reproduce?
- How should results be documented?

### Suggested OMI contribution:
- `docs/validation_methodology.md`

**Outcome:**  
You understand when a design is truly valid.

---

## Contribution Philosophy

OMI encourages contributors to:

- Learn publicly
- Document assumptions
- Share uncertainty
- Improve clarity, not just designs

**Documentation is contribution.**

A contributor who clarifies understanding is as valuable as one who draws schematics.

---

## Final Note

You are not expected to master every stage.

OMI values:

- Depth over speed
- Understanding over imitation
- Completion over ambition

**If you can explain one layer clearly, you belong here.**

---

> Open memory is not given.  
> It is built; carefully, transparently, and together.

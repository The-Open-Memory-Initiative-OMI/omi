# OMI v1 Scope Definition

This document defines the explicit scope boundaries for **Open Memory Initiative — Version 1 (OMI v1)**.

OMI v1 exists to prove that open, reproducible system memory design is possible in practice, not to maximize performance, features, or market relevance.

**Scope discipline is a design requirement.**

---

## Purpose of Version 1

The goal of OMI v1 is to deliver:

> A **fully documented**, **buildable**, **testable**, **reproducible** PC DDR memory module design, developed entirely in the open, using publicly available knowledge and tools.

Success is measured by **clarity and reproducibility**, not performance leadership.

---

## What OMI v1 Includes

OMI v1 includes the complete module-level design of a PC DDR memory module.

### 1. Memory Technology

- One DDR generation only
- Chosen publicly and documented in `meta/decisions/`
- Mature, widely supported DDR technology

*(DDR generation selection is a decision, not an assumption.)*

### 2. Form Factor

- Standard PC UDIMM form factor
- Targeted for desktop-class systems
- Compatibility with commodity PC motherboards

### 3. Design Artifacts (Required)

OMI v1 will publish, at minimum:

- Electrical schematics
- PCB layout files
- PCB stack-up and impedance targets
- Bill of Materials (BOM)
- Design assumptions and constraints
- Design rationale for all major decisions

**All artifacts must be sufficient for an independent engineer to reproduce the design.**

### 4. Documentation (First-Class Deliverable)

**Documentation is not optional.**

OMI v1 includes:

- Memory hierarchy context
- DRAM fundamentals
- DDR protocol interpretation
- DIMM anatomy
- Signal integrity rationale
- Power integrity rationale

**If a design decision cannot be documented openly, it does not belong in v1.**

### 5. Validation and Testing

OMI v1 includes:

- Bring-up methodology
- Platform assumptions
- BIOS/firmware configuration notes
- Test procedures
- Observed results, including failures

**Partial validation is acceptable if clearly documented.**

---

## What OMI v1 Explicitly Excludes

The following are **out of scope** for OMI v1.

### 1. DRAM Chip Design

- No DRAM cell design
- No sense amplifier design
- No silicon-level fabrication work

**OMI v1 is module-level only.**

### 2. Advanced or Specialized Memory

- LPDDR
- HBM
- Server RDIMM / LRDIMM
- Mobile or embedded memory formats

### 3. Performance Optimization

- Overclocking
- Aggressive timing tuning
- Competitive benchmarking

**Correctness and stability take priority.**

### 4. Proprietary or NDA-Gated Information

- Vendor reference designs under NDA
- Licensed IP blocks
- Reverse-engineered confidential material

**All work must be legally and ethically shareable.**

### 5. Commercial Objectives

- Mass production
- Cost optimization for market
- Productization or sales strategy

**OMI v1 is an engineering and knowledge project, not a product launch.**

---

## Scope Control Rules

To protect OMI v1 from uncontrolled expansion:

- Any scope change must be proposed publicly
- Scope changes must be documented in `meta/decisions/`
- If a contribution delays validation, it does not belong in v1
- If a contribution introduces closed dependencies, it is rejected

**Completion is prioritized over expansion.**

---

## Criteria for OMI v1 Completion

OMI v1 is considered complete when:

1. All required design artifacts are published
2. Documentation is sufficient for independent understanding
3. At least one module revision is manufactured
4. Basic operation is demonstrated on real hardware
5. Validation results are publicly available
6. At least one external contributor reproduces part of the work

---

## Final Note

OMI v1 is intentionally narrow.

**This is not a limitation of ambition.**  
**It is a requirement for success.**

One clear, reproducible design is more valuable than many unfinished ideas.

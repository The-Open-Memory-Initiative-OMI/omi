# OMI v1 — Memory Module Form Factor Selection

## Status
**Accepted** — Decision locked for OMI v1

## Scope
OMI Version 1 only

## Authority
OMI Maintainers

## Related
- Stage 5.2 — Form Factor Selection
- Stage 5.1 — DDR4 Selection
- OMI v1 — DDR4 Acceptance Conditions

---

## 1. Purpose

This document defines the **physical memory module form factor** selected for **OMI v1**.

The form factor decision establishes the mechanical, electrical, validation, and documentation boundaries for all subsequent design work. Once finalized, this decision is considered **fixed for OMI v1**.

This document exists to prevent scope drift and to ensure that all contributors operate under a shared and explicit physical constraint.

---

## 2. Decision Criteria

The form factor is evaluated strictly against OMI v1 goals:

- Buildability using standard PCB fabrication and assembly
- Debuggability and physical access during validation
- Platform availability for independent reproduction
- Contributor accessibility and cost considerations
- Educational clarity of layout, routing, and SI behavior

Market trends and density optimization are explicitly excluded as primary criteria.

---

## 3. Options Considered

### 3.1 DDR4 UDIMM (Desktop DIMM)

**Description**

A full-size unbuffered DDR4 Dual Inline Memory Module intended for desktop-class systems and workstations, conforming to JEDEC DDR4 UDIMM mechanical and electrical standards.

**Advantages**

- Largest PCB area, enabling conservative routing and PDN design
- Superior probe access for signal integrity and power analysis
- Easier mechanical handling during bring-up and iteration
- Broad availability of compatible desktop platforms
- Clearer educational value for illustrating DDR4 routing and layout

**Disadvantages**

- Limited applicability to mobile platforms
- Larger physical size compared to SO-DIMM

---

### 3.2 DDR4 SO-DIMM

**Description**

A compact DDR4 Small Outline DIMM primarily used in laptops and small form factor systems.

**Advantages**

- High relevance to modern mobile computing
- Smaller PCB area and lower manufacturing cost

**Disadvantages**

- Significantly tighter routing constraints
- Reduced probe access and debug visibility
- Laptop BIOS and firmware behavior is often opaque
- Higher barrier to independent validation and replication

---

## 4. Selected Form Factor

**OMI v1 selects: DDR4 UDIMM**

The DDR4 UDIMM form factor is selected as the reference physical format for OMI v1.

---

## 5. Rationale for Selection

The DDR4 UDIMM form factor best aligns with OMI v1 objectives for the following reasons:

- **Debuggability:** Larger PCB area and pin spacing significantly improve probe access and observability during validation.
- **Signal Integrity Margin:** Increased routing space allows more conservative impedance control and spacing, reducing SI risk.
- **Platform Transparency:** Desktop platforms provide greater BIOS visibility and configurability compared to mobile systems.
- **Reproducibility:** Contributors are more likely to have access to compatible desktop systems for independent testing.
- **Educational Value:** The UDIMM form factor allows clearer documentation of routing topology, PDN design, and failure modes.

These factors collectively reduce execution risk while preserving technical relevance.

---

## 6. Explicit Rejection of Alternatives

DDR4 SO-DIMM is explicitly rejected for OMI v1 due to:

- Increased routing and SI complexity disproportionate to educational benefit
- Reduced physical access for validation and debugging
- Higher dependency on opaque laptop firmware behavior
- Increased difficulty for contributors to reproduce results independently

This rejection applies **only to OMI v1** and does not preclude future exploration.

---

## 7. Non-Implications of This Decision

Selecting DDR4 UDIMM for OMI v1 does **not** imply:

- Commitment to desktop-only memory in future versions
- Optimization for density or performance
- Support for ECC, RDIMM, or server-class modules
- Exclusion of SO-DIMM in later project stages

This is a **v1 execution decision**, not a long-term roadmap constraint.

---

## 8. Locking Statement

With this document accepted, the DDR4 UDIMM form factor is considered **locked for OMI v1**.

All subsequent schematic, layout, validation, and documentation work MUST conform to this form factor.

Any proposal that violates this constraint is considered **out of scope for OMI v1**.

---

*End of document*

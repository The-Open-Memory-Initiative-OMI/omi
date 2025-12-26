# OMI v1 — Capacity & Organization Decision

## Status
Proposed

## Scope
OMI Version 1 only

## Authority
OMI Maintainers

## Related
- Stage 5.3 — Capacity & Organization Selection
- Stage 5.2 — Form Factor Selection (DDR4 UDIMM)
- OMI v1 — DDR4 Acceptance Conditions

---

## 1. Purpose

This document defines the **logical capacity and internal organization** of the OMI v1 DDR4 UDIMM.

The capacity and organization decision determines:

- DRAM device count and density
- Rank topology
- Data width and byte-lane structure
- Address, command, and control loading
- Routing complexity and validation behavior

Once finalized, this decision is considered **locked for OMI v1** and constrains schematic design, PCB layout, BOM selection, and validation methodology.

---

## 2. Decision Criteria

The selection is evaluated against OMI v1 priorities:

- **Reproducibility:** ability for contributors to build and validate independently  
- **Execution risk:** minimizing failure modes in a first open DDR4 design  
- **Platform compatibility:** predictable behavior on commodity desktop systems  
- **Educational clarity:** clear mapping between organization and observed behavior  
- **Relevance:** representative of modern, real-world DDR4 usage  

Performance optimization and density maximization are explicitly out of scope.

---

## 3. Options Considered

### 3.1 4 GB, Single Rank (1R), x8 Devices

**Characteristics**
- One rank
- x8 DRAM devices
- 64-bit non-ECC data bus

**Advantages**
- Lowest routing and signal integrity complexity
- Simplest bring-up and training behavior
- Reduced component count

**Limitations**
- Lower relevance to contemporary desktop systems
- Reduced educational value for modern capacity expectations
- Risk of being perceived as overly conservative or demonstrative

---

### 3.2 8 GB, Single Rank (1R), x8 Devices

**Characteristics**
- One rank
- Higher-density x8 DRAM devices
- 64-bit non-ECC data bus

**Advantages**
- Representative of common modern desktop memory modules
- Maintains single-rank simplicity
- Widely supported by DDR4-capable platforms
- Clear byte-lane and DQ/DQS group mapping
- Balanced execution risk vs relevance

**Limitations**
- Requires availability of higher-density DRAM components
- Slightly tighter PDN and SI considerations compared to 4 GB

---

### 3.3 8 GB, Dual Rank (2R), x8 Devices

**Characteristics**
- Two ranks
- x8 DRAM devices
- 64-bit non-ECC data bus

**Advantages**
- Common in commercial UDIMMs
- Exposure to rank interleaving concepts

**Limitations**
- Increased routing and control complexity
- Higher address/command loading
- Increased dependency on platform-specific training behavior
- Elevated validation and debug complexity
- Disproportionate execution risk for v1

---

## 4. Selected Configuration

**OMI v1 selects:**

> **8 GB total capacity, Single Rank (1R), x8 DRAM devices, non-ECC (64-bit)**

---

## 5. Rationale for Selection

This configuration represents the most defensible balance between **modern relevance** and **execution discipline** for OMI v1.

### 5.1 Why Single Rank

Single-rank organization:

- Minimizes address and command loading
- Reduces routing and SI complexity
- Produces more predictable training behavior
- Simplifies failure analysis and documentation

For a first open DDR4 design, clarity and diagnosability are prioritized over completeness.

---

### 5.2 Why 8 GB Capacity

An 8 GB capacity:

- Reflects common real-world desktop usage
- Avoids the perception of a demonstrative or obsolete design
- Preserves educational relevance for contributors
- Remains achievable without introducing rank complexity

This choice avoids both extremes: overly conservative (4 GB) and overly complex (8 GB 2R).

---

### 5.3 Why x8, Non-ECC Organization

Using x8 devices and a 64-bit non-ECC data bus:

- Aligns with broad desktop platform support
- Simplifies byte-lane routing and documentation
- Avoids ECC-related platform dependencies
- Preserves contributor accessibility

ECC support is explicitly deferred beyond OMI v1 scope.

---

## 6. Explicit Rejection of Alternatives

### Rejection of 4 GB 1R

While technically simpler, 4 GB 1R was rejected due to limited relevance and reduced instructional value for modern DDR4 systems.

### Rejection of 8 GB 2R

8 GB 2R was rejected due to:

- Elevated routing and SI complexity
- Increased training variability
- Higher validation burden
- Disproportionate execution risk for v1

These risks conflict with OMI v1's completion-first mandate.

---

## 7. Locked Parameters for OMI v1

The following parameters are **fixed for OMI v1**:

- Capacity: **8 GB**
- Rank count: **1R**
- Device width: **x8**
- Data width: **64-bit**
- ECC: **Not supported**
- Variants: **None**

Any proposal violating these parameters is considered **out of scope for OMI v1**.

---

## 8. Non-Implications

This decision does **not** imply:

- Exclusion of other capacities in future versions
- Commitment to non-ECC designs long term
- Optimization for performance or density
- Limitation on future rank experimentation

This is a **v1 execution decision only**.

---

## 9. Locking Statement

With acceptance of this document, the OMI v1 capacity and organization are considered **locked**.

All schematic, layout, validation, and documentation work MUST conform to this configuration.

---

*End of document*

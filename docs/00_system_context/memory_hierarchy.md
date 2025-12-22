# Memory Hierarchy: The Context for Open Memory

This document provides the **system-level context** for the Open Memory Initiative (OMI).

Before designing or documenting DDR memory modules, it is essential to understand **where system memory sits in the overall memory hierarchy** and **why its correctness is assumed by every other layer** of a computing system.

OMI begins here deliberately.

---

## What Is Memory Hierarchy?

Modern computer systems do not use a single type of memory.Instead, they rely on a **hierarchy of memory layers**, each optimized for a different trade-off between:

- Speed
- Cost
- Capacity

From fastest and smallest to slowest and largest, a typical hierarchy looks like:

1. CPU registers
2. L1 / L2 / L3 caches (SRAM)
3. Main memory (DRAM / DDR)
4. Secondary storage (SSD, HDD)
5. Archival or remote storage

Each level exists because no single memory technology can satisfy all requirements at once.

---

## Why the Hierarchy Exists

The memory hierarchy is built around a simple constraint:

> Fast memory is expensive and small.
> Cheap memory is slow and large.

To bridge this gap, systems rely on **locality of access**.

### Temporal Locality

If data is accessed once, it is likely to be accessed again soon.

### Spatial Locality

If a memory location is accessed, nearby locations are likely to be accessed as well.

Caches exploit these properties aggressively.
Main memory exists to support them.

---

## The Role of DRAM in the Hierarchy

DRAM occupies a **critical middle position**:

- It is far slower than CPU caches
- It is vastly faster than storage
- It is large enough to hold active programs and data
- It is the *last layer assumed to be correct*

Unlike storage, DRAM does not tolerate errors.
Unlike caches, DRAM is not tightly controlled by the CPU.

Yet **every higher layer depends on it behaving perfectly**.

---

## The Silent Assumption

From the perspective of software and CPUs:

- Loads return correct values
- Stores persist correctly
- Memory ordering rules are respected
- Data corruption does not occur

These are **assumptions**, not guarantees.

When DRAM violates them:

- Programs crash unpredictably
- Data corruption propagates silently
- Bugs become unreproducible
- Failures are blamed on software

This is why memory failures are among the most difficult system failures to debug.

---

## Why DRAM Errors Are Different

Storage errors are often detected.
Cache errors may be corrected.
Register errors are catastrophic but visible.

DRAM errors are dangerous because they can be:

- Silent
- Data-dependent
- Temperature-dependent
- Timing-dependent
- Platform-specific

A single marginal signal or unstable reference voltage can corrupt data without immediate detection.

From the system's point of view, **DRAM must simply work**.

---

## Education Stops at the Interface

In most curricula and documentation:

- Memory hierarchy is taught abstractly
- DRAM is treated as a black box
- DDR timing is presented as configuration, not engineering
- Module-level design is ignored entirely

Engineers are trained to **use** memory, not to **understand or build** it.

This creates a structural gap:

- Open CPUs rely on closed memory
- Debugging stops at "probably RAM"
- Knowledge is centralized and inaccessible

---

## Why This Matters for OMI

OMI exists to address this gap.

If DRAM is the foundation of the memory hierarchy, then:

- It must be inspectable
- Its design assumptions must be explicit
- Its failure modes must be documented
- Its implementation must be reproducible

Open systems are not complete if their memory layer is opaque.

---

## Scope Implication

This is why OMI starts at the **module level**:

- Not at the CPU
- Not at the silicon cell
- But at the point where electrical reality meets system assumptions

Understanding memory hierarchy is not optional background.
It is the **justification** for everything that follows.

---

## Takeaway

The memory hierarchy works not because DRAM is simple,
but because it is engineered carefully and assumed to be correct.

OMI exists to make that engineering:

- Visible
- Understandable
- Documented
- Reproducible

Only then can the hierarchy be truly open.

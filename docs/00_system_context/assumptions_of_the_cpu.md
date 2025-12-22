# Assumptions of the CPU About Memory

This document explicitly states the **assumptions a CPU makes about system memory**.

These assumptions are rarely written down in one place, yet they define the **minimum correctness requirements** that DRAM and memory modules must satisfy for a system to function reliably.

OMI treats these assumptions as engineering constraints, not abstractions.

---

## Memory Is Not Optional for the CPU

From the CPU's point of view, memory is not a peripheral.
It is a **structural extension of computation**.

Every instruction that:

- Loads data
- Stores data
- Fetches instructions
- Maintains architectural state

implicitly assumes that memory behaves correctly.

The CPU does not ask *whether* memory is correct.
It assumes that it is.

---

## Assumption 1 — Reads Return the Last Written Value

The most fundamental assumption:

> A load from a memory address returns the most recently stored value to that address, according to the defined memory ordering rules.

This assumption underpins:

- Program correctness
- Variable semantics
- Control flow
- Data structures

If this assumption is violated:

- Programs behave unpredictably
- Bugs appear non-deterministic
- Debugging becomes impossible

The CPU does not validate returned data.
It trusts memory completely.

---

## Assumption 2 — Memory Operations Are Deterministic

The CPU assumes that memory behavior is:

- Deterministic
- Repeatable under the same conditions
- Independent of unrelated activity

Memory must not:

- Return different values for the same load
- Fail intermittently without cause
- Depend on temperature, noise, or timing margins in unpredictable ways

When memory becomes probabilistic, the CPU has no mechanism to adapt.

---

## Assumption 3 — Timing Rules Are Always Met

Modern CPUs issue memory requests under strict timing expectations.

They assume that:

- Setup and hold times are met
- Command and data relationships are honored
- Latency is within defined bounds
- Protocol timing parameters are respected

The CPU does not negotiate timing dynamically at the signal level.

Violating timing margins does not slow the system.
It corrupts data.

---

## Assumption 4 — Memory Errors Are Exceptionally Rare

Architecturally, CPUs are designed under the assumption that:

> Memory errors are so rare that they can be ignored in normal operation.

This is why:

- Most systems lack end-to-end memory verification
- Loads do not include integrity checks
- Stores do not confirm correctness

When errors do occur, the system has limited ability to respond meaningfully.

---

## Assumption 5 — Memory Is Cohesive Across the System

The CPU assumes that:

- All cores see a consistent view of memory
- Cache coherence protocols rely on correct memory behavior
- Memory ordering rules are upheld globally

Memory is treated as a **shared, reliable substrate**.

If memory violates this cohesion:

- Coherence breaks
- Synchronization primitives fail
- System correctness collapses

---

## Assumption 6 — Memory Does Not Introduce Side Effects

The CPU assumes that memory:

- Does not alter data silently
- Does not introduce unintended transformations
- Does not behave differently based on access patterns

Memory is expected to be passive, not active.

Any side effects at the memory level break architectural guarantees.

---

## Assumption 7 — Memory Works Below the Level of Visibility

Critically, the CPU assumes that memory works **below the level of architectural visibility**.

This means:

- The CPU does not monitor signal integrity
- The CPU does not track voltage margins
- The CPU does not detect analog instability

All of this is delegated to memory design, validation, and manufacturing.

Failures are surfaced only after damage is done.

---

## What the CPU Does *Not* Assume

The CPU does **not** assume:

- That memory is fast
- That memory is power-efficient
- That memory is optimal
- That memory is over-engineered

It assumes only one thing absolutely:

> That memory is correct.

Performance degradation is tolerable.
Incorrectness is not.

---

## Implications for Memory Design

Because the CPU assumes correctness absolutely:

- There is no safety margin at the architectural level
- There is no graceful degradation
- There is no retry mechanism for corrupted data

This places the burden entirely on:

- Electrical design
- Signal integrity
- Power integrity
- Timing closure
- Validation methodology

Memory must meet these assumptions **at all times**, not just nominally.

---

## Why This Matters for OMI

OMI treats CPU assumptions as **non-negotiable constraints**.

Every design decision in OMI must answer:

- Which CPU assumption does this protect?
- What happens if this margin is violated?
- How is this validated?

Open memory is not just about publishing files.
It is about making these hidden contracts explicit.

---

## Takeaway

The CPU is uncompromising.

It assumes that memory:

- Is correct
- Is deterministic
- Is invisible
- Never lies

DRAM must earn that trust through engineering, not assumption.

OMI exists to document and justify how that trust is built.

# Bank Groups: Scaling Parallelism Without Breaking DRAM

This document explains **bank groups**, why they were introduced in modern DDR generations, and how they affect timing, parallelism, and correctness.

Bank groups exist to scale bandwidth, but they also introduce new constraints that must be respected by controllers and memory designs.

---

## Why Banks Alone Were Not Enough

Early DRAM generations relied on banks to provide parallelism.

Banks allow:

- Independent row activation
- Overlapping operations
- Hiding row activation latency

However, as DRAM density and speed increased:

- More banks were added
- Command rates increased
- Electrical and timing limits were reached

Simply adding more banks stopped scaling efficiently.

---

## The Core Problem: Internal Resource Contention

Even with many banks:

- Internal buses are shared
- Command decoding logic is shared
- Data paths converge toward I/O circuitry
- Power delivery is global

Activating or accessing too many banks simultaneously causes:

- Excessive current draw
- Voltage droop
- Internal timing instability

Banks were logically independent, but **physically coupled**.

---

## What Bank Groups Are

A **bank group** is a higher-level grouping of banks.

Instead of treating all banks equally:

- Banks are divided into multiple groups
- Each group has partially independent internal resources
- Access rules differ within and across groups

Bank groups sit **between banks and the full device** in the hierarchy.

---

## How Bank Groups Improve Throughput

Bank groups enable:

- Higher effective command rates
- Increased parallel column access
- Better pipelining of operations

By alternating accesses across bank groups:

- Internal contention is reduced
- Data paths are better utilized
- Sustained bandwidth increases

This allows higher DDR speeds without redesigning the entire array.

---

## Asymmetry: Same Group vs Different Group

Bank groups introduce **asymmetric timing rules**.

Accessing:

- Two banks in the **same bank group**  
  → Stricter timing constraints

- Two banks in **different bank groups**  
  → More relaxed timing

This reflects the sharing of internal resources within a group.

---

## New Timing Constraints Introduced

Bank groups require additional timing parameters, such as:

- Delays between column commands
- Restrictions on back-to-back accesses
- Limits on simultaneous operations

These constraints protect:

- Internal data paths
- Sense amplifier stability
- Power integrity

They are not arbitrary.
They reflect real hardware limits.

---

## Why Bank Groups Complicate Controllers

With bank groups:

- Command scheduling becomes stateful
- Optimal access patterns are non-trivial
- Poor scheduling reduces performance
- Incorrect scheduling risks corruption

Controllers must now consider:

- Which bank
- Which bank group
- What was accessed recently

This complexity is hidden from software.

---

## Why Software Still Does Not See Bank Groups

Despite their importance:

- Software sees a flat memory address space
- Compilers and programs are unaware of bank groups
- Responsibility lies entirely with hardware

This reinforces the idea that:

> Memory correctness depends on invisible constraints.

---

## Implications for Timing and Margins

Bank group rules exist to:

- Prevent internal contention
- Avoid marginal sensing conditions
- Preserve timing margins at high speeds

Ignoring these rules may:

- Work at low load
- Fail under sustained throughput
- Break only on specific platforms

These are the hardest failures to diagnose.

---

## Implications for Module-Level Design

At the module level:

- Bank group activity increases switching noise
- Burst-heavy traffic stresses power delivery
- Simultaneous accesses amplify signal integrity issues

Poor layout or decoupling:

- Shrinks timing margins
- Exacerbates bank group conflicts
- Turns theoretical constraints into real failures

OMI treats bank groups as a **design-relevant concept**, not just a controller detail.

---

## Why Bank Groups Matter for OMI

OMI documents bank groups because:

- They explain why timing tables became more complex
- They justify conservative design margins
- They show why validation must include stress patterns

Ignoring bank groups leads to:

- Oversimplified models
- Fragile designs
- Misinterpreted failures

---

## Takeaway

Bank groups exist because DRAM cannot scale indefinitely with flat parallelism.

They:

- Increase throughput
- Add complexity
- Introduce asymmetric timing rules

Understanding bank groups is essential to understanding modern DDR behavior.

OMI documents them so this complexity is explicit, not hidden.

# Rows, Columns, and Banks: DRAM Architectural Organization

This document explains **how DRAM cells are organized architecturally** into rows, columns, and banks, and why this structure fundamentally shapes performance, timing, and correctness.

Before understanding DDR commands and timings, it is essential to understand **what those commands operate on**.

---

## Why Organization Matters

DRAM is not accessed as individual bits.

It is organized to:

- Minimize silicon area
- Share expensive circuitry
- Balance density against access speed

The way DRAM is structured determines:

- Access granularity
- Latency behavior
- Timing constraints
- Failure modes

DDR protocols exist to manage this structure safely.

---

## The DRAM Array

At the lowest level, DRAM consists of a **two-dimensional array of cells**.

- Each cell stores one bit
- Cells are arranged in rows and columns
- Rows share wordlines
- Columns share bitlines

This arrangement allows millions or billions of cells to be addressed efficiently.

---

## Rows: The Fundamental Unit of Activation

A **row** is a horizontal slice of the DRAM array.

When a row is activated:

- All cells in that row are connected to their bitlines
- Sense amplifiers detect and amplify stored charge
- Data is restored back into the cells

Key properties:

- Row activation is expensive
- Only one row per bank can be active at a time
- Activated rows remain open until precharged

Row size is typically large (kilobytes), even though accesses may be small.

---

## Columns: Selecting Data Within a Row

Once a row is active:

- Column logic selects a subset of bits from the row
- These bits are transferred to the I/O circuitry
- Data is delivered in bursts

Column access is relatively fast compared to row activation.

This asymmetry is why:

- Sequential access is efficient
- Random access across rows is expensive

---

## Sense Amplifiers: Shared and Critical

Sense amplifiers sit between rows and columns.

They:

- Detect extremely small voltage differences
- Amplify them to full logic levels
- Temporarily store row data while the row is open

Because sense amplifiers are large and power-hungry:

- They are shared across many cells
- Their availability limits parallelism

This sharing drives much of DRAM timing behavior.

---

## Banks: Enabling Limited Parallelism

To improve throughput, DRAM arrays are divided into **banks**.

Each bank:

- Has its own row buffer and sense amplifiers
- Can have one active row independently of other banks
- Operates mostly independently

Banks allow:

- Overlapping operations
- Hiding row activation latency
- Increased effective bandwidth

However, banks are not fully independent.
They share:

- Power rails
- Command buses
- I/O resources

---

## Why Only One Row per Bank

Within a bank:

- Sense amplifiers are reused
- Only one row can be connected at a time

Attempting to activate a second row without closing the first would:

- Corrupt data
- Short multiple cells together
- Destroy stored charge

This is why **precharge** is mandatory before switching rows.

---

## Row Buffer: Opportunity and Risk

The row buffer holds the currently active row.

Benefits:

- Repeated access to the same row is fast
- Sequential accesses are efficient

Risks:

- Accessing different rows causes penalties
- Poor access patterns reduce performance
- Timing violations corrupt data silently

Row buffer behavior is invisible to software but critical to correctness.

---

## Banks vs. Bank Groups (Preview)

Modern DRAM introduces bank groups to:

- Increase parallelism
- Reduce electrical loading
- Improve scalability

However:

- Bank groups introduce additional timing constraints
- They complicate command scheduling

OMI treats bank groups as an extension of this model, not a replacement.

(They are covered in later documents.)

---

## Architectural Consequences

This organization creates fundamental trade-offs:

- Large rows → efficiency but latency penalties
- Shared sense amplifiers → density but serialization
- Limited banks → parallelism but contention

DDR timing parameters exist to protect these architectural realities.

They are not arbitrary.

---

## Why This Matters for OMI

At the module level:

- Signal integrity affects row sensing
- Power noise affects sense amplifier stability
- Timing skew affects row activation correctness

Understanding rows, columns, and banks makes it possible to:

- Interpret DDR timings meaningfully
- Understand performance pathologies
- Design memory modules responsibly

OMI documents this structure so design choices remain grounded in reality.

---

## Takeaway

DRAM is organized to maximize density, not simplicity.

Rows define activation cost.
Columns define access granularity.
Banks define limited parallelism.

Every DDR command exists to safely navigate this structure.

Understanding this architecture is mandatory before discussing protocol or layout.

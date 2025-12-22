# DRAM Cell and Refresh: Physical Reality Behind System Memory

This document explains **how a DRAM cell actually stores data**, why that data is inherently unstable, and why **refresh is mandatory** for correct system operation.

Understanding this is essential before discussing DDR protocols, timings, or module-level design.

---

## The DRAM Cell: Minimal by Design

At its core, a DRAM cell consists of only two components:

- One capacitor
- One access transistor

This simplicity is intentional. It allows DRAM to achieve **very high density** at low cost.

However, this design choice introduces fundamental limitations.

---

## How a DRAM Cell Stores Data

A DRAM cell represents data using **electric charge**:

- Charged capacitor → logical 1
- Discharged capacitor → logical 0

The access transistor acts as a switch:

- It connects the capacitor to the bitline when enabled
- It isolates the capacitor otherwise

Unlike SRAM, there is **no feedback mechanism** to maintain state.

The data exists only as stored charge.

---

## Charge Leakage Is Inevitable

Capacitors are not perfect.

Even when isolated:

- Charge leaks over time
- Leakage rate varies with temperature
- Manufacturing variation affects retention

This means:

> DRAM data **decays continuously**, even when not accessed.

Without intervention, every DRAM cell will eventually lose its stored value.

---

## Why Refresh Exists

Refresh is the process of **periodically restoring charge** in every DRAM cell.

This involves:

1. Activating a row
2. Reading the stored charge
3. Rewriting the same value back into the cell

Refresh is not optional.
It is required to prevent silent data loss.

---

## Refresh Is a System-Wide Operation

Refresh is performed:

- Continuously
- Automatically
- In the background

But it has consequences:

- Memory access is temporarily blocked
- Latency increases during refresh windows
- Timing constraints become tighter

The system must schedule refresh without violating CPU assumptions about memory correctness.

---

## Destructive Reads: A Hidden Cost

Reading a DRAM cell is **destructive**.

When a row is activated:

- The small charge in each cell is sensed
- That charge is drained in the process

Therefore:

> Every read must be followed by a rewrite.

This is why:

- DRAM reads are slower than SRAM reads
- Row activation and precharge timings exist
- Incorrect timing corrupts data

---

## Rows, Sense Amplifiers, and Restoration

DRAM cells are arranged in rows and columns.

When a row is activated:

- All cells in the row connect to their bitlines
- Sense amplifiers detect and amplify tiny voltage differences
- The detected value is written back into each cell

This is both:

- A read operation
- A refresh operation for that row

The architecture optimizes for bulk operations, not individual bits.

---

## Retention Time Is Not Uniform

Not all DRAM cells behave identically.

Differences arise due to:

- Process variation
- Temperature gradients
- Aging effects
- Electrical noise

As a result:

- Some cells lose charge faster than others
- Worst-case behavior determines refresh requirements

Design must assume **the weakest cell**, not the average one.

---

## Why Timing Margins Exist

Because DRAM operates close to physical limits:

- Voltage margins are small
- Timing windows are narrow
- Noise tolerance is limited

Timing parameters exist to ensure:

- Sufficient charge sensing
- Complete restoration
- Safe precharge before the next operation

Violating these margins does not slow memory.
It corrupts it.

---

## Why This Matters for Module-Level Design

At the module level:

- Signal integrity affects sensing accuracy
- Power noise affects charge stability
- Timing skew affects restoration correctness

These are not abstract concerns.
They directly influence whether a DRAM cell retains correct data.

OMI documents these relationships explicitly.

---

## Implications for OMI

Because DRAM data is inherently unstable:

- Memory correctness is probabilistic without margins
- Design choices must preserve retention guarantees
- Validation must include worst-case conditions

Open memory design must acknowledge these physical realities.

Ignoring them creates designs that appear to work — until they do not.

---

## Takeaway

DRAM works not because it is robust,
but because it is **carefully managed**.

Data exists as fragile charge.
Reads destroy information.
Refresh is mandatory.
Margins are narrow.

Every layer above DRAM assumes this complexity has been handled correctly.

OMI exists to make that handling visible.

# Burst Behavior: Why DDR Transfers Data in Bursts

This document explains **why DDR memory transfers data in bursts rather than individual words**, and how burst behavior aligns with DRAM's internal architecture and system-level efficiency.

Burst behavior is not a performance trick.
It is a structural consequence of how DRAM works.

---

## What a Burst Is

In DDR, a **burst** is a sequence of data words transferred consecutively on the data bus as part of a single READ or WRITE operation.

Instead of requesting:

- One word per command

DDR requests:

- A block of contiguous data in one operation

Burst length is defined by the DDR standard and configuration.

---

## Why Single-Word Access Is Inefficient

At the DRAM level:

- Accessing a cell requires activating an entire row
- Sense amplifiers latch all data in that row
- The row buffer holds far more data than a single word

Fetching only one word would:

- Waste most of the activated data
- Pay the full activation cost repeatedly
- Severely limit bandwidth

Burst transfers exist to amortize row activation cost.

---

## Row Buffers and Spatial Locality

Once a row is active:

- Column access is fast
- Adjacent data is readily available
- Repeated column selects are cheap

Burst transfers exploit this by:

- Streaming data from the row buffer
- Minimizing additional commands
- Keeping the row open efficiently

This aligns naturally with spatial locality.

---

## Bursts and the External Data Bus

DDR uses a high-speed data bus with:

- Fixed width
- High toggle rates
- Tight timing margins

Sending data in bursts:

- Keeps the bus efficiently utilized
- Reduces command overhead
- Minimizes turnaround penalties

Idle bus cycles are wasted performance and wasted power.

---

## Why Bursts Improve Bandwidth, Not Latency

Burst behavior:

- Does not reduce the time to first data
- Does not make random access faster

Instead, it:

- Increases sustained throughput
- Makes efficient use of open rows
- Matches DRAM's internal parallelism

Latency is dominated by row activation.
Bursts address efficiency after that cost is paid.

---

## Fixed vs Configurable Burst Lengths

DDR standards define supported burst lengths.

Reasons for fixed or limited options:

- Simplify internal design
- Guarantee predictable timing
- Maintain signal integrity

Arbitrary burst lengths would:

- Complicate control logic
- Increase verification complexity
- Risk timing violations

Predictability is more valuable than flexibility.

---

## Read and Write Burst Behavior

### Read Bursts

- Data is driven by the DRAM onto the bus
- Timing is tightly controlled
- Data must be sampled precisely

### Write Bursts

- Data is driven by the controller
- DRAM must capture and store it
- Write recovery timing ensures stability

Both rely on burst discipline to maintain correctness.

---

## Burst Chop and Partial Transfers

Some DDR generations support:

- Shortened bursts
- Burst chopping

These exist to:

- Improve alignment with cache line sizes
- Reduce wasted transfers

However:

- They do not eliminate row activation cost
- They still rely on full-row sensing internally

The architectural trade-offs remain.

---

## Bursts, Caches, and Cache Lines

Burst sizes are often chosen to:

- Match cache line widths
- Optimize cache fill operations
- Reduce memory-level inefficiency

This tight coupling between:

- CPU cache design
- Memory controller behavior
- DDR burst structure

Is intentional and fundamental.

---

## Implications for Module-Level Design

At the module level:

- Burst transfers stress data lines continuously
- Signal integrity must hold over multiple cycles
- Timing skew accumulates across the burst

Poor routing or termination:

- Causes bit errors mid-burst
- Corrupts cache lines
- Breaks higher-level assumptions

Module design must assume worst-case burst activity.

---

## Why Burst Errors Are Hard to Detect

A burst error may:

- Affect only part of a cache line
- Pass simple functional tests
- Surface only under sustained load

This is another reason why:

- Validation must be stress-based
- Marginal designs are dangerous

---

## Why OMI Documents Burst Behavior

Burst behavior connects:

- DRAM architecture
- DDR protocol
- CPU cache behavior
- Module-level electrical constraints

Ignoring it leads to:

- Misinterpretation of timing
- Underestimating signal integrity needs
- Fragile memory designs

OMI documents bursts to keep design grounded in reality.

---

## Takeaway

DDR uses bursts because:

- Rows are large
- Activation is expensive
- Data is already available in bulk

Bursts are not optional optimizations.
They are the natural way DRAM must be used.

Understanding bursts is understanding how memory achieves bandwidth.

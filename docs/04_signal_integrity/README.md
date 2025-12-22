# Stage 4 — Signal Integrity

Stage 4 explains **why high-speed memory signals behave the way they do**, and how physical design choices translate directly into timing margins, data corruption, or reliability.

This stage is intentionally **analytical**.

It does not focus on layout rules first.
It focuses on understanding the *physics* that make those rules necessary.

---

## Why Signal Integrity Deserves Its Own Stage

At DDR speeds, signal integrity is not an optimization topic.
It is a **correctness topic**.

If signal integrity fails:

- Timing parameters are violated
- Setup and hold margins collapse
- Data is sampled incorrectly
- Errors appear silent and intermittent

No amount of protocol correctness can compensate for poor signal integrity.

---

## What Signal Integrity Actually Means

In the context of DDR memory, signal integrity means:

- Signals arrive when they are expected
- Signals settle to valid logic levels before sampling
- Noise does not cross decision thresholds
- Timing skew remains within margins
- Behavior is predictable across temperature and load

Signal integrity is not about "clean-looking waveforms".
It is about **preserving timing and voltage margins**.

---

## How This Stage Builds on Earlier Stages

Stage 4 depends directly on:

- **Stage 1 — DRAM Fundamentals**  
  (fragile sensing, destructive reads)

- **Stage 2 — DDR Protocol**  
  (tight timing contracts, burst behavior, bank groups)

- **Stage 3 — DIMM Anatomy**  
  (termination, topology, power rails, PCB effects)

Signal integrity explains *why those constraints exist physically*.

---

## Core Questions This Stage Answers

After completing Stage 4, a contributor should be able to answer:

- Why does a trace behave like a transmission line?
- Why do reflections shrink timing margins?
- Why does length mismatch cause data errors?
- Why does termination placement matter?
- Why does noise look pattern-dependent?
- Why do problems appear only at speed or under load?

If these questions feel intuitive, Stage 4 has succeeded.

---

## Documents in This Stage

The documents in Stage 4 should be read **in order**.

### 1. Transmission Lines
**`transmission_lines.md`**

Explains:

- When a wire becomes a transmission line
- Propagation delay
- Characteristic impedance
- Why "short traces" stop being short

This is the foundation of all signal integrity.

---

### 2. Reflections and Impedance Mismatch
**`reflections_and_matching.md`**

Explains:

- Why reflections occur
- How impedance mismatch creates ringing
- How reflections distort timing
- Why matching is about margins, not perfection

---

### 3. Length Matching and Skew
**`length_matching.md`**

Explains:

- How skew accumulates
- Why DDR timing windows are small
- Why byte lanes are matched
- Why address skew matters differently than data skew

---

### 4. Crosstalk and Noise Coupling
**`crosstalk_and_noise.md`**

Explains:

- Capacitive and inductive coupling
- Why adjacent signals interfere
- Why simultaneous switching noise matters
- Why activity-dependent failures occur

---

### 5. Eye Diagrams and Margins
**`eye_diagrams_and_margins.md`**

Explains:

- What an eye diagram represents
- How timing and voltage margins are visualized
- Why "passing" is not binary
- How margins disappear before failure

---

## What This Stage Does NOT Cover (Yet)

Stage 4 does not yet focus on:

- Specific PCB layout rules
- CAD tool workflows
- Vendor-specific constraints

Those come later, once intuition is built.

This stage teaches **why the rules exist**, not how to follow them blindly.

---

## Why OMI Emphasizes Signal Integrity

Many memory designs fail not because:

- The protocol was wrong
- The timings were incorrect
- The schematic was incomplete

But because:

- Physical effects were underestimated
- Margins were assumed instead of measured
- Layout choices were treated as cosmetic

OMI treats signal integrity as **core engineering knowledge**, not tribal expertise.

---

## Takeaway

At DDR speeds:

- Bits are waves
- Timing is geometry
- Noise is data-dependent
- Margins are fragile

Signal integrity is how we keep memory honest.

Stage 4 exists to make that understanding explicit.

---

Proceed to:
➡️ `transmission_lines.md`

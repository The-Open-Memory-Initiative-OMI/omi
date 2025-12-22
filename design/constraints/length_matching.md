# Length Matching Constraints

This document defines the **length matching constraints** for the OMI v1 DIMM design.

It explains:

- Which signals require length matching
- Which signals do not
- Why each constraint exists
- What failure modes each constraint prevents

This document intentionally avoids numerical limits, routing techniques, or tool-specific constraints.

---

## Purpose of Length Matching

Length matching exists to control **skew**.

Skew is the difference in arrival time between signals that are intended to be interpreted together.

In DDR systems:

- Skew directly consumes setup and hold margins
- Margins are extremely limited
- Small mismatches can cause silent data corruption

Length matching is how geometry is translated into timing control.

---

## Guiding Principle

Length matching is not about making everything equal.

It is about:

- Preserving timing windows
- Maintaining correct relative arrival order
- Ensuring stable sampling points

Only signals that are *interpreted together* must be matched.

---

## Signal Groups and Matching Requirements

### 1. Data Signals (DQ) Within a Byte Lane

**Requirement:**  
DQ signals belonging to the same byte lane **must be tightly matched to each other**.

**Why:**

- DQ signals are sampled simultaneously
- Skew between bits shrinks the data eye
- Bit-to-bit misalignment causes data corruption within a burst

**What this protects against:**

- Bit errors within cache lines
- Pattern-dependent corruption
- Mid-burst failures

This is the most critical length-matching requirement.

---

### 2. Data Strobe (DQS) to Its Associated DQ Group

**Requirement:**  
Each DQS signal must be closely matched to its associated DQ signals.

**Why:**

- DQS defines the sampling window for DQ
- Skew between DQS and DQ shifts the sampling point
- Excessive skew causes setup or hold violations

**What this protects against:**

- Sampling valid data too early or too late
- Eye collapse
- Immediate read/write errors

DQS-to-DQ matching is non-negotiable.

---

### 3. Matching Between Byte Lanes

**Requirement:**  
Byte lanes should be **loosely matched relative to each other**, but do not require tight matching.

**Why:**

- Each byte lane is trained independently
- Controllers compensate for lane-to-lane delay
- Absolute alignment is not required

**What this protects against:**

- Excessive calibration range usage
- Uneven margin distribution

Over-matching byte lanes increases routing complexity without benefit.

---

### 4. Address and Command Signals

**Requirement:**  
Address and command signals should be **matched as a group**, but do not require the same tight constraints as data signals.

**Why:**

- These signals are sampled together
- Fly-by topology introduces intentional skew
- Controllers account for ordered arrival

**What this protects against:**

- Command misinterpretation
- Inconsistent sampling across devices

Relative consistency matters more than absolute equality.

---

### 5. Clock Signals

**Requirement:**  
Clock signals must be **symmetrical and balanced**, especially within differential pairs.

**Why:**

- Clock defines global timing reference
- Skew affects all operations
- Differential imbalance introduces jitter

**What this protects against:**

- Setup/hold margin loss across the system
- Calibration instability
- Global timing failure

Clock integrity has system-wide impact.

---

### 6. Reset and Initialization Signals

**Requirement:**  
Reset and initialization signals **do not require tight length matching**.

**Why:**

- They are not high-speed
- They change infrequently
- They are not sampled in tight timing windows

**What this protects against:**

- Unnecessary routing complexity
- Over-constraint of non-critical signals

Clarity matters more than symmetry here.

---

## What Must NOT Be Length-Matched

Over-matching can be harmful.

Signals that should not be aggressively matched include:

- Reset signals
- Low-speed configuration signals
- Signals not sampled relative to each other

Overuse of serpentine routing can:

- Increase crosstalk
- Increase inductance
- Degrade signal integrity

Matching must always be justified by timing relationships.

---

## Relationship to Topology

Length matching constraints follow directly from topology choices:

- Point-to-point data topology → tight DQ/DQS matching
- Fly-by command topology → group-level consistency
- Shared clock topology → balanced distribution

Topology defines *what matching is meaningful*.

---

## Relationship to Signal Integrity

Length matching controls:

- Horizontal eye opening
- Sampling stability
- Timing margin allocation

It does not solve:

- Crosstalk
- Power noise
- Poor impedance control

Those must be handled separately.

---

## Design Intent for OMI v1

For OMI v1:

- Length matching is applied only where justified
- Conservative assumptions are used
- No unnecessary over-constraint is introduced
- Clarity and reproducibility are prioritized

Matching rules must be explainable in plain language.

---

## What This Document Does NOT Decide

This document does not define:

- Exact length tolerances
- Serpentine strategies
- CAD constraint values
- Stack-up-dependent rules

Those belong to later implementation stages.

---

## Takeaway

Length matching is how timing is protected geometrically.

Not everything must match.
Only what is sampled together matters.

For OMI v1, length matching is applied deliberately, not reflexively.

---

Next document in this directory:
- `skew_budget.md`

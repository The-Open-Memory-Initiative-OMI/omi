# Skew Budget

This document defines the **conceptual skew budget** for the OMI v1 DIMM design.

It explains:

- What skew budget means
- Where skew comes from
- How skew consumes timing margin
- How skew is allocated across the system

This document intentionally avoids numerical limits or technology-specific values.

---

## What a Skew Budget Is

A **skew budget** is the portion of the total timing margin that is consumed by differences in signal arrival time.

In DDR systems:

- Total timing margin is extremely limited
- Skew competes with noise, jitter, and uncertainty
- Margin must be shared deliberately

Skew budget is not measured in isolation.
It is part of a larger margin economy.

---

## Why Skew Budget Must Be Explicit

If skew budget is not explicitly considered:

- Geometry silently consumes margin
- Calibration margins are exhausted
- Failures appear intermittent and unexplainable

Explicit skew budgeting ensures that:

- No single source dominates margin loss
- Design decisions remain balanced
- Worst-case behavior remains safe

---

## Sources of Skew

Skew arises from multiple contributors.

### 1. Trace Length Differences

- Differences in physical distance
- Layer changes and via usage
- Routing asymmetry

This is the most obvious source, but not the only one.

---

### 2. Driver and Receiver Variability

- Output driver delay variation
- Input threshold variation
- Process and temperature effects

These are not controlled by routing.

---

### 3. Clock Distribution Skew

- Differences in clock arrival time
- Differential imbalance
- Jitter-induced uncertainty

Clock skew propagates into all synchronous sampling.

---

### 4. Crosstalk and Noise-Induced Timing Shift

- Noise alters edge crossing times
- Activity-dependent interference
- Power-induced reference movement

These effects vary dynamically.

---

### 5. Calibration and Training Error

- Finite resolution of training mechanisms
- Drift over temperature and voltage
- Limited compensation range

Calibration is not infinite or perfect.

---

## Skew Budget as a Shared Resource

The skew budget must be shared among:

- Geometry (layout-induced skew)
- Electrical effects (noise, reflections)
- Clock uncertainty
- Calibration error

Over-consuming budget in one area leaves no margin elsewhere.

This is why conservative architectural decisions matter.

---

## Skew Budget by Signal Group

### Data and Strobes (DQ/DQS)

Data sampling has the tightest skew budget.

Skew budget must account for:

- DQ-to-DQ mismatch within a byte lane
- DQS-to-DQ alignment
- Lane-to-lane delay variation
- Dynamic jitter and noise

Most of the skew budget is consumed here.

---

### Address and Command Signals

Address and command skew budget:

- Is larger than data
- Is influenced by fly-by ordering
- Is partially compensated by protocol timing

However:

- Excessive skew still causes command failure
- Budget must remain bounded

Predictability is more important than symmetry.

---

### Clock Signals

Clock skew budget:

- Affects all signals simultaneously
- Consumes margin globally
- Interacts with jitter and noise

Clock skew must be minimized aggressively because:

- It cannot be compensated locally
- Errors propagate everywhere

---

### Reset and Control Signals

Reset and control skew:

- Is not timing-critical during normal operation
- Has generous tolerance
- Does not meaningfully consume timing margin

These signals are not budget drivers.

---

## Relationship Between Skew and Eye Margins

Skew primarily reduces:

- Horizontal eye opening
- Effective setup and hold windows

When combined with:

- Voltage noise
- Reflections
- Jitter

The eye closes faster than expected.

Skew is rarely the sole cause of failure.
It is a major contributor.

---

## Why Calibration Does Not Eliminate Skew

DDR systems rely on calibration and training, but:

- Calibration has finite resolution
- Calibration assumes bounded skew
- Calibration cannot correct dynamic variation
- Calibration does not remove noise-induced skew

Design must ensure skew stays within correctable limits.

Calibration is a safety net, not a license to ignore geometry.

---

## Design Intent for OMI v1

For OMI v1:

- Skew budget is treated as a limited resource
- No signal group is allowed to consume it excessively
- Conservative assumptions are preferred
- Geometry is controlled to preserve margin

Design decisions must respect the skew budget holistically.

---

## What This Document Does NOT Decide

This document does not define:

- Numerical skew limits
- Timing parameters
- Training algorithms
- Tool-specific constraints

Those belong to implementation and validation stages.

---

## Takeaway

Skew consumes timing margin invisibly.

Once margin is gone, failure follows — often silently.

A skew budget makes timing a managed resource instead of a gamble.

For OMI v1, skew is controlled deliberately, not discovered accidentally.

---

This completes the constraint definition for Stage 5.

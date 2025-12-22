# Data and Strobe Signals

This document defines the **data (DQ) and data strobe (DQS) signal groups** for the OMI v1 DIMM design.

It explains:

- Which signals exist
- How they are grouped
- Who drives and samples them
- Why strobes are required
- How data correctness is preserved

This document intentionally avoids routing rules, timing numbers, and DDR-generation-specific details.

---

## Role of Data and Strobe Signals

Data and strobe signals together form the **data plane** of the memory system.

They are responsible for:

- Transferring payload data between controller and DRAM
- Defining *when* data is valid
- Enabling high-speed, double-data-rate operation

Unlike address and command signals, these signals:

- Are bidirectional
- Operate at the highest toggle rates
- Consume the largest portion of timing margin

---

## Data Signals (DQ)

### What DQ Signals Carry

DQ signals carry:

- Read data from DRAM to controller
- Write data from controller to DRAM

They represent the actual contents of memory.

Errors on DQ signals directly corrupt data.

---

### Directionality

DQ signals are **bidirectional**:

- During WRITE operations: controller → DRAM
- During READ operations: DRAM → controller

Direction changes dynamically based on the active command.

This makes:

- Turnaround behavior
- Signal integrity
- Termination strategy

Critical considerations later in the design.

---

## Data Strobes (DQS)

### Why Strobes Exist

At DDR speeds, it is not reliable to sample data using a global clock alone.

DQS signals exist to:

- Act as timing references for data
- Define the sampling window locally
- Compensate for propagation delay and skew

DQS is the **timing anchor** for data.

---

### Relationship Between DQ and DQS

Each DQS signal is associated with a **group of DQ signals**.

Key properties:

- DQ signals are sampled relative to their associated DQS
- DQS and its DQ group must arrive closely aligned
- Skew between DQ and DQS directly reduces timing margin

This relationship defines the fundamental grouping of data signals.

---

## Byte Lanes

Data signals are organized into **byte lanes**.

A byte lane consists of:

- A group of DQ signals
- One associated DQS (and its complement, if applicable)

Byte lanes:

- Operate largely independently
- Are matched and constrained as a group
- Allow scalable data widths

This structure simplifies timing calibration and signal integrity management.

---

## Bidirectional Timing Responsibility

### During Writes

- Controller drives DQ and DQS
- DRAM samples data relative to incoming DQS

### During Reads

- DRAM drives DQ and DQS
- Controller samples data relative to incoming DQS

This bidirectional role reversal:

- Complicates termination
- Makes timing margins asymmetric
- Requires careful architectural planning

---

## Sensitivity to Skew and Noise

Data and strobe signals are:

- The most timing-sensitive signals on the DIMM
- Highly sensitive to skew, reflections, and crosstalk
- Strongly affected by power and reference noise

Small disturbances here:

- Do not cause command failure
- Do not halt the system
- Quietly corrupt data

This is why DQ/DQS design is treated with the highest priority.

---

## Relationship to Burst Behavior

DDR data transfers occur in bursts.

Implications:

- Errors can appear mid-burst
- Pattern-dependent failures are common
- Marginal designs may pass short tests

Data integrity must be preserved across **entire bursts**, not just single edges.

---

## Electrical Characteristics (High-Level)

Data and strobe signals:

- Are point-to-point or tightly grouped
- Switch at high frequency
- Experience frequent direction changes
- Require controlled impedance

Because of this:

- They are routed differently from address/command signals
- They require stricter matching and constraints

Exact strategies are defined in later documents.

---

## Why Data and Strobes Are Documented Together

DQ and DQS are inseparable:

- Data has no meaning without timing
- Timing has no purpose without data

Grouping them reflects:

- Their physical coupling
- Their shared timing constraints
- Their role in correctness

---

## Design Intent for OMI v1

For OMI v1:

- Data signals are organized into byte lanes
- Each byte lane has a dedicated strobe
- Conservative, standards-compliant assumptions are used
- No exotic data optimizations are attempted

Correctness and reproducibility are the priorities.

---

## What This Document Does NOT Decide

This document does not define:

- Exact data width
- Exact number of byte lanes
- Voltage levels
- Timing margins
- Routing geometry
- Termination values

Those decisions belong to topology and constraint documents.

---

## Takeaway

Data signals carry truth.
Strobe signals define when truth is sampled.

Together, they form the most fragile and critical part of the memory system.

Designing them correctly is non-negotiable.

---

Next documents in this directory:
- `clocks_and_resets.md`

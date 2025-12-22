# Address and Command Signals

This document defines the **address and command signal group** for the OMI v1 DIMM design.

It describes:

- Which signals exist
- Who drives them
- Who receives them
- How they are shared
- Why they are structured this way

This document intentionally avoids routing, timing values, or PCB implementation details.

---

## Role of Address and Command Signals

Address and command signals are used to:

- Select rows, columns, banks, and bank groups
- Issue DDR commands (ACT, READ, WRITE, PRE, REF, etc.)
- Control DRAM operational state

They define **what operation occurs**, not the data itself.

Correct interpretation of these signals is essential for:

- Memory correctness
- Command sequencing
- Timing safety

---

## Signal Direction and Ownership

### Driver

- **Memory controller** (located on the CPU / SoC)

### Receivers

- **All DRAM devices on the DIMM**

Address and command signals are:

- **Unidirectional**
- Driven only by the controller
- Observed by all DRAM devices

There is no contention on this bus.

---

## Shared Nature of the Bus

Address and command signals are **shared across all DRAM devices** on the DIMM.

This means:

- All devices see the same commands
- Device selection is performed internally using:
  - Chip select
  - Address decoding
  - Bank and row fields

The DIMM does not perform command decoding.
It distributes commands electrically.

---

## Core Address Signals

Address signals encode:

- Row address bits
- Column address bits
- Bank address bits
- Bank group address bits (for supported DDR generations)

Key characteristics:

- Used during ACT, READ, WRITE, and REF operations
- Interpreted synchronously with command signals
- Must be stable during defined sampling windows

Address signals are not independent of command signals.
They are interpreted **in context**.

---

## Command Signals

Command signals encode:

- ACT (Activate)
- READ
- WRITE
- PRE (Precharge)
- REF (Refresh)
- Mode register access

Commands are typically encoded using combinations of:

- Row/column control signals
- Control strobes
- Enable lines

The exact encoding is defined by the DDR standard and memory controller.

---

## Chip Select (CS)

Chip select signals determine:

- Which rank responds to a command
- Which devices are active participants

Characteristics:

- Driven by the memory controller
- Observed by all DRAM devices
- Used to enable or disable command acceptance

Chip select allows:

- Multiple ranks per DIMM
- Electrical sharing of the address/command bus

---

## Clock Relationship

Address and command signals are:

- Synchronous to the DDR clock
- Sampled relative to defined clock edges

They are not self-timed.

This makes:

- Clock integrity
- Skew control
- Signal stability

Critical for correct command interpretation.

---

## Timing Sensitivity (Qualitative)

Address and command signals:

- Are sensitive to setup and hold timing
- Are not sampled continuously
- Are less timing-critical than data signals
- Still require controlled skew and integrity

Errors here cause:

- Incorrect command execution
- Wrong row or bank activation
- Catastrophic memory failure

Unlike data errors, command errors usually cause immediate failure.

---

## Electrical Characteristics (High-Level)

Address and command signals:

- Are multi-drop
- See multiple receivers
- Are susceptible to reflections
- Require termination

Because of these properties:

- Topology matters
- Termination strategy matters
- Signal integrity margins must be preserved

These aspects are addressed in the topology documents.

---

## Why These Signals Are Grouped Together

Address and command signals are grouped because:

- They are driven together
- They are sampled together
- They share electrical characteristics
- They share topology constraints

This grouping informs:

- Topology decisions
- Matching strategy
- Termination placement

---

## Design Intent for OMI v1

For OMI v1:

- Address and command signals are treated as a **shared, synchronous bus**
- Conservative, standards-compliant assumptions are used
- No custom encoding or optimization is attempted
- Clarity and correctness take priority

The goal is reproducibility, not novelty.

---

## What This Document Does NOT Decide

This document does not define:

- Exact signal counts
- Voltage levels
- Timing numbers
- Routing topology
- Termination values
- Length matching limits

Those decisions are made in later Stage 5 documents.

---

## Takeaway

Address and command signals:

- Define *what* the memory does
- Are shared across all devices
- Are driven only by the controller
- Must be interpreted correctly by every DRAM device

They are the **control plane** of the memory system.

Getting this structure right is a prerequisite for everything that follows.

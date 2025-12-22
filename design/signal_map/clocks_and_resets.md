# Clocks and Reset Signals

This document defines the **clock and reset-related signal groups** for the OMI v1 DIMM design.

It explains:

- What clock signals exist
- What reset and control signals exist
- Who drives and who receives them
- Why these signals are treated differently from others

This document remains architectural and avoids implementation details.

---

## Role of Clocks and Resets in the Memory System

Clock and reset signals form the **temporal and control foundation** of the memory system.

They are responsible for:

- Defining when signals are sampled
- Synchronizing command and data interpretation
- Bringing DRAM devices into a known, valid state

If clocks or resets are incorrect, **nothing else matters**.

---

## Clock Signals

### Purpose of the DDR Clock

DDR clock signals define:

- The timing reference for address and command sampling
- The phase relationship used by the memory controller
- The basis for timing calibration and alignment

Unlike data strobes (DQS), the DDR clock:

- Is global
- Is unidirectional
- Is always driven by the memory controller

---

### Direction and Ownership

- **Driver:** Memory controller (CPU / SoC)
- **Receivers:** All DRAM devices on the DIMM

Clock signals are:

- Unidirectional
- Shared across all DRAM devices
- Never driven by the DIMM

The DIMM distributes the clock electrically but does not modify it.

---

### Differential Nature

DDR clocks are typically:

- Differential
- Complementary (true and complement)

This improves:

- Noise immunity
- Timing stability
- Signal integrity at high speeds

Clock integrity is fundamental to all other timing relationships.

---

## Relationship Between Clock and Other Signals

- Address and command signals are sampled relative to the clock
- Data strobes (DQS) are phase-related to the clock
- Timing calibration relies on predictable clock behavior

Clock skew or noise affects:

- All commands
- All data transfers
- All timing margins simultaneously

This makes clock quality disproportionately important.

---

## Reset and Initialization Signals

### Purpose of Reset Signals

Reset and initialization-related signals:

- Bring DRAM devices into a known state
- Ensure predictable startup behavior
- Enable safe configuration and training

These signals are typically asserted during system bring-up.

---

### Direction and Ownership

- **Driver:** Memory controller or system logic
- **Receivers:** All DRAM devices

Reset signals are:

- Unidirectional
- Shared
- Not time-critical once initialization completes

---

### Behavior Characteristics

Reset-related signals:

- Change infrequently
- Are not high-speed
- Do not toggle during normal operation

Despite this, they must:

- Be clean
- Be unambiguous
- Meet minimum timing requirements

Incorrect reset behavior can prevent memory from functioning at all.

---

## Clock Enable and Related Control Signals

Some control signals:

- Gate clock interpretation
- Enable or disable command acceptance
- Control power or operational states

These signals:

- Are synchronous with the clock
- Are interpreted in specific protocol-defined contexts
- Affect internal DRAM state machines

They are grouped conceptually with clocks and resets due to their global impact.

---

## Electrical Characteristics (High-Level)

Clock and reset signals:

- Are shared across devices
- See multiple receivers
- Require controlled signal integrity
- Are sensitive to skew and noise

Clock signals, in particular:

- Have strict symmetry requirements
- Demand continuous reference paths
- Influence every other signal group

---

## Why Clocks and Resets Are Grouped Together

These signals are grouped because:

- They define system-wide timing and state
- Errors affect the entire DIMM simultaneously
- They are not data-dependent in normal operation

They form the **global control layer** of the memory system.

---

## Design Intent for OMI v1

For OMI v1:

- Clocks are treated as global, shared references
- Conservative assumptions are used
- No custom clock conditioning or buffering is introduced
- Reset behavior follows standard DDR expectations

Simplicity and correctness are prioritized.

---

## What This Document Does NOT Decide

This document does not define:

- Clock frequency
- Phase relationships
- Skew limits
- Termination strategy
- Routing topology
- Voltage levels

Those decisions belong in later Stage 5 documents.

---

## Takeaway

Clock signals define *when* memory listens.
Reset signals define *how* memory begins.

They are global, shared, and unforgiving.

If clocks or resets are wrong, memory does not degrade — it fails.

---

This completes the signal map for OMI v1.

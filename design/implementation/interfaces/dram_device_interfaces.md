# DRAM Device Interfaces

This document defines the **interface contract between the DRAM array block and individual DRAM devices** in the OMI v1 DIMM design.

It describes:
- How DRAM devices connect to the internal DIMM structure
- Which signal groups reach each device
- How byte-lane organization is enforced
- How power and reference domains are applied at the device level

This document is an interface definition.
It does not define pin numbers, symbols, or specific DRAM parts.

---

## Purpose of the DRAM Device Interface

The DRAM device interface exists to ensure that:
- Each DRAM device receives the correct signals
- Topology and constraint intent is preserved down to the device level
- No ambiguity exists during schematic capture or layout
- Device-level mistakes are structurally prevented

This interface is the **last abstraction boundary** before actual components.

---

## Device-Level View

Each DRAM device is treated as:
- A participant in a rank
- A member of a specific byte lane
- A consumer of shared control and clock signals
- A consumer of dedicated data and strobe signals

Devices are not generic endpoints.
They are role-specific participants in a tightly defined system.

---

## Shared Interfaces to Each DRAM Device

Each DRAM device connects to the following **shared interfaces**:

### Address and Command Interface
- Receives address bits
- Receives command encoding
- Interprets signals synchronously with the clock

Characteristics:
- Unidirectional (DIMM → device)
- Shared across all devices in the rank
- Distributed according to fly-by topology

---

### Clock Interface
- Receives differential clock signals
- Uses clock as the global timing reference

Characteristics:
- Shared across all devices
- Must remain phase-consistent
- Directly affects command interpretation and training

---

### Reset and Global Control Interface
- Receives reset and initialization signals
- Defines device state during bring-up

Characteristics:
- Shared
- Low-speed relative to data
- Not performance-critical during normal operation

---

## Byte Lane–Specific Interfaces

Each DRAM device is associated with **one byte lane** (or a defined slice of one).

### Data Interface (DQ)
- Bidirectional data signals
- Active during reads and writes
- Sampled relative to DQS

Characteristics:
- Point-to-point connectivity
- No sharing with other devices
- Most timing-sensitive interface

---

### Data Strobe Interface (DQS)
- Timing reference for associated DQ signals
- Bidirectional depending on operation

Characteristics:
- One-to-one relationship with its DQ group
- Must remain tightly aligned with DQ
- Defines sampling window

DQS is inseparable from its DQ group.

---

## Power and Reference Interfaces

Each DRAM device receives the following **power-related interfaces**:

### VDD (Core Supply)
- Powers internal memory array and logic

### VDDQ (I/O Supply)
- Powers signal drivers and receivers

### Vref (Reference Voltage)
- Defines logic threshold for input sampling
- Treated as a reference, not a supply

### VTT (Termination Bias)
- Supports signal termination behavior
- May be used dynamically via on-die termination

Each rail remains distinct at the device boundary.

---

## Power Domain Enforcement at Device Level

The interface enforces that:
- No device draws current from the wrong rail
- Reference voltages are not used as supplies
- Termination bias is not overloaded
- Noise isolation intent survives schematic capture

Violations here undermine the entire design.

---

## Rank Participation and Chip Select

Each device:
- Belongs to exactly one rank
- Responds only when its chip select is asserted
- Shares rank-level timing and control behavior

Rank participation is explicit and not inferred.

---

## Training and Calibration Expectations

The interface assumes:
- Device-level timing calibration is performed by the controller
- Byte lanes are trained independently
- Skew remains within correctable bounds (per Stage 5 constraints)

The interface does not attempt to "fix" poor geometry.

---

## What This Interface Explicitly Enforces

This interface enforces:
- Byte-lane isolation
- Shared control and clock visibility
- Point-to-point data connectivity
- Clean power domain separation
- Explicit rank membership

These properties must be visible in the schematic.

---

## What This Document Does NOT Decide

This document does not define:
- Specific DRAM part pinouts
- Exact signal counts
- Voltage levels
- Electrical characteristics
- Timing parameters
- Package types

Those are resolved when selecting actual DRAM components.

---

## Relationship to Earlier Stages

This interface directly implements:
- Signal maps
- Topology decisions
- Length matching and skew constraints
- Power architecture
- Design assumptions

No architectural interpretation is allowed at this stage.

---

## Takeaway

The DRAM device interface is where architecture meets reality.

If this interface is correct:
- Schematic capture is straightforward
- Layout constraints are meaningful
- Signal integrity intent survives
- Errors become hard to introduce silently

For OMI v1, correctness is enforced one interface at a time.

---

This completes the interface definitions for Stage 6.

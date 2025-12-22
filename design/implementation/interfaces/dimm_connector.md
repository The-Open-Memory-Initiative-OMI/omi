# DIMM Connector Interface

This document defines the **DIMM connector interface** for the OMI v1 DIMM design.

It describes:
- What the DIMM exposes to the host system through the connector
- How signals are grouped at the boundary
- Which rails and references enter the DIMM
- How this interface maps to internal blocks

This document is an interface contract.
It does not define an exact pinout or mechanical connector standard.

---

## Purpose of the DIMM Connector Interface

The connector interface is the **system boundary** of the DIMM.

Its purpose is to:
- Provide a clear contract between the DIMM and the host (memory controller + board)
- Ensure the DIMM's internal design maps cleanly to external expectations
- Prevent implementation ambiguity in schematic capture and layout

Everything that enters or leaves the DIMM passes through this interface.

---

## External Owner and Directionality

The host system provides and controls:
- Clock signals
- Address and command signals
- Reset and control signals
- Power rails (as defined in the power architecture)
- Low-speed management bus access for SPD

The DIMM provides:
- Data return during reads (DRAM → controller)
- SPD identification data (via low-speed interface)

Most signals are defined by the DDR standard and are not negotiable.

---

## Signal Grouping at the Connector

The connector interface groups signals into the following domains:

1. **Address and Command**
2. **Data and Strobes (Byte Lanes)**
3. **Clock and Global Control**
4. **Low-Speed Configuration (SPD / management bus)**
5. **Power and Reference Rails**
6. **Ground and return references**

Grouping is intentional and reflects:
- topology decisions
- constraint intent
- power domain separation

---

## 1. Address and Command Domain

This domain includes the shared, unidirectional control plane.

Characteristics:
- Driven by the host memory controller
- Received by all DRAM devices
- Shared across the rank(s)
- Interpreted synchronously with the clock

Internal mapping:
- Enters the **DRAM array block**
- Distributed according to the chosen **fly-by topology**

---

## 2. Data and Strobes Domain (Byte Lanes)

This domain includes all DQ and DQS signals.

Characteristics:
- Bidirectional DQ
- DQS used as the timing reference for DQ sampling
- Grouped by byte lane
- Most timing-critical signals on the DIMM

Internal mapping:
- Enters the **DRAM array block**
- Each byte lane maps to a dedicated internal lane interface
- Structured to preserve **point-to-point topology intent**

---

## 3. Clock and Global Control Domain

This domain includes the global timing reference and state controls.

Characteristics:
- Differential clock signals driven by the host
- Shared across all DRAM devices
- Global reset and initialization control signals

Internal mapping:
- Enters the **DRAM array block**
- Clock distribution must remain coherent with command interpretation
- Reset/control signals define bring-up state behavior

---

## 4. Low-Speed Configuration Domain (SPD / Management Bus)

This domain provides DIMM discovery and configuration capability.

Characteristics:
- Low-speed, host-driven communication
- Used to read SPD data during bring-up
- Not part of high-speed DDR signaling

Internal mapping:
- Enters the **SPD and auxiliary logic block**
- Powered by the auxiliary/standby power domain
- Isolated from high-speed rails and signals

---

## 5. Power and Reference Rails Domain

This domain provides electrical power and bias references into the DIMM.

Rails include:
- VDD (core)
- VDDQ (I/O)
- Vref (reference)
- VTT (termination bias)
- Auxiliary/standby power

Internal mapping:
- Enters the **power block**
- Distributed to DRAM array and auxiliary blocks
- Kept as distinct domains (no rail mixing)

Power rails are treated as part of correctness.

---

## 6. Ground and Return References

Ground pins provide:
- Return paths for high-speed currents
- Reference for impedance control
- Stability for signal thresholds and planes

Ground is not just "0V".
It is a core part of signal integrity.

Internal mapping:
- Connects to the DIMM ground reference structure
- Supports return paths for all high-speed domains
- Must remain continuous and low impedance

---

## Relationship to Implementation Blocks

At the block level:

- Address/command → DRAM array block
- Data/strobes → DRAM array block
- Clocks/control → DRAM array block
- SPD bus → SPD & auxiliary block
- Power rails → power block (then distributed internally)
- Grounds → shared reference system across all blocks

The connector interface is the single point where the host system meets these blocks.

---

## What This Document Does NOT Decide

This document does not define:
- Connector mechanical standard (UDIMM/SODIMM/etc.)
- Exact pin count
- Pin numbering
- Pin-to-net assignment
- Signal voltage levels
- Electrical values for pull-ups/termination

Those decisions occur in later implementation steps and standards alignment.

---

## Takeaway

The DIMM connector interface is the contract between:
- The host memory controller system
- The DIMM's internal architecture

By grouping signals and rails explicitly, OMI v1 ensures:
- implementation consistency
- reviewability
- reproducibility

A correct DIMM begins with a clear boundary.

---

Next documents:
- `dram_device_interfaces.md`

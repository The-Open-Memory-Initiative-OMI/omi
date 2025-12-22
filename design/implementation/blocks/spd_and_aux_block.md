# SPD and Auxiliary Logic Block

This document defines the **SPD and auxiliary logic block** for the OMI v1 DIMM design.

It describes:
- How configuration and discovery are supported
- What low-speed logic exists on the DIMM
- How auxiliary functions are powered and isolated
- How this block interfaces with the rest of the design

This document is block-level only.
It does not define device part numbers, pin assignments, or bus speeds.

---

## Purpose of the SPD and Auxiliary Logic Block

The SPD and auxiliary logic block provides the **configuration and identification layer** of the DIMM.

Its purpose is to:
- Allow the system to discover DIMM characteristics
- Support safe and correct memory bring-up
- Operate independently of high-speed memory signaling
- Remain functional during early power states

This block enables the DIMM to be *understood* before it is *used*.

---

## Functional Scope

This block includes:

- Serial Presence Detect (SPD) storage
- Low-speed configuration interfaces
- Any required pull-ups, biasing, or glue logic
- Power isolation and filtering for auxiliary circuitry

It does not participate in high-speed memory transactions.

---

## SPD Functionality

### Role of SPD

SPD provides:
- DIMM identification
- Capacity and organization data
- Timing and electrical characteristics
- Manufacturer and revision information

This information is read by firmware during system bring-up.

SPD data is **trusted implicitly** by the memory controller.

---

### SPD Independence from DRAM Operation

SPD functionality:
- Does not depend on DRAM being initialized
- Operates before memory training
- Remains accessible even if DRAM fails

This independence is critical for safe configuration.

---

## Interface Characteristics

The SPD and auxiliary block communicates with the system using:
- A low-speed serial interface
- A shared management bus

Key properties:
- Low frequency
- Non-time-critical
- Not performance-sensitive

This interface is logically and electrically isolated from DDR signaling.

---

## Power Domain

The SPD and auxiliary block is powered by:
- A dedicated auxiliary or standby power rail

Characteristics:
- Low current
- Always available during standby and bring-up
- Isolated from high-speed power noise

This ensures reliable operation during early boot.

---

## Isolation from High-Speed Domains

The SPD and auxiliary block is intentionally isolated from:
- VDD (DRAM core)
- VDDQ (I/O signaling)
- Vref (signal reference)
- VTT (termination bias)

Isolation prevents:
- Noise injection into sensitive domains
- Unintended loading of reference rails
- Crosstalk between configuration and data paths

This separation is enforced structurally.

---

## Reset and Control Behavior

Auxiliary logic:
- May observe global reset signals
- Does not control DRAM reset sequencing
- Does not participate in training or calibration

Its role is passive and descriptive, not active.

---

## Failure Containment

Failures within this block:
- Should not affect high-speed memory operation electrically
- Should not inject noise into DRAM domains
- Should be detectable during system bring-up

This block must fail safely.

---

## Relationship to Other Blocks

- Interfaces with the **power block** for auxiliary power
- Interfaces with the **connector interface** for low-speed communication
- Does not interface directly with the DRAM array block

This separation preserves clean block boundaries.

---

## What This Block Explicitly Enforces

This block enforces:
- Separation of configuration and data paths
- Standalone operation during bring-up
- Clean auxiliary power usage
- No hidden coupling to high-speed logic

Any shortcut here risks system-level failure.

---

## What This Block Does NOT Decide

This document does not define:
- SPD memory size
- Exact SPD contents
- Bus pull-up values
- Electrical characteristics of the serial bus
- Firmware behavior

Those belong to later implementation and software stages.

---

## Relationship to Stage 5 Decisions

This block directly implements:
- SPD overview and bring-up assumptions
- Power domain separation
- Design assumptions regarding configurability

No new architectural behavior is introduced.

---

## Takeaway

The SPD and auxiliary logic block allows the DIMM to explain itself.

It enables:
- Safe discovery
- Correct configuration
- Predictable bring-up

Without this block, even perfect hardware cannot be used correctly.

---

This completes the block-level implementation definition for Stage 6.

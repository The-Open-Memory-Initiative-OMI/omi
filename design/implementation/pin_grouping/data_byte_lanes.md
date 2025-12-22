# Data Byte Lane Pin Grouping

This document defines the **logical pin grouping** for data (DQ) and data strobe (DQS) signals in the OMI v1 DIMM design.

It specifies:
- How data signals are grouped into byte lanes
- How DQS is paired with its DQ group
- Lane naming and indexing conventions
- How lanes map to internal DRAM device groupings

This document does not define exact pin numbers, connector mapping, or signal counts.
It provides a stable grouping scheme for schematic capture and review.

---

## Purpose of Data Lane Grouping

Data signals are:
- Bidirectional
- High-speed
- Extremely timing-sensitive
- The most error-prone if represented poorly

Lane grouping exists to:
- Preserve the byte-lane architecture from Stage 5
- Make DQ/DQS relationships unambiguous
- Prevent accidental cross-lane mixing
- Prepare for consistent pin assignment later

If lanes are not represented cleanly, implementation becomes fragile.

---

## Byte Lane as the Fundamental Unit

In OMI v1, the **byte lane** is the fundamental data unit.

Each byte lane consists of:
- A group of DQ bits that move together
- One associated DQS timing reference (and complement if applicable)

All constraints and topology decisions apply per lane.

---

## Lane Indexing Convention

Byte lanes are indexed consistently across all documents and artifacts:

- `LANE0`, `LANE1`, `LANE2`, ... (conceptual indexing)

Indexing must remain stable across:
- DIMM connector grouping
- DRAM array block structure
- Device interface representation
- Constraint translation

Lane index drift is a critical implementation error.

---

## DQ Group Naming

Within each lane, DQ bits are represented as a bundle:

- `DQ<lane>[ ]`

Examples (conceptual):
- `DQ0[ ]` for LANE0 data bits
- `DQ1[ ]` for LANE1 data bits

Notes:
- The width of each `DQ<lane>[ ]` bundle is lane-defined and generation-dependent.
- DQ bits must never be named without lane association.

---

## DQS Pair Naming

Each lane has an associated strobe:

- `DQS<lane>` and (if applicable) `DQS<lane>_n`

Examples (conceptual):
- `DQS0`, `DQS0_n`
- `DQS1`, `DQS1_n`

Rules:
- DQS is always named with its lane index
- DQS is never shared between lanes
- DQS must appear adjacent to its DQ bundle in schematics

DQS is the timing anchor for the lane.

---

## Optional Data Mask / Data Control (Boundary Note)

Some DDR generations include lane-level data mask or lane-level data control signals.

If present, they follow the same rule:
- They are lane-scoped
- They are indexed
- They are represented adjacent to the lane bundle

Naming convention (conceptual):
- `DM<lane>` (or a lane-scoped control equivalent)

This document defines grouping intent, not the exact signal list.

---

## Bidirectional Behavior Representation

Each byte lane is bidirectional.

Schematics must represent the lane as:
- A single logical lane interface
- Not two separate "read" and "write" nets

Direction is determined by protocol state and device driving.
The grouping remains static.

---

## Mapping to DRAM Devices

Each byte lane maps to:
- One DRAM device (or defined device slice)
- A dedicated DQ/DQS interface at that device boundary

Rules:
- A lane's DQ and DQS signals connect only to the device(s) assigned to that lane
- No lane may split across multiple unrelated devices
- No device may receive mixed lane signals

This enforces the point-to-point data topology.

---

## Schematic Representation Rules

To keep schematics reviewable:

- Represent each lane as a single block/bundle
- Place `DQ<lane>[ ]` next to `DQS<lane>` / `DQS<lane>_n`
- Keep lane bundles visually separated from address/command bundles
- Keep lane bundles visually separated from clocks/control bundles
- Avoid mixing lane indices within a symbol

Each lane should look like an independent sub-system.

---

## Consistency and Naming Conventions

The design uses:
- Explicit lane indices everywhere (`0..N`)
- Bundle notation for DQ (`DQ<lane>[ ]`)
- Pair notation for DQS (`DQS<lane>`, `DQS<lane>_n`)

No vendor-specific naming is permitted.
If a contributor cannot tell which lane a net belongs to instantly, the naming is wrong.

---

## Relationship to Constraints

This grouping reflects Stage 5 constraints:

- Tight matching within `DQ<lane>[ ]`
- Tight matching between `DQS<lane>` and its `DQ<lane>[ ]`
- Loose matching between lanes

Grouping makes these constraints visible and enforceable during implementation.

---

## What This Document Does NOT Decide

This document does not define:
- Number of lanes
- Exact DQ width per lane
- Exact presence of optional lane-level signals
- Connector pin assignments
- Electrical termination strategy

Those are defined elsewhere.

---

## Takeaway

Byte lanes are the unit of correctness for the data plane.

By enforcing lane-indexed grouping:
- Topology intent is preserved
- Constraints become enforceable
- Cross-lane mistakes become hard to introduce

If address/command is the control plane,
byte lanes are the truth plane.

---

Next pin grouping document:
- `clock_and_control.md`

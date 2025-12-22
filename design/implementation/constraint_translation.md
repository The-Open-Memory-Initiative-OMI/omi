# Constraint Translation

This document translates **Stage 5 architectural constraints** into **implementation-visible rules** for Stage 6 and beyond.

Its purpose is to ensure that:
- Architectural intent survives schematic capture
- Layout constraints are not guessed or reinterpreted
- Reviews can verify correctness before fabrication
- Violations are detectable early

This document does not introduce new constraints.
It makes existing constraints explicit and enforceable.

---

## Why Constraint Translation Exists

Architectural constraints often fail not because they were wrong,
but because they were **implicit**.

During implementation:
- Schematics abstract timing
- Layout tools hide intent
- Errors appear physically, not logically

Constraint translation ensures that:
> **What must not be violated is visible where violations can occur.**

---

## Source of Constraints

All constraints in this document originate from:

- Stage 5 signal map
- Stage 5 topology decisions
- Stage 5 length matching intent
- Stage 5 skew budget reasoning
- Stage 5 power architecture and decoupling strategy
- Stage 5 design assumptions

No new behavior is introduced here.

---

## Constraint Categories

Constraints are translated into four implementation-relevant categories:

1. **Structural constraints**
2. **Timing relationship constraints**
3. **Power integrity constraints**
4. **Review and verification constraints**

Each category maps directly to schematic and layout checks.

---

## 1. Structural Constraints

### Data Topology Enforcement

- Each byte lane must be represented as an independent interface
- DQ and DQS for a lane must never branch or share stubs
- No data signal may connect to more than one DRAM device group

**Implementation visibility:**
- Byte lane symbols must be isolated
- No shared nets between lanes
- Reviewers must be able to trace a lane end-to-end

---

### Address/Command Topology Enforcement

- Address and command signals must appear as shared buses
- Distribution must reflect fly-by intent
- No star or tree replication is allowed

**Implementation visibility:**
- Single logical bus representation
- Ordered device connection in schematics
- No duplicated command drivers

---

### Clock Topology Enforcement

- Clock signals must be represented as shared differential pairs
- No local regeneration or buffering on the DIMM
- Clock signals must not be mixed with data or command bundles

**Implementation visibility:**
- Single clock source entry
- Clear fan-out to devices
- Differential pairing preserved visually

---

## 2. Timing Relationship Constraints

### DQ-to-DQ (Within Lane)

- DQ signals within a lane must be treated as a matched set
- No asymmetric routing assumptions are allowed

**Implementation visibility:**
- DQ bundled as `DQ<lane>[ ]`
- No individual DQ bits broken out casually

---

### DQS-to-DQ (Per Lane)

- DQS must be visually and structurally adjacent to its DQ group
- No lane may have multiple DQS references
- DQS must not cross lane boundaries

**Implementation visibility:**
- DQS placed next to DQ bundle
- Clear one-to-one lane association

---

### Lane-to-Lane Timing

- Lane-to-lane skew is allowed but bounded
- No artificial alignment mechanisms are introduced at schematic level

**Implementation visibility:**
- No serpentine or delay constructs implied in schematics
- Lane independence preserved

---

## 3. Power Integrity Constraints

### Power Domain Separation

- VDD, VDDQ, Vref, VTT, and auxiliary rails must remain distinct
- No rail may be repurposed or merged

**Implementation visibility:**
- Separate power symbols or net classes
- Explicit rail naming everywhere
- No "implicit power" usage

---

### Vref Handling

- Vref must never power logic
- Vref must not source or sink significant current
- Vref must be isolated from switching noise

**Implementation visibility:**
- Vref only connects to reference pins
- No decoupling that implies load driving
- No logic powered from Vref

---

### VTT Handling

- VTT must be treated as a dynamic termination rail
- VTT must be capable of sourcing and sinking current
- VTT must not be shorted or repurposed

**Implementation visibility:**
- VTT connections only to termination-related pins
- Clear separation from VDD/VDDQ

---

## 4. Decoupling Strategy Translation

### Hierarchical Decoupling

- Bulk, local, and high-frequency decoupling must all be represented
- Decoupling responsibility must be clear per rail

**Implementation visibility:**
- Decoupling placeholders per rail
- No "one-capacitor-fits-all" approach implied

---

### Rail-Specific Intent

- VDD prioritizes stability
- VDDQ prioritizes transient response
- Vref prioritizes noise isolation
- VTT prioritizes dynamic bias stability

**Implementation visibility:**
- Different decoupling classes per rail
- Rail intent documented near symbols

---

## 5. Review and Verification Constraints

### Schematic Review Checklist

A schematic review must be able to answer:

- Can each byte lane be traced independently?
- Is DQS clearly associated with its lane?
- Are command and data planes visually separated?
- Are power domains explicit and isolated?
- Is the clock path unambiguous and global?

If any answer is unclear, the schematic is not ready.

---

### Layout Readiness Check

Before layout begins:

- All constraints must be translatable into layout rules
- No architectural decisions remain implicit
- No "we'll fix it in layout" assumptions exist

Layout is execution, not interpretation.

---

## What This Document Does NOT Decide

This document does not define:
- Numerical timing budgets
- Exact length tolerances
- Specific layout rules
- Simulation targets
- Verification methodologies

Those belong to implementation execution and validation stages.

---

## Takeaway

Constraints only protect a design if they are visible where mistakes happen.

This document ensures that:
- Architecture survives schematics
- Schematics survive layout
- Layout survives fabrication

For OMI v1, correctness is enforced by design, not hope.

---

This completes the implementation translation layer.

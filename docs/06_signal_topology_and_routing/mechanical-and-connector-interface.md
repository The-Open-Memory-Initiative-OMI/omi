# OMI v1 — Mechanical & Connector Interface Block Definition  
*(DDR4 UDIMM, 8 GB, 1R, x8, non-ECC)*

## Status
Draft (Stage 6.5)

## Scope
OMI Version 1 only

## Authority
OMI Maintainers

## Related
- Stage 6.5 — Mechanical & Connector Interface Block
- Stage 6.4 — SPD & Configuration Block
- Stage 6.3 — Data Byte-Lanes & DQS Block
- Stage 6.2 — Address / Command / Clock Block
- Stage 6.1 — Power Delivery & PDN
- OMI v1 — Form Factor Selection

---

## 1. Purpose

This document defines the **mechanical form and connector interface assumptions** for the OMI v1 DDR4 UDIMM.

It specifies:
- The physical envelope of the module
- Edge connector and keying assumptions
- Keep-out and handling constraints
- Labeling and identification philosophy
- Expected mechanical failure modes

This document intentionally **does not include detailed mechanical drawings** or PCB placement rules. Those belong to later stages.

---

## 2. Design Philosophy

Mechanical design for OMI v1 follows these principles:

- **Strict JEDEC alignment**
- **No custom or non-standard features**
- **Compatibility over density**
- **Explicit physical assumptions**
- **Failure treated as observable behavior**

The goal is **fit, insertion reliability, and reproducibility**, not compactness or aesthetics.

---

## 3. Mechanical Form Assumptions

### 3.1 Module Outline

- The module conforms to standard **DDR4 UDIMM mechanical outline**
- Overall dimensions follow JEDEC UDIMM expectations
- No mechanical deviations or experimental shapes are introduced

---

### 3.2 Thickness & Envelope

- PCB thickness follows standard UDIMM practice
- Component height remains within connector and socket clearance limits
- No assumptions are made about heatsinks or enclosures

---

### 3.3 Keying & Orientation

- Standard DDR4 UDIMM key notch is used
- Orientation markers must clearly indicate insertion direction
- Reverse insertion is mechanically prevented by design

---

## 4. Connector Interface Assumptions

### 4.1 Edge Connector Role

- The edge connector is the sole mechanical and electrical interface to the host
- Connector geometry follows JEDEC DDR4 UDIMM standards
- No auxiliary connectors or test headers are assumed

---

### 4.2 Pin-Field Philosophy

- All pins are treated as JEDEC-defined resources
- Pin usage aligns with electrical block assumptions
- No pin re-purposing or overloading is permitted

---

## 5. Keep-Out & Physical Constraints

### 5.1 Connector-Adjacent Zones

- Keep-out regions near the edge connector are respected
- No components are placed where they could interfere with insertion or contact

---

### 5.2 Component Height Considerations

- Tall components are avoided near the connector
- Height consistency is favored to reduce insertion stress

---

## 6. Labeling & Identification

### 6.1 Silkscreen Philosophy

- Clear module orientation markers
- Revision and identifier markings
- No branding-driven silkscreen requirements

---

### 6.2 Traceability

- Revision identification must allow correlation with documentation
- Silkscreen is used as a functional identifier, not decoration

---

## 7. Handling, Assembly & Validation Considerations

Mechanical handling assumptions include:

- Repeated insertion and removal during validation
- Manual probing and inspection
- Exposure to bench-level handling

The design must tolerate these without mechanical degradation.

---

## 8. Expected Mechanical Failure Modes

The following are considered **expected and documentable**:

- Connector wear from repeated insertion
- Damage from improper handling
- Mechanical interference revealed during validation

Such failures are treated as **engineering data**, not hidden defects.

---

## 9. Explicit Non-Goals

This block definition explicitly excludes:

- Custom connectors or sockets
- Non-JEDEC mechanical features
- Thermal management hardware
- Cosmetic or branding-driven design choices

---

## 10. Interface With Other Blocks

The mechanical block constrains:

- PCB layout and component placement
- Power delivery component height
- Signal routing near the connector
- Validation and handling procedures

Any change to mechanical assumptions requires re-evaluation of electrical blocks.

---

## 11. Locking Statement

This document defines the **mechanical and connector interface assumptions** for OMI v1.

All schematic capture, layout, assembly, and validation work MUST conform to the constraints and assumptions stated herein unless this document is explicitly revised.

---

*End of document*

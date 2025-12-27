# OMI v1 — SPD & Configuration Block Definition  
*(DDR4 UDIMM, 8 GB, 1R, x8, non-ECC)*

## Status
Draft (Stage 6.4)

## Scope
OMI Version 1 only

## Authority
OMI Maintainers

## Related
- Stage 6.4 — SPD & Configuration Block
- Stage 6.3 — Data Byte-Lanes & DQS Block
- Stage 6.2 — Address / Command / Clock Block
- Stage 6.1 — Power Delivery & PDN
- OMI v1 — DDR4 Acceptance Conditions
- OMI v1 — Capacity & Organization

---

## 1. Purpose

This document defines the **SPD (Serial Presence Detect) and configuration assumptions** for the OMI v1 DDR4 UDIMM.

It specifies:
- The role of SPD in DDR4 initialization
- What information the module exposes to the platform
- Which timing and organization parameters are declared
- How BIOS and memory controller behavior is expected to interact with SPD
- Expected failure modes related to SPD misconfiguration

This document **does not define** EEPROM part selection, write-protection mechanisms, or programming workflows. Those belong to later stages.

---

## 2. Design Philosophy

SPD handling in OMI v1 follows these principles:

- **JEDEC compliance only**
- **Single, conservative operating profile**
- **Explicit rejection of overclocking profiles**
- **Transparency over optimization**
- **Platform variability treated as observable behavior**

The objective is to ensure the module is **predictable, explainable, and reproducible**, not performance-tuned.

---

## 3. Role of SPD in DDR4 Systems

SPD is the primary mechanism by which a memory module communicates its characteristics to the host system.

In OMI v1, SPD is assumed to provide:

- Module capacity and organization
- Rank count and device width
- Supported timing parameters
- Voltage and operating assumptions
- Identification and metadata

Correct SPD content is **mandatory** for successful memory training and initialization.

---

## 4. SPD Interface Assumptions

### 4.1 Electrical Interface

- SPD is accessed via an **I²C / SMBus-compatible interface**
- Interface behavior follows standard DDR4 UDIMM expectations
- No proprietary or vendor-specific signaling is assumed

---

### 4.2 Addressing Assumptions

- SPD device addressing follows standard UDIMM conventions
- No multi-device SPD complexity is assumed
- Address conflicts or multiplexing are out of scope for OMI v1

---

## 5. Required SPD Content

The SPD contents for OMI v1 **must explicitly describe** the following:

### 5.1 Module Organization
- Total capacity: **8 GB**
- Rank count: **1**
- Device width: **x8**
- Data width: **64-bit**
- ECC: **Not supported**

---

### 5.2 Timing Parameters
- Single JEDEC-defined timing profile
- Conservative data rate selection
- No alternate or performance-oriented profiles

---

### 5.3 Voltage & Operating Conditions
- Nominal DDR4 operating voltage
- No support for voltage scaling or alternate modes

---

### 5.4 Identification Fields
- Manufacturer identification
- Module identification and revision
- Date or lot information (if applicable)

These fields exist for traceability and documentation, not branding.

---

## 6. Timing Profile Assumptions

OMI v1 explicitly supports:

- **Exactly one JEDEC timing profile**
- Chosen to prioritize margin and stability
- Declared clearly and unambiguously in SPD

OMI v1 explicitly rejects:

- XMP
- EXPO
- Vendor-specific extensions
- Multiple selectable profiles

Any platform behavior beyond the declared JEDEC profile is treated as undefined.

---

## 7. BIOS & Platform Interaction

SPD data is expected to be consumed by the BIOS or firmware during memory initialization.

Assumptions:
- BIOS reads SPD contents verbatim
- BIOS behavior may vary between platforms
- SPD misconfiguration may result in:
  - Training failure
  - Silent fallback behavior
  - Reduced operating frequency

Such behavior is treated as **platform variability**, not a design defect.

---

## 8. Observability & Validation Considerations

SPD-related validation expectations include:

- Ability to read SPD contents using standard tools
- Verification of declared parameters against design intent
- Correlation of SPD data with training behavior

SPD-related issues are expected to manifest as:
- Failure to initialize memory
- Unexpected timing selection
- Platform-dependent behavior differences

---

## 9. Expected Failure Modes

The following are considered **expected and documentable**:

- BIOS refusing to train due to inconsistent SPD data
- Platform selecting overly conservative fallback timing
- Silent misinterpretation of organization fields

These failures are **engineering data** and must be documented, not masked.

---

## 10. Explicit Non-Goals

This block definition explicitly excludes:

- Performance tuning via SPD
- Overclocking profiles
- Vendor-specific SPD extensions
- Platform-specific BIOS workarounds
- Undocumented or NDA-protected behavior

---

## 11. Interface With Other Blocks

The SPD & Configuration block interfaces directly with:

- Capacity & Organization definition
- Address / Command / Clock Block
- Data Byte-Lanes & DQS Block
- Validation & Bring-Up Strategy

Any change to these blocks requires re-evaluation of SPD assumptions.

---

## 12. Locking Statement

This document defines the **SPD and configuration assumptions** for OMI v1.

All schematic capture, firmware interaction, validation, and bring-up work MUST conform to the constraints and assumptions stated herein unless this document is explicitly revised.

---

*End of document*

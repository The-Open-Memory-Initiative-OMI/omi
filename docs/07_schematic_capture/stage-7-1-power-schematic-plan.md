# Stage 7.1 — Power Schematic Plan (OMI v1 DDR4 UDIMM)

## Status
Draft

## Purpose
Define the **exact power-rail intent** for the Stage 7 schematic capture, so the Power & PDN page can be implemented without introducing new architectural assumptions.

This plan is **pre-schematic**: it specifies *what must be shown* and *what must be true*, not part numbers or capacitor values.

---

## Inputs (Locked Constraints)
- Technology: DDR4
- Form Factor: UDIMM
- Organization: 8 GB, 1R, x8, non-ECC
- Stage 6.1 Power Delivery assumptions are authoritative
- JEDEC-aligned, conservative behavior only

---

## 1. Rail Inventory (Must Appear on the Power Page)

The Power schematic page MUST explicitly include and name the following rails:

### Primary Rails
- **VDD (1.20 V nominal)** — DRAM core/array power  
- **VDDQ (1.20 V nominal)** — DRAM I/O power (DQ/DQS/CA interfaces)  
- **VPP (2.50 V nominal)** — wordline boost supply  
- **GND** — return reference for all rails and signals

### Reference Rails
- **VREF** — reference for input comparators  
  - Nominal assumption: approximately 0.5 × VDDQ  
  - Must be treated as noise-sensitive and locally stabilized

Notes:
- Exact tolerances are JEDEC-defined and referenced by DDR4 public specs.
- Any additional "helper" rails are out of scope unless required by public DDR4 UDIMM behavior.

---

## 2. Sourcing Model (What the Host Provides vs What the DIMM Does)

### Host-Supplied (via UDIMM edge connector)
For OMI v1, the default assumption is that the host platform supplies:
- VDD
- VDDQ
- VPP
- GND

### VREF Handling
VREF must be explicitly represented.
The schematic must state one of the following (choose during schematic capture and document it clearly on the page notes):
- **Option A:** VREF is provided by the host platform and distributed on-DIMM with local decoupling  
- **Option B:** VREF is derived on-DIMM (from VDDQ) and distributed with local decoupling

Regardless of option, VREF must be:
- explicitly named
- locally decoupled
- treated as a noise-sensitive reference, not a general-purpose rail

Non-assumptions:
- No on-DIMM regulation is assumed for VDD/VDDQ/VPP in OMI v1.
- No vendor-specific "power conditioning magic" is assumed.

---

## 3. Power Consumers (What Each Rail Powers)

The Power schematic must make clear the rail-to-consumer mapping:

- **VDD →** DRAM device VDD pins (all x8 devices)
- **VDDQ →** DRAM device VDDQ pins (all x8 devices), plus SPD/I²C pull-ups if they share this rail (must be explicit)
- **VPP →** DRAM device VPP pins (all x8 devices)
- **VREF →** DRAM device VREF-related pins (as applicable), distributed carefully
- **GND →** all device grounds and reference returns

The schematic must not leave any powered pins implied.

---

## 4. Decoupling & PDN Representation (Conceptual)

The Power page must show **decoupling intent**, without committing to final placement:

- Bulk decoupling presence per major rail (symbolic)
- Local decoupling presence at DRAM devices (symbolic)
- Clear separation of:
  - bulk (low-frequency stability)
  - local (high-frequency transients)

Rules:
- No aggressive or exotic PDN techniques in v1.
- Exact capacitor values and placement are deferred to Stage 10 (layout guidelines) unless required for schematic completeness.

---

## 5. Observability Requirements (Bring-Up Friendly)

The Power page must support the Stage 6.6 validation philosophy by ensuring rails are observable:

- Rails must be named consistently for probing and reporting:
  - VDD, VDDQ, VPP, VREF
- The plan assumes the builder can measure rails with basic equipment.
- If test points are used, they are allowed only if they do not introduce new features or mechanical conflicts.

(Implementation detail of testpoints can be deferred, but **observability must be considered now**.)

---

## 6. Page-Level Notes (Must Appear on the Power Page)

Add a small notes box on the Power page stating:

- OMI v1 is JEDEC-only, margin-first
- Host supplies VDD/VDDQ/VPP by default (UDIMM standard assumption)
- VREF is noise-sensitive and must be locally stabilized
- No on-DIMM regulators are assumed for v1

This prevents future readers from inferring hidden design intent.

---

## 7. Review Checklist (Power Page Gate)

Before moving to CA or data pages, reviewers must be able to answer:

- Can every rail be traced from connector to every consumer?
- Is VREF explicitly handled and not left vague?
- Are there any floating power pins?
- Is the sourcing model stated clearly (host vs on-DIMM)?
- Does anything on the page contradict Stage 6.1?

If any answer is "unclear," the power page is not review-clean.

---

## 8. Completion Criteria (Stage 7.1 Done)

Stage 7.1 is complete when:

- The Power & PDN schematic page exists
- Rail names match this plan
- VREF option (A or B) is explicitly chosen and documented on-page
- The page passes one structured review
- The page is considered frozen before proceeding

---

*End of plan*

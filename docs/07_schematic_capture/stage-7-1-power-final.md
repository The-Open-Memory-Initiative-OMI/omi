# Stage 7.1 — Power & PDN (Final)

## Project
Open Memory Initiative (OMI) — OMI v1 DDR4 UDIMM

## Status
✅ Frozen (Final)

## Scope
This document captures the **final, reviewed state** of Stage 7.1 within Stage 7 (Schematic Capture).

Stage 7.1 focuses **exclusively** on:
- Power rails
- Power sourcing
- DRAM power consumption
- Reference voltage (VREF) strategy

No signal connectivity is included at this stage.

---

## Architectural Decisions (Locked)

### Memory Type
- DDR4
- UDIMM
- x8 DRAM devices
- Single-rank baseline assumption

### VREF Strategy
- **Option A — Host-provided VREF**
  - VREF is supplied by the host platform via the UDIMM connector
  - The DIMM does not generate VREF locally
  - The DIMM distributes VREF to DRAM devices
  - No resistor dividers, buffers, or regulators are present at this stage

This decision is locked for OMI v1.

---

## Power Rails Defined

The following global power nets are declared:

- `VDD`   — DRAM core supply
- `VDDQ`  — DRAM I/O supply
- `VPP`   — DRAM wordline boost supply
- `VREF`  — Reference voltage (host-provided)
- `GND`   — Common ground (VSS / VSSQ)

No voltage values are encoded in net names.

---

## Host Power Entry

- A placeholder connector (`UDIMM_HOST_POWER`) represents power sourced from the host motherboard.
- The connector provides:
  - `VDD`
  - `VDDQ`
  - `VPP`
  - `VREF`
  - `GND`

This connector is **architectural**, not pin-accurate, and will be refined later.

---

## DRAM Devices

### Devices Placed
Eight DDR4 x8 DRAM devices are instantiated:

```
U_DRAM0
U_DRAM1
U_DRAM2
U_DRAM3
U_DRAM4
U_DRAM5
U_DRAM6
U_DRAM7
```

### Connections (Power Only)

For **all DRAM devices**, the following connections are made:

- `VDD`     → `VDD`
- `VDDQ`    → `VDDQ`
- `VPP`     → `VPP`
- All `VSS` / `VSSQ` pins → `GND`
- `VREFCA`  → `VREF`

No other pins are connected.

---

## Explicit Exclusions

The following are **intentionally not included** in Stage 7.1:

- Address / Command / Clock connectivity
- Data (DQ/DQS) connectivity
- SPD / I²C connectivity
- Decoupling capacitors
- Bulk capacitance
- Power sequencing logic
- Voltage regulators
- Layout or routing considerations

All of the above are deferred to later stages.

---

## Verification

- Net hover test confirms all DRAM power pins share common rails
- No unintended local nets exist
- ERC warnings are limited to expected unconnected signal pins

---

## Artifacts

- **Schematic PDF**  
  `design/power/exports/omi_v1_power_pdn_stage7_1_final.pdf`

---

## Completion Statement

Stage 7.1 is complete and frozen.

All DRAM devices are powered consistently, reference voltage strategy is locked, and no functional signal connectivity has begun.

The project may now safely proceed to:

➡ **Stage 7.2 — Address / Command / Clock Schematic Page**

---

*End of Stage 7.1*

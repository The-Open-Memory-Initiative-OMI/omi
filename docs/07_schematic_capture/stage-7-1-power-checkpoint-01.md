# Stage 7.1 — Power & PDN Checkpoint 01 (OMI v1)

## Status
Frozen (Checkpoint)

## Date
2025-12-29

## Scope
This checkpoint captures the current Stage 7.1 state for the **Power & PDN** schematic page only.

---

## What is included

- Power rails declared: `VDD`, `VDDQ`, `VPP`, `VREF`, `GND`
- Host power entry represented via connector placeholder (`UDIMM_HOST_POWER`)
- `U_DRAM0` placed as a template DRAM device symbol (DDR4 x8)
- `U_DRAM0` connections:
  - `VDD` connected to `VDD`
  - `VDDQ` connected to `VDDQ`
  - `VPP` connected to `VPP`
  - All `VSS*` pins connected to `GND`
  - `VREFCA` connected to `VREF`

No other pins on `U_DRAM0` are connected.

---

## VREF Strategy (Locked)

- **Option A (Host-provided VREF)** is in effect:
  - VREF is supplied by the host platform via the UDIMM connector
  - The DIMM does not generate VREF locally
  - Only distribution and local decoupling are permitted (decoupling not yet implemented)

Reference: `docs/07_schematic_capture/stage-7-1-vref-decision.md`

---

## What is explicitly NOT included

- No CA / address / command / clock connectivity
- No DQ / DQS / data-lane connectivity
- No SPD / I²C connectivity
- No decoupling capacitor selection or placement decisions
- No regulators or rail generation circuits
- No layout or routing considerations

---

## Artifact

- Power page PDF export (recommended location):
  - `design/power/exports/omi_v1_power_pdn_stage7_1_checkpoint.pdf`

---

## Next planned step (not executed)

- Replicate DRAM device power pins for all devices (power-only), OR
- Proceed to decoupling intent representation after confirming replication approach

---

*End of checkpoint*

# Stage 7.4 — SPD & Configuration (Final)

## Project
Open Memory Initiative (OMI) — OMI v1 DDR4 UDIMM

## Status
✅ Frozen (Final)

## Scope
This stage defines SPD EEPROM connectivity for OMI v1:
- SPD EEPROM power
- SMBus/I²C bus signals (SCL/SDA)
- Address strap pins (SA0/SA1/SA2)
- Write-protect behavior

This stage does NOT include:
- Temperature sensor / TS-on-DIMM device
- Pin-accurate UDIMM edge connector mapping
- Any firmware/SPD content programming workflow

---

## Nets (Locked)
- `VDDSPD`, `GND`
- `SPD_SCL`, `SPD_SDA`
- `SA0`, `SA1`, `SA2`

---

## Components
- `J_HOST_SPD` — host SMBus/SPD placeholder connector (architectural anchor)
- `U_SPD0` — DDR4 SPD EEPROM symbol (I²C)

---

## Connectivity (Final)
- `U_SPD0.VCC` → `VDDSPD`
- `U_SPD0.VSS` → `GND`
- `U_SPD0.SCL` → `SPD_SCL`
- `U_SPD0.SDA` → `SPD_SDA`
- `U_SPD0.A0/A1/A2` → `SA0/SA1/SA2`

### Write Protect (Decision Locked)
- `U_SPD0.WP` → `GND` (writes enabled)

Rationale:
- OMI v1 prioritizes learning, reproducibility, and bring-up friendliness.
- Hardware write-protect is deferred to future revisions if needed.

---

## System Assumptions (Explicit)
- SMBus pull-ups for `SPD_SCL` and `SPD_SDA` are provided by the host platform.
- `SA0/SA1/SA2` are slot/address straps controlled host-side.

---

## Verification
- Net highlight confirms correct endpoint connectivity.
- ERC: no duplicate references; SPD power and bus nets resolve cleanly.

---

## Artifact
- `omi_v1_stage7_4_spd_final.pdf`

---

## Next
➡ Stage 7.5 — Pin-accurate connector mapping (UDIMM edge interface) and mechanical integration, then Stage 7 closure.

*End of Stage 7.4*

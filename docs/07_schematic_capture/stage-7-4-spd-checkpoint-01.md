# Stage 7.4 — SPD & Configuration (Checkpoint 01)

## Status
Checkpoint (not final)

## Scope
Defines SPD EEPROM connectivity for OMI v1:
- SPD EEPROM power
- SMBus/I²C signals (SCL/SDA)
- Address strap pins (SA0/SA1/SA2)
- Write-protect behavior

No temperature sensor, no pin-accurate UDIMM mapping, and no firmware content are included.

---

## Implemented

### Nets
- `VDDSPD`, `GND`
- `SPD_SCL`, `SPD_SDA`
- `SA0`, `SA1`, `SA2`

### Components
- `J_HOST_SPD` — host SMBus/SPD placeholder connector
- `U_SPD0` — DDR4 SPD EEPROM symbol (I²C)

### Connections
- `U_SPD0.VCC` → `VDDSPD`
- `U_SPD0.VSS` → `GND`
- `U_SPD0.SCL` → `SPD_SCL`
- `U_SPD0.SDA` → `SPD_SDA`
- `U_SPD0.A0/A1/A2` → `SA0/SA1/SA2`
- `U_SPD0.WP` → `GND` (writes enabled for development)

### Assumptions
- SMBus pull-ups for `SPD_SCL`/`SPD_SDA` provided by host platform.
- SA pins are slot/address straps (host-side).

---

## Verification
- Net highlight confirms endpoint connectivity.
- ERC: no duplicate references; SPD power and bus nets resolve.

---

## Artifact
- `omi_v1_stage7_4_spd_checkpoint_01.pdf`

---

## Next
- Decide whether SPD write-protect should remain tied low for v1 final, or be strap-selectable.
- Optional: add thermal sensor (TSE2004-class) as a separate, explicitly-scoped v1.x enhancement.

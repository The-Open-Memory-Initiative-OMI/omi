# L1 Bench Electrical — Measurement Procedures

## Overview

This document provides step-by-step procedures for each L1 validation session.
Follow the sessions in order. Do not proceed to Session 2 until Session 1 is
fully complete with all measurements recorded.

> **Safety:** DDR4 voltages are low (≤2.5 V logic, 3.6 V max VDDSPD) but
> always verify power supply current limits before connecting to the module.
> A short circuit on a power rail can damage DRAM devices.

---

## Equipment Required

| Equipment | Purpose | Minimum Specification |
|-----------|---------|----------------------|
| Digital Multimeter (DMM) | Continuity and resistance | 0.1 Ω resolution, continuity beep |
| Bench Power Supply | PDN testing | Dual-channel, 0–5 V, 2 A per channel |
| Oscilloscope | Waveform verification | ≥100 MHz bandwidth, ≥2 channels |
| Logic Analyzer (optional) | I2C protocol decode | I2C protocol support |
| Test Jig / Socket | Module mounting | DDR4 UDIMM 288-pin socket (Class C) |
| Probes | Pin access | Fine-tip DMM probes for 0.85 mm pitch |

---

## Session 1 — Continuity Audit (Unpowered)

### Purpose

Verify all 288 edge connector pins have correct connectivity before applying
power. This session detects open circuits, shorts, and manufacturing defects.

### Setup

1. Insert the OMI v1 module into the test jig. **Do not apply power.**
2. Set DMM to continuity mode (beep on <50 Ω) or resistance mode (0.1 Ω range).
3. Open the measurement log template CSV.
4. Generate the probe sequence: `python generate_probe_sequence.py --reference ddr4_udimm_288_pinmap.csv`

### Procedure

#### Group 1A — GND Continuity

**Goal:** Verify all VSS/GND pins are connected with ≤1 Ω resistance.

1. Connect DMM black probe to a known GND reference (e.g., pin 2 = VSS).
2. Probe each GND pin listed in the probe sequence.
3. Record the resistance value in the measurement log.
4. **Pass:** ≤1 Ω. **Fail:** >1 Ω or no continuity beep.

#### Group 1B — Power Rail Continuity

**Goal:** Verify pin-to-pin continuity within each power rail.

1. For each power rail (VDD, VPP, VREF, VDDSPD, VTT):
   - Connect DMM to any two pins on the same rail.
   - Verify continuity (should beep).
2. Record PASS or resistance value per pin.
3. **Pass:** Continuity confirmed. **Fail:** Open between same-rail pins.

#### Group 1C — DQ/DQS Signal Continuity

**Goal:** Verify each data signal reaches its DRAM device.

1. For each byte lane (D0 through D7):
   - Probe the edge connector pin for each DQ, DQS_t, DQS_c, and DM_DBI_n signal.
   - Verify continuity from edge connector to the corresponding DRAM component pad.
2. Record PASS/FAIL per pin.
3. **Pass:** Continuity beep. **Fail:** No continuity (open circuit).

> **Tip:** A systematic lane-by-lane approach is faster than random probing.
> Start with lane 0 (pins 3, 5, 7, 10, 12, 148, 150, 152, 153, 155, 157),
> then proceed through lanes 1–7.

#### Group 1D — CA/CLK Signal Continuity

**Goal:** Verify all address, command, and clock signals are connected.

1. Probe each CA_CLK pin that has a non-NC net assignment.
2. Verify continuity from edge connector to the bus / DRAM devices.
3. **Key pins:** RESET_n (58), CKE0 (60), ACT_n (62), CS0_n (84), CK_t (74), CK_c (75).
4. **Pass:** Continuity. **Fail:** Open.

#### Group 1E — SPD Bus Continuity

**Goal:** Verify I2C bus wiring from edge connector to SPD EEPROM.

1. Probe SCL (pin 141) → EEPROM SCL pad. Verify continuity.
2. Probe SDA (pin 285) → EEPROM SDA pad. Verify continuity.
3. Probe SA0 (pin 139), SA1 (pin 140), SA2 (pin 238) → EEPROM address pads.
4. Probe VDDSPD (pin 284) → EEPROM VCC pad. Verify continuity.
5. **Pass:** All six connections show continuity. **Fail:** Any open.

#### Group 1F — NC Pin Isolation

**Goal:** Verify NC pins are not shorted to adjacent active pins.

1. Set DMM to high-resistance mode (MΩ range).
2. For each NC pin, measure resistance to the two adjacent pins.
3. **Pass:** ≥1 MΩ (typically shows OL / overload). **Fail:** <1 MΩ.

> **Note:** Not every NC pin needs to be measured individually. Spot-check at
> least 5 NC pins spread across the connector (e.g., pins 1, 8, 19, 93, 144).

---

## Session 2 — PDN Initialization (Powered)

### Purpose

Verify power rails reach correct voltages and are properly isolated from
each other when the module is powered.

### Setup

1. Module remains in the test jig.
2. Connect bench power supply:
   - **Channel 1:** VPP = 2.5 V, current limit 200 mA
   - **Channel 2:** VDD = 1.2 V, current limit 1 A
   - VDDSPD: supplied by host or separate 3.3 V source
3. **CRITICAL SEQUENCING:** Apply VPP **before** VDD (JEDEC DDR4 requirement).

### Procedure

#### Group 2A — Rail Voltage Verification

1. **VPP first:** Apply 2.5 V to VPP pins (142, 143, 286, 287, 288).
   - Probe pin 142 with DMM. Expected: 2.375–2.625 V (±5%).
2. **VDD second:** Apply 1.2 V to VDD pins (59, 61, 64, 67, ...).
   - Probe pin 64 with DMM. Expected: 1.140–1.260 V (±5%).
3. **VDDSPD:** Apply 3.3 V (or host-supplied) to VDDSPD (pin 284).
   - Probe pin 284. Expected: 2.2–3.6 V.
4. **VTT:** Supplied by host. Probe pins 77 or 221.
   - Expected: VDD/2 = 0.54–0.66 V.
5. **VREF:** Probe pin 146 (VREFCA).
   - Expected: VDD/2 = 0.54–0.66 V.

#### Group 2B — Rail-to-Rail Isolation

**Perform these measurements with power OFF (unpowered).**

1. Set DMM to high-resistance mode (kΩ/MΩ).
2. Measure resistance between each rail pair:

| Rail A (pin) | Rail B (pin) | Minimum |
|-------------|-------------|---------|
| VDD (64) | VPP (142) | ≥10 kΩ |
| VDD (64) | VDDSPD (284) | ≥10 kΩ |
| VDD (64) | VTT (77) | ≥10 kΩ |
| VDD (64) | VREF (146) | ≥10 kΩ |
| VDD (64) | GND (2) | ≥10 kΩ |
| VPP (142) | VDDSPD (284) | ≥10 kΩ |
| VPP (142) | GND (2) | ≥10 kΩ |
| VDDSPD (284) | GND (2) | ≥10 kΩ |
| VTT (77) | GND (2) | ≥10 kΩ |
| VREF (146) | GND (2) | ≥10 kΩ |

3. **Pass:** All pairs ≥10 kΩ. **Fail:** Any pair <10 kΩ.

#### Group 2C — Current Draw Sanity

1. With VDD and VPP applied, note the quiescent current draw.
2. Expected: <50 mA total (no active DRAM operations, just leakage).
3. If current is unusually high (>200 mA), suspect a short. **Stop immediately.**

---

## Session 3 — SPD Bus Analysis (Powered)

### Purpose

Verify the I2C bus can communicate with the SPD EEPROM. This is a
prerequisite for L2 (Host Enumeration).

### Setup

1. Module powered with VDDSPD active (2.2–3.6 V on pin 284).
2. Connect oscilloscope or logic analyzer to SCL (pin 141) and SDA (pin 285).
3. If using a host platform: boot to a minimal OS with I2C tools available.

### Procedure

#### Group 3A — VDDSPD Supply Verification

1. Confirm VDDSPD is present and stable:
   - Probe pin 284 with DMM. Expected: 2.2–3.6 V.
   - If 0 V or floating: EEPROM has no power — **L1 FAIL** (see FS-01).

#### Group 3B — Bus Signal Waveform

1. With host performing an I2C scan (e.g., `i2cdetect -y <bus>`):
   - Observe SCL (pin 141) on scope. Should show clean clock transitions.
   - Observe SDA (pin 285) on scope. Should show data transitions with
     pull-up recovery (not stuck low, not floating).
2. Verify pull-up behavior:
   - Both lines should idle HIGH (~VDDSPD level).
   - During transactions, LOW levels should be <0.3 × VDDSPD.
   - Rise time should be smooth (RC pull-up), not step-function.
3. If lines are stuck LOW: possible short to GND. Check continuity.
4. If lines are floating (no pull-up): pull-ups are host-side in OMI v1.
   Verify host board provides pull-ups on SCL/SDA.

#### Group 3C — Address Pin Verification

1. Measure voltage on SA0 (pin 139), SA1 (pin 140), SA2 (pin 238).
2. In OMI v1 design, all three should be tied LOW (GND).
3. This gives EEPROM address 0x50 (1010_000 in 7-bit I2C addressing).
4. If any SA pin is floating or HIGH, the address will be different.

#### Group 3D — SPD Read Test

1. Using `i2cdetect` or equivalent, verify the EEPROM responds at address 0x50.
2. Read the first 16 bytes of the EEPROM.
3. **Pass criteria:**
   - Device ACKs at address 0x50.
   - Returned data is not all-0xFF (blank EEPROM) or all-0x00.
   - Byte 2 (SPD revision) contains a valid DDR4 value.
4. **Fail:** NACK, timeout, or all-0xFF/0x00 response.

> If SPD read fails, see **FS-01** in `08-5_failure_signatures.md` for
> systematic debug.

---

## Recording Results

1. Fill in the measurement log CSV for every pin measured.
2. Use `PASS` or `FAIL` in the `pass_fail` column.
3. For resistance measurements, record the numeric value in `measured_value`
   and `ohm` in the `unit` column.
4. For voltage measurements, record the voltage in `measured_value` and `V`
   in the `unit` column.
5. Run the validator: `python validate_continuity_log.py --reference <csv> --measurements <log>`

---

## References

- `08-2_bringup_ladder.md` — L1 pass/fail criteria
- `08-5_failure_signatures.md` — FS-01 (SPD not detected), FS-02 (training failure)
- `generate_probe_sequence.py` — generates the complete probe list
- `validate_continuity_log.py` — validates your measurement log

---

*Document version 1.0.0 — OMI Stage 8 L1 Bench Electrical*

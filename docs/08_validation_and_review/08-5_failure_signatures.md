# Stage 8.5 — Failure Signatures (OMI v1)

## Project
Open Memory Initiative (OMI) — OMI v1 DDR4 UDIMM

## Status
Draft

## Purpose
Catalog common DDR4 failure patterns with symptom → likely cause mappings and recommended next measurements. This makes failures explainable rather than mysterious.

> Use this reference when a bring-up test fails. Match the symptom, read the likely causes, take the recommended measurements before opening an issue.

---

## FS-01 — SPD Not Detected / I²C NACK

**Symptom:**
- BIOS skips the DIMM slot silently
- `i2cdump` returns NACK or all-0xFF
- `decode-dimms` outputs no module found
- SMBus transaction times out

**Likely causes (in order of probability):**

| Priority | Cause | How to distinguish |
|----------|-------|--------------------|
| 1 | VDDSPD rail missing or < 2.2 V | Probe VDDSPD on edge connector (pin 284) with DVM |
| 2 | SA0/SA1/SA2 address bits wrong | Check device address: default is 0x50 (SA=000); probe pins 139/140/238 |
| 3 | SDA or SCL open circuit | Continuity from pin 141 (SCL) and 285 (SDA) to EEPROM |
| 4 | No host pull-up on SDA/SCL | Pull-ups are host-side in OMI v1; confirm host board has them |
| 5 | EEPROM WP held high | WP tied to GND in OMI v1 design — verify |
| 6 | EEPROM unprogrammed | Dump raw bytes; all-0x00 or all-0xFF means blank chip |

**Recommended measurements:**
1. DVM: VDDSPD pin 284 → GND — expect 2.2–3.6 V with host powered
2. DVM: continuity SCL (141) → EEPROM SCL pad
3. DVM: continuity SDA (285) → EEPROM SDA pad
4. Logic analyzer / scope on SCL/SDA — confirm pull-up waveform shape (should not be floating/square-wave-only)

---

## FS-02 — Memory Training Failure (Boot Loop / No POST)

**Symptom:**
- System reboots repeatedly during POST
- BIOS shows memory error code / beep code
- System posts but hangs before OS
- BIOS shows 0 MB or wrong capacity

**Likely causes:**

| Priority | Cause | How to distinguish |
|----------|-------|--------------------|
| 1 | VDD or VDDQ rail missing / marginal | Probe VDD (e.g., pin 64) and VDDQ on known-good supply; check voltage under load |
| 2 | RESET_n not releasing (stuck low) | Probe pin 58 — should go HIGH (≥ 0.8 × VDD) during POST |
| 3 | CKE0 not asserting | Probe pin 60 — should toggle during training sequence |
| 4 | CK_t / CK_c not reaching module | Probe pins 74/75 for differential clock signal |
| 5 | CS0_n not asserted | Probe pin 84 |
| 6 | DQ lane(s) open | See FS-04 — wrong capacity often accompanies training |
| 7 | Termination rail VTT absent | Probe pins 77/221; should be VDD/2 |
| 8 | VREF absent or wrong level | Probe pin 146 (VREFCA); should be ~VDD/2 |

**Recommended measurements:**
1. DVM: VDD and VDDQ under load — expect 1.2 V ± 5%
2. Scope: RESET_n (pin 58) during cold power-on — confirm deassert after DRAM power-up sequence
3. Scope: CK_t/CK_c (pins 74/75) — confirm differential clock, no missing transitions
4. Scope: CKE0 (pin 60) — confirm it toggles during POST

---

## FS-03 — Module Detected but Wrong Capacity

**Symptom:**
- BIOS shows 4 GB instead of 8 GB (or similar fraction)
- OS reports less RAM than expected
- memtest tests a smaller region than installed capacity

**Likely causes:**

| Priority | Cause | How to distinguish |
|----------|-------|--------------------|
| 1 | One or more DQ byte lanes open | Wrong capacity appears as 50%/25% of expected; lane-level |
| 2 | Address bit open (A0–A13) | Causes mirrored/aliased address space |
| 3 | BA0/BA1/BG0/BG1 open | Reduces accessible bank count |
| 4 | SPD capacity field wrong | Compare SPD byte 0x04/0x06 against JEDEC DDR4 SPD spec |

**Recommended measurements:**
1. FPGA/Class B: isolate individual DQ lanes with BIST — identify which lane is open
2. Continuity: check each DQ lane from edge connector pin → DRAM ball
3. SPD dump: verify capacity bytes (0x04: bank/row/col; 0x06: primary bus width)

---

## FS-04 — Random Single-Bit Errors (Deterministic Address)

**Symptom:**
- memtest reports error at the same address every run
- Stuck bit — always 0 or always 1
- Error pattern is address-independent within one lane

**Likely causes:**

| Priority | Cause | How to distinguish |
|----------|-------|--------------------|
| 1 | DQ pin open or shorted to neighbour | Continuity test on that specific DQ pin |
| 2 | DQS not reaching the DRAM for that lane | Probe DQS_t/DQS_c for the failing lane |
| 3 | DM/DBI pin shorted to a DQ pin in the lane | Check DM pin continuity; DM stuck low masks all writes |
| 4 | VDD marginal to that DRAM device | Check per-device decoupling; probe VDD at the DRAM |

**How to identify failing lane from error address:**
- Lane assignment: `lane = error_bit // 8`
- Bit within lane: `bit = error_bit % 8`
- Map to connector pin via `ddr4_udimm_288_pinmap.csv` → `omi_net = D{lane}_DQ{bit}`

**Recommended measurements:**
1. Look up the failing DQ net in the CSV
2. Continuity: front-side edge pin → DRAM pad
3. Scope: DQS_t/c for the failing lane during write burst
4. Scope: DQ signal eye quality on the failing bit

---

## FS-05 — Intermittent / Thermally-Triggered Errors

**Symptom:**
- memtest passes in cold run; fails after warm soak
- Errors appear after 4+ hours of stress, then the system stabilizes
- Error count increases monotonically over time

**Likely causes:**

| Priority | Cause | How to distinguish |
|----------|-------|--------------------|
| 1 | Marginal solder joint expanding with temperature | Errors worsen when heated; clear when cooled — reflow suspect joint |
| 2 | VDD/VDDQ droops under sustained load | Scope VDD with memory benchmark running; measure ripple |
| 3 | Signal integrity marginal at operating temperature | Errors in specific lane, correlated with DRAM temp |
| 4 | DRAM self-heating beyond operating range | Check DRAM junction temperature; add airflow |

**Recommended measurements:**
1. Record error onset time and ambient temperature
2. Scope VDD ripple under load vs. idle
3. Thermal camera or IR thermometer on DRAM devices at failure time
4. Repeat test with active cooling — if errors disappear, thermal root cause confirmed

---

## FS-06 — SPD Read Succeeds, Training Fails

**Symptom:**
- BIOS detects the DIMM and reads SPD correctly
- Training fails on first or subsequent boot
- BIOS reports unsupported speed or timing

**Likely causes:**

| Priority | Cause | How to distinguish |
|----------|-------|--------------------|
| 1 | SPD timing bytes incorrect for actual module | Compare SPD tCL/tRCD/tRP/tRAS to DRAM datasheet spec |
| 2 | Clock signal marginal (jitter / levelissue) | Scope CK_t/CK_c; check eye opening |
| 3 | Platform does not support the programmed speed | Try lower speed profile in BIOS (force DDR4-2133) |
| 4 | VREF marginal | Probe pin 146 (VREFCA) during training |

**Recommended measurements:**
1. SPD dump: compare timing bytes against JEDEC DDR4 SPD spec table
2. Force BIOS to DDR4-2133 (minimum JEDEC baseline) — if training passes, SPD speed profile is wrong
3. Scope CK differential eye at edge connector

---

## Quick Reference: Symptom → Signature Map

| Symptom | First signature to check |
|---------|--------------------------|
| DIMM slot not detected | FS-01 (VDDSPD / SPD) |
| Boot loop at POST | FS-02 (VDD/RESET_n/CKE) |
| Wrong capacity shown | FS-03 (DQ lane open) |
| Same address fails every run | FS-04 (stuck DQ bit) |
| Errors after hours of soak | FS-05 (thermal / margin) |
| SPD OK but training fails | FS-06 (timing / clock) |

---

*See also: `08-2_bringup_ladder.md` (stop conditions), `08-3_test_matrix.md` (failure taxonomy).*

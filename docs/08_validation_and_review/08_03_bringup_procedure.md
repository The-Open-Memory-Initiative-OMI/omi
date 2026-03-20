# Stage 8.03 — Bring-Up Procedure (OMI v1)

## Project
Open Memory Initiative (OMI) — OMI v1 DDR4 UDIMM

## Status
Draft

## Purpose
Provide a step-by-step bring-up procedure from bare fabricated PCB to OS boot. Written so another engineer can follow it independently without oral instructions. This is the operational counterpart to the validation ladder defined in [08-2_bringup_ladder.md](./08-2_bringup_ladder.md).

> **Rule:** Do not skip levels. Do not proceed to the next step until the current step passes. A failed step is a valid result — document it per [08_04_success_criteria_and_failure_modes.md](./08_04_success_criteria_and_failure_modes.md) §4.

---

## Relationship to Existing Documents

This document **extends** the following:

- [08-2_bringup_ladder.md](./08-2_bringup_ladder.md) — Defines L0–L4 levels, pass/fail criteria, and stop conditions. This document operationalizes those levels into step-by-step procedures.
- [L1_bench_electrical/measurement_procedures.md](./L1_bench_electrical/measurement_procedures.md) — Detailed L1 bench measurement procedures (Session 1: continuity, Session 2: PDN, Session 3: SPD bus). This document references those procedures; it does not duplicate them.
- [08-5_failure_signatures.md](./08-5_failure_signatures.md) — Failure signatures FS-01 through FS-06. Referenced throughout for diagnostics.
- [08-4_reporting_template.md](./08-4_reporting_template.md) — Report format and Run ID scheme used for all evidence.

**What this document adds:** A single, ordered procedure document that an engineer follows from start to finish, with cross-references to detailed sub-procedures and clear go/no-go decision points.

---

## Prerequisites

Before starting bring-up, ensure:

1. **L0 validation has passed.** All automated scripts pass, peer review is complete, L0 report is committed. See [08-2_bringup_ladder.md](./08-2_bringup_ladder.md) §L0.
2. **Post-fabrication pre-insertion checklist is complete.** See [08_05_review_checklists.md](./08_05_review_checklists.md) §2. Module has a build ID label.
3. **Equipment is available:**
   - Digital multimeter (DVM) with continuity mode and resistance measurement
   - Oscilloscope with ≥ 500 MHz bandwidth (for L1 power rail and L3 signal measurements)
   - Class A validation platform verified with known-good DIMM (see [08_02_validation_platform_strategy.md](./08_02_validation_platform_strategy.md) §5)
   - Bootable USB with Linux live environment (Ubuntu Server or similar) and memtest86+
   - Camera or screenshot tool for evidence capture
4. **A Run ID has been assigned** per [08-4_reporting_template.md](./08-4_reporting_template.md): `RUN-YYYYMMDD-PLATFORM-LEVEL-SEQ`
5. **An evidence directory has been created:** `validation/runs/[PLATFORM_ID]/`

---

## Step 1 — Pre-Insertion Bench Checks (L1 Scope)

**Goal:** Confirm the module is electrically sound before inserting it into any powered host. This protects both the module and the host platform from damage due to manufacturing defects.

### 1.1 Visual Inspection

Perform the visual inspection items from [08_05_review_checklists.md](./08_05_review_checklists.md) §2 if not already completed.

**Evidence:** Photograph both sides of the module. File as `OMI-V1-[PLATFORM]-L1-[DATE]-visual-front.jpg` and `-back.jpg`.

### 1.2 Unpowered Continuity Audit

Follow [L1_bench_electrical/measurement_procedures.md](./L1_bench_electrical/measurement_procedures.md) **Session 1** in full. This session covers 6 net groups:

| Group | What to Check | Expected | Failure Action |
|-------|--------------|----------|---------------|
| GND | All VSS pins interconnected | < 1 Ω between any two GND pins | **STOP.** Open circuit on ground is a manufacturing defect. |
| Power rails | VDD, VDDQ, VPP, VDDSPD, VTT, VREF — each isolated from GND and from each other | > 100 kΩ between distinct rails (capacitor charge effect may give low initial reading; wait 2–3 seconds for reading to stabilize) | **STOP if short detected.** Do not power on. See [08_04](./08_04_success_criteria_and_failure_modes.md) §2 L1 failures. |
| DQ/DQS | Spot-check lane 0: D0_DQ0 (pin 5) to DRAM pad | Continuity (< 10 Ω) | Open → manufacturing defect on that trace |
| CA/CLK | Spot-check: CK_t (pin 74), CS0_n (pin 84) to DRAM | Continuity (< 10 Ω) | Open → manufacturing defect |
| SPD | SCL (pin 141) and SDA (pin 285) to EEPROM | Continuity (< 10 Ω) | Open → SPD will not be readable |
| NC pins | Spot-check 3–5 NC pins | No continuity to any net (> 1 MΩ) | Short → NC pin connected to something it shouldn't be |

**Evidence:** Completed [measurement_log_template.csv](./L1_bench_electrical/measurement_log_template.csv). File as `OMI-V1-[PLATFORM]-L1-[DATE]-continuity-log.csv`.

### 1.3 I²C Bus Pull-Up Verification

Measure resistance from SDA (pin 285) to VDDSPD (pin 284):
- **Expected:** 2.2–10 kΩ if the host or jig provides pull-ups. If measuring on a bare module without host, expect open circuit (pull-ups are host-side in OMI v1).
- **If open (on bare module):** This is expected. Pull-ups will be provided by the host. Note this in the log.
- **If shorted (< 100 Ω):** Manufacturing defect. Do not power on.

Repeat for SCL (pin 141) to VDDSPD (pin 284).

### 1.4 Go/No-Go Decision

| Result | Action |
|--------|--------|
| All checks pass | Proceed to Step 2 |
| Any power rail short detected | **STOP.** Do not power on. Document failure per [08_04](./08_04_success_criteria_and_failure_modes.md) §4 template. |
| Open circuit on functional net | **STOP.** Document which net is open. This will cause downstream failures (wrong capacity, training failure, etc.) — there is no point proceeding until repaired. |
| Minor anomaly (e.g., higher-than-expected resistance on one pin) | Document and proceed with caution. Monitor that net during powered testing. |

---

## Step 2 — First Power-Up (L1 Scope)

**Goal:** Confirm power rails come up correctly when the module is inserted into a powered host.

### 2.1 Preparation

1. Power off the Class A host platform completely. Unplug AC power.
2. Insert the OMI v1 module into the DDR4 UDIMM slot. Ensure the module seats fully — both retention clips should engage.
3. Attach scope probes to test points (see [08_01_test_point_and_dft_plan.md](./08_01_test_point_and_dft_plan.md)):
   - Channel 1: VDD test point (pin 64 area)
   - Channel 2: VPP test point (pin 142 area)
   - Ground clip: GND test point
4. Set scope trigger to single-shot on Channel 1 rising edge to capture power-up sequence.

### 2.2 Power On

1. Reconnect AC power to the host platform.
2. Press power button. Observe scope for power rail sequencing.
3. Measure DC voltages at test points with DVM:

| Rail | Test Point | Expected Voltage | Acceptable Range (±5%) | Failure Threshold |
|------|-----------|-----------------|----------------------|-------------------|
| VDD | Pin 64 area | 1.200 V | 1.140 – 1.260 V | < 1.0 V or > 1.4 V |
| VDDQ | Board-level TP | 1.200 V | 1.140 – 1.260 V | < 1.0 V or > 1.4 V |
| VPP | Pin 142 area | 2.500 V | 2.375 – 2.625 V | < 2.0 V or > 3.0 V |
| VDDSPD | Pin 284 area | 3.300 V (typical) | 2.200 – 3.600 V | < 2.0 V |

4. Measure quiescent current draw if possible (requires series current measurement on host supply — skip if not feasible without modifying host).

### 2.3 What to Watch For

- **Rails come up in expected order:** JEDEC specifies VPP should be present before or simultaneously with VDD. Capture the scope trace.
- **No excessive ripple:** VDD ripple should be < 50 mV peak-to-peak at idle. High ripple suggests inadequate decoupling.
- **No thermal events:** Touch the DRAM devices briefly after 10 seconds of power-on. They should be at ambient temperature or barely warm. **If any component is hot to the touch, REMOVE POWER IMMEDIATELY.**

### 2.4 Safety Stop Conditions

| Condition | Action |
|-----------|--------|
| Any component smells of burning | **REMOVE POWER IMMEDIATELY.** Unplug AC. Do not re-power. Photograph the module. Document as critical failure. |
| Any component is hot to the touch within 10 seconds | **REMOVE POWER.** Likely short circuit or wrong component value. Check for solder bridges. |
| Rail voltage is zero | Host may not be supplying power to the DIMM slot. Verify with known-good DIMM. If known-good DIMM also shows zero, the slot or host is the issue, not the OMI module. |
| Rail voltage is significantly wrong (> 20% off) | Document and investigate. May indicate host power delivery issue rather than module fault. |

**Evidence:** Scope capture of power-up sequence, DVM voltage readings. File as `OMI-V1-[PLATFORM]-L1-[DATE]-powerup-scope.png` and `-voltage-readings.txt`.

### 2.5 Go/No-Go Decision

| Result | Action |
|--------|--------|
| All rails within spec, no thermal events | Proceed to Step 3 |
| One or more rails out of spec | **STOP.** See [08-5_failure_signatures.md](./08-5_failure_signatures.md) FS-02. Document failure. |
| Thermal event | **STOP.** Critical failure. Do not re-power without root cause analysis. |

---

## Step 3 — SPD Verification (L2 Scope)

**Goal:** Confirm the host can read the SPD EEPROM and the module identifies itself correctly.

### 3.1 BIOS-Level SPD Check

1. Allow the host to complete POST (or fail with error code — either is informative).
2. Enter BIOS/UEFI setup.
3. Navigate to memory information screen.
4. Check if the DIMM slot shows the OMI module:
   - **Expected:** DDR4, 8192 MB (or 8 GB), 1Rx8, DDR4-2400 (or DDR4-2400T)
   - **If not detected:** See [FS-01](./08-5_failure_signatures.md). Do not proceed to OS.

**Evidence:** Photo of BIOS memory information screen. File as `OMI-V1-[PLATFORM]-L2-[DATE]-bios-spd.jpg`.

### 3.2 OS-Level SPD Verification

1. Boot Linux from USB (skip if BIOS did not detect the module — go to failure procedure).
2. Install I²C tools if not present: `sudo apt install i2c-tools`
3. Detect SPD on I²C bus:
   ```
   sudo modprobe i2c-dev
   sudo i2cdetect -l           # List available I²C buses
   sudo i2cdetect -y <bus>     # Scan for devices (expect 0x50)
   ```
4. Dump raw SPD bytes:
   ```
   sudo i2cdump -y <bus> 0x50 b > spd_dump.txt
   ```
5. Decode SPD:
   ```
   sudo decode-dimms
   ```

### 3.3 SPD Validation Checks

Compare the SPD readout against expected values:

| SPD Field | Expected Value | Byte Offset(s) | What Mismatch Means |
|-----------|---------------|-----------------|-------------------|
| Module type | DDR4 SDRAM (0x0C) | Byte 2 | Wrong EEPROM content; reprogram |
| Module format | UDIMM (0x02) | Byte 3[3:0] | Wrong module type; reprogram |
| Total capacity | 8 GB | Bytes 4, 6, 12 | Capacity encoding error |
| Bus width | 64-bit (non-ECC) | Byte 13 | Bus width or ECC flag wrong |
| Speed grade | DDR4-2400 | Bytes 12, 17–19 | Timing parameters wrong |
| Ranks | 1 (single rank) | Byte 12[5:3] | Rank encoding error |
| Device width | x8 | Byte 12[2:0] | Device width encoding error |

**If SPD reads correctly:** L2 passes. Proceed to Step 4.

**If SPD read fails or data is wrong:** Document per [08_04](./08_04_success_criteria_and_failure_modes.md) §4 failure reporting template. Follow [FS-01](./08-5_failure_signatures.md) diagnostic sequence. This is a valid and valuable result.

**Evidence:** Raw SPD hex dump, `decode-dimms` output. File as `OMI-V1-[PLATFORM]-L2-[DATE]-spd-dump.txt` and `-decode-dimms.txt`.

---

## Step 4 — Memory Training (L3 Scope)

**Goal:** Confirm the host memory controller can train the DDR4 interface and complete POST.

### 4.1 Training Observation

1. Cold boot the host (full power cycle, not warm reboot).
2. Observe POST sequence:
   - **Expected:** POST completes normally. Memory count or memory OK message appears. No error codes or beep codes.
   - **Training time:** DDR4 training typically takes 2–10 seconds. If POST hangs for > 30 seconds on memory initialization, training may be failing silently.

### 4.2 BIOS Settings to Document

Record these settings for every training attempt — they are part of the test environment and affect reproducibility:

| Setting | Value | Notes |
|---------|-------|-------|
| Memory speed | Auto / Manual (specify) | If Auto fails, try forcing DDR4-2133 |
| Memory timing mode | Auto / Manual | Start with Auto |
| XMP/EXPO profile | Disabled | OMI v1 SPD uses JEDEC base, not XMP |
| Memory training mode | Default | Do not enable "fast boot" or "skip training" |
| Memory voltage override | None (auto) | Do not override host VDD/VDDQ |

### 4.3 What Training Success Looks Like

- BIOS completes POST without error codes
- BIOS memory summary shows: DDR4-2400 (or host-selected speed), 8192 MB, single channel (if single-slot)
- No boot loops (system does not restart during POST)

### 4.4 What Training Failure Looks Like

| Symptom | Likely Cause | Next Step |
|---------|-------------|-----------|
| Boot loop (system restarts repeatedly) | Training fails, BIOS retries and gives up | See [FS-02](./08-5_failure_signatures.md). Probe VDD, RESET_n, CK. |
| BIOS error code (varies by vendor) | Training fails on specific step | Record exact error code. See [FS-02](./08-5_failure_signatures.md). Try DDR4-2133. |
| POST completes but shows 0 MB or wrong capacity | Partial training; DQ lanes open | See [FS-03](./08-5_failure_signatures.md). Check DQ lane continuity. |
| POST completes, correct capacity, but no OS boot | Training OK but secondary issue | Proceed to Step 5; may be boot device issue, not memory. |

> **Important:** A training failure is a VALID and VALUABLE result. It narrows the problem space. Do not discard training failures — document them with full BIOS settings, platform details, and any error codes.

**Evidence:** Photo of BIOS POST screen (memory summary), any error codes. File as `OMI-V1-[PLATFORM]-L3-[DATE]-bios-post.jpg`.

---

## Step 5 — OS Boot and Basic Memory Test (L3 Scope)

**Goal:** Boot an OS and verify the host can use the installed memory without errors.

### 5.1 OS Boot

1. Boot Linux from USB (Ubuntu Server or minimal live distribution).
2. Verify boot completes to a login prompt or desktop.

### 5.2 OS-Level Memory Verification

Run the following commands and capture output:

```bash
# Memory detection
sudo dmidecode --type 17 > dmidecode_memory.txt

# Kernel memory info
cat /proc/meminfo | head -5 > meminfo.txt

# Kernel boot messages related to memory
dmesg | grep -i "memory\|ram\|dimm\|ddr" > dmesg_memory.txt
```

**Expected `dmidecode` output should include:**
- Size: 8192 MB (or 8 GB)
- Type: DDR4
- Speed: 2400 MT/s (or host-selected speed)
- Form Factor: DIMM

### 5.3 Short Memory Test

Run a basic memory test for initial validation:

```bash
# Option A: memtester (runs from within Linux)
sudo memtester 4G 1 > memtester_output.txt 2>&1

# Option B: Reboot into memtest86+ from USB
# (Preferred — tests all memory, not just what OS doesn't use)
```

**Minimum duration:** 10 minutes for initial smoke test.

**Pass criteria:** Zero errors reported. All test patterns complete.

**If errors are found:** Do not continue to L4. Document per [08_04](./08_04_success_criteria_and_failure_modes.md) §4. See [FS-04](./08-5_failure_signatures.md) for deterministic errors, [FS-05](./08-5_failure_signatures.md) for intermittent errors.

**Evidence:** `dmidecode` output, `meminfo`, `dmesg` excerpt, memtester/memtest86+ result. File as `OMI-V1-[PLATFORM]-L3-[DATE]-dmidecode.txt`, `-memtest-result.png`, etc.

---

## Step 6 — Stress and Soak Testing (L4 Scope — DEFERRED)

**This section documents intent only.** Detailed L4 procedures will be written post-fabrication when real hardware and real failure data are available. See [08-3_test_matrix.md](./08-3_test_matrix.md) §T5/T6/T7 for test category definitions.

### 6.1 What L4 Will Require

| Test | Tool | Minimum Duration | Pass Criterion |
|------|------|-----------------|---------------|
| Extended memtest | memtest86+ v6.00+ | ≥ 24 hours (≥ 2 full passes) | Zero errors |
| Cold boot repeatability | Manual power cycle | 20 consecutive cold boots | Training succeeds 20/20 times |
| Thermal monitoring | IR thermometer or thermal camera | Duration of soak test | DRAM case temp < 85°C |
| Multi-platform replication | Second Class A platform | Full L3 sequence on 2nd platform | L3 passes on both platforms |

### 6.2 What L4 Pass Looks Like (In Principle)

- Zero errors in 24-hour memtest86+ run
- Successful training on 20 out of 20 cold boots on the primary platform
- No thermal anomalies (no component exceeding datasheet maximum)
- L3 pass replicated on at least one additional platform

### 6.3 When L4 Procedures Will Be Written

L4 procedures will be developed after:
1. At least one module has completed L3 successfully
2. Actual failure modes (if any) have been observed and documented
3. The project has real data to inform soak test parameters (e.g., actual power draw, actual thermal behavior)

> L4 is not required for Stage 8 closure. See [08_06_stage8_closure_criteria.md](./08_06_stage8_closure_criteria.md) §2.

---

## Step 7 — Evidence Collection Protocol

### 7.1 File Naming Convention

All evidence files follow this pattern:

```
OMI-V1-[PLATFORM]-[LEVEL]-[DATE]-[DESCRIPTION].[ext]
```

| Field | Format | Example |
|-------|--------|---------|
| PLATFORM | Short platform ID | INTEL-B660-MSI |
| LEVEL | L1 / L2 / L3 / L4 | L2 |
| DATE | YYYYMMDD | 20260320 |
| DESCRIPTION | Lowercase, hyphens, no spaces | spd-dump, bios-post, continuity-log |
| ext | File extension | txt, csv, jpg, png |

**Example:** `OMI-V1-INTEL-B660-MSI-L2-20260320-spd-dump.txt`

### 7.2 Storage Location

```
validation/runs/
  └── [PLATFORM_ID]/
        ├── L1/
        │   ├── OMI-V1-INTEL-B660-MSI-L1-20260320-visual-front.jpg
        │   ├── OMI-V1-INTEL-B660-MSI-L1-20260320-continuity-log.csv
        │   └── OMI-V1-INTEL-B660-MSI-L1-20260320-powerup-scope.png
        ├── L2/
        │   ├── OMI-V1-INTEL-B660-MSI-L2-20260320-spd-dump.txt
        │   └── OMI-V1-INTEL-B660-MSI-L2-20260320-decode-dimms.txt
        └── L3/
            ├── OMI-V1-INTEL-B660-MSI-L3-20260320-bios-post.jpg
            ├── OMI-V1-INTEL-B660-MSI-L3-20260320-dmidecode.txt
            └── OMI-V1-INTEL-B660-MSI-L3-20260320-memtest-result.png
```

### 7.3 What to Capture at Each Step

| Step | Required Evidence | Format |
|------|------------------|--------|
| Step 1 (Pre-insertion) | Module photos (front/back), continuity log | JPG, CSV |
| Step 2 (Power-up) | Scope capture of rail sequencing, DVM voltage readings | PNG, TXT |
| Step 3 (SPD) | BIOS SPD screenshot, raw SPD hex dump, decode-dimms output | JPG, TXT |
| Step 4 (Training) | BIOS POST screenshot, error codes (if any) | JPG |
| Step 5 (OS boot) | dmidecode output, meminfo, dmesg excerpt, memtest result | TXT, PNG |

### 7.4 Evidence Integrity

- All evidence must be from the actual test run — no stock images, no re-creations.
- Evidence must be publicly shareable — no screenshots containing proprietary information (blur serial numbers if needed).
- For formal reports, include file SHA-256 hashes in the report for tamper evidence.

---

## Cross-References

- [08-2_bringup_ladder.md](./08-2_bringup_ladder.md) — Validation ladder with pass/fail criteria and stop conditions
- [L1_bench_electrical/measurement_procedures.md](./L1_bench_electrical/measurement_procedures.md) — Detailed L1 bench measurement procedures (Sessions 1–3)
- [08-5_failure_signatures.md](./08-5_failure_signatures.md) — Failure signatures FS-01 through FS-06
- [08-4_reporting_template.md](./08-4_reporting_template.md) — Validation report format and Run ID scheme
- [08_01_test_point_and_dft_plan.md](./08_01_test_point_and_dft_plan.md) — Test point locations for probe attachment
- [08_02_validation_platform_strategy.md](./08_02_validation_platform_strategy.md) — Platform selection and documentation requirements
- [08_04_success_criteria_and_failure_modes.md](./08_04_success_criteria_and_failure_modes.md) — Success criteria, failure catalog, and failure reporting template
- [08_05_review_checklists.md](./08_05_review_checklists.md) — Pre-insertion checklist (prerequisite for Step 1)

---

*This document defines how to bring up the module. For what success and failure look like, see [08_04_success_criteria_and_failure_modes.md](./08_04_success_criteria_and_failure_modes.md). For where to probe, see [08_01_test_point_and_dft_plan.md](./08_01_test_point_and_dft_plan.md).*

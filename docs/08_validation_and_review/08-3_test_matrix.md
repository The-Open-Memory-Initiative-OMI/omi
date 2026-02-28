# Stage 8.3 — Test Matrix (OMI v1)

## Project
Open Memory Initiative (OMI) — OMI v1 DDR4 UDIMM

## Status
Draft

## Purpose
Define what tests to run, minimum durations, pass criteria, and a failure taxonomy for OMI v1 validation. This matrix is the authoritative reference for deciding what "success" means at each level.

---

## 1. Test Categories

### T1 — SPD / I²C Read

| Field | Detail |
|-------|--------|
| What it tests | SPD EEPROM accessibility and data integrity |
| Platform | Class A (host SMBus) or Class B (I²C controller) |
| Tools | `decode-dimms` (Linux), `i2cdump`, Windows SPD reader, BIOS SPD display |
| Duration | Single pass (~30 seconds) |

**Pass criteria:**
- 256 bytes returned without SMBus error
- Module type byte = DDR4 (0x0C)
- Capacity, width, and speed grade fields match expected values
- CRC check bytes pass (if tool validates)

**Reported artifact:** raw hex dump (256 bytes) + tool output screenshot

---

### T2 — Memory Training

| Field | Detail |
|-------|--------|
| What it tests | Host controller can train DDR4 at target speed |
| Platform | Class A (primary); Class B (alternative) |
| Tools | BIOS POST (automatic); FPGA MIG training log |
| Duration | Single boot cycle (1–5 minutes) |

**Pass criteria:**
- Training completes without reboot loop
- BIOS reports trained speed ≥ DDR4-2400 (baseline)
- No training-related error codes in POST
- Module capacity shown correctly in BIOS memory map

**Reported artifact:** BIOS POST photo or log; trained speed confirmed

---

### T3 — OS Boot + Capacity Verification

| Field | Detail |
|-------|--------|
| What it tests | OS can use the full memory range without errors |
| Platform | Class A |
| Tools | OS boot log; `dmidecode -t memory` (Linux); Windows Task Manager / msinfo32 |
| Duration | Single boot cycle + 5 min OS observation |

**Pass criteria:**
- OS boots to usable state
- OS reports correct total RAM (within 0.1% of expected)
- No memory-related kernel errors at boot (`dmesg`, Event Viewer)
- All DIMM slots' memory is accessible

**Reported artifact:** OS memory report screenshot + dmesg/event log snippet

---

### T4 — Smoke Test (Short Memtest)

| Field | Detail |
|-------|--------|
| What it tests | Basic read/write correctness at full capacity |
| Platform | Class A |
| Tools | `memtest86+` ≥ v6.00; `memtester` (OS-level); Windows Memory Diagnostic |
| **Minimum duration** | **1 hour** (at least 1 full pass) |

**Pass criteria:**
- 0 errors after 1 full pass
- All test patterns complete (walking bits, modulo, random)
- No system crash or hang

**Reported artifact:** memtest screenshot showing 0 errors, pass count, capacity tested, duration

---

### T5 — Soak Test (Extended Memtest)

| Field | Detail |
|-------|--------|
| What it tests | Sustained correctness and thermal stability |
| Platform | Class A |
| Tools | `memtest86+` continuous; `stress-ng --vm`; Prime95 Blend |
| **Minimum duration** | **8 hours** (standard soak) |

**Pass criteria:**
- 0 errors across full test duration
- System remains stable (no crash, no hang, no thermal throttle affecting memory)
- Error count remains 0 at 1h, 4h, and 8h checkpoints

**Reported artifact:** log at each checkpoint (1h, 4h, 8h); final screenshot; ambient temperature recorded

---

### T6 — Stress Test (Full Soak)

| Field | Detail |
|-------|--------|
| What it tests | Long-duration reliability under worst-case workload |
| Platform | Class A |
| Tools | `memtest86+` continuous; OS-level stress in parallel with CPU/IO |
| **Minimum duration** | **24 hours** |

**Pass criteria:**
- 0 errors throughout
- System does not restart or freeze
- No correctable or uncorrectable errors in OS event logs

**Reported artifact:** 24h log with periodic checkpoints; pass/fail summary; platform thermal data if available

---

### T7 — Temperature Variance

| Field | Detail |
|-------|--------|
| What it tests | Stability across ambient temperature range |
| Platform | Class A (with temperature monitoring) |
| Tools | memtest86+ or stress-ng; ambient/board temperature sensor |
| **Minimum duration** | 1h smoke at each temp point |
| Temperature points | Typical: ~25°C; Warm: ~40°C (enclosed case); Cold start: ~10°C |

**Pass criteria:**
- 0 errors at each temperature point
- Training succeeds at cold start
- No errors introduced by temperature transition

**Reported artifact:** test log per temperature point; temperature measurement method documented

> Note: formal thermal characterization is not required for OMI v1. Temperature variance testing is optional but recommended before declaring L4 complete.

---

## 2. Minimum Run Duration Summary

| Test | Category | Minimum Duration | Level Gate |
|------|----------|-----------------|-----------|
| T1 — SPD read | Single pass | ~30 sec | L2 |
| T2 — Training | Single boot | 1–5 min | L3 |
| T3 — OS boot | Single boot + observation | ~5 min | L3 |
| T4 — Smoke | Short memtest | **1 hour** | L4 entry |
| T5 — Soak | Extended memtest | **8 hours** | L4 standard |
| T6 — Stress | Full stress | **24 hours** | L4 full |
| T7 — Temperature | Per temp point | **1 hour each** | L4 optional |

---

## 3. Failure Taxonomy

### 3A — Deterministic Failures

> Failure occurs every time the test runs under the same conditions.

| Symptom | Probable cause | Severity |
|---------|---------------|----------|
| SPD read always fails / NACK | VDDSPD missing, SCL/SDA open, SA address wrong | **Critical** — L2 blocker |
| Training always loops/fails | CK, RESET_n, CKE open; VDD/VDDQ marginal | **Critical** — L3 blocker |
| OS reports wrong capacity | DQ lane open; CA addressing wrong | **Critical** — L3 blocker |
| memtest shows same error address every run | Stuck bit in DQ lane; bad via/trace on that lane | **Critical** — L4 blocker |
| System won't POST | Severe rail problem; module not seated | **Critical** |

**Action:** halt immediately, open issue labeled `DETERMINISTIC-FAIL`, document exact conditions and symptoms.

---

### 3B — Intermittent Failures

> Failure occurs inconsistently — not every run, not at the same address.

| Symptom | Probable cause | Severity |
|---------|---------------|----------|
| memtest error appears, then disappears | Signal margin borderline; thermal drift; power supply ripple | **High** — do not ignore |
| Training passes sometimes, fails sometimes | Clock marginal; impedance mismatch; power noise | **High** |
| Errors appear only after warm soak | Thermal expansion causing marginal contact | **Medium–High** |
| Single correctable error in 24h soak | Possible single event or real margin issue | **Medium** — investigate |

**Action:** do not waive intermittent failures. Run an additional 8-hour soak to determine if error rate increases. Open issue labeled `INTERMITTENT-FAIL` with error frequency, conditions, and test parameters.

> **Policy:** An intermittent failure is not a passing result. OMI v1 requires 0 errors, not "rarely any errors".

---

### 3C — Environment Failures

> Failure is caused by the test environment, not the module under test.

| Symptom | Likely cause | Action |
|---------|-------------|--------|
| All DIMMs fail in the same slot | Slot damaged or dirty | Try another slot; clean connector |
| Failure on one platform only | Platform-specific incompatibility | Test on a second platform |
| Failure only when another DIMM is populated | Dual-rank/dual-slot interaction | Isolate to single-slot single-DIMM |

**Action:** document environment isolation steps taken before attributing failure to the module.

---

*Next: `08-4_failure_mode_reference.md` — debug hooks and root-cause reference per failure type.*

# Stage 8.1 — Validation Platforms (OMI v1)

## Project
Open Memory Initiative (OMI) — OMI v1 DDR4 UDIMM

## Status
Draft

## Purpose
Define which platforms are accepted for OMI v1 validation, why each is chosen, what evidence each can generate, and what minimum requirements must be met before a platform result is considered valid.

---

## 1. Platform Classes

### Class A — Consumer/Workstation PC Motherboard

| Attribute | Detail |
|-----------|--------|
| Interface | Native DDR4 UDIMM slot (288-pin JEDEC) |
| Examples | Intel 10th–12th gen desktop boards; AMD AM4/AM5 with DDR4 UDIMM slots |
| Availability | High; widely available for testing |
| Risk | BIOS may enforce SPD limits; limited low-level observability |

**What it proves:**
- SPD EEPROM is readable (BIOS/OS reads SPD over SMBus correctly)
- Module is electrically compatible with a real DDR4 host controller
- Training completes (host controller trains successfully against the DIMM)
- OS boots and recognizes the full advertised capacity
- Stress tests (memtest, memory bandwidth benchmarks) pass without errors

---

### Class B — FPGA Platform with DDR4 DIMM Interface

| Attribute | Detail |
|-----------|--------|
| Interface | DDR4 UDIMM slot via FPGA MIG (Memory Interface Generator) or equivalent |
| Examples | Xilinx/AMD VCU118, KC705 with DIMM mezzanine; Intel/Altera Stratix board |
| Availability | Medium; requires development board access |
| Risk | Pinout adapter may be required; FPGA DDR4 controller IP licenses may apply |

**What it proves:**
- Raw electrical continuity of data lanes (loopback or pattern tests at controllable rates)
- Training behavior at specific speeds (frequency-sweepable)
- Lane-by-lane failure isolation (individual DQ lanes observable)
- SPD read at controller level without BIOS abstraction

---

### Class C — Lab Jig / Continuity Fixture

| Attribute | Detail |
|-----------|--------|
| Interface | Passive breakout PCB + 288-pin DDR4 UDIMM socket |
| Examples | Custom continuity jig; DIMM socket breakout with test points |
| Availability | Must be fabricated or sourced |
| Risk | No active validation; only passive measurements |

**What it proves:**
- Continuity: all 288 edge contacts reach intended nets
- No shorts between adjacent pins (resistance measurement)
- Rail presence and isolation (power rails present; no cross-rail shorts)
- Physical insertion: module seats correctly in the connector

---

## 2. Minimum Requirements per Platform

| Requirement | Class A | Class B | Class C |
|------------|---------|---------|---------|
| 288-pin DDR4 UDIMM slot (no adapter) | ✅ required | ⚠️ adapter permitted if documented | N/A (passive) |
| DDR4-2400 or faster rated | ✅ required | ✅ required | N/A |
| SMBus / I²C access to SPD EEPROM | ✅ host BIOS | ✅ via I²C controller | N/A |
| Platform documentation provided in results | ✅ | ✅ | ✅ |
| Tools and procedures documented | ✅ | ✅ | ✅ |
| Failures reported (not only successes) | ✅ | ✅ | ✅ |

> If an adapter is used on a Class B platform, the adapter model and pinout mapping must be documented in the validation report.

---

## 3. Evidence Each Platform Can Generate

| Evidence Type | Class A | Class B | Class C |
|--------------|---------|---------|---------|
| Continuity / no-shorts | ❌ indirect | ⚠️ partial | ✅ direct |
| Rail presence / isolation | ❌ indirect | ⚠️ partial | ✅ direct |
| SPD read (raw bytes) | ✅ via OS tools | ✅ via I²C | ❌ |
| BIOS/host enumeration | ✅ | ❌ | ❌ |
| Training completion log | ✅ via BIOS POST | ✅ via MIG log | ❌ |
| OS boot + capacity recognition | ✅ | ❌ | ❌ |
| Stress / error-rate measurement | ✅ (memtest86+, etc.) | ✅ (PRBS, BIST) | ❌ |
| Lane-level failure isolation | ❌ limited | ✅ | ❌ |
| Frequency sweep | ❌ BIOS-controlled | ✅ | ❌ |

---

## 4. Validation Ladder Mapping

| Ladder Level | Minimum Platform |
|-------------|-----------------|
| L0 — Artifact Integrity | No hardware needed |
| L1 — Bench Electrical (continuity, rails) | Class C (or Class B with scope) |
| L2 — Host Enumeration (SPD read in host) | Class A or Class B |
| L3 — Training + Boot | Class A |
| L4 — Stress + Soak | Class A (primary), Class B (lane-level companion) |

---

## 5. Reporting Requirements

Every platform validation result must include:

1. **Platform identification:** board model, BIOS/firmware version, DDR4 slot used
2. **Tools used:** OS, memtest version, scripts, FPGA IP version
3. **Procedure summary:** steps taken in order
4. **Results:** pass/fail per checklist item; raw logs where available
5. **Failures:** all failures reported with symptoms, not omitted
6. **Waivers:** any deviation from minimum requirements, with justification

> Validation without documented failures is not trusted — it means failures were not looked for.

---

*Next: `08-2_bringup_procedure.md` — step-by-step bring-up sequence for OMI v1.*

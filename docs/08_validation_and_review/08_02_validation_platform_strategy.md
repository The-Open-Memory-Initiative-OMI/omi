# Stage 8.02 — Validation Platform Strategy (OMI v1)

## Project
Open Memory Initiative (OMI) — OMI v1 DDR4 UDIMM

## Status
Draft

## Purpose
Define specific host platforms for OMI v1 validation, with concrete board recommendations, cost estimates, a phased deployment strategy, and an honest assessment of platform risks. This document operationalizes the platform taxonomy defined in [08-1_validation_platforms.md](./08-1_validation_platforms.md).

---

## Relationship to Existing Documents

This document **extends** the following:

- [08-1_validation_platforms.md](./08-1_validation_platforms.md) — Defines the Class A / B / C platform taxonomy, minimum requirements per class, evidence capabilities, and ladder-level mapping. **Read that document first.** This document does not repeat those definitions.
- [08-4_reporting_template.md](./08-4_reporting_template.md) — Defines the Run ID scheme and report format used for all platform results.

**What this document adds:** specific board recommendations, approximate costs, a phased strategy for which platform to use when, a platform documentation template, and a risk register.

---

## 1. Detailed Platform Requirements

Any platform used for OMI v1 validation must meet these requirements beyond the Class minimums in [08-1](./08-1_validation_platforms.md):

### 1.1 Hardware Requirements

| Requirement | Why It Matters |
|-------------|---------------|
| At least one DDR4 UDIMM slot (288-pin, no adapter) | Adapters introduce contact resistance and signal integrity unknowns that confound debugging |
| Rated for DDR4-2400 or faster | OMI v1 targets DDR4-2400; the platform must support this speed natively |
| Single-DIMM operation supported | Some platforms require matched pairs; OMI v1 must be testable in isolation |
| Physical access to DIMM slot for probe attachment | Slots buried under heatsinks or shrouds prevent L1 bench measurements |

### 1.2 Firmware/BIOS Requirements

| Requirement | Why It Matters |
|-------------|---------------|
| SPD readout visible in BIOS setup | Confirms L2 (SPD read) without requiring OS boot |
| Memory speed configurable (auto + manual) | If training fails at DDR4-2400, ability to force DDR4-2133 helps isolate whether speed or connectivity is the issue |
| Memory training error reporting | Platforms that silently skip a failed DIMM provide no diagnostic value |
| BIOS version documented and reproducible | Training behavior can change between BIOS updates; results must be tied to a specific version |

### 1.3 Software Requirements

| Requirement | Why It Matters |
|-------------|---------------|
| Bootable from USB (Linux live environment) | Eliminates OS installation as a variable; enables `i2cdetect`, `decode-dimms`, `memtest86+` |
| I²C/SMBus access from OS | Required for L2 SPD verification using `i2c-tools` |
| `dmidecode` or equivalent available | Required for L3 OS-level memory reporting |

---

## 2. Option A — Consumer Motherboard (Class A)

### Why consumer boards are the primary v1 platform

Consumer motherboards are cheap, widely available, and represent the most common host environment for DDR4 UDIMMs. If the OMI v1 module works in a consumer board, it works in the real world. This is the most meaningful validation for an open reference design.

### Recommended board families

| Board Family | Chipset | Socket | DDR4 Slot Count | Approx. Cost (Used) | Notes |
|-------------|---------|--------|-----------------|---------------------|-------|
| **Intel B660 / H670** | Intel 600-series | LGA 1700 | 2–4 UDIMM | $60–$120 | 12th gen Intel; widely available; well-documented BIOS behavior; DDR4 variants common |
| **Intel B560 / H570** | Intel 500-series | LGA 1200 | 2–4 UDIMM | $50–$100 | 10th/11th gen Intel; very common on used market; stable BIOS ecosystem |
| **AMD B550 / B450** | AMD 500/400-series | AM4 | 2–4 UDIMM | $50–$100 | Ryzen 3000/5000 series; strong community BIOS support; DDR4 native |

### Pros

- **Low cost:** $50–$120 for a used board; add $30–$80 for a compatible CPU (e.g., Celeron G6900 for LGA 1700, Athlon 3000G for AM4). Total platform cost under $200.
- **Real-world host behavior:** Proves the module works with actual memory controllers and training algorithms that end users will encounter.
- **Wide availability:** Easy for community contributors to replicate results on similar hardware.
- **Fast iteration:** Insert module, power on, observe. No FPGA bitstream compilation or IP licensing.

### Cons

- **Closed firmware:** BIOS training algorithms are proprietary. If training fails, the BIOS error code may be cryptic or undocumented.
- **Limited debug visibility:** No access to internal training state, read leveling results, or write leveling margins.
- **Platform-specific quirks:** Intel and AMD memory controllers train differently. A module that trains on Intel may fail on AMD (or vice versa). This is not an OMI design flaw — it is a platform constraint that must be documented.
- **BIOS updates change behavior:** A BIOS update on the test platform can change training results. Pin validation to a specific BIOS version.

### Recommended v1 configurations

**Primary (Intel):**
- Board: Any Intel B660 with 2+ DDR4 UDIMM slots (e.g., MSI PRO B660M-A DDR4, ASUS PRIME B660M-A D4)
- CPU: Intel Celeron G6900 or Pentium Gold G7400 (cheapest LGA 1700 DDR4 option)
- Estimated total: ~$100–$150 used

**Secondary (AMD):**
- Board: Any AMD B550 with DDR4 UDIMM slots (e.g., MSI B550M PRO-VDH, Gigabyte B550M DS3H)
- CPU: AMD Athlon 3000G or Ryzen 3 3100 (cheapest AM4 option)
- Estimated total: ~$80–$130 used

> **Why two platforms?** Testing on both Intel and AMD confirms the module works with fundamentally different memory controller implementations. If the module works on both, platform-specific training is not a concern. If it works on one but not the other, the failure is documented and informs v2.

---

## 3. Option B — FPGA-Based Validation (Class B)

### Why FPGA validation exists as an option

FPGA-based DDR4 controllers provide full visibility into the training process: read leveling delays, write leveling results, per-lane error counts, and frequency sweeping. This is invaluable for deep characterization but comes at significant cost and complexity.

### Available platforms

| Platform | FPGA | DDR4 Interface | UDIMM Slot? | Approx. Cost | Open-Source Controller? |
|----------|------|---------------|-------------|-------------|----------------------|
| **Xilinx VCU118** | Virtex UltraScale+ | DDR4 DIMM | Yes (full-size) | $5,000+ | No (Xilinx MIG IP, licensed) |
| **Xilinx ZCU104** | Zynq UltraScale+ | DDR4 component | **No** (BGA pads only) | $1,000+ | No (Xilinx MIG IP) |
| **LiteDRAM on Arty A7** | Artix-7 | DDR3 only | No (SO-DIMM) | $130 | **Yes** (LiteDRAM, open-source) |
| **Antmicro DDR4 Tester** | Xilinx K7/KU | DDR4 RDIMM | **No** (RDIMM, not UDIMM) | Custom fab | **Yes** (open-source KiCad design) |

### Honest assessment for OMI v1

**The FPGA path has significant barriers for v1:**

1. **No affordable FPGA board has a full-size DDR4 UDIMM slot.** The VCU118 does, but costs $5,000+. All other options require either SO-DIMM adapters (which change SI characteristics) or are DDR3/RDIMM only.
2. **LiteDRAM** is the most promising open-source DDR controller, but its DDR4 support targets component-down designs (BGA DRAM soldered to the FPGA board), not DIMM-slot configurations.
3. **Antmicro's DDR4 tester** is open-source KiCad, but targets RDIMM (registered DIMMs), not UDIMM. An RDIMM tester cannot validate a UDIMM without a custom adapter and register emulation.
4. **FPGA DDR4 PHY complexity** is substantial. Even with MIG IP, achieving reliable DDR4-2400 training on an FPGA requires careful PCB design on the FPGA board itself — a second hardware problem layered on top of the one we're trying to solve.

**Recommendation:** Defer FPGA-based validation to v2 or as a community stretch goal. Do not block v1 validation on FPGA availability.

---

## 4. Recommended v1 Phased Strategy

| Phase | Validation Levels | Platform | Rationale |
|-------|------------------|----------|-----------|
| Phase 0 | L0 (Artifact Integrity) | None — desktop review only | L0 requires no hardware; completed pre-fabrication |
| Phase 1 | L1 (Bench Electrical) | Class C jig or multimeter at edge connector | Continuity and rail checks do not require a powered host; a passive breakout jig or careful probing at the edge connector is sufficient |
| Phase 2 | L2 (SPD Read) | Class A — cheapest available consumer board | SPD verification requires a powered host with SMBus; the cheapest Intel or AMD board that POSTs is sufficient |
| Phase 3 | L3 (Training + Boot) | Same Class A board from Phase 2 | No reason to switch platforms; training is the next step after SPD |
| Phase 4 | L3 replication | Second Class A board (different vendor: Intel if Phase 2 was AMD, or vice versa) | Cross-platform replication; confirms module is not accidentally tuned to one controller |
| Phase 5 | L4 (Stress + Soak) | Same Class A boards | Extended testing on proven platforms; add thermal monitoring |
| Stretch | Deep characterization | Class B (FPGA) | Only if community provides access to a VCU118 or equivalent with UDIMM slot |

**Total estimated hardware cost for Phases 1–5:** $200–$350 (two consumer boards + two budget CPUs + a DDR4 UDIMM breakout jig or careful probing).

---

## 5. Platform Documentation Template

Every validation run must record the following platform details. This template is required for all reports submitted per [08-4_reporting_template.md](./08-4_reporting_template.md).

```markdown
## Platform Record

| Field | Value |
|-------|-------|
| **Platform ID** | [Short identifier, e.g., INTEL-B660-MSI-01] |
| **Board manufacturer** | |
| **Board model** | |
| **Board revision** | [PCB revision if printed on board] |
| **Chipset** | |
| **CPU model** | |
| **CPU stepping** | [If known; from /proc/cpuinfo or CPU-Z] |
| **Socket** | |
| **BIOS/UEFI vendor** | [AMI, Phoenix, Insyde, etc.] |
| **BIOS version** | [Exact version string] |
| **BIOS date** | |
| **DDR4 slot used** | [Slot label, e.g., DIMMA1] |
| **Other DIMMs installed** | [None / describe if present] |
| **BIOS memory speed setting** | [Auto / Manual — specify if manual] |
| **BIOS memory timing mode** | [Auto / Manual — specify if manual] |
| **BIOS XMP/EXPO setting** | [Enabled / Disabled / N/A] |
| **BIOS memory training options** | [Any non-default settings] |
| **OS** | [e.g., Ubuntu 24.04 Server, memtest86+ v6.20] |
| **OS boot method** | [USB / SSD / PXE] |
| **Power supply** | [Model, wattage] |
| **Ambient temperature** | [°C at time of test] |
| **Date platform acquired** | |
| **Date platform last verified working** | [With a known-good DIMM] |
```

> **Critical:** Before testing an OMI v1 module, verify the platform works correctly with a known-good commercial DDR4 UDIMM. A platform that cannot train a commercial module will not train the OMI module — and the resulting failure is a platform problem, not an OMI problem. Document the known-good DIMM model and test date.

---

## 6. Known Platform Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| **BIOS rejects unknown SPD vendor ID** | Low–Medium | L2 blocked: host refuses to enumerate module with unrecognized manufacturer code | Program SPD with a well-known vendor ID for testing (document this as a workaround, not a permanent solution); try multiple BIOS versions |
| **BIOS enforces timing not in SPD** | Medium | L3 blocked: host applies tighter timings than SPD specifies, causing training failure | Use BIOS manual timing mode to force JEDEC base timings (CL17-17-17 for DDR4-2400); document the override |
| **Consumer board has only 1 DIMM slot** | Low | Limits ability to test multi-DIMM configurations | Acceptable for v1 (single-DIMM testing only); verify slot count before purchasing |
| **DDR4 boards becoming scarce** | Medium (increasing) | Platform availability decreases as DDR5 adoption grows | Source 2+ test boards early; document exact models for reproducibility |
| **BIOS update changes training behavior** | Medium | Results become non-reproducible across BIOS versions | Lock BIOS version for all v1 testing; document version in every report; do not update BIOS mid-validation |
| **Platform-specific training sensitivity** | High | Module trains on Intel but not AMD (or vice versa) | **This is expected and is not a failure of the OMI design.** Document platform-specific results separately; investigate root cause only if the module fails on ALL platforms |
| **Motherboard power delivery insufficient** | Low | VDD/VDDQ droop under load causes intermittent errors | Use boards with adequate VRM (not ultra-budget); measure rail voltages at test points under load |

> **Important:** Platform-specific incompatibilities are a fact of life in DDR4 validation. Different memory controllers have different training algorithms, impedance calibration ranges, and timing tolerances. A result of "works on Intel B660, fails on AMD B550" is a **valid and valuable** engineering finding — it narrows the debug space and informs SPD tuning for v2.

---

## Cross-References

- [08-1_validation_platforms.md](./08-1_validation_platforms.md) — Platform class definitions (Class A/B/C)
- [08-2_bringup_ladder.md](./08-2_bringup_ladder.md) — Ladder levels and minimum platform per level
- [08-4_reporting_template.md](./08-4_reporting_template.md) — Run ID scheme and report format
- [08_03_bringup_procedure.md](./08_03_bringup_procedure.md) — Step-by-step procedure that uses these platforms

---

*This document defines where to test. For how to test, see [08_03_bringup_procedure.md](./08_03_bringup_procedure.md). For what success looks like, see [08-2_bringup_ladder.md](./08-2_bringup_ladder.md).*

# Stage 8.01 — Test Point & Design-for-Test Plan (OMI v1)

## Project
Open Memory Initiative (OMI) — OMI v1 DDR4 UDIMM

## Status
Draft

## Purpose
Define which nets require physical test points on the PCB layout, what measurements each enables, and what probe access geometry is needed. This document feeds directly into Stage 9/10 layout decisions — if test points are not planned now, there will be no room for probe access on the fabricated board.

> **Scope:** This plan covers OMI v1 first-article prototypes only. Production DFT, boundary scan, and automated test interfaces are explicitly out of scope.

---

## 1. DFT Philosophy for OMI v1

OMI v1 is a reference design, not a production module. The primary goal is **debug accessibility**, not signal integrity optimization or production testability.

**What this means in practice:**

- Test points may introduce trace stubs that degrade signal integrity at higher frequencies. This is an acceptable tradeoff for a DDR4-2400 reference design operating well within JEDEC timing margins.
- Test point pads consume PCB area that would otherwise be available for routing. This constrains layout but is necessary for first-article validation.
- Every domain boundary (power, clock, data, configuration) must have at least one observable point. An unobservable failure is an unexplainable failure, and unexplainable failures violate OMI's validation philosophy.

**Why this matters:**

Without test points, the only debug path for a non-functional module is to insert it into a host and interpret cryptic BIOS error codes. Test points allow direct measurement of power rails, clock quality, and signal presence — turning "it doesn't work" into "VDD is 0.8V instead of 1.2V" or "CK has no transitions."

> See [08-5_failure_signatures.md](./08-5_failure_signatures.md) — every failure signature (FS-01 through FS-06) requires probe access to at least one net listed in this plan.

---

## 2. Power Rail Test Points

Power rail observability is the single highest-priority DFT requirement. If rails are wrong, nothing else matters.

| Rail | Net Name | Edge Pin(s) | Board-Level TP? | Why It's Needed | What to Measure | Recommended Pad |
|------|----------|-------------|------------------|-----------------|-----------------|-----------------|
| Core supply | `VDD` | Pin 64 | Yes | Primary DRAM supply; most common root cause of training failures (FS-02) | DC voltage (1.2V ± 5%), ripple under load (< 50 mV pk-pk) | 50 mil round pad |
| I/O supply | `VDDQ` | — (internal) | **Yes (board-level only)** | DRAM I/O driver supply; not present on edge connector; must be probed on-board near DRAM | DC voltage (1.2V ± 5%), ripple during DQ switching | 50 mil round pad |
| Wordline boost | `VPP` | Pin 142 | Yes | DRAM internal wordline voltage; absence prevents DRAM operation entirely | DC voltage (2.5V ± 5%) | 50 mil round pad |
| Ground reference | `GND` | Pin 2 (and many others) | Yes | Scope ground clip attachment point; required for all differential measurements | Ground reference continuity | 100 mil round pad or loop |
| SPD supply | `VDDSPD` | Pin 284 | Yes | SPD EEPROM will not respond without this rail; first thing to check for FS-01 | DC voltage (2.2–3.6V range, host-dependent) | 50 mil round pad |
| Termination | `VTT` | Pin 77, 221 | Nice-to-have | On-die termination reference; absence causes training failure but harder to diagnose | DC voltage (~0.6V, VDD/2) | 20 mil pad |
| Reference | `VREF` | Pin 146 | Nice-to-have | CA bus reference voltage; marginal VREF causes FS-06 | DC voltage (~0.6V, VDDQ/2), noise | 20 mil pad |

**Note on VDDQ:** The JEDEC DDR4 UDIMM connector does not have a dedicated VDDQ pin — VDDQ is generated or distributed on the module itself. The test point must be placed on the PCB trace between the edge connector power input and the DRAM VDDQ balls. This is the only test point in this plan that cannot be probed at the edge connector.

---

## 3. Signal Integrity Test Points — Byte Lane 0

### Why one byte lane is sufficient for v1

All 8 byte lanes (D0–D7) are architecturally identical: same DRAM device type, same trace topology intent, same termination scheme. For a first-article reference design, measuring one representative lane confirms that the design intent is correct. If lane 0 shows clean eye diagrams and correct timing, the other lanes will behave similarly (layout-dependent variations are a Stage 10 concern).

Lane 0 is chosen because:
- It has the lowest pin numbers on the edge connector, making it easiest to locate
- It is typically routed first in layout, making it the most likely to have clean routing
- Failure signature FS-04 (stuck bit) provides a lane-identification formula that starts with lane 0

### Test points for byte lane 0

| Net Name | Edge Pin | Signal Type | What to Measure | Probe Requirements |
|----------|----------|-------------|-----------------|-------------------|
| `D0_DQ0` | Pin 5 | Single-ended data | Eye diagram at DDR4-2400 (833 MHz effective); rise/fall time; voltage swing | High-Z passive probe, ≥ 1 GHz BW; 20 mil pad near DRAM |
| `D0_DQS_t` | Pin 153 | Differential strobe (true) | Differential eye with D0_DQS_c; duty cycle; jitter | Differential probe pair, ≥ 1 GHz BW; paired 20 mil pads |
| `D0_DQS_c` | Pin 152 | Differential strobe (complement) | (Paired with D0_DQS_t above) | (Paired with D0_DQS_t above) |
| `D0_DM_DBI_n` | Pin 7 | Data mask / bus inversion | Verify toggle during writes; confirm not stuck | High-Z passive probe; 20 mil pad |

**Measurement objectives:**
1. **Eye diagram:** Confirm the DQ eye opening meets JEDEC DDR4-2400 minimum (setup/hold time > 55 ps per JESD79-4). This proves the schematic connectivity and basic SI are functional.
2. **DQS-to-DQ timing:** Confirm DQS transitions are centered in the DQ eye. Gross misalignment indicates a connectivity or topology error.
3. **Voltage swing:** Confirm DQ swings between VOL (< 0.2V) and VOH (> 0.8 × VDDQ). Reduced swing indicates termination or driver issues.

> **v2 consideration:** If v1 validation reveals lane-to-lane variation, v2 should add test points on lane 4 (mid-bus) and lane 7 (end-of-bus) for comparison.

---

## 4. Clock Test Points

The differential clock pair is the heartbeat of the DDR4 interface. If CK is absent or degraded, no training or data transfer is possible.

| Net Name | Edge Pin | What to Measure | Probe Requirements |
|----------|----------|-----------------|-------------------|
| `CK_t` | Pin 74 | Differential clock with CK_c; frequency (1200 MHz for DDR4-2400); jitter (< 50 ps pk-pk per JEDEC); duty cycle (47–53%) | Differential probe, ≥ 2 GHz BW; paired 20 mil pads with controlled spacing |
| `CK_c` | Pin 75 | (Paired with CK_t above) | (Paired with CK_t above) |

**Why clock measurements matter:**
- **Jitter:** Excessive clock jitter reduces the timing margin for every DQ bit on every lane. Clock jitter is the single largest contributor to timing margin erosion in DDR4.
- **Duty cycle:** DDR4 uses both rising and falling clock edges. Duty cycle distortion (DCD) asymmetrically reduces setup/hold time on one edge, potentially causing intermittent failures (FS-05).
- **Probe access geometry:** The CK test points must be a closely-spaced differential pair (< 1 mm center-to-center) to minimize common-mode noise pickup during measurement. Consider a 2-pin 0.050" header footprint or SMA-compatible pad pair if board area permits.

> See [08-5_failure_signatures.md](./08-5_failure_signatures.md) FS-02 and FS-06 for clock-related failure diagnostics.

---

## 5. SPD Bus Test Points

The SPD I²C bus is the module's first interaction with any host. If SPD fails, the host cannot identify the module, and all subsequent validation is blocked.

| Net Name | Edge Pin | What to Measure | Probe Requirements |
|----------|----------|-----------------|-------------------|
| `SPD_SCL` | Pin 141 | I²C clock: frequency (~100 kHz standard mode), pull-up voltage level (should reach VDDSPD), waveform quality (clean transitions, no bus contention) | Passive probe, any bandwidth; 50 mil pad |
| `SPD_SDA` | Pin 285 | I²C data: ACK/NACK response from EEPROM, data integrity, bus contention check | Passive probe, any bandwidth; 50 mil pad |

**Why I²C visibility is critical:**
- FS-01 (SPD not detected) is the most common first-power-up failure mode. Without SCL/SDA test points, diagnosing FS-01 requires guessing between 6 possible root causes.
- With test points, a single scope capture shows: (a) whether SCL is toggling (host is trying), (b) whether SDA shows ACK (EEPROM is responding), and (c) whether pull-ups are functional (signals reach VDDSPD level).
- I²C is low-speed (~100 kHz), so test point stubs have zero impact on signal integrity. There is no reason to omit SPD test points.

---

## 6. Address/Command Bus Test Points

The CA bus has 33+ signals. Providing test points for all of them is impractical on a UDIMM form factor. One representative signal is sufficient for v1 to confirm that the CA bus is electrically active during training.

### Selected signal: CS0_n (Chip Select, rank 0)

| Net Name | Edge Pin | What to Measure | Probe Requirements |
|----------|----------|-----------------|-------------------|
| `CS0_n` | Pin 84 | Active-low chip select: confirm host asserts CS0_n during training; verify voltage levels (VOL < 0.2V when active, VOH > 0.8 × VDD when inactive); timing relative to CK | Passive probe, ≥ 500 MHz BW; 20 mil pad |

**Why CS0_n:**
- CS0_n is the most diagnostic single signal on the CA bus. If CS0_n is not asserted, the DRAM device ignores all commands — making it the first signal to check when training fails (FS-02).
- Unlike address bits (which require specific command sequences to observe), CS0_n toggles on every command, making it easy to capture on a scope without triggering complexity.
- FS-02 diagnostic step 5 specifically calls for probing CS0_n (pin 84).

**Secondary CA test point (nice-to-have):** `RESET_n` (pin 58) — confirms the DRAM reset sequence completes. RESET_n should transition from LOW to HIGH during power-up. If it stays LOW, the DRAM never exits reset.

---

## 7. Test Point Summary Table

| Net Name | Edge Pin | Signal Domain | Purpose | Priority | Probe Type |
|----------|----------|---------------|---------|----------|------------|
| `VDD` | 64 | Power | Core supply verification | P1 — Must-have | 50 mil pad |
| `VDDQ` | — (board) | Power | I/O supply verification | P1 — Must-have | 50 mil pad (board-level) |
| `VPP` | 142 | Power | Wordline boost verification | P1 — Must-have | 50 mil pad |
| `GND` | 2 | Power | Scope ground reference | P1 — Must-have | 100 mil pad/loop |
| `VDDSPD` | 284 | Power | SPD supply verification (FS-01) | P1 — Must-have | 50 mil pad |
| `SPD_SCL` | 141 | Configuration | I²C clock observability (FS-01) | P1 — Must-have | 50 mil pad |
| `SPD_SDA` | 285 | Configuration | I²C data observability (FS-01) | P1 — Must-have | 50 mil pad |
| `CK_t` | 74 | Clock | Differential clock true (FS-02/06) | P1 — Must-have | 20 mil differential pair |
| `CK_c` | 75 | Clock | Differential clock complement | P1 — Must-have | 20 mil differential pair |
| `CS0_n` | 84 | Command | Chip select observability (FS-02) | P1 — Must-have | 20 mil pad |
| `D0_DQ0` | 5 | Data | Representative DQ eye diagram | P2 — Needed for L3+ | 20 mil pad |
| `D0_DQS_t` | 153 | Data | Strobe true (differential pair) | P2 — Needed for L3+ | 20 mil differential pair |
| `D0_DQS_c` | 152 | Data | Strobe complement | P2 — Needed for L3+ | 20 mil differential pair |
| `D0_DM_DBI_n` | 7 | Data | Data mask verification | P3 — Nice-to-have | 20 mil pad |
| `VTT` | 77 | Power | Termination rail check | P3 — Nice-to-have | 20 mil pad |
| `VREF` | 146 | Power | Reference voltage check (FS-06) | P3 — Nice-to-have | 20 mil pad |
| `RESET_n` | 58 | Command | Reset sequence verification (FS-02) | P3 — Nice-to-have | 20 mil pad |

**Total test points:** 17 (10 must-have, 3 needed-for-L3+, 4 nice-to-have)

---

## 8. Scope Boundaries — What v1 Does NOT Include

The following DFT features are explicitly **out of scope** for OMI v1:

| Excluded Feature | Why Excluded | When It Might Be Added |
|-----------------|--------------|----------------------|
| JTAG / boundary scan | Requires JTAG TAP controller on module; UDIMMs do not have JTAG infrastructure | Not applicable to UDIMM form factor |
| Production ICT (in-circuit test) pads | Designed for automated factory testing with bed-of-nails fixtures; irrelevant for a reference design | Only if OMI targets volume production |
| BGA-side probing pads | Requires access to the underside of BGA DRAM packages; not feasible without specialized equipment | v2 if flip-chip debug is needed |
| Eye diagram compliance test points | JEDEC-compliant eye measurement requires specific load and probe fixtures defined in JESD79-4 | v2 with proper SI test methodology |
| All-lane DQ test points | 64 DQ bits × 2 (pad + ground) = 128 additional pads; not feasible on UDIMM form factor | v2 if lane-to-lane variation is observed in v1 |
| Thermal sensor test points | DDR4 DRAM devices have internal thermal sensors accessible via MRS commands, not external pins | Use host-side thermal monitoring instead |
| Power sequencing debug headers | Would require multi-pin headers for VPP/VDD/VDDQ sequencing capture | v2 if sequencing issues are observed |

---

## Cross-References

- [08-5_failure_signatures.md](./08-5_failure_signatures.md) — Every failure signature requires probe access to nets in this plan
- [L1_bench_electrical/measurement_procedures.md](./L1_bench_electrical/measurement_procedures.md) — L1 bench procedures reference these test point locations
- [ddr4_udimm_288_pinmap.csv](../../design/connector/ddr4_udimm_288_pinmap.csv) — Authoritative pin-to-net mapping; all pin numbers in this document are sourced from this CSV
- [08-2_bringup_ladder.md](./08-2_bringup_ladder.md) — Test points enable measurements required at each ladder level

---

*This document defines where to probe. For what to measure at each step, see [08_03_bringup_procedure.md](./08_03_bringup_procedure.md). For pass/fail criteria, see [08-2_bringup_ladder.md](./08-2_bringup_ladder.md).*

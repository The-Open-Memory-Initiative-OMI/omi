# Stage 7.5 — Edge Pin Map (Final Reference)

## Project
Open Memory Initiative (OMI) — OMI v1 DDR4 UDIMM

## Status
✅ Frozen (Final)

---

## 1. Primary Source

| Field       | Value |
|-------------|-------|
| Title       | *8GB (x64, SR x8) 288-Pin DDR4 UDIMM* |
| Publisher   | Micron Technology Inc. (Crucial brand) |
| Revision    | CTL0226.fm — Rev. 12/04/15 |
| Table used  | **Table 4: Pin Assignments — 288-Pin DDR4 UDIMM Front/Back** |
| URL         | <https://docs.rs-online.com/6ecf/0900766b81641250.pdf> |

Pin numbers and symbols are taken verbatim from Table 4.
No other pinout source was used. If a conflict arises, Table 4 wins.

---

## 2. Related Files

| Artifact | Path |
|----------|------|
| Net manifest (source of truth) | `docs/07_schematic_capture/stage-7-5-net-manifest.md` |
| Pin map CSV | `design/connector/ddr4_udimm_288_pinmap.csv` |
| Pinout source decision | `docs/07_schematic_capture/stage-7-5-pinout-source-decision.md` |

---

## 3. CSV Column Definitions

| Column    | Meaning |
|-----------|---------|
| `pin`     | Edge contact number (1–288) from Table 4 |
| `symbol`  | Exact symbol string from Table 4 |
| `omi_net` | OMI schematic net name (from net manifest); `NC` if unused |
| `group`   | `POWER`, `CA_CLK`, `DQ_DQS`, `SPD`, `OTHER` |
| `notes`   | Rationale, source annotation, or tie-off decision |

---

## 4. Net Mapping Rules Applied

### Power rails
| Table 4 symbol | `omi_net` |
|---------------|-----------|
| VDD | VDD |
| VSS | GND |
| VPP | VPP |
| VREFCA | VREF |
| VTT | VTT |
| VDDSPD | VDDSPD |

### Data bus (formula)
```
DQn        →  lane = n // 8 ; bit = n % 8  →  D{lane}_DQ{bit}
DQSx_t/c  →  D{x}_DQS_t / D{x}_DQS_c
DMx_n      →  D{x}_DM_DBI_n
```

### CA / CLK
- Multiplexed symbols (e.g., `RAS_n/A16`) — `omi_net` uses the address name (`A16`).
- `CK0_t` / `CK0_c` → `CK_t` / `CK_c` (rank 0 rename).

### SPD
| Symbol | `omi_net` |
|--------|-----------|
| SCL | SPD_SCL |
| SDA | SPD_SDA |
| SA0 / SA1 / SA2 | SA0 / SA1 / SA2 |

---

## 5. Tie-off Policy

| Category | Rule |
|----------|------|
| **NC (no connect)** | `omi_net = NC`; edge pin left unconnected. |
| **NF (not fitted)** | `omi_net = NC`; `notes = "NF in Table 4"`. Only pin 78 (`EVENT_n`) has this designation in Table 4. |
| **Rank-1 unused** | `omi_net = NC`; `notes = "single-rank v1: unused"`. Applies to: `CK1_t`, `CK1_c`, `CS1_n`, `CKE1`, `ODT1`. These edge pins are present in the connector but not driven. |
| **DM/DBI on x64** | DM/DBI pins exist on x64. Mapped to `D{x}_DM_DBI_n`. Whether DBI is enabled is a host/controller configuration choice; OMI v1 maps pins electrically but does not assume DBI enabled. |
| **ECC / CB lane** | Pins `CB0–CB7`, `DQS8_t/c`, `DM8_n/DBI8_n` — all `NC` on this x64 non-ECC module. |
| **A17 (density-dependent)** | `omi_net = NC`; `notes = "density-dependent; NC for 8Gb-class devices"`. A17 is only used for ≥16Gb density DRAMs. Pin 230 is NC in this module's Table 4. Net manifest retains A17 as optional. |

---

## 6. Locked Policies (v1)

| Signal | Status | Policy |
|--------|--------|--------|
| `ALERT_n` (pin 208) | **Routed** — `omi_net = ALERT_n` | Host pull-up assumed; no on-DIMM pull-up required by OMI v1. |
| `PARITY` (pin 222) | **Routed** — `omi_net = PARITY` | OMI v1 does not enable parity; signal wiring preserved for compatibility. |
| `VTT` (pins 77, 221) | **Routed** — `omi_net = VTT` | Rail supplied by host platform. OMI module does not generate VTT. |
| `WP` (SPD EEPROM) | **Not a connector pin** — tied to GND on EEPROM | Remains GND for v1 development. |

---

## 7. Coverage

| Group | Rows |
|-------|------|
| POWER (VDD/VSS/VPP/VREF/VTT/VDDSPD) | 129 |
| DQ\_DQS (DQ0–63, DQS0–7, DM0–7) | 88 |
| CA\_CLK (address, bank, clk, control) | 35 |
| OTHER (NC/NF/ECC/CB/reserved) | 31 |
| SPD (SCL/SDA/SA0–SA2) | 5 |
| **Total connector pins** | **288** |

---

## 8. CSV Integrity Checks (required before Frozen)

| Check | Expected | Actual |
|-------|----------|--------|
| `row_count` | 288 | **288** ✅ |
| `unique(pin)` | 288 | **288** ✅ |
| `pins covered` | {1..288} | **{1..288}** ✅ |
| No duplicate pins | 0 | **0** ✅ |

Integrity verified 2026-02-28. All 288 edge contacts mapped with no gaps or duplicates.

---

*End of Stage 7.5 edge pin map reference.*

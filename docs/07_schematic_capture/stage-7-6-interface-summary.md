# Stage 7.6 — Block Interface Summary (OMI v1)

## Project
Open Memory Initiative (OMI) — OMI v1 DDR4 UDIMM

## Status
Draft (Ready for review)

## Purpose
Stage 7.6 provides a single, authoritative summary of how Stage 7 schematic blocks interface:
- which nets exist
- which sheet owns each net group
- cross-sheet naming/linking rules
- connector mapping authority (Stage 7.5 CSV)

This document is the "glue" between Stage 7 schematic capture and Stage 8 validation/bring-up planning.

---

## 1. Authoritative Sources

The following artifacts are authoritative:

- Net manifest (source of truth):
  - `docs/07_schematic_capture/stage-7-5-net-manifest.md`
- UDIMM edge pin map (source of truth for connector pins):
  - `design/connector/ddr4_udimm_288_pinmap.csv`
- Edge pin map reference:
  - `docs/07_schematic_capture/stage-7-5-edge-pinmap-final.md`

Stage 7.6 does not redefine nets. It summarizes and cross-references.

---

## 2. Sheet Ownership Model

OMI v1 uses "sheet ownership" to keep the design reviewable.

| Sheet | File | Owns |
|-------|------|------|
| Power & PDN | (Stage 7.1 sheet) | power rails, sourcing model, DRAM power pins, VREF policy |
| Address/Command/Clock | `address-command-clock.kicad_sch` | CA/CLK/control connectivity (schematic topology = simplified star) |
| Data (DQ/DQS) | `data-byte-lanes-dqs.kicad_sch` | DQ/DQS lane naming + grouping; host-side anchors; endpoint labeling |
| SPD & Configuration | `spd-and-configuration.kicad_sch` | SPD EEPROM connectivity + assumptions (host pull-ups, WP tied low) |
| UDIMM Edge Interface | `udimm-edge-interface.kicad_sch` (or CSV-only) | connector mapping is authoritative via Stage 7.5 CSV |

Notes:
- Placeholder host connectors are allowed for labeling/anchoring during Stage 7.
- Pin-accurate connector mapping is controlled by the CSV (Stage 7.5).

---

## 3. Cross-Sheet Connectivity Rule

### Rule (OMI v1)
All cross-sheet connectivity uses **global net naming consistency**:
- If two pins on different sheets share the same net name, they are intended to be connected.
- Stage 7.5 CSV is the authority when mapping those nets to edge pins.

### Allowed labeling mechanisms
- Global labels for nets that must exist across sheets (preferred for v1 simplicity)
- No implicit connectivity by proximity
- No duplicate net naming conventions (avoid aliases)

---

## 4. Interface Groups

### 4.1 Power Rails
| Net | Description | Notes |
|-----|-------------|-------|
| VDD | DDR4 core rail | host supplied |
| VDDQ | DDR4 I/O rail | host supplied |
| VPP | wordline boost rail | host supplied |
| VREF | reference rail | maps to VREFCA edge pins; host supplied (Option A) |
| VTT | termination rail | connector-level rail; host supplied |
| VDDSPD | SPD supply rail | connector-level rail; host supplied |
| GND | ground | maps from VSS/VSSQ in symbols |

Policy:
- Option A for VREF is locked (host-provided; DIMM distributes; no local generation).

---

### 4.2 CA / CLK / Control
Topology:
- **Simplified star representation in schematic**
- **Fly-by enforcement deferred to layout constraints** (Stage 8/Stage 10)

Nets (rank 0):
- CK_t, CK_c
- A0..A17 (density-dependent; some may be NC in the chosen module pin table)
- BA0, BA1, BG0, BG1
- ACT_n, CS0_n, CKE0, ODT0, RESET_n
- PARITY, ALERT_n (wired; feature enable is platform/config dependent)

Rank-1 connector pins:
- present in connector mapping, set to NC for single-rank OMI v1

---

### 4.3 DQ / DQS / DM/DBI (x64 non-ECC)
Naming rule (locked):
- Per-DRAM prefix prevents shorts between chips

For lane `i ∈ {0..7}`:
- Di_DQ0..Di_DQ7
- Di_DQS_t, Di_DQS_c
- Di_DM_DBI_n

Notes:
- ECC/CB lane pins are NC in OMI v1 (x64 non-ECC).
- Whether DBI is enabled is a host/controller configuration decision; OMI v1 does not assume DBI enabled.

---

### 4.4 SPD / Configuration
Nets:
- SPD_SCL, SPD_SDA
- SA0, SA1, SA2

Policies (locked for v1):
- Host provides SMBus pull-ups (no on-DIMM pull-ups assumed)
- SPD EEPROM WP is tied low (writes enabled)

---

## 5. Connector Mapping Authority

All mapping from nets → UDIMM edge pins is controlled by:

- `design/connector/ddr4_udimm_288_pinmap.csv`

Rules:
- `symbol` column matches the primary source pin table naming
- `omi_net` maps each pin to an OMI net, NC, or explicit tie-off
- CSV integrity checks must pass (288/288, no duplicates, no missing)

---

## 6. Review Checklist (Stage 7.6)

- [ ] Each net group (POWER, CA_CLK, DQ_DQS, SPD) has a defined owner sheet
- [ ] Cross-sheet naming policy is consistent and documented
- [ ] Connector mapping authority is unambiguous (CSV is the source of truth)
- [ ] Locked decisions referenced (VREF Option A; CA/CLK topology; per-lane DQ naming; SPD WP)
- [ ] Density-dependent pins (e.g., A17) are clearly documented as mapped per Table 4
- [ ] Rank-1 pins policy is explicit (NC for v1)

---

## 7. Next
➡ Stage 7.7 — Stage 7 Closure (final checklist + artifact index + handoff to Stage 8 validation)

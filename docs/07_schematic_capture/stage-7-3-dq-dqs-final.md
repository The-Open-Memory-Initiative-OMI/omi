# Stage 7.3 — Data (DQ/DQS) Byte-Lanes (Final)

## Project
Open Memory Initiative (OMI) — OMI v1 DDR4 UDIMM

## Status
✅ Frozen (Final)

## Scope
Defines data-plane net naming and connectivity for:
- DQ[7:0]
- DQS differential strobe pair
- DM/DBI_n (DDR4 shared function pin)

This stage does NOT include:
- Termination networks
- SI/length matching
- ECC
- SPD/I²C
- Any routing/ordering constraints

---

## Topology Representation
**Simplified star** representation in schematic:
- Connectivity is declared via labels
- Physical routing/topology is enforced at layout/constraints stage

---

## Naming Convention (Locked)

Per-DRAM prefix is used to prevent accidental shorts between devices:

For DRAM index `i ∈ {0..7}`:

- `Di_DQ0` … `Di_DQ7`
- `Di_DQS_t`, `Di_DQS_c`
- `Di_DM_DBI_n`

Mapping intent:
- `D0_*` ↔ `U_DRAM0`
- `D1_*` ↔ `U_DRAM1`
- …
- `D7_*` ↔ `U_DRAM7`

---

## Implementation Summary

### Host-side anchoring
Host-side placeholder connectors are used only to anchor labels (not pin-accurate UDIMM mapping).

- One or more host placeholder connectors (e.g., `J_HOST_DQ`, or `J_HOST_DQ_A/B/C`) provide enough pins to anchor all nets.
- All data nets are implemented as **Global Labels** to allow cross-sheet visibility.

### DRAM endpoints
Each DRAM `U_DRAM0..U_DRAM7` has:
- `DQ0..DQ7` labeled with `Di_DQ0..Di_DQ7`
- `DQS_t/DQS_c` labeled with `Di_DQS_t/Di_DQS_c`
- DM/DBI pin labeled with `Di_DM_DBI_n`

No data signals are shared across DRAMs.

---

## Verification
- ERC: no duplicate references
- Collision checks performed on representative nets:
  - `D0_DQ0`, `D3_DQS_t`, `D7_DM_DBI_n`
  ensuring each net appears only on the correct host anchor and the corresponding DRAM

---

## Artifacts
- `omi_v1_stage7_3_dq_dqs_host_final.pdf`
- `omi_v1_stage7_3_dq_dqs_endpoints_final.pdf`

---

## Next
➡ Stage 7.4 — SPD & Configuration (I²C/SA) sheet setup and net naming (no firmware behavior assumptions yet)

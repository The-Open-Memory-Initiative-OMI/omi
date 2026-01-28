# Stage 7.2 — Address / Command / Clock (Final)

## Project
Open Memory Initiative (OMI) — OMI v1 DDR4 UDIMM

## Status
✅ Frozen (Final)

## Topology (Locked)
**Simplified star representation in schematic.**  
JEDEC fly-by behavior is deferred to layout/SI constraints.

## Scope
This stage defines CA/CLK/control connectivity only:
- CK_t/CK_c
- A0..A17
- BA0/BA1, BG0/BG1
- ACT_n
- CS0_n
- CKE0
- ODT0
- RESET_n

No DQ/DQS, SPD, or termination networks are included here.

## Implementation Summary
- `address-command-clock.kicad_sch` created and populated
- Host CA/CLK source represented by placeholder connector `J_HOST` (Conn_01x40)
- DRAM devices U_DRAM0..U_DRAM7 present exactly once in the project (no duplicated components)
- CA/CLK nets are consistently named and replicated across all DRAMs
- Stage 7.1 remains rails/entry only; DRAM placement moved to avoid duplication

## Verification
- ERC: no duplicate references
- Representative hover checks: CK_t, RESET_n, A0 consistent across DRAMs
- Power nets preserved: VDD, VDDQ, VPP, VREF, GND

## Artifacts
- `omi_v1_ca_clk_stage7_2_final.pdf`

## Next
➡ Stage 7.3 — Data (DQ/DQS) sheet creation and net naming (no routing, no SI tuning)

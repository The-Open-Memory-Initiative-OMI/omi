# Stage 7.2 — CA/CLK Checkpoint 01

## Status
Checkpoint (not final)

## Completed
- Stage 7.2 topology decision locked: simplified star (schematic)
- Stage 7.2 sheet created: `address-command-clock.kicad_sch`
- Host placeholder `J_HOST` resized to `Conn_01x40` to anchor CA/CLK nets
- DRAM symbols moved off the Stage 7.1 power page to avoid duplicate components
- Stage 7.1 page now acts as rails/entry only (power-only intent preserved)
- CA/CLK net naming applied: CK_t/CK_c, RESET_n, CS0_n, CKE0, ACT_n, ODT0, BA0/BA1, BG0/BG1, A0..A17
- Power nets preserved after refactor: VDD, VDDQ, VPP, VREF, GND

## Verification
- ERC: no duplicate references (expected unconnected signal warnings remain)
- Spot-checked nets: VDD/VDDQ/VPP/VREF/GND and representative CA signals

## Next
- Ensure CA/CLK labels are replicated across U_DRAM0..U_DRAM7 (if not already)
- Freeze a "Stage 7.2 Final" after replication is complete
- Proceed to Stage 7.3 (Data DQ/DQS) only after Stage 7.2 is frozen

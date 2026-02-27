# Stage 7.5 — Net Manifest (Source of Truth)

## Project
Open Memory Initiative (OMI) — OMI v1 DDR4 UDIMM

## Purpose
This manifest lists every named net defined across Stages 7.1–7.4.
It is the authoritative reference for edge-pin mapping in Stage 7.5.

---

## 1. Power Rails
*(Stages 7.1 + 7.4)*

| Net      | Description                                      |
|----------|--------------------------------------------------|
| `VDD`    | Core supply (1.2 V nominal, DDR4)                |
| `VDDQ`   | I/O supply (DDR4 interface I/O rail)             |
| `VPP`    | DRAM activating power supply (2.5 V)             |
| `VREF`   | Reference voltage (maps to VREFCA pins)          |
| `VDDSPD` | SPD EEPROM supply (2.5 V nominal on DDR4 UDIMMs) |
| `GND`    | Ground                                           |

---

## 2. CA / CLK Bus
*(Stage 7.2)*

| Net       | Description                     |
|-----------|---------------------------------|
| `CK_t`    | Differential clock — true       |
| `CK_c`    | Differential clock — complement |
| `A0`      | Address bit 0                   |
| `A1`      | Address bit 1                   |
| `A2`      | Address bit 2                   |
| `A3`      | Address bit 3                   |
| `A4`      | Address bit 4                   |
| `A5`      | Address bit 5                   |
| `A6`      | Address bit 6                   |
| `A7`      | Address bit 7                   |
| `A8`      | Address bit 8                   |
| `A9`      | Address bit 9                   |
| `A10`     | Address bit 10                  |
| `A11`     | Address bit 11                  |
| `A12`     | Address bit 12                  |
| `A13`     | Address bit 13                  |
| `A14`     | Address bit 14                  |
| `A15`     | Address bit 15                  |
| `A16`     | Address bit 16                  |
| `A17`     | Address bit 17                  |
| `BA0`     | Bank address 0                  |
| `BA1`     | Bank address 1                  |
| `BG0`     | Bank group 0                    |
| `BG1`     | Bank group 1                    |
| `ACT_n`   | Activate command (active low)   |
| `CS0_n`   | Chip select 0 (active low)      |
| `CKE0`    | Clock enable 0                  |
| `ODT0`    | On-die termination 0            |
| `RESET_n` | DRAM reset (active low)         |
| `PAR`     | Command/address parity input (optional/system-dependent) |
| `ALERT_n` | Alert output — CRC/parity error or other events (optional/system-dependent) |

---

## 3. DQ / DQS Bus
*(Stage 7.3)*

### Byte Lane 0 — D0
| Net           | Description                        |
|---------------|------------------------------------|
| `D0_DQ0`      | Data bit 0                         |
| `D0_DQ1`      | Data bit 1                         |
| `D0_DQ2`      | Data bit 2                         |
| `D0_DQ3`      | Data bit 3                         |
| `D0_DQ4`      | Data bit 4                         |
| `D0_DQ5`      | Data bit 5                         |
| `D0_DQ6`      | Data bit 6                         |
| `D0_DQ7`      | Data bit 7                         |
| `D0_DQS_t`    | Data strobe — true                 |
| `D0_DQS_c`    | Data strobe — complement           |
| `D0_DM_DBI_n` | Data mask / data bus inversion     |

### Byte Lane 1 — D1
| Net           | Description                        |
|---------------|------------------------------------|
| `D1_DQ0`–`D1_DQ7`   | Data bits 0–7                |
| `D1_DQS_t`    | Data strobe — true                 |
| `D1_DQS_c`    | Data strobe — complement           |
| `D1_DM_DBI_n` | Data mask / data bus inversion     |

### Byte Lane 2 — D2
| Net           | Description                        |
|---------------|------------------------------------|
| `D2_DQ0`–`D2_DQ7`   | Data bits 0–7                |
| `D2_DQS_t`    | Data strobe — true                 |
| `D2_DQS_c`    | Data strobe — complement           |
| `D2_DM_DBI_n` | Data mask / data bus inversion     |

### Byte Lane 3 — D3
| Net           | Description                        |
|---------------|------------------------------------|
| `D3_DQ0`–`D3_DQ7`   | Data bits 0–7                |
| `D3_DQS_t`    | Data strobe — true                 |
| `D3_DQS_c`    | Data strobe — complement           |
| `D3_DM_DBI_n` | Data mask / data bus inversion     |

### Byte Lane 4 — D4
| Net           | Description                        |
|---------------|------------------------------------|
| `D4_DQ0`–`D4_DQ7`   | Data bits 0–7                |
| `D4_DQS_t`    | Data strobe — true                 |
| `D4_DQS_c`    | Data strobe — complement           |
| `D4_DM_DBI_n` | Data mask / data bus inversion     |

### Byte Lane 5 — D5
| Net           | Description                        |
|---------------|------------------------------------|
| `D5_DQ0`–`D5_DQ7`   | Data bits 0–7                |
| `D5_DQS_t`    | Data strobe — true                 |
| `D5_DQS_c`    | Data strobe — complement           |
| `D5_DM_DBI_n` | Data mask / data bus inversion     |

### Byte Lane 6 — D6
| Net           | Description                        |
|---------------|------------------------------------|
| `D6_DQ0`–`D6_DQ7`   | Data bits 0–7                |
| `D6_DQS_t`    | Data strobe — true                 |
| `D6_DQS_c`    | Data strobe — complement           |
| `D6_DM_DBI_n` | Data mask / data bus inversion     |

### Byte Lane 7 — D7
| Net           | Description                        |
|---------------|------------------------------------|
| `D7_DQ0`–`D7_DQ7`   | Data bits 0–7                |
| `D7_DQS_t`    | Data strobe — true                 |
| `D7_DQS_c`    | Data strobe — complement           |
| `D7_DM_DBI_n` | Data mask / data bus inversion     |

---

## 4. SPD / Configuration Bus
*(Stage 7.4)*

| Net       | Description                                              |
|-----------|----------------------------------------------------------|
| `SPD_SCL` | SMBus/I²C clock (pull-ups on host side)                  |
| `SPD_SDA` | SMBus/I²C data (pull-ups on host side)                   |
| `SA0`     | SPD address strap 0 (host-controlled)                    |
| `SA1`     | SPD address strap 1 (host-controlled)                    |
| `SA2`     | SPD address strap 2 (host-controlled)                    |

> **Note:** `WP` is tied to `GND` (writes enabled for OMI v1). No dedicated WP net is needed.

---

## 5. Connector-Level Nets — Present on Edge, Unused in OMI v1

These signals exist in the DDR4 UDIMM pin table and must be mapped at the edge connector (as NC or tied per spec). They are not driven in OMI v1's single-rank design.

| Net     | Description                                    |
|---------|------------------------------------------------|
| `CKE1`  | Clock enable — rank 1 (unused in v1)           |
| `ODT1`  | On-die termination — rank 1 (unused in v1)     |
| `CS1_n` | Chip select — rank 1 (unused in v1, if present in chosen pin table) |

---

## Summary Count

| Group                        | Net Count                   |
|------------------------------|-----------------------------|
| Power rails                  | 6                           |
| CA / CLK bus                 | 31 (incl. `PAR`, `ALERT_n`) |
| DQ / DQS bus                 | 88 (11 × 8 lanes)           |
| SPD bus                      | 5                           |
| Connector-present / unused   | 3                           |
| **Total**                    | **133**                     |

---

*This manifest is the input to Stage 7.5 edge-pin mapping.*

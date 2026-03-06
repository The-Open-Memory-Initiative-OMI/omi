# L0 Naming Rules — OMI v1 DDR4 UDIMM

## Purpose

This document defines the exact naming conventions and regular expression patterns
used to validate net names across the OMI v1 schematic artifacts.
These rules are enforced by the automated L0 verification scripts
(`verify_pinmap.py`, `verify_naming.py`).

All patterns use Python `re` module syntax.

---

## 1. Data Bus — DQ Nets

**Convention:** `D{lane}_DQ{bit}`

| Field | Range | Description |
|-------|-------|-------------|
| `lane` | 0–7 | Byte lane index (maps to DRAM U1–U8) |
| `bit` | 0–7 | Per-device DQ bit index (local numbering) |

**Regex:** `^D[0-7]_DQ[0-7]$`

**Examples:** `D0_DQ0`, `D3_DQ7`, `D7_DQ4`

**Count:** 64 nets total (8 lanes x 8 bits)

---

## 2. Data Strobe — DQS Nets

**Convention:** `D{lane}_DQS_{polarity}`

| Field | Values | Description |
|-------|--------|-------------|
| `lane` | 0–7 | Byte lane index |
| `polarity` | `t`, `c` | True or complement (differential pair) |

**Regex:** `^D[0-7]_DQS_[tc]$`

**Examples:** `D0_DQS_t`, `D0_DQS_c`, `D5_DQS_t`

**Count:** 16 nets total (8 lanes x 2 polarities)

---

## 3. Data Mask / DBI — DM Nets

**Convention:** `D{lane}_DM_DBI_n`

| Field | Range | Description |
|-------|-------|-------------|
| `lane` | 0–7 | Byte lane index |

**Regex:** `^D[0-7]_DM_DBI_n$`

**Examples:** `D0_DM_DBI_n`, `D7_DM_DBI_n`

**Count:** 8 nets total (1 per lane)

---

## 4. Byte Lane Summary

Each byte lane (D0–D7) contains exactly **11 nets:**

| Net Type | Count | Pattern |
|----------|-------|---------|
| DQ data | 8 | `D{N}_DQ0` through `D{N}_DQ7` |
| DQS strobe | 2 | `D{N}_DQS_t`, `D{N}_DQS_c` |
| DM/DBI | 1 | `D{N}_DM_DBI_n` |
| **Total per lane** | **11** | |
| **Total all lanes** | **88** | 8 lanes x 11 nets |

### Lane-to-DRAM Mapping

| Lane | Prefix | DRAM Device | JEDEC DQ Range |
|------|--------|-------------|----------------|
| 0 | `D0_` | U1 | DQ[0:7] |
| 1 | `D1_` | U2 | DQ[8:15] |
| 2 | `D2_` | U3 | DQ[16:23] |
| 3 | `D3_` | U4 | DQ[24:31] |
| 4 | `D4_` | U5 | DQ[32:39] |
| 5 | `D5_` | U6 | DQ[40:47] |
| 6 | `D6_` | U7 | DQ[48:55] |
| 7 | `D7_` | U8 | DQ[56:63] |

**Isolation rule:** A net prefixed `D{N}_` must connect exclusively to DRAM U{N+1}
and the edge connector. No cross-lane connections are permitted.

---

## 5. Command/Address Bus — CA Nets

### Address Nets

**Regex:** `^A(0|[1-9]|1[0-7])$`

**Valid nets:** `A0` through `A17`

> Note: `A17` is listed in the net manifest but mapped to `NC` on the edge connector
> for 8Gb-class DRAM devices (pin 230 in the CSV).

### Bank / Bank Group Nets

**Regex:** `^B(A[01]|G[01])$`

**Valid nets:** `BA0`, `BA1`, `BG0`, `BG1`

### Control Nets

These are enumerated explicitly (no pattern — fixed set):

| Net | Description |
|-----|-------------|
| `ACT_n` | Activate command (active low) |
| `CS0_n` | Chip select rank 0 (active low) |
| `CKE0` | Clock enable rank 0 |
| `ODT0` | On-die termination rank 0 |
| `RESET_n` | DRAM reset (active low) |
| `ALERT_n` | Alert output (host pull-up assumed) |
| `PARITY` | Command/address parity |

### Clock Nets

**Regex:** `^CK_[tc]$`

**Valid nets:** `CK_t` (true), `CK_c` (complement)

---

## 6. SPD / Configuration Bus

These are enumerated explicitly:

| Net | Description |
|-----|-------------|
| `SPD_SDA` | SMBus/I2C data line |
| `SPD_SCL` | SMBus/I2C clock line |
| `SA0` | SPD address strap 0 |
| `SA1` | SPD address strap 1 |
| `SA2` | SPD address strap 2 |

---

## 7. Power Nets

These are enumerated explicitly:

| Net | Description |
|-----|-------------|
| `VDD` | Core supply (1.2 V) |
| `VDDQ` | I/O supply |
| `VPP` | DRAM activating supply (2.5 V) |
| `VREF` | Reference voltage (maps to VREFCA) |
| `VDDSPD` | SPD EEPROM supply (2.2–3.6 V) |
| `VTT` | Termination rail (host-supplied) |
| `GND` | Ground |

**Isolation rule:** No two power domains may share the same edge connector pin.
Each power net must be independently routable.

> Note: `VDDQ` is defined in the net manifest but does not appear on the
> 288-pin edge connector (it is an internal DIMM rail). This is expected behavior,
> not a validation failure.

---

## 8. No Connect Convention

**Value:** `NC`

All pins that are unused, reserved, or not applicable to the OMI v1 configuration
(8 GB, 1R, x8, non-ECC) are mapped with `omi_net = NC`.

This includes:
- ECC/CB lane pins (CB0–CB7, DQS8, DM8/DBI8)
- Unused rank-1 signals (CS1_n, ODT1, CKE1, CK1_t, CK1_c)
- JEDEC-reserved NC pins
- EVENT_n (NF in Table 4)
- Density-dependent pins (A17 for 8Gb-class)

---

## 9. Edge Connector Pin Groups

The `group` column in `ddr4_udimm_288_pinmap.csv` classifies each pin:

| Group | Description | Allowed `omi_net` Values |
|-------|-------------|--------------------------|
| `DQ_DQS` | Data bus signals | `D[0-7]_DQ[0-7]`, `D[0-7]_DQS_[tc]`, `D[0-7]_DM_DBI_n` |
| `CA_CLK` | Command/Address/Clock | CA set (A0–A16, BA*, BG*, control, clock) or `NC` |
| `POWER` | Power and ground | `VDD`, `VPP`, `VREF`, `VDDSPD`, `VTT`, `GND` |
| `SPD` | SPD configuration | `SPD_SDA`, `SPD_SCL`, `SA0`, `SA1`, `SA2` |
| `OTHER` | NC / reserved | `NC` |

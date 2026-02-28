# Stage 8.4 — Validation Report Template (OMI v1)

## Purpose
Standardized reporting format for all OMI v1 validation contributions.
Every test result submitted to the project must use this format.

> Fill all required fields. Leave no field blank — write `N/A` or `not tested` explicitly.
> Do not omit failures. Incomplete reports will not be merged.

---

## Run ID

```
RUN-<YYYYMMDD>-<PLATFORM_SHORT>-<LEVEL>-<SEQUENCE>
```

**Example:** `RUN-20260228-Z690-L3-001`

| Field | Format | Example |
|-------|--------|---------|
| Date | YYYYMMDD | 20260228 |
| Platform short name | Board abbreviation, no spaces | Z690, AM5-B650, VCU118 |
| Level | L0 / L1 / L2 / L3 / L4 | L3 |
| Sequence | 3-digit serial (001, 002, …) for same platform+level | 001 |

Include the Run ID in the filename: `RUN-20260228-Z690-L3-001.md`

---

## 1. Platform & Environment

```markdown
| Field               | Value |
|---------------------|-------|
| Board manufacturer  |       |
| Board model         |       |
| Chipset             |       |
| BIOS / firmware ver |       |
| BIOS date           |       |
| DDR4 slot used      |       |
| Other DIMMs present | Yes / No — describe if Yes |
| OS (if applicable)  |       |
| OS version          |       |
| Ambient temperature |       |
| Test date           |       |
| Tester              |       |
```

---

## 2. Module Under Test

```markdown
| Field               | Value |
|---------------------|-------|
| OMI module version  | OMI v1 DDR4 UDIMM |
| PCB revision        |       |
| BOM variant         |       |
| Serial / ID         |       |
| Notes               |       |
```

---

## 3. Test Level & Category

```markdown
| Field          | Value |
|----------------|-------|
| Ladder level   | L0 / L1 / L2 / L3 / L4 |
| Test category  | T1 / T2 / T3 / T4 / T5 / T6 / T7 (see 08-3_test_matrix.md) |
| Tools used     |       |
| Tool versions  |       |
```

---

## 4. Procedure (Step-by-Step)

> List the exact steps taken in order. Be specific enough that another engineer can reproduce the result.

```markdown
1. [Step description]
2. [Step description]
3. [Step description]
...
```

**Example (L2 SPD read on Linux):**
```markdown
1. Inserted OMI v1 module into DIMM slot A2 on the test board (all other slots empty).
2. Powered on — waited for BIOS POST to complete.
3. Booted Ubuntu 22.04 from USB.
4. Installed `i2c-tools`: `sudo apt install i2c-tools`
5. Ran `sudo i2cdetect -l` to identify SMBus bus.
6. Ran `sudo i2cdump -y 0x5X 0x50` to dump SPD EEPROM.
7. Ran `decode-dimms` and captured output.
8. Compared key SPD bytes against expected values per datasheet.
```

---

## 5. Results

```markdown
| Check | Expected | Actual | Pass / Fail |
|-------|----------|--------|-------------|
|       |          |        |             |
|       |          |        |             |
```

**Overall result:** `PASS` / `FAIL` / `PARTIAL`

> PARTIAL is only allowed with an explicit list of which items passed and which failed.
> Do not use PARTIAL to avoid reporting failures.

---

## 6. Artifact Checklist

Check every applicable artifact. Attach or link each one.

```markdown
- [ ] SPD raw hex dump (256 bytes) — filename: `spd_dump_<RunID>.txt`
- [ ] SPD tool output screenshot — filename: `spd_tool_<RunID>.png`
- [ ] BIOS POST screenshot / log — filename: `bios_post_<RunID>.png`
- [ ] OS memory report screenshot — filename: `os_memory_<RunID>.png`
- [ ] memtest result screenshot — filename: `memtest_<RunID>.png`
- [ ] Continuity / DVM measurement log — filename: `continuity_<RunID>.txt`
- [ ] Stress tool log — filename: `stress_<RunID>.txt`
- [ ] Temperature log (if T7) — filename: `temp_<RunID>.txt`
- [ ] Other (describe): _______________
```

> All files named with the Run ID. Store in `validation/results/<RunID>/`.

---

## 7. Failure Notes

> Complete this section for every failure or anomaly — even if overall result is PASS.
> An empty failure section is only valid if every check was explicitly confirmed passing.

```markdown
### Failure / Anomaly <N>

- **Run ID:** 
- **Test step:** (step number from Section 4)
- **Category:** DETERMINISTIC / INTERMITTENT / ENVIRONMENT
- **Symptom:** (exact observed behavior)
- **Expected behavior:** 
- **Reproduction:** (did it repeat? how many times out of how many attempts?)
- **Suspected root cause:** 
- **Debug steps taken:** 
- **Issue opened:** (link to GitHub issue or `None — waived because:`)
```

> Waivers require justification. "It worked the second time" is not a waiver justification.

---

## 8. Sign-Off

```markdown
| Field       | Value |
|-------------|-------|
| Reported by |       |
| Date        |       |
| Run ID      |       |
| Result      | PASS / FAIL / PARTIAL |
| Linked PR / issue | |
```

---

## Naming & Storage Conventions

| Item | Convention |
|------|-----------|
| Report file | `validation/results/<RunID>/<RunID>.md` |
| Artifacts dir | `validation/results/<RunID>/` |
| Issue label (fail) | `validation-fail`, `L<n>-FAIL`, `DETERMINISTIC-FAIL` or `INTERMITTENT-FAIL` |
| PR title | `validation: <RunID> — <platform> — <level> — <PASS/FAIL>` |

---

*See also: `08-2_bringup_ladder.md` (level definitions), `08-3_test_matrix.md` (test categories and durations).*

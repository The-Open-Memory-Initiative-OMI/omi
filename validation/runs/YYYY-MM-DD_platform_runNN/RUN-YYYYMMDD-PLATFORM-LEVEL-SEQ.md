# Validation Run Report

> Copy this from `docs/08_validation_and_review/08-4_reporting_template.md`
> Rename file to: `RUN-YYYYMMDD-PLATFORM-LEVEL-SEQ.md`

---

## Run ID

`RUN-YYYYMMDD-PLATFORM-LEVEL-001`

---

## 1. Platform & Environment

| Field               | Value |
|---------------------|-------|
| Board manufacturer  |       |
| Board model         |       |
| Chipset             |       |
| BIOS / firmware ver |       |
| BIOS date           |       |
| DDR4 slot used      |       |
| Other DIMMs present |       |
| OS (if applicable)  |       |
| OS version          |       |
| Ambient temperature |       |
| Test date           |       |
| Tester              |       |

---

## 2. Module Under Test

| Field               | Value |
|---------------------|-------|
| OMI module version  | OMI v1 DDR4 UDIMM |
| PCB revision        |       |
| BOM variant         |       |
| Serial / ID         |       |
| Notes               |       |

---

## 3. Test Level & Category

| Field          | Value |
|----------------|-------|
| Ladder level   |       |
| Test category  |       |
| Tools used     |       |
| Tool versions  |       |

---

## 4. Procedure

1. 
2. 
3. 

---

## 5. Results

| Check | Expected | Actual | Pass / Fail |
|-------|----------|--------|-------------|
|       |          |        |             |

**Overall result:** `PASS` / `FAIL` / `PARTIAL`

---

## 6. Artifact Checklist

- [ ] SPD raw hex dump — `spd_dump_<RunID>.txt`
- [ ] SPD tool output screenshot — `spd_tool_<RunID>.png`
- [ ] BIOS POST screenshot — `bios_post_<RunID>.png`
- [ ] OS memory report — `os_memory_<RunID>.png`
- [ ] memtest result — `memtest_<RunID>.png`
- [ ] Continuity log — `continuity_<RunID>.txt`
- [ ] Stress log — `stress_<RunID>.txt`
- [ ] Other:

---

## 7. Failure Notes

_(none — or describe each failure using the format in 08-4_reporting_template.md)_

---

## 8. Sign-Off

| Field       | Value |
|-------------|-------|
| Reported by |       |
| Date        |       |
| Run ID      |       |
| Result      |       |
| Linked PR / issue |  |

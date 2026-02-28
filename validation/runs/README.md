# Validation Runs

This folder contains all OMI v1 validation run artifacts.

## Folder naming convention

```
YYYY-MM-DD_<platform>_run<NN>/
```

| Field | Format | Example |
|-------|--------|---------|
| Date | YYYY-MM-DD | 2026-03-15 |
| Platform | Short board name, underscores only | z690_msi, am5_b650, fpga_vcu118 |
| Run number | run + 2-digit serial per platform per day | run01, run02 |

**Example folder:** `2026-03-15_z690_msi_run01/`

---

## Minimum folder contents per run

```
<run_folder>/
  <RunID>.md          ← Completed report (from 08-4_reporting_template.md)
  spd_dump_<RunID>.txt
  bios_post_<RunID>.png
  os_memory_<RunID>.png
  memtest_<RunID>.png
  [additional artifacts as applicable]
```

All artifact filenames must include the Run ID (see `08-4_reporting_template.md` for the Run ID format).

---

## Run ID ↔ folder mapping

The Run ID used in the report (`RUN-YYYYMMDD-PLATFORM-LEVEL-SEQ`) maps to the folder name:

| Run ID | Folder |
|--------|--------|
| `RUN-20260315-Z690MSI-L3-001` | `2026-03-15_z690_msi_run01/` |

---

## Submitting a run

1. Create a folder using the naming convention above.
2. Fill out the report template (`docs/08_validation_and_review/08-4_reporting_template.md`).
3. Place the completed report and all artifacts in the folder.
4. Open a PR with title: `validation: <RunID> — <platform> — <level> — <PASS/FAIL>`
5. If any check failed, open a separate issue labeled `validation-fail` and link it in the report.

---

## Index of completed runs

| Run ID | Date | Platform | Level | Result |
|--------|------|----------|-------|--------|
| _(none yet)_ | — | — | — | — |

Update this table when a run is merged.

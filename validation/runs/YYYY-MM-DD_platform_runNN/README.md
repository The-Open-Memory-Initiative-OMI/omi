# Example Run Folder

This folder shows the required structure for a validation run submission.

**Rename this folder** to match the naming convention before submitting:
```
YYYY-MM-DD_<platform>_run<NN>/
```

**Rename the report file** to match the Run ID:
```
RUN-YYYYMMDD-PLATFORM-LEVEL-SEQ.md
```

## Required contents for this folder

```
RUN-<RunID>.md                ← Completed report (mandatory)
spd_dump_<RunID>.txt          ← 256-byte SPD hex dump (L2+)
bios_post_<RunID>.png         ← BIOS POST screenshot (L2+)
os_memory_<RunID>.png         ← OS memory report screenshot (L3+)
memtest_<RunID>.png           ← memtest86+ result screenshot (L4)
[additional artifacts]
```

Delete this README.md when you populate the folder with real artifacts.

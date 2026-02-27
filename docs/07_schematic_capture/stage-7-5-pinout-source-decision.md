# Stage 7.5 — Pinout Source Decision (UDIMM Edge Mapping)

## Status
Locked

## Date
2026-02-27

## Primary Source (Authoritative pin assignments)
- Title: **8GB (x64, SR x8) 288-Pin DDR4 UDIMM** (Micron Technology Inc.)
- Revision: CTL0226.fm — Rev. 12/04/15
- Why this source: Contains **Table 4: Pin Assignments** for **288-Pin DDR4 UDIMM Front/Back**, used as the authoritative mapping table.

Primary PDF:
https://docs.rs-online.com/6ecf/0900766b81641250.pdf

## What is authoritative from the Primary Source
- Edge contact pin numbers and their **Pin Symbol** naming (Table 4).
- Presence of connector-level rails/signals such as **VTT**, **VDDSPD**, **EVENT_n**, **PARITY**, **ALERT_n**, etc., as listed in Table 4.

## Notes (mechanical reference)
The primary source references the UDIMM outline **MO-309** (Figure 1), and is used as the public mechanical compatibility anchor for OMI v1.

## Conflict Policy
- If a pin symbol name differs from OMI internal net naming:
  - **Pin map CSV uses the Primary Source symbol name**
  - `omi_net` field maps to the closest OMI net (no silent renaming)
- If additional connector-level pins exist but OMI v1 does not use them:
  - They are still mapped in CSV as `NC` or explicit tie-off (with notes).

Why this doc matters: it prevents "random pinout images" or mixed sources from creeping in later.

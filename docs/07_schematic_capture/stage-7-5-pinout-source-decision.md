# Stage 7.5 — Pinout Source Decision (UDIMM Edge Mapping)

## Status
Locked

## Primary Source (Authoritative Pin Symbols + Pin Numbers)
- **Document:** Micron — *8GB (×64, SR ×8) 288-Pin DDR4 UDIMM* Core Data Sheet
- **Table:** "Table 4: Pin Assignments — 288-Pin DDR4 UDIMM Front/Back"
- **URL:** <https://docs.rs-online.com/6ecf/0900766b81641250.pdf>
- **Why:** This is the authoritative Micron UDIMM core datasheet containing the pin-symbol-to-pin-number mapping used to assign every edge contact to an OMI net.

## Secondary Source (Electrical Rail Sanity Checks)
- **Document:** Micron — *8GB (×64, Single Rank ×8) 288-Pin DDR4 UDIMM* Module Data Sheet
- **Part number:** MTA16ATF1G64AZ
- **URL:** <https://media.digikey.com/pdf/Data%20Sheets/Micron%20Technology%20Inc%20PDFs/MTA16ATF1G64AZ.pdf>
- **Used for:** Confirming nominal rail voltages (VDD = 1.2 V, VPP = 2.5 V, VDDSPD = 2.5 V) and validating power-rail descriptions in the OMI net manifest.

## Mechanical Reference (Form Factor Compatibility)
- **Document:** Amphenol CS — *DDR4 Memory Module Socket (SSIO Series)* Data Sheet
- **Product spec:** GS-12-1092; JEDEC MO-309 compliant; 288-pin, 0.85 mm pitch
- **URL:** <https://cdn.amphenol-cs.com/media/wysiwyg/files/documentation/datasheet/ssio/ssio_ddr4.pdf>
- **Used for:** Confirming 288-pin edge-connector mechanical compatibility (pin pitch, seating plane, module outline) for OMI v1 PCB design assumptions.

## Conflict Policy
- If pin symbol/name differs: follow Primary Source.
- If voltage/rail nominal differs: use Secondary Source to annotate OMI docs (do not rename nets).

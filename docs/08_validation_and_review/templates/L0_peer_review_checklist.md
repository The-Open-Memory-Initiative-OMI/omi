# L0 Peer Review & Adversarial Sign-off Checklist

**Reviewing Engineer:** [Name / Handle]
**Reviewing Target Commit:** [Git SHA]
**L0 Report Under Review:** [link to PR or report file]
**Review Date:** YYYY-MM-DD

---

## Artifact Reproducibility Verification

- [ ] **State Replication:** I cloned the repository and checked out the exact
      commit hash specified in the L0 report.

- [ ] **ERC Verification:** I executed the ERC in my local EDA environment and
      achieved the identical 0 Errors result shown in the submitter's report.

- [ ] **Pin Map Script Verification:** I ran `verify_pinmap.py` locally and
      independently confirm the 288/288 pass result. My output matches the
      submitter's `pinmap_report.json`.

- [ ] **Naming Script Verification:** I ran `verify_naming.py` locally and
      independently confirm byte-lane isolation. My output matches the
      submitter's `naming_report.json`.

- [ ] **Hash Verification:** I computed SHA-256 hashes of the input CSV and
      they match the hashes reported in the L0 evidence package.

- [ ] **Waiver Audit:** I reviewed the waivers listed in the L0 report.
      The engineering justifications are electrically sound for a DDR4 UDIMM
      1R x8 non-ECC architecture.

---

## Visual & Logical Sanity Audit

- [ ] **Lane Isolation:** I used the EDA tool's net highlighting feature on at
      least one random DQ net per byte lane. I confirmed isolation to a single
      DRAM component with no cross-talk to other chips.

- [ ] **Power Sanity:** I confirmed that VDD, VPP, and VREF are properly
      distributed to all required logic components, including the SPD EEPROM
      (via VDDSPD).

- [ ] **NC Pin Audit:** I spot-checked that rank-1 signals (CS1_n, ODT1, CKE1,
      CK1_t, CK1_c) and ECC lanes (CB0-CB7, DQS8, DM8) are mapped to NC.

- [ ] **SPD Supply Isolation:** I verified that VDDSPD is wired as a distinct
      net and not aliased to VDD or VDDQ.

---

## Final Determination

**Review Result:** PASS / FAIL / NEEDS REVISION

**Comments / Findings:**

> [Provide detailed findings here. If FAIL or NEEDS REVISION, list specific
> items that must be corrected before L0 can be approved.]

---

**Signed:** [Reviewer Name / Handle]
**Date:** YYYY-MM-DD

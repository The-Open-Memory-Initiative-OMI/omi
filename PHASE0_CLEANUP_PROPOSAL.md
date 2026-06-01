# Phase 0 — Documentation & License Hygiene: Cleanup Proposal

**Branch:** `phase0-doc-hygiene`
**Status:** Proposed (for review via PR; `main` untouched, nothing merged)
**Scope owner:** Phase 0 only — documentation/governance/license hygiene. No engineering
artifacts, no status/claims language, no rename/rebrand. Those belong to later phases (P1–P7).

---

## 1. Problem / Motivation

An independent audit found that this repository — a **single-author DDR4 UDIMM reference-design
study** with zero external contributors — was carrying **consortium-grade governance** (a ~500-line
charter with a multi-maintainer stewardship model, decision-making "forums," and "community over
authority" framing) and **three separate LICENSE files** whose split was assumed to be undocumented.
That weight is mismatched to a solo educational study. Phase 0 right-sizes the governance prose and
makes the licensing intent explicit **without** stripping the repo's professional, credible face
(it is referenced from the author's CV, website, and LinkedIn).

A read-only inventory pass (three parallel sub-agents: licenses, governance/meta docs, reference
graph) was run before any change. Its findings **refined two of the audit's assumptions**:

1. **The license split is already documented**, not orphaned. The README already maps each license
   to a content type (lines ~175–187) and seven docs already carry
   `<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->` headers. All three license files are
   **distinct** (MD5-confirmed) and **load-bearing** (each linked from the README). → The correct
   action is to **document the split more clearly, not delete** any license. This matches the brief's
   rule: *never blind-delete a license without proving nothing depends on it.*
2. **The consortium theater is concentrated in `CHARTER.md`** (§4.6 and §9), so it can be
   **right-sized in place** rather than by deleting files.

The inventory also surfaced **one genuine defect** the audit had not named:
`CODE_OF_CONDUCT.md` is a **mis-pasted Code of Conduct from an unrelated project** — it pledges to
the "World Monitor community" and routes incident reports to `github.com/koala73/worldmonitor/issues`.
This is a correctness bug (a foreign project's identity left in OMI's repo), not a rebrand of OMI,
and it is fixed here.

---

## 2. Method (read-only inventory, then implement)

Per the Phase 0 brief, **Step 1 was a read-only fan-out** — no files were changed while inventorying:

- **Sub-agent A — Licenses:** found exactly **3** license files; identified each license from its
  actual text; confirmed all three are distinct (no duplicates) and which content type each covers.
- **Sub-agent B — Governance/meta docs:** enumerated every governance/meta doc with line counts and
  flagged the consortium-theater language (concentrated in `CHARTER.md`).
- **Sub-agent C — Reference graph:** grepped the whole repo for inbound references to separate
  **load-bearing** files from **orphans**, and verified which README internal links are broken.

The three results were cross-checked against each other before this proposal was written.

---

## 3. Decision table

**Legend:** KEEP = leave as-is · KEEP+EDIT = keep the file, surgically right-size/correct it ·
CONSOLIDATE = trim in place · DROP = delete · FLAG = leave unchanged this phase, raise for a later phase.

### 3a. License files

| File / path | License / role | Referenced by? | Action | Reason |
|---|---|---|---|---|
| `LICENSE` | CERN-OHL-S-2.0 — **hardware** (`design/**`) | README:180 (linked); covers KiCad/PCB artifacts | **KEEP** | Load-bearing, correct license for hardware. The brief explicitly keeps CERN-OHL-S-2.0 for hardware. |
| `LICENSE-docs` | CC-BY-SA-4.0 — **prose docs** | README:182 (linked); SPDX headers in 7 docs | **KEEP** (flag SA) | Load-bearing; claimed by SPDX headers. Existing license is CC-BY-**SA**-4.0 (copyleft). The brief *suggested* CC-BY-4.0 (permissive); switching would **remove ShareAlike**, a substantive legal change, so it is **not** done unilaterally — see Open Question (§6). |
| `LICENSE-software` | Apache-2.0 — **code** (Python tooling) | README:184 (linked) | **KEEP** | Load-bearing; matches the brief's recommendation (one permissive license for the scripts so they're cleanly reusable downstream). |

**No license file is deleted.** All three are distinct and load-bearing; the reference graph
contradicts the "orphaned license" hypothesis.

### 3b. Governance / meta docs (root)

| File / path | Role | Referenced by? | Action | Reason |
|---|---|---|---|---|
| `README.md` | Project front page | Entry point; links most docs | **KEEP+EDIT** | Add an explicit **Licensing** section mapping *license → directory*; add a Code of Conduct link. Broken nav links **flagged, not fixed** (see §5). No status/claims wording touched. |
| `CHARTER.md` (508 lines) | Charter: purpose, scope, principles, governance | 9 inbound refs — load-bearing | **CONSOLIDATE** | Right-size **§4.6** ("Community Over Authority") and **§9** ("Community, Governance, and Contribution Model"): remove the multi-maintainer stewardship / revocable-role / decision-"forum" / "no one contributor has full control" framing that dresses a solo study as a standards body. **Preserve** §1–8 and §10–12 (the study's substance) and **all** status/claims wording. Link the real CoC from §9.6. |
| `CODE_OF_CONDUCT.md` (121 lines) | Contributor Covenant v2.1 | **0 inbound refs (orphan)**; also mis-references another project | **KEEP+EDIT** | The brief keeps a CoC for a professional face. **Fix** the mis-pasted "World Monitor" / `koala73/worldmonitor` references to OMI (pure correctness), and **link** it from README + CONTRIBUTING to remove its orphan status. Not deleted. |
| `CONTRIBUTING.md` (167 lines) | Contribution workflow | 4 inbound refs — load-bearing | **KEEP+EDIT** | Sound and procedural. Only change: point its "Code of Conduct" section at the actual `CODE_OF_CONDUCT.md`. |
| `START_HERE.md` (234 lines) | Onboarding / repo map | 6 inbound refs — load-bearing | **KEEP** | Brief-protected (educational identity). Its "community"/tracks framing is normal open-source onboarding aspiration, not standards-body machinery, so it is **kept**. Its broken stage-dir links are **flagged** (§5), consistent with the README. |
| `SCOPE_V1.md` (161 lines) | Operational v1 scope boundaries | Weak (1 ref) | **KEEP** | Brief-protected; more precise than the charter's scope prose. "When unsure, KEEP." |
| `LEARNING_ROADMAP.md` (254 lines) | Self-paced learning curriculum | Weak (1 ref) | **KEEP** | Brief leans KEEP — part of the educational identity, not duplicative of the README. |

### 3c. Other meta / docs (non-governance, listed for completeness)

| File / path | Role | Action | Reason |
|---|---|---|---|
| `docs/how_omi_is_engineered.md` | Engineering methodology | **KEEP** | Study substance, not governance theater. Carries an SPDX header already. |
| `docs/08_validation_and_review/templates/**` (6 templates) | L0/L1 PR + review + report templates | **KEEP** | Operational validation artifacts (Stage 8 substance), not consortium theater. |
| `docs/00…10/**`, `docs/v1/**` | Engineering design-rationale | **KEEP (untouched)** | Hard-protected: this prose *is* the study and feeds later phases. |
| `meta/` | (empty directory) | **KEEP** | Empty; nothing to do. |
| `AUDIT_REPO_POSITION.md` | Prior audit working doc (untracked) | **LEAVE UNTRACKED** | Not a requested Phase-0 deliverable; left untracked (neither committed nor deleted). |
| `PHASE0_DOC_HYGIENE_BRIEF.md` | This phase's briefing (untracked) | **DO NOT COMMIT** | Per the brief, it is a working document, never a repo artifact. |

### 3d. Out of scope — not touched this phase (verbatim hard exclusions)

`design/**` · `design/connector/ddr4_udimm_288_pinmap.csv` ·
`docs/08_validation_and_review/scripts/**` · `validation/evidence/**`.

---

## 4. What changed (files this PR edits)

| File | Change | One-line description |
|---|---|---|
| `PHASE0_CLEANUP_PROPOSAL.md` | added | This decision record (committed artifact). |
| `README.md` | edited | Renamed `## License` → `## Licensing`, added a license→directory mapping table; added a Code of Conduct link. No status/claims changes. |
| `CHARTER.md` | edited | Right-sized §4.6 and §9 to a solo-maintained, transparent-but-not-consortium framing; linked the real CoC. Substance (§1–8, §10–12) preserved. |
| `CODE_OF_CONDUCT.md` | edited | Corrected the mis-pasted "World Monitor" / `koala73/worldmonitor` references to OMI. Content otherwise unchanged (still Contributor Covenant v2.1). |
| `CONTRIBUTING.md` | edited | Linked the actual `CODE_OF_CONDUCT.md` from its Code of Conduct section. |

**Net file deletions: none.** The right-sizing is achieved by trimming prose inside `CHARTER.md`, not
by removing files — consistent with the brief's "right-size, do not gut" and "don't over-delete."

---

## 5. Flagged, not fixed (deferred to a later phase)

- **Broken README/START_HERE navigation links** to `docs/05_architecture_decisions/` and
  `docs/06_block_decomposition/`. These directories do not exist; the real dirs are
  `docs/05_power_delivery_and_pdn/` and `docs/06_signal_topology_and_routing/`. This is **not** a
  clean path typo: the README/START_HERE narrative numbers stages as "Stage 5 = Architecture
  Decisions / Stage 6 = Block Decomposition" (also in the README's *Completed* claims), but the
  `docs/00…10` tree uses different **topic** names. Repairing the link target alone makes the label
  incoherent; repairing the label edits the Stage-numbering **status/structure narrative**, which is
  reserved for the later "make claims honest" phase. Per the brief ("only if cheap and *unambiguous*"
  + "when unsure, KEEP and flag"), these are left unchanged and flagged here.

- **SPDX headers on Python scripts.** Desirable (the brief recommends it), but every Python file lives
  under `docs/08_validation_and_review/scripts/**`, a **hard exclusion** this phase. Deferred to the
  phase that owns those scripts.

- **CC-BY-SA-4.0 vs CC-BY-4.0 for docs.** See Open Question (§6).

---

## 6. Open question (for the reviewer)

> **Recommended:** per-content-type license split —
> **CERN-OHL-S-2.0** (hardware) / **Apache-2.0** (code) / **CC-BY-SA-4.0** (docs).
> **Alternative:** consolidate to a single license.
> Confirm the split, or tell me to unify and I'll amend.

Secondary flag within the split: the docs license is currently **CC-BY-SA-4.0** (ShareAlike /
copyleft). The brief floated **CC-BY-4.0** (permissive). Kept SA to avoid a unilateral copyleft
change — say the word to switch.

---

## 7. Verification

- `git status` clean before/after; checkpoint commit (this proposal) precedes any content removal.
- `main` unchanged; all work on `phase0-doc-hygiene`; no force-push, no history rewrite.
- Every license file and governance/meta doc has an action + reason in §3.
- README has a Licensing section mapping license → directory.
- No out-of-scope artifact touched (`design/**`, the keystone CSV, `docs/08…/scripts/**`,
  `validation/evidence/**`); design-rationale docs not gutted.
- No status/claims/maturity wording changed; no rename/rebrand of OMI.
- Diffs are content-only (no line-ending mass-rewrite).
- The briefing file and `AUDIT_REPO_POSITION.md` are not committed.

---

## 8. Related docs

- `PHASE0_DOC_HYGIENE_BRIEF.md` — the authoritative Phase 0 spec (working file, untracked).
- `CHARTER.md`, `README.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md` — the edited governance set.
- `LICENSE`, `LICENSE-docs`, `LICENSE-software` — the three retained licenses.

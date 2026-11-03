# Bhoomi Federation Constitutional Foundations Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a dated, source-linked fictional canon registry and constitutional, government, legal-order, and citizenship foundation pages without changing the original 2025 archive; encode the founder-specific Chief Architect office and the Assembly’s later collective supervision, then prepare the feature branch for coordinator review and verified publication.

**Architecture:** Keep the current static HTML/CSS/JSON architecture. Store new BHF/006–009/2026 canon separately in `data/canon.json`, add C1–C6 as comparative references in `data/sources.json`, and expose the content through `/canon/` and `/foundations/` with the existing navigation and styles. The history archive remains the sole source of 2025 claims; new content is visibly dated and non-operational.

**Tech Stack:** HTML, CSS, JSON, Python standard-library `unittest`, Node built-in `node:test`; no new dependencies or JavaScript behavior.

**Spec:** `docs/superpowers/specs/2026-11-03-bhoomi-constitutional-foundations-design.md`

## Global Constraints

- Preserve BHF/001–005/2025 data, original titles/dates, claims and uncertainty notes unchanged.
- Assign new sequential IDs BHF/006/2026–BHF/009/2026, all dated 2026-11-03 and explicitly marked `new_fictional_canon`.
- Link S3/S4 only as 2025 historical anchors and C1–C6 only as design references, never as evidence of Bhoomi legal force or statehood.
- Do not invent territory, capital, unit count/names/borders, demographics, flags, seals, live applications or operational services; do not add a personal name or end date for the founder/Chief Architect or invent a successor. Identify the founder only by the owner-specified Chief Architect title.
- The Chief Architect is the founder-specific, non-elective Head of Country; do not invent an identity or tenure end date. After the founder’s tenure, the office remains vacant and cannot be filled by election or appointment; the Assembly then supervises collectively, without becoming a successor Head of Country.
- Every new page must state that it is fictional canon with no real-world legal effect; preserve the existing base path `/Bhoomi-Federation/`.
- Reuse current visual classes and navigation structure; do not redesign or add dependencies.
- Implement and verify only on `feat/constitutional-foundations`; the current worker does not push. After independent review and verification, the coordinator may merge/push the approved slice and must verify the live Pages routes before calling it published.

## Review Focus

- The original archive stays intact: test exact original record count, ordered IDs and dates, existing claims and source entries.
- Unknown geography remains unknown: assert no named or invented territory/unit and visible disclosure that the schedule is blank.
- The succession boundary is respected: assert no Chief Architect election/appointment, named holder or end date; after vacancy the Assembly is a collective supervisor, not a successor Head of Country, while the Prime Minister remains Assembly-accountable.
- Cross-level powers and amendment rules remain usable before units exist: test unit-dependent ratification is conditional on future units.
- Comparative sources are never mistaken for binding Bhoomi law: test every source ID resolves and the page labels the sources as references with scope limitations.
- Citizenship is not operational: assert no application endpoint/form, no actual people or records, and clear anti-statelessness and review safeguards.

---

### Task 1: Add failing canon and page-contract tests

**Files:**
- Create: `tests/test_foundations.py`
- Modify: `tests/test_portal.py`

**Interfaces:**
- Canon dataset shape: top-level `edition_date` (`2026-11-03`), `fictional_only` (`true`), `real_world_legal_effect` (`"none"`) and `records`; each record has `number`, `title`, `issue_date`, `document_type`, `canon_status` (`"new_fictional_canon"`), `operational_status` (`"framework_only"`), `authority_note`, `summary`, `prior_record_numbers`, `historical_source_ids`, `design_reference_ids` and `page_anchor`.
- Pages use the existing project base, shared navigation and visible source anchors.

- [x] **Step 1: Write tests** for four canonical IDs and titles BHF/006–009/2026, all dated 2026-11-03, exact status values, no duplicate original IDs, linkages to S3/S4, and resolution of C1–C6.
- [x] **Step 2: Add page assertions** for fictional status, the four foundations, the founder-specific non-elective Chief Architect role, permanent vacancy/no successor, collective Assembly supervision, Assembly-accountable Prime Minister, no personal name or end date for the founder and no invented holder, government directory purpose/powers/appointments/terms/accountability, unknown territory, blank member-unit schedule, no real-world recognition, no applications, source citations, and all four registry entries.
- [x] **Step 3: Run the focused tests and verify they fail for missing canon data/routes/source IDs.**

Run: `python3 -m unittest discover -s tests -p 'test_foundations.py' -v`
Expected: assertion failures for absent deliverables, not setup errors.

- [x] **Step 4: Commit the red tests** on the local feature branch.

### Task 2: Implement canon data, source ledger and public pages

**Files:**
- Create: `data/canon.json`
- Modify: `data/sources.json`
- Modify: `sources/index.html`
- Modify: `documents/index.html`
- Modify: all existing page navigation shells
- Create: `canon/index.html`
- Create: `foundations/index.html`
- Modify: `README.md`
- Use: `docs/constitutional-references.md` (already committed with the design documents; no file change expected)

**Interfaces:**
- `data/canon.json` is independent of the 2025 `data/documents.json` and has stable links to source IDs and page anchors.
- C1–C6 use the existing `id`, `title`, `kind`, `url`, `limitation` source contract.
- New public pages use semantic headings, a skip link, one H1, existing shared navigation and visible source citations.

- [x] **Step 1: Create four linked, same-day fictional records** with distinct roles: Constitution (BHF/006), Federal Institutions and Accountability Act (BHF/007), Public Law and Administration Act (BHF/008), Citizenship and Identity Act (BHF/009).
- [x] **Step 2: Add six official-source records** with article/section scope and limitations; add corresponding source anchors and cited summaries to the Sources page.
- [x] **Step 3: Build `/canon/`** as a registry, stating the 2026 additions are not 2025 records and have no real-world legal effect or operational government/application.
- [x] **Step 4: Build `/foundations/`** with the Constitution, Government Directory, Legal Order and Citizenship sections exactly as specified, including the Chief Architect as founder-specific non-elective Head of Country, an unfilled permanent vacancy after the founder’s tenure, the Assembly’s collective supervisory role (not a successor Head of Country), one delegate and equal vote per future member unit, Assembly-accountable Prime Minister, court/commission appointment procedures, terms, limits, accountability, emergency review, amendment rules and the no-test, anti-statelessness citizenship process.
- [x] **Step 5: Add the two new navigation routes everywhere** and a short cross-link from the original Documents page; do not modify original record metadata.
- [x] **Step 6: Run focused tests and verify green.**

Run: `python3 -m unittest discover -s tests -p 'test_foundations.py' -v && python3 -m unittest discover -s tests -p 'test_portal.py' -v`
Expected: all foundation and existing portal tests pass; all original 2025 assertions remain unchanged.

- [x] **Step 7: Commit the completed canon/data/pages** on the local feature branch.

### Task 3: Full release verification and coordinator handoff

**Files:** all changed files in Tasks 1–2.

- [x] **Step 1: Run the full Python suite** with `python3 -m unittest discover -s tests -v`.
- [x] **Step 2: Run the Node suite** with `node --test tests/documents.test.mjs`.
- [x] **Step 3: Parse every JSON file and run `git diff --check`.**
- [x] **Step 4: Serve the site locally under `/Bhoomi-Federation/` and verify the two new routes, all local links, and source anchors; inspect 390 px navigation/content for overflow without redesigning.
- [x] **Step 5: Review the complete branch diff against this spec; record any deferred minor issue in the progress ledger.**
- [x] **Step 6: Hand off the exact branch/worktree path and verification results to the coordinator for independent review and verification. The current worker does not push or publish.**
- [ ] **Coordinator-only release gate:** After independent review and verification, the coordinator may merge/push the approved branch, confirm the GitHub Pages deployment, and check live `/Bhoomi-Federation/canon/` and `/Bhoomi-Federation/foundations/` plus existing routes. Do not claim publication until those live checks pass.

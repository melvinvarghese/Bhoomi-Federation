# Bhoomi Federation Constitutional Foundations Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a dated, source-linked fictional canon registry and constitutional, government, legal-order, and citizenship foundation pages without changing the original 2025 archive or publishing the branch.

**Architecture:** Keep the current static HTML/CSS/JSON architecture. Store new BHF/006–009/2026 canon separately in `data/canon.json`, add C1–C6 as comparative references in `data/sources.json`, and expose the content through `/canon/` and `/foundations/` with the existing navigation and styles. The history archive remains the sole source of 2025 claims; new content is visibly dated and non-operational.

**Tech Stack:** HTML, CSS, JSON, Python standard-library `unittest`, Node built-in `node:test`; no new dependencies or JavaScript behavior.

**Spec:** `docs/superpowers/specs/2026-11-03-bhoomi-constitutional-foundations-design.md`

## Global Constraints

- Preserve BHF/001–005/2025 data, original titles/dates, claims and uncertainty notes unchanged.
- Assign new sequential IDs BHF/006/2026–BHF/009/2026, all dated 2026-11-03 and explicitly marked `new_fictional_canon`.
- Link S3/S4 only as 2025 historical anchors and C1–C6 only as design references, never as evidence of Bhoomi legal force or statehood.
- Do not invent territory, capital, unit count/names/borders, demographics, officeholders, flags, seals, live applications or operational services.
- Every new page must state that it is fictional canon with no real-world legal effect; preserve the existing base path `/Bhoomi-Federation/`.
- Reuse current visual classes and navigation structure; do not redesign or add dependencies.
- Work only on `feat/constitutional-foundations`; do not push, merge, deploy or change Pages settings.

## Review Focus

- The original archive stays intact: test exact original record count, ordered IDs and dates, existing claims and source entries.
- Unknown geography remains unknown: assert no named or invented territory/unit and visible disclosure that the schedule is blank.
- Cross-level powers and amendment rules remain usable before units exist: test unit-dependent ratification is conditional on future units.
- Comparative sources are never mistaken for binding Bhoomi law: test every source ID resolves and the page labels the sources as references with scope limitations.
- Citizenship is not operational: assert no application endpoint/form, no actual people or records, and clear anti-statelessness and review safeguards.

---

### Task 1: Add failing canon and page-contract tests

**Files:**
- Create: `tests/test_foundations.py`
- Modify: `tests/test_portal.py`

**Interfaces:**
- Canon dataset shape: top-level `edition_date`, `fictional_only`, and `records`; each record has number, title, issue date, category, status, operational status, authority note, summary, prior record numbers, historical source IDs, design-reference IDs and page anchor.
- Pages use the existing project base, shared navigation and visible source anchors.

- [ ] **Step 1: Write tests** for four canonical IDs/categories BHF/006–009/2026, date 2026-11-03, new-fictional/non-operational labels, linkages to S3/S4, and resolution of C1–C6.
- [ ] **Step 2: Add page assertions** for fictional status, the four foundations, government directory fields, unknown territory, no real-world recognition, no officeholders or applications, source citations, and all four registry entries.
- [ ] **Step 3: Run the focused tests and verify they fail for missing canon data/routes/source IDs.**

Run: `python3 -m unittest discover -s tests -p 'test_foundations.py' -v`
Expected: assertion failures for absent deliverables, not setup errors.

- [ ] **Step 4: Commit the red tests** on the local feature branch.

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
- Create: `docs/constitutional-references.md` (already staged in the feature workspace)

**Interfaces:**
- `data/canon.json` is independent of the 2025 `data/documents.json` and has stable links to source IDs and page anchors.
- C1–C6 use the existing `id`, `title`, `kind`, `url`, `limitation` source contract.
- New public pages use semantic headings, a skip link, one H1, existing shared navigation and visible source citations.

- [ ] **Step 1: Create four linked, same-day fictional records** with distinct roles: Constitution (BHF/006), Federal Institutions and Accountability Act (BHF/007), Public Law and Administration Act (BHF/008), Citizenship and Identity Act (BHF/009).
- [ ] **Step 2: Add six official-source records** with article/section scope and limitations; add corresponding source anchors and cited summaries to the Sources page.
- [ ] **Step 3: Build `/canon/`** as a registry, stating the 2026 additions are not 2025 records and have no real-world legal effect or operational government/application.
- [ ] **Step 4: Build `/foundations/`** with the Constitution, Government Directory, Legal Order and Citizenship sections exactly as specified, including powers, appointments, terms, limits, accountability, emergency review, amendment rules and anti-statelessness safeguards.
- [ ] **Step 5: Add the two new navigation routes everywhere** and a short cross-link from the original Documents page; do not modify original record metadata.
- [ ] **Step 6: Run focused tests and verify green.**

Run: `python3 -m unittest discover -s tests -p 'test_foundations.py' -v && python3 -m unittest discover -s tests -p 'test_portal.py' -v`
Expected: all foundation and existing portal tests pass; all original 2025 assertions remain unchanged.

- [ ] **Step 7: Commit the completed canon/data/pages** on the local feature branch.

### Task 3: Full release verification and coordinator handoff

**Files:** all changed files in Tasks 1–2.

- [ ] **Step 1: Run the full Python suite** with `python3 -m unittest discover -s tests -v`.
- [ ] **Step 2: Run the Node suite** with `node --test tests/documents.test.mjs`.
- [ ] **Step 3: Parse every JSON file and run `git diff --check`.**
- [ ] **Step 4: Serve the site locally under `/Bhoomi-Federation/` and verify the two new routes, all local links, and source anchors; inspect 390 px navigation/content for overflow without redesigning.
- [ ] **Step 5: Review the complete branch diff against this spec; record any deferred minor issue in the progress ledger.**
- [ ] **Step 6: Hand off the exact branch/worktree path and verification results to the coordinator. Do not push or publish.**

# Bhoomi Federation Phase 1: Verified Portal and National Archive Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the Phase 1 static, source-backed portal for The Bhoomi Federation, preserving the documented 2025 record and making its five original records discoverable without implying real-world statehood or inventing national institutions.

**Architecture:** A small multi-page static site uses plain HTML and one shared stylesheet, with locally stored JSON as the source of truth for documents, claims, and provenance. The document registry is complete in HTML before JavaScript runs; a small enhancement adds search and filters from the JSON data. All local routes and assets use the GitHub Pages project prefix.

**Tech Stack:** HTML, CSS, browser JavaScript (ES modules), JSON, Python standard-library `unittest`, and Node's built-in `node:test`; no framework, bundler, runtime service, or production dependency.

**Spec:** `docs/superpowers/specs/2026-11-03-bhoomi-verified-portal-phase-1-design.md`

## Global Constraints

- Use plain HTML, CSS, JavaScript, and JSON, without a framework or bundler.
- Every internal link and asset URL must work under `/Bhoomi-Federation/`; verify project-path URLs, not just domain-root URLs.
- Every factual claim must trace to a source entry. Claim statuses are exactly `primary_record`, `legacy_site`, `metadata_only`, and `unresolved`.
- Treat the original document as authoritative for its wording; Archive.org metadata locates the record and records its displayed rights statement, but does not override the PDF or establish uploader authority.
- Do not render a precise official flag or claim an exact official green until the `#008A45` PDF extraction versus `#008445` Archive.org OCR discrepancy is resolved from the original visual record. Use only a typographic wordmark; invent no emblem or other official symbol.
- Do not redistribute a PDF without a recorded, supportable rights basis. All five records currently list CC BY-NC-ND 4.0 as platform metadata; absent separate authorization evidence, use Archive.org item links only and preserve originals unchanged if redistribution is later supported.
- Do not label a document “currently in force.” Do not add out-of-scope constitution, government, geography, officeholders, eligibility rules, statistics, simulated history, backend, accounts, database, API dependency, cookies, tracking, or visitor-persisted state.
- The complete five-record list must remain readable if JavaScript is disabled or fails. Keep search and filters keyboard-operable, labelled, and progressively enhanced.
- Use semantic HTML, a skip link, logical headings, visible focus, sufficient contrast, reduced-motion support, local assets, and system fonts; do not add remote font or icon dependencies.
- Create a 1280 × 640 social-preview PNG under 1 MB, with typography and a neutral landscape, no flag or invented official symbol. GitHub’s [official guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview) accepts PNG/JPG/GIF under 1 MB and recommends at least 640 × 320 (1280 × 640 for best display). Prepare the asset only; do not change repository settings.
- This plan is not implementation approval. Do not write site code, publish, or change GitHub settings until the owner has reviewed the plan and authorized an execution approach.

## Review Focus

- Empty or whitespace-only search should leave every record visible; test `filterDocuments` with `""` and `"   "` and expect five records.
- Search should tolerate letter case and match either title or document number; test a mixed-case partial title and `bhf/001/2025`.
- Combined filters should intersect rather than override one another; test year, type, and authority together, then an unknown filter value and expect no matches.
- If local JSON loading fails, or JavaScript is disabled, all five static records and their Archive.org links must remain available and the filter controls must not obstruct them; test the no-script HTML and manually block the JSON request.
- On a 320 px viewport, keyboard users must be able to reach, operate, and reset every filter with visible focus; manually test the narrow layout and keyboard-only flow.

---

## Scope and File Map

This is one coherent portal, not multiple independent subsystems: the records, provenance, routes, and presentation must agree. No source PDFs are copied into the repository. Preserve the existing `README.md`, `.github/FUNDING.yml`, approved spec, Git history, and GitHub Pages settings.

| File | Responsibility |
|---|---|
| `data/sources.json` | Source inventory for S1–S5, L1–L4, R1–R2, and P1 (the owner-provided brief as editorial provenance for unresolved research leads), including source ID, title, kind, URL when public, and evidence limitation. |
| `data/claims.json` | Stable claim IDs, claim text, allowed evidence status, source IDs, and conflict/uncertainty notes. |
| `data/documents.json` | The five original-record metadata entries and redistribution decisions. |
| `index.html` | Home page: fictional-status notice, founding date, four documented values, sourced introduction, and route links. |
| `about/index.html` | Sourced chronology, legacy public vision, values, and separate unresolved-history note. |
| `calendar/index.html` | Only the documented weekday/weekend and public-holiday rules, with the annual National Day distinction. |
| `sources/index.html` | Source inventory, status definitions, provenance model, and licensing caveat. |
| `documents/index.html` | Complete static fallback list first; later enhanced with search/filter controls and results status. |
| `documents/bhf-001-2025/index.html` … `documents/bhf-005-2025/index.html` | One detail page per original record. |
| `assets/css/site.css` | Shared responsive layout, typography, focus styles, UI-only colors, and reduced-motion behavior. |
| `assets/js/documents.mjs` | Pure record-filtering function plus small DOM enhancement for the registry. |
| `assets/images/social-preview.png` | GitHub repository social-preview artwork, ready for later selection in settings. |
| `tests/test_portal.py` | Standard-library checks for JSON provenance, site routes/links, semantic accessibility hooks, and image properties. |
| `tests/documents.test.mjs` | Node built-in tests for the exported document-filter function. |

Do not add placeholder pages, a build system, a package manifest, copied PDFs, or new national canon.

## Task 1: Add the Provenance and Document Data

**Files:**
- Create: `data/sources.json`
- Create: `data/claims.json`
- Create: `data/documents.json`
- Create: `tests/__init__.py`
- Create: `tests/test_portal.py`

**Interfaces:**
- `sources.json`: records contain `id`, `title`, `kind`, `url`, and `limitation`.
- `claims.json`: records contain `id`, `text`, `status`, `source_ids`, and `uncertainty_note`.
- `documents.json`: records contain `number`, `title`, `issue_date` (`YYYY-MM-DD`), `document_type`, `issuing_authority`, `summary`, `canonical_source_url`, `archive_item_url`, `archive_file_url`, `displayed_license`, `redistribution_decision`, and `uncertainty_notes`.
- Use stable claim IDs `C-FOUNDING-DATE`, `C-NATIONAL-DAY`, `C-VALUES`, `C-FLAG-ADOPTION`, `C-CITIZEN-DESIGNATION`, `C-CALENDAR-RULES`, `C-LEGACY-VISION`, and `C-EARLIER-NAMES`; add a further claim only when a page needs a separately sourced factual statement.
- Source IDs S1–S5, L1–L4, and R1–R2 refer to the sources listed in the approved spec. P1 is the owner-provided brief, used only as editorial provenance for the unresolved research leads, not as historical evidence; because it is private project input, its public URL is null. Set each record’s `redistribution_decision` to `link_only` unless separate, supportable authorization is documented; do not treat the Archive.org license listing as that authorization.

- [ ] **Step 1: Write the failing data-contract tests** in `tests/test_portal.py`: assert the five ordered number/date/title tuples are `(BHF/001/2025, 2025-06-04, Flag Adoption Proclamation)`, `(BHF/002/2025, 2025-06-05, National Day Proclamation)`, `(BHF/003/2025, 2025-06-05, Founding Proclamation)`, `(BHF/004/2025, 2025-06-06, Citizens (Bhoomians), Executive Order No. 1)`, and `(BHF/005/2025, 2025-06-07, Adoption of the Official National Calendar)`; assert each `canonical_source_url`, `archive_item_url`, and `archive_file_url` matches the corresponding S1–S5 URLs in the spec; assert the required fields, valid claim/source references, allowed statuses, displayed-license caveat, and `link_only` decision. Assert the exact four values—clarity of thought, ethical governance, dignity of individual existence, collective peace—and the recorded calendar rules; pin the flag-color, BHF/003 title, and BHF/005 Executive Order 2 discrepancies as uncertainties, not resolved facts.
- [ ] **Step 1: Write the failing data-contract tests** in `tests/test_portal.py`: assert the five ordered number/date/title tuples are `(BHF/001/2025, 2025-06-04, Flag Adoption Proclamation)`, `(BHF/002/2025, 2025-06-05, National Day Proclamation)`, `(BHF/003/2025, 2025-06-05, Founding Proclamation)`, `(BHF/004/2025, 2025-06-06, On the Official Designation of Citizens of the Bhoomi Federation)`, and `(BHF/005/2025, 2025-06-07, Adoption of the Official National Calendar)`; assert each `canonical_source_url`, `archive_item_url`, and `archive_file_url` matches the corresponding S1–S5 URLs in the spec; assert the required fields, valid claim/source references, allowed statuses, displayed-license caveat, and `link_only` decision. Assert the exact four values—clarity of thought, ethical governance, dignity of individual existence, collective peace—and the recorded calendar rules; pin the flag-color, BHF/003 title, and BHF/005 Executive Order 2 discrepancies as uncertainties, not resolved facts.
- [ ] **Step 2: Create an empty `tests/__init__.py`** so Python 3.12 unittest discovery can import the test directory.

- [ ] **Step 3: Run the tests and verify they fail** because the JSON data files do not yet exist.

  Run: `python3 -m unittest discover -s tests -p 'test_portal.py' -v`

  Expected: FAIL on missing data files or missing required records.
- [ ] **Step 4: Populate the three JSON files** from the approved spec and original PDFs. Use the PDF’s printed title, date, type, and issuing authority; if an authority is not stated, record “Not stated in PDF” rather than inventing one. Preserve the BHF/003 title discrepancy, BHF/005 metadata-only “Executive Order 2” label, same-day order uncertainty for BHF/002 and BHF/003, citizenship-process gap, and flag-color discrepancy in uncertainty notes. Record CC BY-NC-ND 4.0 as displayed platform metadata, not proof of redistribution rights. Store National Day’s annual recurrence as sourced to BHF/002 and BHF/003, not BHF/005.
- [ ] **Step 5: Run the data tests and verify they pass.**

  Run: `python3 -m unittest discover -s tests -p 'test_portal.py' -v`

  Expected: PASS; all five records and claims resolve to known source IDs and none is marked as currently in force.
- [ ] **Step 6: Commit** the tested data contract and tests.

  ```bash
  git add data/sources.json data/claims.json data/documents.json tests/__init__.py tests/test_portal.py
  git commit -m "feat: add sourced Phase 1 archive data"
  ```

## Task 2: Build Shared Presentation and Core Pages

**Files:**
- Create: `assets/css/site.css`
- Create: `index.html`
- Create: `about/index.html`
- Create: `calendar/index.html`
- Create: `sources/index.html`
- Create: `documents/index.html`
- Modify: `tests/test_portal.py`

**Interfaces:**
- Each page uses the same five-link navigation: Home, About & History, Official Documents, National Calendar, and Sources and provenance. Link to the routes under `/Bhoomi-Federation/`; the Documents route is a complete static list in this task.
- Each sourced factual block uses `data-claim-id="<stable claim id>"` and a visible citation linking to `/Bhoomi-Federation/sources/#<source id>` with the evidence status written as text.
- The Sources page gives each source row an `id` equal to its source ID. Shared CSS defines `--color-text`, `--color-muted`, `--color-link`, `--color-surface`, and `--color-focus`; its palette must not be described as an official national identity or an exact flag color.

- [ ] **Step 1: Add failing page-contract tests** to `tests/test_portal.py`: assert each required core route exists, has a descriptive title, one `h1`, `lang="en"`, a skip link, and shared navigation with the five exact route links; assert local `href`/`src` paths use the project prefix, claim IDs resolve to `claims.json`, and visible citations link to source IDs. Assert the home-page disclosure, founding date, and four exact values; the About page’s separate unresolved-research note; the Calendar’s rules and annual-National-Day citations; the Sources page’s four status definitions and license caveat; and the static Documents route’s five complete records and Archive.org links, including a no-JavaScript list.
- [ ] **Step 2: Run the page tests and verify they fail** because the pages do not exist.

  Run: `python3 -m unittest discover -s tests -p 'test_portal.py' -v`

  Expected: FAIL on the missing route files and page contracts.
- [ ] **Step 3: Implement the shared stylesheet, four core pages, and static Documents list.** Home identifies Bhoomi as fictional, states 5 June 2025 and the four values exactly—clarity of thought, ethical governance, dignity of individual existence, and collective peace—and links to History, Documents, and Calendar. About & History gives the dated record chronology without inventing an order between the two 5 June records; it labels legacy-site statements as historical public vision and the Republic of Harmonia/Melvin Welfare Dominion only as unresolved research leads. Calendar states Monday–Friday working days, weekends non-working, and June 5 as the sole public holiday under BHF/005; separately cite BHF/002 and BHF/003 for annual National Day and do not attribute that recurrence to BHF/005. Sources defines all four statuses and explains the Archive.org licensing caveat. The Documents page lists all five records and their Archive.org links in static HTML, matching `documents.json`. Add no unsupported live statistics or inactive institutional routes.
- [ ] **Step 4: Run the page tests and verify they pass.**

  Run: `python3 -m unittest discover -s tests -p 'test_portal.py' -v`

  Expected: PASS; every core page has the shared accessible shell and every factual block maps to cited provenance.
- [ ] **Step 5: Commit** the core pages and shared styling.

  ```bash
  git add assets/css/site.css index.html about/index.html calendar/index.html sources/index.html tests/test_portal.py
  git commit -m "feat: add sourced portal pages"
  ```

## Task 3: Build the Official Documents Registry and Record Pages

**Files:**
- Create: `documents/index.html`
- Create: `documents/bhf-001-2025/index.html`
- Create: `documents/bhf-002-2025/index.html`
- Create: `documents/bhf-003-2025/index.html`
- Create: `documents/bhf-004-2025/index.html`
- Create: `documents/bhf-005-2025/index.html`
- Create: `assets/js/documents.mjs`
- Create: `tests/documents.test.mjs`
- Modify: `documents/index.html`
- Modify: `tests/test_portal.py`

**Interfaces:**
- Export `filterDocuments(records, { query = "", year = "", type = "", authority = "" } = {})` from `assets/js/documents.mjs`. Each record has the Task 1 `documents.json` shape. Return records matching every selected filter; search is trimmed, case-insensitive, and matches `title` or `number`; `year` is the first four characters of `issue_date`; `type` and `authority` match their corresponding fields exactly. Keep this function importable in Node without a DOM; run browser initialization only when `document` exists.
- Registry cards use `data-document-number` values matching the JSON `number`. Static HTML contains all five cards and Archive.org item links before enhancement; filter controls start hidden and are revealed only after local JSON loads successfully.

- [ ] **Step 1: Write failing tests** in `tests/documents.test.mjs` for all five records, title/number search, empty and whitespace queries, mixed-case partial matches, combined filters, unknown filters, and zero-result output. Add Python checks that the static list contains all five records, each card agrees with `documents.json`, and the no-JavaScript fallback exposes all Archive.org links. Also assert every individual route exists and shows its record’s exact title, number, date, type, printed authority, `primary_record` status, license note, and Archive.org item link, with no direct PDF preview or download while its decision is `link_only`.
- [ ] **Step 2: Run the tests and verify they fail** because the module and registry are absent.

  Run: `node --test tests/documents.test.mjs && python3 -m unittest discover -s tests -p 'test_portal.py' -v`

  Expected: FAIL because the exported function and required routes are missing.
- [ ] **Step 3: Implement `filterDocuments` and the registry enhancement.** Keep the five static cards available by default; after successful local JSON loading, populate labelled year/type/authority controls, apply all filters together, update a polite results-status message, and expose a clear/reset control. If loading fails, leave controls hidden and the complete static list visible. Do not put visitor input into HTML markup or persistent storage. Each document detail page shows its title, number, date, type, printed authority, neutral description, source status, license note, and Archive.org item link. Because the current rights basis is unsupported, do not embed, preview, or link directly to a hosted copy; do not call any record “currently in force.”
- [ ] **Step 4: Run both test suites and verify they pass.**

  Run: `node --test tests/documents.test.mjs && python3 -m unittest discover -s tests -p 'test_portal.py' -v`

  Expected: PASS; all five static records match the JSON source and the filter helper returns the expected intersections without affecting the fallback.
- [ ] **Step 5: Commit** the registry, detail pages, enhancement, and tests.

  ```bash
  git add documents/ assets/js/documents.mjs tests/documents.test.mjs tests/test_portal.py
  git commit -m "feat: add searchable official documents registry"
  ```

## Task 4: Create the GitHub Social-Preview Asset

**Files:**
- Create: `assets/images/social-preview.png`
- Modify: `tests/test_portal.py`

**Interfaces:**
- The image is a static repository asset, not a national symbol and not a change to repository settings.

- [ ] **Step 1: Add a failing image test** that reads the PNG header and asserts dimensions of 1280 × 640 and file size below 1 MB.
- [ ] **Step 2: Run the image test and verify it fails** because the file does not exist.

  Run: `python3 -m unittest discover -s tests -p 'test_portal.py' -v`

  Expected: FAIL on the missing image.
- [ ] **Step 3: Create `assets/images/social-preview.png`** with the typographic name “The Bhoomi Federation” and a restrained neutral landscape. Do not include a flag, emblem, seal, invented symbol, exact flag-color claim, or language implying real-world statehood or recognition. Keep the file below 1 MB.
- [ ] **Step 4: Run the image test and visually inspect the asset** at native and reduced preview size.

  Run: `python3 -m unittest discover -s tests -p 'test_portal.py' -v`

  Expected: PASS; PNG header reports 1280 × 640 and file is under 1 MB; visual inspection confirms no prohibited symbol or claim.
- [ ] **Step 5: Commit** the preview asset and its test.

  ```bash
  git add assets/images/social-preview.png tests/test_portal.py
  git commit -m "feat: add neutral repository social preview"
  ```

## Task 5: Run Phase 1 Accessibility and Release Checks

**Files:**
- Modify: `tests/test_portal.py`
- No production file changes unless a failing acceptance check identifies a defect; fix such a defect in its owning task and rerun that task’s tests.

**Interfaces:**
- Automated checks use only Python and Node standard-library test runners; no package install or build step is introduced.
- Production base URL is `https://melvinvarghese.github.io/Bhoomi-Federation/`.

- [ ] **Step 1: Add final acceptance assertions** for all local links/assets resolving to existing files beneath `/Bhoomi-Federation/`, required semantic/accessibility hooks, and CSS contrast. Assert `--color-text`, `--color-muted`, and `--color-link` each reach at least 4.5:1 against `--color-surface`, and `--color-focus` reaches at least 3:1 against that surface; confirm the stylesheet honors `prefers-reduced-motion`. Keep color-only meaning out of status labels.
- [ ] **Step 2: Run the full automated suite.**

  Run: `python3 -m unittest discover -s tests -v && node --test tests/documents.test.mjs`

  Expected: PASS with no missing routes, invalid source references, broken local paths, contrast failures, or filter regressions.
- [ ] **Step 3: Verify project-base paths on a local static server.** Start `python3 -m http.server 8000 --directory /workspace`, then request the home page, every listed route, stylesheet, module, JSON file, and social image under `http://127.0.0.1:8000/Bhoomi-Federation/`. Expected: each returns HTTP 200; no route or asset relies on `/` as the site root.
- [ ] **Step 4: Perform manual browser checks** at 320 px and 1280 px: keyboard-only navigation and filter/reset operation, visible focus, heading order, readable contrast, no color-only status, reduced-motion behavior, and layout without horizontal overflow. Disable JavaScript and separately block `data/documents.json`; in both cases confirm the five records and Archive.org item links remain visible. Confirm the unresolved-history note, licensing caveat, and no-flag design are clear.
- [ ] **Step 5: After implementation is authorized and the owner separately authorizes publication, verify the published GitHub Pages routes and assets** at the production base URL. Do not change Pages or repository social-preview settings. Do not claim the site is published or release-ready until the public route checks pass.
- [ ] **Step 6: Commit** any final test-only changes after all checks pass.

  ```bash
  git add tests/test_portal.py
  git commit -m "test: verify Phase 1 portal acceptance"
  ```

## Self-Review

- **Spec coverage:** The route set, static five-record list, and home/history/calendar/sources content are covered in Task 2; all five original records, metadata conflicts, rights decisions, provenance, and no-current-force rule are covered in Tasks 1–3; progressive enhancement is covered in Task 3; the social preview is covered in Task 4; base paths, accessibility, and post-publication checks are covered in Task 5.
- **Step scan:** Production tasks 1–4 follow write-failing-test → run and observe failure → implement the bounded deliverable → run and observe success → commit. Task 5 is a release gate, not a production-change task. The only browser-only checks are explicit manual acceptance checks in Task 5.
- **Type/interface consistency:** `documents.json` field names match `filterDocuments` and the registry-card contract. Claim IDs, source IDs, and status values are stable across data and pages. All five route slugs map to the file paths in the file map.
- **Review Focus:** All five listed conditions are assigned to Task 3 or Task 5 tests/manual checks; the fallback condition is tested both as static HTML and with the JSON request blocked.
- **Proportion:** The plan names the cross-file decisions, test assertions, and exact commands without prescribing page markup or copying the source documents.
- **Scope check:** This remains one static archive portal. Future constitutional, governmental, demographic, economic, geographic, or simulation systems have no task here.

## Execution Handoff

**Recommended execution method: Native.** The five tasks share a compact data contract, visual system, and route structure; one implementer is likelier to keep the provenance and page patterns consistent, with a fresh whole-branch reviewer checking the finished implementation. The owner must review this plan and authorize an execution method before implementation begins.

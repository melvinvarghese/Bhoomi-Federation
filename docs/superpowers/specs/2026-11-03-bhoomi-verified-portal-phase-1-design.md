# Bhoomi Federation Phase 1: Verified Portal and National Archive

**Status:** Design spec submitted for owner review
**Date:** 2026-11-03
**Repository:** `melvinvarghese/Bhoomi-Federation`
**Target:** GitHub Pages at `https://melvinvarghese.github.io/Bhoomi-Federation/`

## 1. Purpose

Phase 1 establishes a credible public digital home for The Bhoomi Federation by recovering and presenting the documented 2025 record, the early public vision, and a usable national-document registry. It must distinguish primary-source facts from legacy website claims, unresolved evidence, and later additions. The portal must identify Bhoomi as a fictional federation and must not imply real-world statehood, recognition, or membership in actual institutions.

The repository currently has no website implementation or structured national records. Its tracked files are a minimal README and a funding template. GitHub Pages is already enabled from `main` at the repository root; the project is served below `/Bhoomi-Federation/`. The implementation must preserve that base path in every internal link and asset URL.

## 2. Phase 1 boundaries

### In scope

- A responsive, accessible static portal hosted in the existing repository and on GitHub Pages.
- A concise home page and About & History page grounded in cited sources.
- A searchable/filterable Official Documents registry for the five original records listed below.
- A National Calendar page that reports only rules stated by the adopted record and linked National Day proclamation.
- A provenance/source ledger that records each claim, its source, status, and known uncertainty.
- Preservation of original files only where redistribution is supportable; otherwise, link to the Archive.org record.
- A visitor-facing explanation that separates established 2025 canon from unresolved history and future development.
- A GitHub social-preview image using typography and a neutral landscape treatment; it must not reproduce the disputed flag colors or invent an official emblem.

### Out of scope

Phase 1 does not create a constitution, legislature, ministries, judiciary, citizenship eligibility rules, government officeholders, territory, capital, population, households, economy, budget, development indicators, simulation, or simulation-generated history. It does not invent a flag, emblem, seal, anthem, or official symbol. It does not replace or edit the original 2025 documents, change the old website, or create a backend, user accounts, database, API dependency, or separate archive site. Later nation-building phases require their own approved design and plan.

## 3. Evidence and historical model

The original document itself is authoritative for its own wording. Archive.org item metadata is used to locate the record and note its displayed rights statement, not to silently override the PDF. Legacy website statements are presented as historical public-facing vision unless an original legal record supports a stronger status. Every factual claim in the portal must be traceable to a source entry.

### Established 2025 record

- **BHF/001/2025, Flag Adoption Proclamation:** dated 4 June 2025; it adopts a vertical blue-white-green triband and states it takes immediate effect. The PDF's extracted green value is `#008A45`, while Archive.org's OCR metadata gives `#008445`; do not render a precise official flag asset until the discrepancy is resolved from the original visual record. [S1]
- **BHF/002/2025, National Day Proclamation:** dated 5 June 2025; it identifies 5 June as the Federation's inception and establishes it as an annual National Day. [S2]
- **BHF/003/2025, Founding Proclamation:** dated 5 June 2025; it declares the Federation formally established, names itself the founding act, states the foundation date and National Day, and sets four values: clarity of thought, ethical governance, dignity of individual existence, and collective peace. The Archive.org description uses “The Bhoomi Foundation,” while the PDF says “Bhoomi Federation”; the portal follows the PDF for the document title and records the metadata discrepancy. [S3]
- **BHF/004/2025, Citizens (Bhoomians), Executive Order No. 1:** dated 6 June 2025; it designates people granted citizenship under the Federation's legal and administrative framework as Bhoomians. It does not itself define eligibility or a grant process. [S4]
- **BHF/005/2025, Adoption of the Official National Calendar:** dated 7 June 2025; the PDF specifies Monday–Friday as working days, weekends as non-working days, and June 5 as the sole public holiday, with immediate effect. The “Executive Order 2” label appears in Archive.org metadata, not in the PDF title. The annual recurrence of National Day is stated in BHF/002 and BHF/003, not BHF/005. [S5]

The sequence is BHF/001 on 4 June; BHF/002 and BHF/003 both on 5 June; BHF/004 on 6 June; and BHF/005 on 7 June. The records do not specify the order of BHF/002 and BHF/003 within 5 June. The one-day-before-founding flag proclamation says it takes immediate effect and becomes a founding document; do not invent an hour-by-hour order.

The founding record says Bhoomi is not defined by geographic borders. The reviewed primary records provide no territory, capital, real-world statehood, or international recognition. The earlier names “Republic of Harmonia” and “Melvin Welfare Dominion” are supplied as research leads in the brief but were not found in the reviewed site pages or five records. Show them only in an explicitly unresolved research note, not as a verified timeline.

The old site's About page describes dignity, justice, and welfare; its homepage also promotes ethical governance, universal welfare, and philosophical leadership “without the chaos of elections.” These are legacy public statements, not a detailed constitutional or welfare programme. The old citizenship page said citizenship was not then being issued and offered a waitlist; the portal may cite this as a dated legacy-site statement, not as a current application status. The old Offerings and Contact routes display a missing-page message and must not be treated as active institutional pages.

## 4. Rights and document handling

The five Archive.org records list CC BY-NC-ND 4.0. This listing is platform metadata and does not independently establish that the uploader was authorized to grant the licence. Before mirroring a PDF, record the basis that redistribution is permitted. If that basis cannot be supported, show the document's metadata and link to its Archive.org record without hosting a copy. If a PDF is mirrored, preserve the original bytes, filename where practical, and licence/attribution information; do not edit, recompress, OCR-overwrite, or otherwise create a derivative. The site's own summaries and metadata are new material and must not be presented as replacements for the originals.

## 5. Information architecture

Use a small, multi-page static site with these public routes:

- `/` — Home: country name, fictional status, founding date, four documented values, short source-backed introduction, and direct links to History, Documents, and Calendar. No unsupported live statistics or simulated clock.
- `/about/` — About & History: a sourced chronology, the early public vision, the documented founding values, and a visibly separate “unverified / unresolved” note for gaps. Do not invent a continuous history between records.
- `/documents/` — Official Documents: all five record entries, searchable by title/number and filterable by year, type, and issuing authority. The complete list must remain readable without JavaScript; search/filter controls may progressively enhance it.
- `/documents/bhf-001-2025/` through `/documents/bhf-005-2025/` — individual record pages with the title, number, date, document type, issuing authority as printed, neutral description, source status, any licence note, Archive.org item link, and a download/preview only if permitted.
- `/calendar/` — National Calendar: the stated weekday/weekend and public-holiday rules with direct citations to BHF/002 and BHF/005; explain the difference between National Day's annual recurrence and BHF/005's wording.
- `/sources/` — Sources and provenance: source inventory, evidence status definitions, licensing caveat, and the difference between primary records, legacy site material, and unresolved claims.

If a route is unavailable in the local preview, verify its GitHub Pages-compatible output and correct base path before release. Do not add placeholder pages for out-of-scope systems; the navigation should say what exists now.

## 6. Content data and provenance

Store record metadata and source-backed canon in structured, human-editable local data (JSON is preferred). Each canon claim must carry a stable identifier, concise claim text, status, source URL, and a note where evidence conflicts or is incomplete. At minimum, statuses distinguish:

- `primary_record` — stated by a reviewed original document.
- `legacy_site` — stated by the former public website, without implying legal force.
- `metadata_only` — shown in Archive.org metadata but not supported by the document text.
- `unresolved` — conflicting, incomplete, or not yet source-supported.

Each document record must retain title as printed, number, issue date, type, issuing authority as printed, summary, canonical source URL, Archive.org item URL, Archive.org file URL if known, displayed licence, redistribution decision, and uncertainty notes. Do not derive new legal status from the page design or database field. No document may be labelled “currently in force” unless that status is supported by a defined national legal framework; Phase 1 contains no such new framework.

## 7. Visual and interaction design

Use a restrained civic/editorial identity: clear typography, strong hierarchy, readable measure, calm neutral surfaces, and limited blue/green accents informed by the documented flag colors. These are website design choices, not additional official national symbols. Until the exact green discrepancy is resolved, do not claim an exact brand or flag color code. Use a typographic wordmark only. No invented emblem, lotus, shield, star, animal, or seal.

Keep the interface lightweight and usable on phone and desktop. Use semantic HTML, keyboard-operable navigation and filters, visible focus, sufficient text contrast, descriptive page titles, a skip link, logical headings, reduced-motion support, and labels/status text that do not rely on color alone. Prefer local assets and system fonts; avoid remote font or icon dependencies. The document list should still expose all five records if scripts fail.

Create the repository social-preview image at GitHub's supported preview dimensions, using the same restrained typographic direction and a neutral landscape motif. Until the flag discrepancy is resolved, do not use a flag or claim that a color treatment is an official national identity. The image is a visual asset, not a new national symbol.

## 8. Technical approach

Build with plain HTML, CSS, JavaScript, and JSON, without a framework or bundler in Phase 1. Use a small shared stylesheet and minimal progressive-enhancement JavaScript for document search/filtering. Keep content and presentation separate. Internal links and assets must work under the repository project path `/Bhoomi-Federation/`; test production paths rather than assuming domain-root deployment. Do not use server-side rendering, backend services, cookies, tracking, external APIs, credentials, or visitor-controlled state.

## 9. Acceptance criteria

Phase 1 is ready to release only when:

1. Every displayed historical fact has an explicit source/status and no unverified claim is presented as established canon.
2. All five source records have complete metadata matching the original PDF; discrepancies and unknowns are visible.
3. No exact flag rendering is presented until the green discrepancy has been resolved from the original visual record.
4. No original PDF is redistributed without a recorded, supportable rights basis; any hosted original is unchanged and passes a byte comparison to the source file.
5. Search/filter works when JavaScript is available; the full document list and source links remain available without it.
6. All internal routes, CSS/JS/data assets, Archive.org links, and permitted document links work at the GitHub Pages project base path.
7. The portal clearly identifies Bhoomi as fictional and does not imply actual statehood, recognition, officeholders, institutions, or live simulation.
8. Keyboard navigation, focus visibility, mobile layout, text contrast, heading structure, and reduced-motion behavior receive automated and manual checks.
9. The published Pages site is checked after deployment; no deployment claim is made before the route checks pass.
10. The GitHub social-preview image is present at the intended dimensions, has no unverified official symbol, and is ready to select in repository settings.

## 10. Decisions reserved for later phases

A later, separately reviewed nation-building blueprint may establish new constitutional, governmental, legal, social, geographic, economic, and simulation canon. It must assign dates, document numbers, legal authority, and provenance without retroactively altering 2025 history. A later implementation plan may then build those systems against the approved framework. This Phase 1 spec authorizes neither that new canon nor a simulation.

## Sources

- [S1] [Flag Adoption Proclamation — Archive.org item](https://archive.org/details/flag-adoption-proclamation) · [PDF](https://archive.org/download/flag-adoption-proclamation/Flag%20Adoption%20Proclamation.pdf)
- [S2] [National Day Proclamation — Archive.org item](https://archive.org/details/national-day-proclamation) · [PDF](https://archive.org/download/national-day-proclamation/National%20Day%20Proclamation.pdf)
- [S3] [Founding Proclamation — Archive.org item](https://archive.org/details/founding-proclamation) · [PDF](https://archive.org/download/founding-proclamation/Founding%20Proclamation.pdf)
- [S4] [BHF/004/2025 — Archive.org item](https://archive.org/details/004-2025-citizens-bhoomians-executive-order-1) · [PDF](https://archive.org/download/004-2025-citizens-bhoomians-executive-order-1/004-2025%20Citizens%20-%20Bhoomians%20Executive%20Order%201.pdf)
- [S5] [BHF/005/2025 — Archive.org item](https://archive.org/details/005-2025-national-calendar-executive-order-2) · [PDF](https://archive.org/download/005-2025-national-calendar-executive-order-2/005-2025%20National%20Calendar%20Executive%20Order%202.pdf)
- [L1] [Bhoomi Federation home page](https://bhoomi.rf.gd/)
- [L2] [Bhoomi Federation About page](https://bhoomi.rf.gd/about/)
- [L3] [Become a Citizen page](https://bhoomi.rf.gd/become-a-citizen/)
- [L4] [Bhoomi sitemap](https://bhoomi.rf.gd/wp-sitemap.xml)
- [R1] [Bhoomi Federation GitHub repository](https://github.com/melvinvarghese/Bhoomi-Federation)
- [R2] [GitHub Pages site](https://melvinvarghese.github.io/Bhoomi-Federation/)

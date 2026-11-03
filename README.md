# Bhoomi Federation

A static, source-led project site. Its original 2025 records are preserved as a documentary archive; later fictional additions are dated and stored separately so they cannot be mistaken for historical documents.

## Content map

- `data/documents.json` and `documents/`: the five original records from 2025, their source links and uncertainty notes.
- `data/claims.json` and `sources/`: historical claim evidence and the source inventory.
- `data/canon.json`, `canon/` and `foundations/`: four new fictional canon records dated 3 November 2026, with constitutional, government, legal-order and citizenship foundations. They have no real-world legal effect and do not claim statehood or recognition.
- `docs/constitutional-references.md`: the comparative primary-source research and design trade-offs behind the new fictional foundations.

The site uses plain HTML, CSS and JSON at the project base path `/Bhoomi-Federation/`. The additions reuse the existing page shell and styles; no server or new dependency is required.

## Checks

Run the full Python acceptance suite and the Node document-filter tests from the repository root:

```sh
python3 -m unittest discover -s tests -v
node --test tests/documents.test.mjs
```

# The Bhoomi Federation

Official website of The Bhoomi Federation.

## National information

- `index.html`, `about/`, and `calendar/`: national information, history, and calendar.
- `documents/`: National Records, with the five records issued in 2025 and constitutional records issued in 2026.
- `foundations/`: Constitution, government, public law, and citizenship.
- `data/documents.json`: the 2025 record details used by the National Records filters.

The static site is served from `/Bhoomi-Federation/`.

## Checks

Run the Python acceptance suite and Node record-filter tests from the repository root:

```sh
python3 -m unittest discover -s tests -v
node --test tests/documents.test.mjs
```

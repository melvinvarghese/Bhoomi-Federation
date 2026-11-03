"""Behavioral checks for Phase 1 source and document data."""

import json
import re
import struct
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

EXPECTED_DOCUMENTS = [
    ("BHF/001/2025", "2025-06-04", "Flag Adoption Proclamation"),
    ("BHF/002/2025", "2025-06-05", "National Day Proclamation"),
    ("BHF/003/2025", "2025-06-05", "Founding Proclamation"),
    (
        "BHF/004/2025",
        "2025-06-06",
        "On the Official Designation of Citizens of the Bhoomi Federation",
    ),
    (
        "BHF/005/2025",
        "2025-06-07",
        "Adoption of the Official National Calendar",
    ),
]

EXPECTED_URLS = {
    "BHF/001/2025": (
        "https://archive.org/details/flag-adoption-proclamation",
        "https://archive.org/download/flag-adoption-proclamation/Flag%20Adoption%20Proclamation.pdf",
    ),
    "BHF/002/2025": (
        "https://archive.org/details/national-day-proclamation",
        "https://archive.org/download/national-day-proclamation/National%20Day%20Proclamation.pdf",
    ),
    "BHF/003/2025": (
        "https://archive.org/details/founding-proclamation",
        "https://archive.org/download/founding-proclamation/Founding%20Proclamation.pdf",
    ),
    "BHF/004/2025": (
        "https://archive.org/details/004-2025-citizens-bhoomians-executive-order-1",
        "https://archive.org/download/004-2025-citizens-bhoomians-executive-order-1/004-2025%20Citizens%20-%20Bhoomians%20Executive%20Order%201.pdf",
    ),
    "BHF/005/2025": (
        "https://archive.org/details/005-2025-national-calendar-executive-order-2",
        "https://archive.org/download/005-2025-national-calendar-executive-order-2/005-2025%20National%20Calendar%20Executive%20Order%202.pdf",
    ),
}

REQUIRED_DOCUMENT_FIELDS = {
    "number",
    "title",
    "issue_date",
    "document_type",
    "issuing_authority",
    "summary",
    "canonical_source_url",
    "archive_item_url",
    "archive_file_url",
    "displayed_license",
    "redistribution_decision",
    "uncertainty_notes",
}

ALLOWED_CLAIM_STATUSES = {
    "primary_record",
    "legacy_site",
    "metadata_only",
    "unresolved",
}

EXPECTED_SOURCE_IDS = {
    "S1", "S2", "S3", "S4", "S5",
    "L1", "L2", "L3", "L4",
    "R1", "R2", "P1",
}

REQUIRED_CLAIM_IDS = {
    "C-FOUNDING-DATE",
    "C-NATIONAL-DAY",
    "C-VALUES",
    "C-FLAG-ADOPTION",
    "C-CITIZEN-DESIGNATION",
    "C-CALENDAR-RULES",
    "C-LEGACY-VISION",
    "C-EARLIER-NAMES",
}

EXPECTED_VALUES = (
    "clarity of thought",
    "ethical governance",
    "dignity of individual existence",
    "collective peace",
)

PROJECT_BASE = "/Bhoomi-Federation/"
EXPECTED_NAVIGATION = {
    "/Bhoomi-Federation/": "Home",
    "/Bhoomi-Federation/about/": "About & History",
    "/Bhoomi-Federation/documents/": "Official Documents",
    "/Bhoomi-Federation/calendar/": "National Calendar",
    "/Bhoomi-Federation/sources/": "Sources & Provenance",
}


class PageMarkup(HTMLParser):
    """Collect observable page semantics and route boundaries without a parser dependency."""

    def __init__(self):
        super().__init__()
        self.lang = None
        self.title = []
        self.body_text = []
        self.headings = []
        self.h1_count = 0
        self.skip_link = False
        self.ids = []
        self.labels = []
        self.live_region_ids = []
        self.nav_depth = 0
        self.nav_links = {}
        self.hrefs = []
        self.srcs = []
        self.claim_ids = []
        self.document_numbers = []
        self.tags = []
        self.datetime_values = []
        self.hidden_ids = []
        self.document_cards = []
        self.current_document_card = None
        self.collect_card_title = False
        self.source_links = set()
        self.source_anchors = set()
        self.heading_stack = []
        self.collect_title = False
        self.collect_heading = False

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        self.tags.append(tag)
        if tag == "time" and attributes.get("datetime"):
            self.datetime_values.append(attributes["datetime"])
        if "hidden" in attributes and attributes.get("id"):
            self.hidden_ids.append(attributes["id"])
        if tag == "html":
            self.lang = attributes.get("lang")
        if attributes.get("id"):
            self.ids.append(attributes["id"])
        if tag == "label" and attributes.get("for"):
            self.labels.append(attributes["for"])
        if attributes.get("role") == "status" or attributes.get("aria-live"):
            if attributes.get("id"):
                self.live_region_ids.append(attributes["id"])
        if tag == "title":
            self.collect_title = True
        if tag in {"h1", "h2", "h3"}:
            if tag == "h1":
                self.h1_count += 1
            self.heading_stack.append(tag)
            self.headings.append([tag, ""])
            self.collect_heading = True
        if tag == "nav":
            self.nav_depth += 1
        if tag == "a":
            href = attributes.get("href")
            if href:
                self.hrefs.append(href)
                if href.startswith(PROJECT_BASE + "sources/#"):
                    self.source_links.add(href.rsplit("#", 1)[1])
                if self.nav_depth:
                    self.nav_links[href] = ""
            if attributes.get("id") == "skip-link" and href == "#main":
                self.skip_link = True
        src = attributes.get("src")
        if src:
            self.srcs.append(src)
        claim_id = attributes.get("data-claim-id")
        if claim_id:
            self.claim_ids.append(claim_id)
        document_number = attributes.get("data-document-number")
        if document_number:
            self.document_numbers.append(document_number)
            self.current_document_card = {
                "number": document_number,
                "title": "",
                "issue_date": None,
                "document_type": attributes.get("data-document-type"),
                "issuing_authority": attributes.get("data-document-authority"),
            }
            self.document_cards.append(self.current_document_card)
        if tag == "h2" and self.current_document_card is not None:
            self.collect_card_title = True
        if tag == "time" and self.current_document_card is not None:
            self.current_document_card["issue_date"] = attributes.get("datetime")
        if tag in {"section", "article", "div"} and attributes.get("id", "").startswith(("S", "L", "R", "P")):
            self.source_anchors.add(attributes["id"])

    def handle_endtag(self, tag):
        if tag == "title":
            self.collect_title = False
        if tag in {"h1", "h2", "h3"} and self.heading_stack:
            self.heading_stack.pop()
            self.collect_heading = bool(self.heading_stack)
        if tag == "nav" and self.nav_depth:
            self.nav_depth -= 1
        if tag == "h2":
            self.collect_card_title = False
        if tag == "li" and self.current_document_card is not None:
            self.current_document_card = None

    def handle_data(self, data):
        text = data.strip()
        if not text:
            return
        self.body_text.append(text)
        if self.collect_title:
            self.title.append(text)
        if self.collect_heading and self.headings:
            self.headings[-1][1] += text
        if self.collect_card_title and self.current_document_card is not None:
            self.current_document_card["title"] += text
        if self.nav_depth and self.nav_links:
            last_href = next(reversed(self.nav_links))
            if not self.nav_links[last_href]:
                self.nav_links[last_href] = text


def parse_page(path):
    parser = PageMarkup()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


class PhaseOneDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.documents = json.loads((DATA / "documents.json").read_text(encoding="utf-8"))
        cls.claims = json.loads((DATA / "claims.json").read_text(encoding="utf-8"))
        cls.sources = json.loads((DATA / "sources.json").read_text(encoding="utf-8"))
        cls.documents_by_number = {item["number"]: item for item in cls.documents}
        cls.claims_by_id = {item["id"]: item for item in cls.claims}
        cls.sources_by_id = {item["id"]: item for item in cls.sources}

    def test_five_original_records_keep_printed_titles_and_dates(self):
        actual = [
            (record["number"], record["issue_date"], record["title"])
            for record in self.documents
        ]
        self.assertEqual(actual, EXPECTED_DOCUMENTS)

    def test_each_record_links_to_its_expected_archive_item_and_pdf(self):
        for number, (item_url, file_url) in EXPECTED_URLS.items():
            with self.subTest(number=number):
                record = self.documents_by_number[number]
                self.assertEqual(record["archive_item_url"], item_url)
                self.assertEqual(record["archive_file_url"], file_url)
                self.assertEqual(record["canonical_source_url"], file_url)

    def test_document_records_have_required_fields_and_link_only_rights_decision(self):
        self.assertEqual(len(self.documents), 5)
        for record in self.documents:
            with self.subTest(number=record["number"]):
                self.assertTrue(REQUIRED_DOCUMENT_FIELDS.issubset(record))
                self.assertTrue(record["displayed_license"].startswith("CC BY-NC-ND 4.0"))
                self.assertIn("Archive.org metadata", record["displayed_license"])
                self.assertEqual(record["redistribution_decision"], "link_only")
                self.assertTrue(record["uncertainty_notes"])
                self.assertNotEqual(record.get("legal_status"), "currently_in_force")
                self.assertNotEqual(record.get("status"), "currently_in_force")

    def test_claim_statuses_and_references_resolve_to_real_sources(self):
        self.assertTrue(REQUIRED_CLAIM_IDS.issubset(self.claims_by_id))
        self.assertEqual(set(self.sources_by_id), EXPECTED_SOURCE_IDS)
        self.assertEqual(len(self.sources), 12)
        for claim in self.claims:
            with self.subTest(claim=claim["id"]):
                self.assertIn(claim["status"], ALLOWED_CLAIM_STATUSES)
                self.assertTrue(claim["source_ids"])
                self.assertTrue(claim["uncertainty_note"])
                for source_id in claim["source_ids"]:
                    self.assertIn(source_id, self.sources_by_id)
        for source in self.sources:
            with self.subTest(source=source["id"]):
                self.assertTrue({"id", "title", "kind", "url", "limitation"}.issubset(source))
                self.assertTrue(source["limitation"])

    def test_founding_values_match_the_original_document(self):
        text = self.claims_by_id["C-VALUES"]["text"].casefold()
        for value in EXPECTED_VALUES:
            with self.subTest(value=value):
                self.assertIn(value, text)

    def test_calendar_claim_keeps_workweek_and_holiday_wording(self):
        text = self.claims_by_id["C-CALENDAR-RULES"]["text"].casefold()
        for phrase in ("monday", "friday", "saturday", "sunday", "5 june", "sole"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_calendar_claim_and_document_summary_include_office_closure(self):
        claim = self.claims_by_id["C-CALENDAR-RULES"]["text"].casefold()
        summary = self.documents_by_number["BHF/005/2025"]["summary"].casefold()
        for text in (claim, summary):
            self.assertIn("government offices", text)
            self.assertIn("remain closed", text)

    def test_annual_national_day_recurrence_is_not_attributed_to_calendar_order(self):
        claim = self.claims_by_id["C-NATIONAL-DAY"]
        self.assertEqual(set(claim["source_ids"]), {"S2", "S3"})
        self.assertNotIn("S5", claim["source_ids"])

    def test_flag_color_conflict_is_preserved_as_uncertainty(self):
        claim = self.claims_by_id["C-FLAG-ADOPTION"]
        note = claim["uncertainty_note"].casefold()
        self.assertIn("#008a45", note)
        self.assertIn("#008445", note)
        self.assertEqual(claim["status"], "primary_record")

    def test_same_day_order_and_archive_metadata_labels_stay_unresolved(self):
        founding = " ".join(self.documents_by_number["BHF/003/2025"]["uncertainty_notes"]).casefold()
        calendar = " ".join(self.documents_by_number["BHF/005/2025"]["uncertainty_notes"]).casefold()
        self.assertIn("archive.org", founding)
        self.assertIn("both dated 5 june 2025", founding)
        self.assertIn("order within that date is not stated", founding)
        self.assertIn("executive order 2", calendar)
        self.assertIn("metadata", calendar)

    def test_citizenship_claim_does_not_invent_eligibility_or_process(self):
        claim = self.claims_by_id["C-CITIZEN-DESIGNATION"]
        note = claim["uncertainty_note"].casefold()
        self.assertIn("eligibility", note)
        self.assertIn("process", note)


class PhaseOnePageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = {
            "/Bhoomi-Federation/": ROOT / "index.html",
            "/Bhoomi-Federation/about/": ROOT / "about/index.html",
            "/Bhoomi-Federation/documents/": ROOT / "documents/index.html",
            "/Bhoomi-Federation/calendar/": ROOT / "calendar/index.html",
            "/Bhoomi-Federation/sources/": ROOT / "sources/index.html",
        }
        cls.claims = json.loads((DATA / "claims.json").read_text(encoding="utf-8"))
        cls.claims_by_id = {item["id"]: item for item in cls.claims}
        cls.documents = json.loads((DATA / "documents.json").read_text(encoding="utf-8"))
        for record in cls.documents:
            slug = record["number"].replace("/", "-").casefold()
            cls.pages[f"{PROJECT_BASE}documents/{slug}/"] = ROOT / "documents" / slug / "index.html"

    def test_core_pages_have_accessible_shared_shell_and_project_navigation(self):
        for route, path in self.pages.items():
            with self.subTest(route=route):
                self.assertTrue(path.is_file(), f"Missing route file for {route}")
                page = parse_page(path)
                self.assertTrue(page.title, "Page title must not be empty")
                self.assertEqual(page.lang, "en")
                self.assertEqual(page.h1_count, 1)
                self.assertTrue(page.skip_link)
                self.assertIn("main", page.tags)
                self.assertIn("header", page.tags)
                self.assertIn("footer", page.tags)
                self.assertEqual(page.nav_links, EXPECTED_NAVIGATION)

    def test_every_project_base_link_and_local_asset_resolves_inside_repository(self):
        parsed_pages = {path: parse_page(path) for path in self.pages.values() if path.is_file()}
        for route, path in self.pages.items():
            with self.subTest(route=route):
                self.assertTrue(path.is_file(), f"Missing route file for {route}")
                page = parsed_pages[path]
                for target in [*page.hrefs, *page.srcs]:
                    if not target.startswith(PROJECT_BASE):
                        continue
                    parsed = urlsplit(target)
                    relative = parsed.path.removeprefix(PROJECT_BASE)
                    target_path = ROOT / relative
                    if not relative or relative.endswith("/") or not target_path.suffix:
                        target_path = target_path / "index.html"
                    self.assertTrue(target_path.is_file(), f"{route} links to missing {target}")
                    if parsed.fragment:
                        target_page = parsed_pages.get(target_path)
                        if target_page:
                            self.assertIn(parsed.fragment, target_page.ids, f"{target} has no matching anchor")

    def test_filter_controls_are_labeled_and_results_have_a_polite_live_region(self):
        page = parse_page(self.pages["/Bhoomi-Federation/documents/"])
        self.assertTrue({"document-search", "document-year", "document-type", "document-authority"}.issubset(page.labels))
        self.assertIn("document-results-status", page.live_region_ids)

    def test_public_pages_link_to_archive_items_not_direct_pdf_files(self):
        for route, path in self.pages.items():
            with self.subTest(route=route):
                page = parse_page(path)
                download_links = [
                    href
                    for href in page.hrefs
                    if "/download/" in urlsplit(href).path.casefold()
                    or urlsplit(href).path.casefold().endswith(".pdf")
                ]
                self.assertEqual(download_links, [])

    def test_same_day_order_note_cites_both_primary_records(self):
        html = (ROOT / "documents" / "index.html").read_text(encoding="utf-8")
        claim = re.search(r'<div\s+data-claim-id="C-FOUNDING-DATE"[^>]*>.*?</div>', html, re.DOTALL)
        self.assertIsNotNone(claim)
        cited_sources = set(re.findall(r'href="/Bhoomi-Federation/sources/#([^"]+)"', claim.group()))
        self.assertTrue({"S2", "S3"}.issubset(cited_sources))

    def test_css_contrast_and_reduced_motion_meet_release_thresholds(self):
        css = (ROOT / "assets" / "css" / "site.css").read_text(encoding="utf-8")
        tokens = dict(re.findall(r"--color-([a-z-]+):\s*(#[0-9a-fA-F]{6})", css))

        def luminance(color):
            channels = [int(color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
            linear = [value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4 for value in channels]
            return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]

        def contrast(foreground, background):
            lighter, darker = sorted((luminance(foreground), luminance(background)), reverse=True)
            return (lighter + 0.05) / (darker + 0.05)

        surface = tokens["surface"]
        for token in ("text", "muted", "link"):
            with self.subTest(color=token):
                self.assertGreaterEqual(contrast(tokens[token], surface), 4.5)
        self.assertGreaterEqual(contrast(tokens["focus"], surface), 3.0)
        self.assertIn("@media (prefers-reduced-motion: reduce)", css)
        self.assertIn("scroll-behavior: auto", css)

    def test_every_factual_claim_has_a_known_id_and_visible_source_citations(self):
        for route, path in self.pages.items():
            if not path.exists():
                continue
            with self.subTest(route=route):
                page = parse_page(path)
                for claim_id in page.claim_ids:
                    self.assertIn(claim_id, self.claims_by_id)
                    required_sources = set(self.claims_by_id[claim_id]["source_ids"])
                    self.assertTrue(required_sources.issubset(page.source_links))

    def test_home_discloses_fictional_status_and_shows_founding_date_and_values(self):
        page = parse_page(self.pages[PROJECT_BASE])
        text = " ".join(page.body_text).casefold()
        self.assertIn("fictional", text)
        self.assertIn("5 june 2025", text)
        for value in EXPECTED_VALUES:
            with self.subTest(value=value):
                self.assertIn(value, text)

    def test_home_historical_overview_rows_have_claim_tags_and_citations(self):
        page = parse_page(self.pages[PROJECT_BASE])
        self.assertTrue(
            {
                "C-FOUNDING-DATE",
                "C-VALUES",
                "C-FLAG-ADOPTION",
                "C-NATIONAL-DAY",
                "C-CALENDAR-RULES",
            }.issubset(page.claim_ids)
        )
        self.assertTrue({"S1", "S2", "S3", "S5"}.issubset(page.source_links))

    def test_about_separates_unresolved_research_leads_from_verified_history(self):
        page = parse_page(self.pages["/Bhoomi-Federation/about/"])
        headings = [text.casefold() for tag, text in page.headings]
        body = " ".join(page.body_text).casefold()
        self.assertTrue(any("unresolved" in heading for heading in headings))
        self.assertIn("republic of harmonia", body)
        self.assertIn("melvin welfare dominion", body)

    def test_calendar_states_only_recorded_workweek_and_cites_both_rules(self):
        page = parse_page(self.pages["/Bhoomi-Federation/calendar/"])
        text = " ".join(page.body_text).casefold()
        self.assertIn("monday", text)
        self.assertIn("friday", text)
        self.assertIn("saturday", text)
        self.assertIn("sunday", text)
        self.assertIn("sole public holiday", text)
        self.assertIn("government offices remain closed", text)
        self.assertIn("annual", text)
        self.assertTrue({"S2", "S3", "S5"}.issubset(page.source_links))

    def test_sources_page_defines_evidence_statuses_and_license_limit(self):
        page = parse_page(self.pages["/Bhoomi-Federation/sources/"])
        text = " ".join(page.body_text).casefold()
        for status in ALLOWED_CLAIM_STATUSES:
            with self.subTest(status=status):
                self.assertIn(status, text)
        self.assertIn("cc by-nc-nd 4.0", text)
        self.assertIn("does not independently establish", text)

    def test_documents_static_fallback_lists_all_records_and_archive_item_links(self):
        page = parse_page(self.pages["/Bhoomi-Federation/documents/"])
        self.assertEqual(
            set(page.claim_ids),
            {
                "C-FLAG-ADOPTION",
                "C-NATIONAL-DAY",
                "C-FOUNDING-DATE",
                "C-VALUES",
                "C-CITIZEN-DESIGNATION",
                "C-CALENDAR-RULES",
            },
        )
        self.assertTrue({"S1", "S2", "S3", "S4", "S5"}.issubset(page.source_links))
        expected_numbers = [record["number"] for record in self.documents]
        self.assertEqual(page.document_numbers, expected_numbers)
        self.assertEqual(
            page.document_cards,
            [
                {
                    "number": item["number"],
                    "title": item["title"],
                    "issue_date": item["issue_date"],
                    "document_type": item["document_type"],
                    "issuing_authority": item["issuing_authority"],
                }
                for item in self.documents
            ],
        )
        self.assertIn("primary record", " ".join(page.body_text).casefold())
        self.assertIn("document-filters", page.hidden_ids)
        self.assertIn("document-results-status", page.hidden_ids)
        for record in self.documents:
            with self.subTest(number=record["number"]):
                self.assertIn(record["number"], " ".join(page.body_text))
                self.assertIn(record["title"], " ".join(page.body_text))
                self.assertIn(record["archive_item_url"], page.hrefs)
                slug = record["number"].replace("/", "-").casefold()
                self.assertIn(f"/Bhoomi-Federation/documents/{slug}/", page.hrefs)

    def test_each_document_detail_page_matches_its_json_record_and_link_only_policy(self):
        for record in self.documents:
            slug = record["number"].replace("/", "-").casefold()
            route = f"/Bhoomi-Federation/documents/{slug}/"
            path = ROOT / "documents" / slug / "index.html"
            with self.subTest(number=record["number"]):
                self.assertTrue(path.is_file(), f"Missing detail route {route}")
                page = parse_page(path)
                text = " ".join(page.body_text)
                headings = [value for tag, value in page.headings if tag == "h1"]
                self.assertEqual(headings, [record["title"]])
                self.assertIn(record["number"], text)
                self.assertIn(record["issue_date"], page.datetime_values)
                self.assertIn(record["document_type"], text)
                self.assertIn(record["issuing_authority"], text)
                self.assertIn("Primary record", text)
                self.assertIn("CC BY-NC-ND 4.0", text)
                self.assertIn("does not independently establish uploader authority", text)
                self.assertIn(record["archive_item_url"], page.hrefs)
                self.assertNotIn(record["archive_file_url"], page.hrefs)
                self.assertFalse(any(href.lower().endswith(".pdf") for href in page.hrefs))

    def test_social_preview_has_expected_png_dimensions_and_size(self):
        path = ROOT / "assets" / "images" / "social-preview.png"
        self.assertTrue(path.is_file(), "The GitHub social preview should exist")
        image = path.read_bytes()
        self.assertEqual(image[:8], b"\x89PNG\r\n\x1a\n")
        width, height = struct.unpack(">II", image[16:24])
        self.assertEqual((width, height), (1280, 640))
        self.assertLess(len(image), 1024 * 1024)


if __name__ == "__main__":
    unittest.main()

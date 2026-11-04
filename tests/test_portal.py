"""Acceptance checks for the Bhoomi Federation public portal and national records."""

import json
import re
import struct
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
PROJECT_BASE = "/Bhoomi-Federation/"

EXPECTED_DOCUMENTS = [
    ("BHF/001/2025", "2025-06-04", "Flag Adoption Proclamation"),
    ("BHF/002/2025", "2025-06-05", "National Day Proclamation"),
    ("BHF/003/2025", "2025-06-05", "Founding Proclamation"),
    ("BHF/004/2025", "2025-06-06", "On the Official Designation of Citizens of the Bhoomi Federation"),
    ("BHF/005/2025", "2025-06-07", "Adoption of the Official National Calendar"),
]

EXPECTED_ITEM_URLS = {
    "BHF/001/2025": "https://archive.org/details/flag-adoption-proclamation",
    "BHF/002/2025": "https://archive.org/details/national-day-proclamation",
    "BHF/003/2025": "https://archive.org/details/founding-proclamation",
    "BHF/004/2025": "https://archive.org/details/004-2025-citizens-bhoomians-executive-order-1",
    "BHF/005/2025": "https://archive.org/details/005-2025-national-calendar-executive-order-2",
}

EXPECTED_VALUES = (
    "clarity of thought",
    "ethical governance",
    "dignity of individual existence",
    "collective peace",
)

EXPECTED_NAVIGATION = {
    "/Bhoomi-Federation/": "Home",
    "/Bhoomi-Federation/about/": "About & History",
    "/Bhoomi-Federation/documents/": "National Records",
    "/Bhoomi-Federation/calendar/": "National Calendar",
    "/Bhoomi-Federation/foundations/": "Constitution & Government",
    "/Bhoomi-Federation/economy/": "Economy",
}


class PageMarkup(HTMLParser):
    """Collect accessible page semantics and links without a parser dependency."""

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
        self.datetime_values = []
        self.hidden_ids = []
        self.document_cards = []
        self.current_document_card = None
        self.collect_title = False
        self.collect_heading = False
        self.collect_card_title = False
        self.heading_stack = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
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
                if self.nav_depth:
                    self.nav_links[href] = ""
            if attributes.get("id") == "skip-link" and href == "#main":
                self.skip_link = True
        if attributes.get("src"):
            self.srcs.append(attributes["src"])
        if attributes.get("data-document-number"):
            self.current_document_card = {
                "number": attributes["data-document-number"],
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


class PortalDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.documents = json.loads((DATA / "documents.json").read_text(encoding="utf-8"))

    def test_five_2025_records_keep_their_printed_titles_and_dates(self):
        actual = [(record["number"], record["issue_date"], record["title"]) for record in self.documents]
        self.assertEqual(actual, EXPECTED_DOCUMENTS)

    def test_2025_record_data_has_only_public_record_fields(self):
        expected_fields = {"number", "title", "issue_date", "document_type", "issuing_authority", "summary", "archive_item_url"}
        self.assertEqual(len(self.documents), 5)
        for record in self.documents:
            with self.subTest(number=record["number"]):
                self.assertEqual(set(record), expected_fields)
                self.assertEqual(record["archive_item_url"], EXPECTED_ITEM_URLS[record["number"]])
                self.assertIn("Melvin Varghese, Chief Architect, The Bhoomi Federation", record["issuing_authority"])

    def test_new_constitutional_records_remain_distinct_and_dated_in_2026(self):
        page = parse_page(ROOT / "documents" / "index.html")
        text = " ".join(page.body_text)
        self.assertIn("3 November 2026", text)
        self.assertIn("2026-11-03", page.datetime_values)
        for number, title in (
            ("BHF/006/2026", "Constitution of the Bhoomi Federation"),
            ("BHF/007/2026", "Federal Institutions and Accountability Act"),
            ("BHF/008/2026", "Public Law and Administration Act"),
            ("BHF/009/2026", "Citizenship and Identity Act"),
        ):
            with self.subTest(number=number):
                self.assertIn(number, text)
                self.assertIn(title, text)
        self.assertTrue(all(not date.startswith("2026") for _, date, _ in EXPECTED_DOCUMENTS))


class PortalPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.documents = json.loads((DATA / "documents.json").read_text(encoding="utf-8"))
        cls.pages = {
            PROJECT_BASE: ROOT / "index.html",
            f"{PROJECT_BASE}about/": ROOT / "about" / "index.html",
            f"{PROJECT_BASE}documents/": ROOT / "documents" / "index.html",
            f"{PROJECT_BASE}calendar/": ROOT / "calendar" / "index.html",
            f"{PROJECT_BASE}foundations/": ROOT / "foundations" / "index.html",
            f"{PROJECT_BASE}economy/": ROOT / "economy" / "index.html",
        }
        for record in cls.documents:
            slug = record["number"].replace("/", "-").casefold()
            cls.pages[f"{PROJECT_BASE}documents/{slug}/"] = ROOT / "documents" / slug / "index.html"
        cls.parsed_pages = {route: parse_page(path) for route, path in cls.pages.items() if path.is_file()}

    def test_core_pages_have_accessible_shared_shell_and_official_navigation(self):
        for route, path in self.pages.items():
            with self.subTest(route=route):
                self.assertTrue(path.is_file(), f"Missing route file for {route}")
                page = self.parsed_pages[route]
                self.assertTrue(page.title)
                self.assertEqual(page.lang, "en")
                self.assertEqual(page.h1_count, 1)
                self.assertTrue(page.skip_link)
                self.assertEqual(page.nav_links, EXPECTED_NAVIGATION)

    def test_old_navigation_routes_and_internal_notes_are_absent(self):
        self.assertFalse((ROOT / "canon" / "index.html").exists())
        self.assertFalse((ROOT / "sources" / "index.html").exists())
        self.assertFalse((ROOT / "data" / "sources.json").exists())
        self.assertFalse((ROOT / "data" / "claims.json").exists())
        self.assertFalse((ROOT / "data" / "canon.json").exists())
        self.assertFalse((ROOT / "docs").exists())

    def test_every_local_portal_link_resolves(self):
        parsed_by_path = {self.pages[route]: page for route, page in self.parsed_pages.items()}
        for route, page in self.parsed_pages.items():
            for target in [*page.hrefs, *page.srcs]:
                if not target.startswith(PROJECT_BASE):
                    continue
                parsed = urlsplit(target)
                relative = parsed.path.removeprefix(PROJECT_BASE)
                target_path = ROOT / relative
                if not relative or relative.endswith("/") or not target_path.suffix:
                    target_path = target_path / "index.html"
                self.assertTrue(target_path.is_file(), f"{route} links to missing {target}")
                if parsed.fragment and target_path in parsed_by_path:
                    self.assertIn(parsed.fragment, parsed_by_path[target_path].ids, f"{target} has no matching anchor")

    def test_home_shows_founding_date_values_and_national_records_link(self):
        page = self.parsed_pages[PROJECT_BASE]
        text = " ".join(page.body_text).casefold()
        self.assertIn("5 june 2025", text)
        self.assertIn(f"{PROJECT_BASE}documents/", page.hrefs)
        for value in EXPECTED_VALUES:
            with self.subTest(value=value):
                self.assertIn(value, text)

    def test_homepage_uses_corrected_banner_asset_without_unbuilt_sections(self):
        page = self.parsed_pages[PROJECT_BASE]
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        banner_path = f"{PROJECT_BASE}assets/images/homepage-banner.webp"
        banner_asset = ROOT / "assets" / "images" / "homepage-banner.webp"

        self.assertIn(banner_path, page.srcs)
        self.assertTrue(banner_asset.is_file())
        self.assertIn(
            'alt="The Bhoomi Federation banner with a vertical blue-white-green flag and only the areas Constitution &amp; Government, National Records, and National Calendar."',
            home,
        )
        self.assertNotRegex(
            " ".join(page.body_text).casefold(),
            r"\b(citizens|geography)\b",
        )

    def test_about_page_keeps_2025_national_history(self):
        page = self.parsed_pages[f"{PROJECT_BASE}about/"]
        text = " ".join(page.body_text).casefold()
        for phrase in ("4 june 2025", "5 june 2025", "6 june 2025", "7 june 2025", "bhoomians", "national day"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_calendar_preserves_workweek_holiday_and_annual_observance_facts(self):
        page = self.parsed_pages[f"{PROJECT_BASE}calendar/"]
        text = " ".join(page.body_text).casefold()
        for phrase in ("monday", "friday", "saturday", "sunday", "sole public holiday", "government offices remain closed", "annually"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)
        for number in ("bhf-002-2025", "bhf-003-2025", "bhf-005-2025"):
            self.assertIn(f"{PROJECT_BASE}documents/{number}/", page.hrefs)

    def test_national_records_lists_five_2025_and_four_2026_records(self):
        page = self.parsed_pages[f"{PROJECT_BASE}documents/"]
        text = " ".join(page.body_text)
        self.assertEqual([card["number"] for card in page.document_cards], [record[0] for record in EXPECTED_DOCUMENTS])
        for record in self.documents:
            with self.subTest(number=record["number"]):
                self.assertIn(record["title"], text)
                self.assertIn(record["issue_date"], page.datetime_values)
                self.assertIn(record["archive_item_url"], page.hrefs)
                slug = record["number"].replace("/", "-").casefold()
                self.assertIn(f"{PROJECT_BASE}documents/{slug}/", page.hrefs)
        for number, title in (
            ("BHF/006/2026", "Constitution of the Bhoomi Federation"),
            ("BHF/007/2026", "Federal Institutions and Accountability Act"),
            ("BHF/008/2026", "Public Law and Administration Act"),
            ("BHF/009/2026", "Citizenship and Identity Act"),
        ):
            with self.subTest(number=number):
                self.assertIn(number, text)
                self.assertIn(title, text)
        self.assertTrue({"document-search", "document-year", "document-type", "document-authority"}.issubset(page.labels))
        self.assertIn("document-results-status", page.live_region_ids)
        self.assertIn("document-filters", page.hidden_ids)

    def test_each_2025_record_page_matches_public_record_metadata(self):
        for record in self.documents:
            slug = record["number"].replace("/", "-").casefold()
            route = f"{PROJECT_BASE}documents/{slug}/"
            page = self.parsed_pages[route]
            text = " ".join(page.body_text)
            headings = [value for tag, value in page.headings if tag == "h1"]
            with self.subTest(number=record["number"]):
                self.assertEqual(headings, [record["title"]])
                self.assertIn(record["number"], text)
                self.assertIn(record["issue_date"], page.datetime_values)
                self.assertIn(record["document_type"], text)
                self.assertIn(record["issuing_authority"], text)
                self.assertIn(record["archive_item_url"], page.hrefs)
                self.assertIn(f"{PROJECT_BASE}documents/", page.hrefs)
                self.assertFalse(any(urlsplit(href).path.casefold().endswith(".pdf") for href in page.hrefs))

    def test_existing_visual_assets_remain_accessible_release_assets(self):
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
            self.assertGreaterEqual(contrast(tokens[token], surface), 4.5)
        self.assertGreaterEqual(contrast(tokens["focus"], surface), 3.0)
        self.assertIn("@media (prefers-reduced-motion: reduce)", css)
        self.assertIn("scroll-behavior: auto", css)
        preview = (ROOT / "assets" / "images" / "social-preview.png").read_bytes()
        self.assertEqual(preview[:8], b"\x89PNG\r\n\x1a\n")
        width, height = struct.unpack(">II", preview[16:24])
        self.assertEqual((width, height), (1280, 640))
        self.assertLess(len(preview), 1024 * 1024)


if __name__ == "__main__":
    unittest.main()

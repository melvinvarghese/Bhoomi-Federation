"""Acceptance checks for the public constitutional and government pages."""

import unittest
from html.parser import HTMLParser

from test_portal import PROJECT_BASE, ROOT, parse_page


EXPECTED_RECORDS = [
    ("BHF/006/2026", "Constitution of the Bhoomi Federation"),
    ("BHF/007/2026", "Federal Institutions and Accountability Act"),
    ("BHF/008/2026", "Public Law and Administration Act"),
    ("BHF/009/2026", "Citizenship and Identity Act"),
]

EXPECTED_MINISTRIES = [
    "Finance and Treasury",
    "Justice and Constitutional Affairs",
    "Public Administration and Federal Affairs",
    "Health and Social Development",
    "External Affairs and Cooperation",
    "Education",
    "Science",
    "Culture",
    "Economy",
    "Industry",
    "Trade",
    "Infrastructure",
    "Transport",
    "Public Works",
    "Environment",
    "Water",
    "Natural Resources",
]


class SectionMarkup(HTMLParser):
    """Collect text and semantic lists from one section of an HTML page."""

    def __init__(self, section_id):
        super().__init__()
        self.section_id = section_id
        self.section_depth = 0
        self.match_count = 0
        self.text = []
        self.list_groups = []
        self.list_headings = []
        self.list_stack = []
        self.current_item = None
        self.current_heading = None
        self.collecting_heading = False
        self.heading_parts = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "section":
            if self.section_depth:
                self.section_depth += 1
            elif attributes.get("id") == self.section_id:
                self.match_count += 1
                if self.match_count == 1:
                    self.section_depth = 1
            return
        if not self.section_depth:
            return
        if tag in {"h2", "h3"}:
            self.collecting_heading = True
            self.heading_parts = []
        if tag in {"ul", "ol"}:
            group = []
            self.list_groups.append(group)
            self.list_headings.append(self.current_heading)
            self.list_stack.append(group)
        elif tag == "li":
            self.current_item = []

    def handle_endtag(self, tag):
        if self.section_depth:
            if tag in {"h2", "h3"} and self.collecting_heading:
                self.current_heading = " ".join(" ".join(self.heading_parts).split())
                self.collecting_heading = False
            elif tag == "li" and self.current_item is not None:
                item_text = " ".join(" ".join(self.current_item).split())
                if self.list_stack:
                    self.list_stack[-1].append(item_text)
                self.current_item = None
            elif tag in {"ul", "ol"} and self.list_stack:
                self.list_stack.pop()
            elif tag == "section":
                self.section_depth -= 1

    def handle_data(self, data):
        if not self.section_depth:
            return
        text = " ".join(data.split())
        if not text:
            return
        self.text.append(text)
        if self.collecting_heading:
            self.heading_parts.append(text)
        if self.current_item is not None:
            self.current_item.append(text)

    @property
    def section_text(self):
        return " ".join(self.text)


def parse_section(path, section_id):
    markup = SectionMarkup(section_id)
    markup.feed(path.read_text(encoding="utf-8"))
    return markup


class ConstitutionalPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        records_path = ROOT / "documents" / "index.html"
        foundations_path = ROOT / "foundations" / "index.html"
        cls.records_page = parse_page(records_path) if records_path.is_file() else None
        cls.page = parse_page(foundations_path) if foundations_path.is_file() else None
        cls.constitution = parse_section(foundations_path, "constitution") if foundations_path.is_file() else None
        cls.government = parse_section(foundations_path, "government-directory") if foundations_path.is_file() else None

    def require_page(self):
        self.assertIsNotNone(self.page, f"Missing route file for {PROJECT_BASE}foundations/")
        return self.page

    def require_constitution(self):
        self.require_page()
        self.assertIsNotNone(self.constitution, "Missing Constitution section")
        return self.constitution

    def require_government(self):
        self.require_page()
        self.assertIsNotNone(self.government, "Missing Government and institutions section")
        return self.government

    def test_2026_constitutional_records_are_separately_dated(self):
        self.assertIsNotNone(self.records_page)
        records_text = " ".join(self.records_page.body_text)
        for number, title in EXPECTED_RECORDS:
            with self.subTest(number=number):
                self.assertIn(number, records_text)
                self.assertIn(title, records_text)
        self.assertIn("2026-11-03", self.records_page.datetime_values)
        self.assertEqual(self.require_page().datetime_values.count("2026-11-03"), 4)

    def test_constitution_does_not_claim_highest_law_during_founder_tenure(self):
        text = self.require_constitution().section_text.casefold()
        self.assertIn(
            "the constitution protects every person, allocates the powers of the federation, and guarantees self-government to its member units.",
            text,
        )
        self.assertNotIn("the constitution is the highest law of the federation", text)

    def test_chief_architect_is_founder_only_first_person_with_supreme_authority(self):
        text = self.require_government().section_text.casefold()
        for phrase in (
            "the founder alone may hold the chief architect position",
            "“first person”",
            "during the founder’s tenure",
            "supreme authority above the constitution and all institutions",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_office_stays_permanently_vacant_after_tenure_without_a_successor(self):
        text = self.require_government().section_text.casefold()
        for phrase in (
            "after the founder’s tenure ends",
            "the chief architect position is permanently vacant and cannot be held by anyone",
            "does not succeed to the chief architect position",
            "or become a successor head of country",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_assembly_supervises_under_constitution_and_pm_cabinet_model_remains(self):
        text = self.require_government().section_text.casefold()
        for phrase in (
            "the assembly supervises the nation collectively under the constitution",
            "the prime minister is chosen by the assembly",
            "remains in office only while it has confidence",
            "the cabinet is accountable to the assembly",
            "remain below the chief architect’s supreme authority",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_government_directory_lists_seventeen_distinct_ministries(self):
        government = self.require_government()
        ministries_lists = [
            group
            for heading, group in zip(getattr(government, "list_headings", []), government.list_groups)
            if heading == "Ministries"
        ]
        self.assertEqual(ministries_lists, [EXPECTED_MINISTRIES])
        text = government.section_text.casefold()
        for combined_name in (
            "education, science and culture",
            "economy, industry and trade",
            "infrastructure, transport and public works",
            "environment, water and natural resources",
        ):
            with self.subTest(combined_name=combined_name):
                self.assertNotIn(combined_name, text)
        self.assertNotIn("department", text)

    def test_government_section_occurs_exactly_once(self):
        self.assertEqual(getattr(self.require_government(), "match_count", 0), 1)

    def test_section_parser_does_not_combine_duplicate_target_sections(self):
        markup = SectionMarkup("government-directory")
        markup.feed(
            '<section id="government-directory"><h3>Government</h3><p>First section</p></section>'
            '<section id="government-directory"><h3>Duplicate</h3><p>Second section</p></section>'
        )
        self.assertEqual(markup.section_text, "Government First section")
        self.assertEqual(markup.match_count, 2)

    def test_section_parser_associates_lists_with_their_heading(self):
        markup = SectionMarkup("government-directory")
        markup.feed(
            '<section id="government-directory"><h3>Ministries</h3>'
            '<ul><li>Education</li></ul></section>'
        )
        self.assertEqual(getattr(markup, "list_headings", []), ["Ministries"])
        self.assertEqual(markup.list_groups, [["Education"]])

    def test_ministry_directory_does_not_claim_unapproved_powers(self):
        text = self.require_government().section_text.casefold()
        self.assertIn("ministries are established by statute and budget", text)
        self.assertIn("directory labels do not create ministries, powers, budgets, appointments, or authorities by themselves", text)

    def test_constitutional_and_citizenship_rules_remain_public(self):
        text = " ".join(self.require_page().body_text).casefold()
        for phrase in ("rights belong to every person", "courts are independent", "public register", "citizenship may pass by descent", "five years", "dual nationality is allowed", "cannot be lost if that would make a person stateless"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_2025_record_links_anchor_the_historical_values_and_demonym(self):
        page = self.require_page()
        self.assertIn(f"{PROJECT_BASE}documents/bhf-003-2025/", page.hrefs)
        self.assertIn(f"{PROJECT_BASE}documents/bhf-004-2025/", page.hrefs)


if __name__ == "__main__":
    unittest.main()

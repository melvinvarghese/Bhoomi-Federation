"""Acceptance checks for the public constitutional and government pages."""

import unittest

from test_portal import PROJECT_BASE, ROOT, parse_page


EXPECTED_RECORDS = [
    ("BHF/006/2026", "Constitution of the Bhoomi Federation"),
    ("BHF/007/2026", "Federal Institutions and Accountability Act"),
    ("BHF/008/2026", "Public Law and Administration Act"),
    ("BHF/009/2026", "Citizenship and Identity Act"),
]


class ConstitutionalPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        records_path = ROOT / "documents" / "index.html"
        foundations_path = ROOT / "foundations" / "index.html"
        cls.records_page = parse_page(records_path) if records_path.is_file() else None
        cls.page = parse_page(foundations_path) if foundations_path.is_file() else None

    def require_page(self):
        self.assertIsNotNone(self.page, f"Missing route file for {PROJECT_BASE}foundations/")
        return self.page

    def test_2026_constitutional_records_are_separately_dated(self):
        self.assertIsNotNone(self.records_page)
        records_text = " ".join(self.records_page.body_text)
        for number, title in EXPECTED_RECORDS:
            with self.subTest(number=number):
                self.assertIn(number, records_text)
                self.assertIn(title, records_text)
        self.assertIn("2026-11-03", self.records_page.datetime_values)
        self.assertEqual(self.require_page().datetime_values.count("2026-11-03"), 4)

    def test_chief_architect_is_the_non_elective_founder_head_of_country(self):
        text = " ".join(self.require_page().body_text).casefold()
        for phrase in ("chief architect", "head of country", "founder", "not elected or appointed"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_office_stays_vacant_after_tenure_without_a_successor(self):
        text = " ".join(self.require_page().body_text).casefold()
        self.assertIn("when the founder’s tenure ends", text)
        self.assertIn("the office remains vacant", text)
        self.assertIn("no successor head of country", text)

    def test_assembly_supervises_collectively_but_does_not_inherit_the_office(self):
        text = " ".join(self.require_page().body_text).casefold()
        for phrase in ("collective supervisory authority", "as a body", "not a successor head of country", "prime minister", "confidence", "cabinet", "independent courts"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

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

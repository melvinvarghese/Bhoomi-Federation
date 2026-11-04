"""Acceptance tests for the public Economy page and proposed tax Bill."""

import re
import unittest

try:
    from .test_portal import PROJECT_BASE, ROOT, parse_page
except ImportError:
    from test_portal import PROJECT_BASE, ROOT, parse_page


PAGE_PATH = ROOT / "economy" / "index.html"


class EconomyPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = parse_page(PAGE_PATH)
        cls.text = " ".join(cls.page.body_text).casefold()

    def test_bill_is_proposed_until_passage_and_publication(self):
        self.assertIn("annual income tax bill is proposed", self.text)
        self.assertIn("not yet in force", self.text)
        self.assertIn("both chambers", self.text)
        self.assertIn("public register", self.text)
        self.assertNotIn("annual income tax is in force", self.text)

    def test_tax_rate_and_exemptions_match_the_approved_rule(self):
        for phrase in (
            "10 per cent",
            "adult",
            "annual income",
            "a minor is exempt",
            "a student without a job is exempt",
            "if annual income is 10, tax would be 1",
            "if annual income is zero, no income tax would be due",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)

    def test_page_uses_the_current_publication_date_and_legal_order_link(self):
        self.assertIn("4 november 2026", self.text)
        self.assertIn("2026-11-04", self.page.datetime_values)
        self.assertIn(f"{PROJECT_BASE}foundations/#legal-order", self.page.hrefs)

    def test_page_does_not_leak_private_material_or_deferred_national_figures(self):
        self.assertFalse(any("/workspace/" in href or "Phase-3" in href for href in self.page.hrefs))
        self.assertNotRegex(self.text, r"\b(private framework|implementation plan|comparative sources|fictional project)\b")
        self.assertNotRegex(self.text, r"\b(?:GDP|population total|debt ceiling|currency code)\b")
        self.assertNotRegex(self.text, r"\b(?:tax authority|central bank|collection agency)\b")


if __name__ == "__main__":
    unittest.main()

"""Acceptance checks for the separate fictional foundations slice."""

import json
import unittest

from test_portal import DATA, PROJECT_BASE, ROOT, parse_page


EXPECTED_RECORDS = [
    ("BHF/006/2026", "Constitution of the Bhoomi Federation"),
    ("BHF/007/2026", "Federal Institutions and Accountability Act"),
    ("BHF/008/2026", "Public Law and Administration Act"),
    ("BHF/009/2026", "Citizenship and Identity Act"),
]


class FoundationCanonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        canon_path = DATA / "canon.json"
        cls.canon = json.loads(canon_path.read_text(encoding="utf-8")) if canon_path.is_file() else None
        cls.sources = json.loads((DATA / "sources.json").read_text(encoding="utf-8"))
        cls.documents = json.loads((DATA / "documents.json").read_text(encoding="utf-8"))
        cls.sources_by_id = {source["id"]: source for source in cls.sources}
        cls.original_numbers = {record["number"] for record in cls.documents}

    def test_new_canon_is_separate_dated_fiction_with_no_real_world_effect(self):
        self.assertIsNotNone(self.canon, "Missing data/canon.json")
        self.assertEqual(self.canon["edition_date"], "2026-11-03")
        self.assertIs(self.canon["fictional_only"], True)
        self.assertEqual(self.canon["real_world_legal_effect"], "none")
        self.assertEqual(
            [(record["number"], record["title"]) for record in self.canon["records"]],
            EXPECTED_RECORDS,
        )
        self.assertTrue(self.original_numbers.isdisjoint(record["number"] for record in self.canon["records"]))
        self.assertEqual(len(self.documents), 5)

    def test_each_canon_record_has_resolvable_provenance_and_framework_status(self):
        self.assertIsNotNone(self.canon, "Missing data/canon.json")
        required = {
            "number",
            "title",
            "issue_date",
            "document_type",
            "canon_status",
            "operational_status",
            "authority_note",
            "summary",
            "prior_record_numbers",
            "historical_source_ids",
            "design_reference_ids",
            "page_anchor",
        }
        all_numbers = self.original_numbers | {number for number, _ in EXPECTED_RECORDS}
        self.assertEqual(len(self.canon["records"]), 4)
        for record in self.canon["records"]:
            with self.subTest(number=record.get("number")):
                self.assertTrue(required.issubset(record))
                self.assertEqual(record["issue_date"], "2026-11-03")
                self.assertEqual(record["canon_status"], "new_fictional_canon")
                self.assertEqual(record["operational_status"], "framework_only")
                self.assertTrue(record["authority_note"])
                self.assertTrue(record["summary"])
                self.assertTrue(record["page_anchor"])
                self.assertTrue(set(record["prior_record_numbers"]).issubset(all_numbers))
                for source_id in record["historical_source_ids"] + record["design_reference_ids"]:
                    self.assertIn(source_id, self.sources_by_id)
                self.assertTrue(all(source_id.startswith("C") for source_id in record["design_reference_ids"]))
                serialized = json.dumps(record, ensure_ascii=False).casefold()
                for forbidden in ("melvin varghese", "founder_name", "tenure_end_date"):
                    self.assertNotIn(forbidden, serialized)

    def test_2025_historical_dataset_remains_separate_and_unchanged_in_shape(self):
        self.assertEqual([record["number"] for record in self.documents], [
            "BHF/001/2025",
            "BHF/002/2025",
            "BHF/003/2025",
            "BHF/004/2025",
            "BHF/005/2025",
        ])
        self.assertEqual({record["issue_date"] for record in self.documents}, {
            "2025-06-04", "2025-06-05", "2025-06-06", "2025-06-07"
        })


class FoundationPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        canon_path = ROOT / "canon" / "index.html"
        foundations_path = ROOT / "foundations" / "index.html"
        cls.canon_page = parse_page(canon_path) if canon_path.is_file() else None
        cls.foundations_page = parse_page(foundations_path) if foundations_path.is_file() else None
        cls.sources_page = parse_page(ROOT / "sources" / "index.html")
        cls.documents_page = parse_page(ROOT / "documents" / "index.html")

    def require_page(self, page, route):
        self.assertIsNotNone(page, f"Missing route file for {route}")
        return page

    def test_registry_shows_all_new_records_and_separates_them_from_2025_history(self):
        page = self.require_page(self.canon_page, f"{PROJECT_BASE}canon/")
        text = " ".join(page.body_text).casefold()
        for number, title in EXPECTED_RECORDS:
            with self.subTest(number=number):
                self.assertIn(number.casefold(), text)
                self.assertIn(title.casefold(), text)
        for phrase in ("new fictional canon", "not a 2025 record", "no real-world legal effect", "framework only"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)
        self.assertIn("/Bhoomi-Federation/documents/bhf-003-2025/", page.hrefs)
        self.assertIn("/Bhoomi-Federation/documents/bhf-004-2025/", page.hrefs)

    def test_chief_architect_is_founder_specific_and_never_has_a_successor(self):
        page = self.require_page(self.foundations_page, f"{PROJECT_BASE}foundations/")
        text = " ".join(page.body_text).casefold()
        for phrase in (
            "chief architect",
            "head of country",
            "founder",
            "not elected or appointed",
            "no end date",
            "remains vacant permanently",
            "no successor head of country",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)
        self.assertNotIn("federation convenor", text)
        self.assertNotIn("melvin varghese", text)

    def test_assembly_becomes_collective_supervisor_without_replacing_the_head_of_country(self):
        page = self.require_page(self.foundations_page, f"{PROJECT_BASE}foundations/")
        text = " ".join(page.body_text).casefold()
        for phrase in (
            "collective supervisory authority",
            "the assembly as a body",
            "not a successor head of country",
            "prime minister",
            "confidence",
            "cabinet",
            "independent institutions",
            "independent courts",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_new_pages_cite_historical_and_constitutional_sources(self):
        canon_page = self.require_page(self.canon_page, f"{PROJECT_BASE}canon/")
        foundations_page = self.require_page(self.foundations_page, f"{PROJECT_BASE}foundations/")
        expected_design_sources = {f"C{number}" for number in range(1, 7)}
        self.assertTrue(expected_design_sources.issubset(self.sources_page.source_anchors))
        self.assertTrue(expected_design_sources.issubset(foundations_page.source_links))
        self.assertTrue({"S3", "S4"}.issubset(foundations_page.source_links))
        self.assertTrue(expected_design_sources.issubset(canon_page.source_links))
        self.assertIn(f"{PROJECT_BASE}foundations/", canon_page.hrefs)

    def test_documents_page_links_to_the_separate_canon_registry(self):
        self.assertIn(f"{PROJECT_BASE}canon/", self.documents_page.hrefs)
        text = " ".join(self.documents_page.body_text).casefold()
        self.assertIn("2026", text)
        self.assertIn("separate fictional canon", text)

    def test_foundation_page_does_not_create_an_operational_citizenship_application(self):
        page = self.require_page(self.foundations_page, f"{PROJECT_BASE}foundations/")
        text = " ".join(page.body_text).casefold()
        self.assertIn("no live application", text)
        self.assertIn("no language or knowledge exam", text)
        self.assertIn("cannot be lost if that would make a person stateless", text)
        self.assertIn("appealed to an independent court", text)


if __name__ == "__main__":
    unittest.main()

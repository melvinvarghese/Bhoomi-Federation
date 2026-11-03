"""Behavioral checks for Phase 1 source and document data."""

import json
import unittest
from pathlib import Path


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


if __name__ == "__main__":
    unittest.main()

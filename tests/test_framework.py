import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_case import validate
from score_opportunity import calculate, band, WEIGHTS


class FrameworkTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "examples/industrial-compressor-case.json").read_text(encoding="utf-8"))

    def test_synthetic_case_is_valid(self):
        self.assertEqual(validate(self.data), [])

    def test_unknown_source_is_rejected(self):
        self.data["claims"][0]["source_ids"] = ["MISSING"]
        self.assertTrue(any("unknown source_id" in item for item in validate(self.data)))

    def test_synthetic_source_must_be_grade_d(self):
        self.data["sources"][0]["grade"] = "A"
        self.assertTrue(any("Synthetic source" in item for item in validate(self.data)))

    def test_score_range_is_enforced(self):
        self.data["opportunity_score"]["relevance"] = 6
        self.assertTrue(any("relevance" in item for item in validate(self.data)))

    def test_weighted_score(self):
        self.assertEqual(calculate({key: 5 for key in WEIGHTS}), 5.0)

    def test_invalid_score_rejected(self):
        scores = {key: 3 for key in WEIGHTS}
        scores["relevance"] = 0
        with self.assertRaises(ValueError):
            calculate(scores)

    def test_missing_dimension_rejected(self):
        scores = {key: 3 for key in WEIGHTS if key != "execution"}
        with self.assertRaises(ValueError):
            calculate(scores)

    def test_score_band(self):
        self.assertEqual(band(4.5), "Priority for validation; hard gates still apply")
        self.assertEqual(band(2.0), "Do not prioritize at this stage")


if __name__ == "__main__":
    unittest.main()

import sys
import unittest
from collections import Counter
from pathlib import Path

# Ensure local modules are importable when running from repo root.
THIS_DIR = Path(__file__).resolve().parent
ROOT_DIR = THIS_DIR.parent
sys.path.insert(0, str(THIS_DIR))
sys.path.insert(0, str(ROOT_DIR))

import generate_stimuli
import process_results


class ProcessResultsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.zip_path = THIS_DIR / "jatos_results_20251127094830.jrzip"
        cls.practice_path = ROOT_DIR / "experiment" / "stimuli_practice.json"
        cls.experimental_path = ROOT_DIR / "experiment" / "stimuli_experimental.json"

        cls.practice_lookup, cls.experimental_lookup = process_results.load_stimuli(
            cls.practice_path, cls.experimental_path
        )
        cls.df, _ = process_results.process_zip(
            cls.zip_path,
            cls.practice_lookup,
            cls.experimental_lookup,
            skip_missing_prolific=False,  # keep the test participant even without PROLIFIC_PID
        )

        cls.practice_spec, cls.control_spec = generate_stimuli.build_practice_and_controls()
        cls.critical_spec = generate_stimuli.build_critical_trials()
        cls.experimental_spec = cls.critical_spec + cls.control_spec

    def test_trial_counts_match_stimuli_files(self) -> None:
        self.assertEqual(
            len(self.df),
            len(self.practice_lookup) + len(self.experimental_lookup),
            "Total rows should equal total stimuli presented.",
        )
        self.assertEqual(
            len(self.df[self.df["SESSION"] == "PRACTICE"]),
            len(self.practice_lookup),
            "Practice trials count mismatch.",
        )
        self.assertEqual(
            len(self.df[self.df["SESSION"] == "EXPERIMENTAL"]),
            len(self.experimental_lookup),
            "Experimental trials count mismatch.",
        )

    def test_items_match_generation_spec(self) -> None:
        practice_items = set(self.df[self.df["SESSION"] == "PRACTICE"]["item"])
        expected_practice = {row["ITEM"] for row in self.practice_spec}
        self.assertSetEqual(practice_items, expected_practice)

        experimental_items = set(self.df[self.df["SESSION"] == "EXPERIMENTAL"]["item"])
        expected_experimental = {row["ITEM"] for row in self.experimental_spec}
        self.assertSetEqual(experimental_items, expected_experimental)

    def test_pair_type_counts_match_spec(self) -> None:
        expected = Counter(row["PAIR_TYPE"] for row in self.experimental_spec)
        actual = Counter(self.df[self.df["SESSION"] == "EXPERIMENTAL"]["pair_type"])
        self.assertEqual(actual, expected)

    def test_domain_counts_match_spec(self) -> None:
        expected = Counter(row["DOMAIN"] for row in self.experimental_spec)
        actual = Counter(self.df[self.df["SESSION"] == "EXPERIMENTAL"]["domain"])
        self.assertEqual(actual, expected)

    def test_conclusion_forms_match_spec(self) -> None:
        expected = Counter((row["PAIR_TYPE"], row["CONCLUSION_FORM"]) for row in self.experimental_spec)
        actual = Counter(
            (row["pair_type"], row["conclusion_form"])
            for row in self.df[self.df["SESSION"] == "EXPERIMENTAL"].to_dict("records")
        )
        self.assertEqual(actual, expected)

    def test_validate_counts_passes(self) -> None:
        # Should not raise
        process_results.validate_counts(self.df, self.practice_lookup, self.experimental_lookup)

    def test_stimulus_plaintext(self) -> None:
        samples = self.df["stimulus"].dropna().astype(str)
        self.assertTrue(len(samples) > 0)
        self.assertTrue(all(not s.strip().startswith("<") for s in samples))
        self.assertTrue(all("Premise:" in s and "Conclusion:" in s for s in samples))


if __name__ == "__main__":
    unittest.main()

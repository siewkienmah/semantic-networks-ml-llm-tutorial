"""Run from the repository root: python -m unittest discover -s tests -v."""

import unittest

from starter.semantic_network import UNKNOWN, lookup
from starter.ml_metrics import CONFUSION_MATRIX, accuracy, class_recall, macro_f1, split_counts
from starter.llm_safety import CASE, SAFE_DRAFT, UNSAFE_DRAFT, build_prompt, validate_draft


class SemanticNetworkTests(unittest.TestCase):
    def test_inherited_property(self):
        self.assertIs(lookup("Canary", "can_fly"), True)
        self.assertIs(lookup("Canary", "breathes"), True)

    def test_local_false_overrides_default(self):
        self.assertIs(lookup("Penguin", "can_fly"), False)

    def test_missing_property(self):
        self.assertEqual(lookup("Fish", "colour"), UNKNOWN)
        self.assertEqual(lookup("UnlistedDevice", "can_fly"), UNKNOWN)


class MLMetricsTests(unittest.TestCase):
    def test_split(self):
        self.assertEqual(split_counts(), (180, 60))

    def test_recall(self):
        for index, expected in enumerate([15 / 25, 2 / 6, 21 / 29]):
            self.assertAlmostEqual(class_recall(CONFUSION_MATRIX, index), expected)

    def test_accuracy(self):
        self.assertAlmostEqual(accuracy(CONFUSION_MATRIX), 38 / 60)

    def test_macro_f1(self):
        self.assertAlmostEqual(macro_f1(CONFUSION_MATRIX), (30 / 51 + 4 / 10 + 42 / 59) / 3)

    def test_majority_baseline(self):
        baseline = [[0, 0, 25], [0, 0, 6], [0, 0, 29]]
        self.assertAlmostEqual(accuracy(baseline), 29 / 60)
        self.assertAlmostEqual(macro_f1(baseline), (58 / 89) / 3)
        self.assertEqual(class_recall(baseline, 1), 0)

    def test_empty_counts(self):
        self.assertEqual(class_recall([[0]], 0), 0.0)
        self.assertEqual(accuracy([]), 0.0)
        self.assertEqual(macro_f1([]), 0.0)


class LLMSafetyTests(unittest.TestCase):
    def test_prompt_contains_evidence(self):
        prompt = build_prompt(CASE)
        self.assertIsInstance(prompt, str)
        for value in ["STN-042", "current_temperature_c", "dispatch_rebalancing_van"]:
            self.assertIn(value, prompt)
        # The instructions themselves require human review in answers.md.

    def test_safe_structured_draft(self):
        self.assertEqual(validate_draft(SAFE_DRAFT, CASE), {
            "unsupported_facts": [], "rejected_actions": [], "safe_to_show": True})

    def test_unknown_temperature_and_unsupported_action(self):
        self.assertEqual(validate_draft(UNSAFE_DRAFT, CASE), {
            "unsupported_facts": ["current_temperature_c"],
            "rejected_actions": ["close_station"], "safe_to_show": False})

    def test_changed_and_absent_facts(self):
        draft = {"facts": {"bikes_available": 99, "weather": "sunny"}, "actions": []}
        self.assertEqual(validate_draft(draft, CASE)["unsupported_facts"],
                         ["bikes_available", "weather"])
        self.assertIs(validate_draft(draft, CASE)["safe_to_show"], False)


if __name__ == "__main__":
    unittest.main()

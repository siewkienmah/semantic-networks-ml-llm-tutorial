# Tutorial TODO Checklist

Work in your own fork or downloaded copy. Do not edit the shared teaching repository.
Allow 60 minutes: setup 5, Part A 15, Part B 20, Part C 15, submission 5.

- [ ] Open the project root in your Python editor; Python 3.10+ is recommended.
- [ ] Run `python -m unittest discover -s tests -v` once. Initial
  NotImplementedError errors are expected because the functions are unfinished.
- [ ] A1-A4: complete `lookup()` in `starter/semantic_network.py`.
- [ ] Run `python -m starter.semantic_network` and record the four outputs.
- [ ] Run `python -m unittest discover -s tests -p test_exercises.py -k SemanticNetworkTests -v`.
- [ ] B1-B4: complete the four functions in `starter/ml_metrics.py`.
- [ ] Run `python -m starter.ml_metrics` and record the metrics.
- [ ] Run `python -m unittest discover -s tests -p test_exercises.py -k MLMetricsTests -v`.
- [ ] Explain preprocessing and leakage in `answers.md`. The supplied confusion
  matrix is from the slides; these tasks do not train a model or need a CSV file.
- [ ] C1-C4: complete `build_prompt()` and `validate_draft()` in `starter/llm_safety.py`.
- [ ] Run `python -m starter.llm_safety` and inspect the safe/unsafe examples.
- [ ] Run `python -m unittest discover -s tests -p test_exercises.py -k LLMSafetyTests -v`.
- [ ] Complete every TODO in `answers.md`, including limitations of the gate.
- [ ] Run all tests again. All 13 tests should pass after completing the code.
- [ ] Submit your fork URL or a ZIP of your completed starter files and answers.md
  through the lecturer's usual submission channel.

## Hints

Use dictionary membership to distinguish a missing property from a stored False.
Recall uses the actual-class row total. Macro-F1 gives each class equal weight.
Compare each claimed fact with the case and each proposed action with the allowed list.

## What the Tests Do Not Assess

Tests check the supplied examples and selected edge cases. The lecturer reviews
prompt instructions, leakage explanations, operational reasoning and reflections.
Do not change the tests to make unfinished code pass.

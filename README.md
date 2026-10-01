# Tutorial Exercise: Semantic Networks, Machine Learning and LLM Safety

Date: 1 October 2026  
Course: BCS2143 / BIT3203
Estimated time: 60 minutes
Mode: individual or pair work

## Before You Start

Read this page directly on GitHub. Use a Python notebook or editor for Parts A and C, and a Markdown file for your written answers. Python 3 is sufficient for the required coding tasks. Part B is a planning and calculation exercise using the supplied figures; no dataset download is required. No API key, paid LLM service or live model is required.

If you want to run the optional preprocessing snippet in Part B, install scikit-learn with `python -m pip install scikit-learn`.

## Learning Outcomes

By the end of this exercise, students should be able to:

1. Represent structured knowledge using nodes, labelled links and ISA inheritance.
2. Explain why missing knowledge means `UNKNOWN`, not `False`.
3. Build a supervised learning pipeline without leaking test data.
4. Compare a model against a baseline using accuracy, macro-F1 and a confusion matrix.
5. Design a simple LLM wrapper that grounds output in validated facts and blocks unsupported actions.

## Scenario

You are building a small intelligent help desk system.

The system has three layers:

1. A semantic network stores facts about tickets, devices and response rules.
2. A machine learning classifier predicts the ticket response tier.
3. A large language model drafts a short explanation for a human officer, but only after the output passes safety checks.

The central principle is simple: each layer must pass validated information forward. Unknown facts must remain unknown. The classifier must beat a baseline. The LLM must explain a decision, not invent one.

## Part A: Semantic Network

### Given Knowledge

Use this inheritance structure:

```text
Animal
  Bird
    Canary
    Penguin
  Fish
```

Use these properties:

```python
isa = {
    "Canary": "Bird",
    "Penguin": "Bird",
    "Bird": "Animal",
    "Fish": "Animal"
}

props = {
    "Animal": {"breathes": True},
    "Bird": {"can_fly": True, "has_part": "wings"},
    "Canary": {"colour": "Yellow"},
    "Penguin": {"can_fly": False}
}
```

### Task A1

Write a function called `lookup(node, prop)` that:

1. Checks the node itself first.
2. If the property is missing, follows the ISA link to the parent.
3. Stops at the first value found.
4. Returns `UNKNOWN` if the property is not found anywhere.

### Expected Results

```text
lookup("Canary", "can_fly")     returns True
lookup("Penguin", "can_fly")    returns False
lookup("Canary", "breathes")    returns True
lookup("Fish", "colour")        returns UNKNOWN
```

### Reflection Question

Why must `lookup("Fish", "colour")` return `UNKNOWN` rather than `False`?

Write two or three sentences. A strong answer should say that the network has no evidence about fish colour. Absence of a stored fact does not prove the opposite fact.

## Part B: Supervised Machine Learning

### Dataset Description

You are given a help desk dataset with 240 labelled tickets.

Target column:

```text
response_tier
```

Classes:

```text
log_only             48%
assign_technician    42%
escalate_now         10%
```

Predictor columns:

```text
wait_time_minutes
reopened_count
resolution_notes_length
device_type
error_code
reported_severity
```

The dataset has 18 missing cells across three predictor columns. Do not drop rows just because values are missing.

### Task B1

Explain why `ticket_id` must not be used as a feature.

Write one sentence. A strong answer should say that `ticket_id` identifies the row but does not contain a generalisable pattern for future tickets.

### Task B2

Build the preprocessing plan.

Use:

```text
Numeric columns:
median imputation, then standard scaling

Categorical columns:
most-frequent imputation, then one-hot encoding
```

Write the scikit-learn components you would use. You do not need the full dataset to answer this part.

Split the raw data before fitting preprocessing. Fit imputation, scaling, encoding and the classifier on training data only, ideally in one `Pipeline`. Apply the fitted pipeline to the test set without fitting it again. Explain how this prevents test data leakage.

Suggested structure:

```python
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

num = ["wait_time_minutes", "reopened_count", "resolution_notes_length"]
cat = ["device_type", "error_code", "reported_severity"]

pre = ColumnTransformer([
    ("num", Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler())
    ]), num),
    ("cat", Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("encode", OneHotEncoder(handle_unknown="ignore"))
    ]), cat)
])
```

### Task B3

Split the data into 75% training and 25% testing using:

```text
random_state = 42
stratify = response_tier
```

Given 240 tickets, calculate the number of records in each set.

Expected answer:

```text
Training set: 180 tickets
Test set: 60 tickets
```

### Task B4

Explain why a `DummyClassifier(strategy="most_frequent")` baseline is necessary.

Use these baseline results:

```text
Accuracy: 48.3%
Macro-F1: 0.217
Escalations caught: 0 of 6
```

Write three sentences. A strong answer should mention that accuracy alone looks acceptable because `log_only` is common, but the model has no skill on the rarer high-risk class. Macro-F1 exposes this weakness because every class contributes equally.

### Task B5

Interpret this confusion matrix for a decision tree with `max_depth = 5`.

Rows are true classes. Columns are predicted classes.

```text
                         Predicted
True class          assign_tech   escalate_now   log_only
assign_technician        15             2            8
escalate_now              3             2            1
log_only                  8             0           21
```

Calculate recall for each class.

Expected answer:

```text
assign_technician recall = 15 / 25 = 60%
escalate_now recall      = 2 / 6  = 33%
log_only recall          = 21 / 29 = 72%
```

### Reflection Question

Why is `escalate_now` recall the most important warning signal in this case?

Write two or three sentences. A strong answer should say that `escalate_now` is rare but costly to miss. A system that misses urgent tickets can create operational harm even when its overall accuracy looks acceptable.

## Part C: LLM Wrapper and Safety Gates

### Given Case

```json
{
  "station_id": "STN-042",
  "zone": "NORTH-CAMPUS",
  "bikes_available": 2,
  "docks_available": 1,
  "demand_trend": "rising",
  "decision": "rebalance_now",
  "validated_actions": ["dispatch_rebalancing_van", "notify_zone_supervisor"],
  "unknown_facts": ["current_temperature_c"]
}
```

### Task C1

Write a grounded prompt for an LLM.

The prompt must tell the model to:

1. Use only the facts provided.
2. State unknown facts plainly.
3. Recommend only actions from `validated_actions`.
4. Write for the on-duty operations officer.

### Task C2

Read this draft briefing:

```text
Station STN-042 in NORTH-CAMPUS has 2 bikes and 1 dock available. Demand is rising, so rebalance now. Conditions are cool at 24°C. Dispatch a rebalancing van and close the station until supply recovers.
```

Identify two safety failures.

Expected answer:

```text
Failure 1: The briefing invents current_temperature_c = 24°C, although temperature is unknown.
Failure 2: The briefing recommends close_station, which is not in validated_actions.
```

### Task C3

Complete the safety gate logic.

```python
def reject_unsupported_actions(text, validated, candidates):
    rejected = []
    for action in candidates:
        if action in text and action not in validated:
            rejected.append(action)
    return rejected

validated = ["dispatch_rebalancing_van", "notify_zone_supervisor"]
candidates = ["dispatch_rebalancing_van", "notify_zone_supervisor", "close_station"]

draft = "Dispatch a rebalancing van and close_station."
rejected = reject_unsupported_actions(draft, validated, candidates)
safe_to_show = len(rejected) == 0

print(rejected)
print(safe_to_show)
```

Expected output:

```text
['close_station']
False
```

This is a deliberately limited teaching check: it recognises exact action identifiers such as `close_station`. It does not recognise every paraphrase, check invented facts or establish that a briefing is safe. In particular, it would miss the phrase "close the station" in Task C2. Explain this limitation and propose one additional check before an officer sees the briefing.

### Reflection Question

Why should the human officer remain accountable even after the LLM output passes the safety gates?

Write two or three sentences. A strong answer should say that code checks can detect defined risks, but they cannot cover every operational judgement. The wrapper prepares information for review. It does not replace human responsibility.

## Submission

Submit one Markdown file or notebook containing:

1. Your `lookup()` function and four test outputs.
2. Your ML preprocessing plan and split calculation.
3. Your answers to the baseline and confusion matrix questions.
4. Your grounded LLM prompt.
5. Your safety failure analysis and gate output.
6. Your three reflection answers.

## Marking Rubric

| Criterion | Marks |
|---|---:|
| Semantic network inheritance works and handles exceptions | 20 |
| Missing knowledge is treated as `UNKNOWN`, not `False` | 10 |
| ML preprocessing avoids data leakage | 15 |
| Baseline, class imbalance and macro-F1 are explained correctly | 20 |
| Confusion matrix recall calculations are correct | 15 |
| LLM prompt is grounded and safety failures are identified | 15 |
| Writing is clear, precise and self-explanatory | 5 |
| **Total** | **100** |

## Instructor Notes

This exercise is intentionally small. The intellectual difficulty is not coding volume. The key point is disciplined system design: structure knowledge explicitly, measure learning honestly, and never allow fluent generated text to outrun verified facts.


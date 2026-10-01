"""Part C: ground a prompt and validate structured draft fields offline."""

import json

CASE = {
    "station_id": "STN-042",
    "zone": "NORTH-CAMPUS",
    "bikes_available": 2,
    "docks_available": 1,
    "demand_trend": "rising",
    "decision": "rebalance_now",
    "validated_actions": ["dispatch_rebalancing_van", "notify_zone_supervisor"],
    "unknown_facts": ["current_temperature_c"],
}
# Structured examples avoid pretending that a substring search validates prose.
SAFE_DRAFT = {
    "facts": {"station_id": "STN-042", "bikes_available": 2, "docks_available": 1},
    "actions": ["dispatch_rebalancing_van"],
}
UNSAFE_DRAFT = {
    "facts": {"station_id": "STN-042", "current_temperature_c": 24},
    "actions": ["dispatch_rebalancing_van", "close_station"],
}


def build_prompt(case):
    """Return instructions followed by the supplied case as JSON."""
    # TODO C1: instruct the model to use only supplied facts, state unknowns,
    # recommend only validated_actions and address the on-duty officer.
    # Include json.dumps(case) so the prompt contains the actual evidence.
    raise NotImplementedError("Complete TODO C1")


def validate_draft(draft, case):
    """Return {unsupported_facts: list, rejected_actions: list, safe_to_show: bool}.

    Inputs in this exercise have facts as a dictionary and actions as a list.
    Validate every claimed fact against case; metadata keys validated_actions
    and unknown_facts are not factual claims. Unknown, absent or changed values
    must fail. Preserve input order in returned lists.
    """
    # TODO C2: collect fact keys whose values are unknown, absent or mismatched.
    # TODO C3: collect action names not present in case['validated_actions'].
    # TODO C4: safe_to_show is True only when both lists are empty.
    # This gate checks supplied structured fields, not all free-text meaning.
    raise NotImplementedError("Complete TODO C2-C4")


if __name__ == "__main__":
    print(build_prompt(CASE))
    print("Safe example:", validate_draft(SAFE_DRAFT, CASE))
    print("Unsafe example:", validate_draft(UNSAFE_DRAFT, CASE))

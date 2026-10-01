"""Part A: follow ISA links and respect local exceptions."""

UNKNOWN = "UNKNOWN"
ISA = {"Canary": "Bird", "Penguin": "Bird", "Bird": "Animal", "Fish": "Animal"}
PROPERTIES = {
    "Animal": {"breathes": True},
    "Bird": {"can_fly": True, "has_part": "wings"},
    "Canary": {"colour": "Yellow"},
    "Penguin": {"can_fly": False},
}


def lookup(node, prop):
    """Return the nearest stored value, or the string UNKNOWN."""
    # TODO A1: check whether prop is a key on the current node.
    # TODO A2: return its value even when that value is False.
    # TODO A3: follow ISA parents until a value is found or the chain ends.
    # TODO A4: return UNKNOWN when no node provides the property.
    raise NotImplementedError("Complete TODO A1-A4")


if __name__ == "__main__":
    for node, prop in [("Canary", "can_fly"), ("Penguin", "can_fly"),
                       ("Canary", "breathes"), ("Fish", "colour")]:
        print(node, prop, lookup(node, prop))

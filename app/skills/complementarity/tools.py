import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from bio.sequence import Sequence


def generate_complement(sequence: str, operation: str) -> str:
    """Generates complementary and/or reverse complementary strand."""
    try:
        seq = Sequence(sequence)
        result = {"original_sequence": sequence}

        if operation in ("complement", "both"):
            result["complement"] = str(seq.complement())

        if operation in ("reverse_complement", "both"):
            result["reverse_complement"] = str(seq.reverse_complement())

        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

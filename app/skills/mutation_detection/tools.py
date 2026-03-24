import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from bio.sequence import Sequence


def detect_mutation(
    sequence: str,
    position: int,
    original_base: str,
    mutated_base: str,
) -> str:
    """Detects whether a point mutation is present at the indicated position."""
    try:
        seq = Sequence(sequence)

        if position >= len(seq):
            return json.dumps({
                "status": "ERROR",
                "message": f"Position {position} exceeds the sequence length ({len(seq)})",
            }, ensure_ascii=False)

        found_base = seq[position]

        if found_base == mutated_base:
            status = "MUTATION_PRESENT"
            description = f"Mutation {original_base}->{mutated_base} detected at position {position}"
        elif found_base == original_base:
            status = "NO_MUTATION"
            description = f"Original base '{original_base}' maintained at position {position}"
        else:
            status = "DIFFERENT_BASE"
            description = f"Base '{found_base}' found (neither {original_base} nor {mutated_base})"

        return json.dumps({
            "position": position,
            "found_base": found_base,
            "expected_original_base": original_base,
            "expected_mutated_base": mutated_base,
            "status": status,
            "description": description,
        }, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

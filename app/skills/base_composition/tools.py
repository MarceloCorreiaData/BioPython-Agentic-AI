import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from bio.sequence import Sequence


def analyze_composition(sequence: str) -> str:
    """Calculates percentage of A, T, C, G and GC content."""
    try:
        seq = Sequence(sequence)

        # Internal pipeline: 5 calls to calculate_percentage
        percentage_a = seq.calculate_percentage(["A"])
        percentage_t = seq.calculate_percentage(["T"])
        percentage_c = seq.calculate_percentage(["C"])
        percentage_g = seq.calculate_percentage(["G"])
        gc_content = seq.calculate_percentage(["G", "C"])

        return json.dumps({
            "sequence_length": len(seq),
            "percentage_A": round(percentage_a, 4),
            "percentage_T": round(percentage_t, 4),
            "percentage_C": round(percentage_c, 4),
            "percentage_G": round(percentage_g, 4),
            "gc_content": round(gc_content, 4),
        }, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

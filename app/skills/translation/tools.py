import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from bio.sequence import Sequence


def translate_dna_to_protein(sequence: str, stop: bool = False) -> str:
    """Translates a DNA sequence to protein using the codon table."""
    try:
        seq = Sequence(sequence)
        protein = seq.translate(stop=stop)
        return json.dumps({
            "dna_sequence": sequence[:100] + ("..." if len(sequence) > 100 else ""),
            "protein": protein[:200] + ("..." if len(protein) > 200 else ""),
            "protein_length": len(protein),
            "stop_at_stop": stop,
        }, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

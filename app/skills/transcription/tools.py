import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from bio.sequence import Sequence


def transcribe_dna_to_rna(sequence: str) -> str:
    """Transcribes a DNA sequence to RNA (T -> U)."""
    try:
        seq = Sequence(sequence)
        rna = seq.transcribe()
        return json.dumps({
            "dna_sequence": sequence,
            "rna_sequence": str(rna),
        }, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

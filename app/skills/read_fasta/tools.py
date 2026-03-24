import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from bio.read_fasta import read_fasta


def read_fasta_file(file_path: str) -> str:
    """Reads and parses a FASTA file, returning organisms."""
    try:
        organisms = read_fasta(file_path)
        result = []
        for org in organisms:
            result.append({
                "id": org.id,
                "name": org.name,
                "sequence_length": len(org.sequence),
            })
        return json.dumps({
            "total_organisms": len(result),
            "organisms": result,
        }, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

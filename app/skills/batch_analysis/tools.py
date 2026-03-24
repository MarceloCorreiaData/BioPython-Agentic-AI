import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from bio.read_fasta import read_fasta
from bio.sequence import Sequence


def analyze_batch(
    file_path: str,
    operation: str,
    sort_by: str = None,
    top_n: int = None,
    extra_parameters: dict = None,
) -> str:
    """Executes a skill in batch for all organisms in the FASTA file."""
    try:
        organisms = read_fasta(file_path)
        results = []

        for org in organisms:
            seq = org.sequence
            item = {"id": org.id, "name": org.name}

            if operation == "base_composition":
                item["percentage_A"] = round(seq.calculate_percentage(["A"]), 4)
                item["percentage_T"] = round(seq.calculate_percentage(["T"]), 4)
                item["percentage_C"] = round(seq.calculate_percentage(["C"]), 4)
                item["percentage_G"] = round(seq.calculate_percentage(["G"]), 4)
                item["gc_content"] = round(seq.calculate_percentage(["G", "C"]), 4)
                item["length"] = len(seq)

            elif operation == "translation":
                stop = (extra_parameters or {}).get("stop", False)
                protein = seq.translate(stop=stop)
                item["protein"] = protein[:100] + ("..." if len(protein) > 100 else "")
                item["protein_length"] = len(protein)

            elif operation == "transcription":
                rna = seq.transcribe()
                item["rna_sequence"] = str(rna)[:100] + ("..." if len(rna) > 100 else "")

            elif operation == "mutation_detection":
                params = extra_parameters or {}
                position = params.get("position", 1000)
                original_base = params.get("original_base", "A")
                mutated_base = params.get("mutated_base", "G")

                if position >= len(seq):
                    item["status"] = "SHORT_SEQUENCE"
                else:
                    base = seq[position]
                    if base == mutated_base:
                        item["status"] = "MUTATION_PRESENT"
                    elif base == original_base:
                        item["status"] = "NO_MUTATION"
                    else:
                        item["status"] = f"DIFFERENT_BASE ({base})"
                    item["found_base"] = base

            else:
                return json.dumps({
                    "error": f"Operation '{operation}' not supported. Use: base_composition, translation, transcription, mutation_detection"
                }, ensure_ascii=False)

            results.append(item)

        # Sort if requested
        if sort_by and results and sort_by in results[0]:
            results.sort(key=lambda x: x.get(sort_by, 0), reverse=True)

        # Limit if requested
        total = len(results)
        if top_n:
            results = results[:top_n]

        return json.dumps({
            "total_organisms": total,
            "results_returned": len(results),
            "operation": operation,
            "sorted_by": sort_by,
            "results": results,
        }, ensure_ascii=False)

    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

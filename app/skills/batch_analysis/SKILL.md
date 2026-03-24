# Skill: Batch Analysis

## Description
Executes a batch analysis for all organisms in a FASTA file.
Avoids the need to call a skill 159 times individually.

## Capability
Internal orchestration: reads the FASTA and applies a skill to all organisms at once.

## Internal tools
- `read_fasta` + any other skill (composite/pipeline)

## Parameters
| Name | Type | Required | Description |
|---|---|---|---|
| file_path | string | yes | Path to the FASTA file |
| operation | string | yes | Skill to apply: "base_composition", "translation", "transcription", "mutation_detection" |
| sort_by | string | no | Field to sort results by (e.g., "gc_content"). Default: no sorting |
| top_n | integer | no | Return only the top N results. Default: all |
| extra_parameters | object | no | Additional parameters for the skill (e.g., {"position": 1000, "original_base": "A", "mutated_base": "G"} for mutation_detection) |

## Return
JSON with list of results (one per organism), optionally sorted and limited.

## Usage example
```
Question: "Which organism has the highest GC content?"
Skill called: batch_analysis(file_path="data/Flaviviridae-genomes.fasta", operation="base_composition", sort_by="gc_content", top_n=5)
```

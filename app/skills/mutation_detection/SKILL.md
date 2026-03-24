# Skill: Mutation Detection

## Description
Detects whether a specific mutation is present at a given position in a DNA sequence.

## Capability
Identification of point mutations (nucleotide substitutions) in genomic sequences.

## Internal tools
- indexing + comparison (1:N pipeline)

## Parameters
| Name | Type | Required | Description |
|---|---|---|---|
| sequence | string | yes | DNA sequence to analyze |
| position | integer | yes | Position (0-indexed) to check |
| original_base | string | yes | Expected base without mutation (e.g., "A") |
| mutated_base | string | yes | Base that indicates mutation (e.g., "G") |

## Return
JSON with position, found base, status (MUTATION_PRESENT, NO_MUTATION, DIFFERENT_BASE) and description.

## Usage example
```
Question: "Check if there is an A->G mutation at position 1000"
Skill called: mutation_detection(sequence="...", position=1000, original_base="A", mutated_base="G")
Result: {"status": "MUTATION_PRESENT", "description": "Mutation A->G detected at position 1000"}
```

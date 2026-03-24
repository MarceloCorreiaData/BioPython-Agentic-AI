# Skill: Base Composition

## Description
Calculates the complete nucleotide composition: percentage of A, T, C, G and GC content.

## Capability
Statistical analysis of DNA sequence composition.

## Internal tools
- `calculate_percentage` (1:1 tool, internal pipeline with 5 calls)

## Parameters
| Name | Type | Required | Description |
|---|---|---|---|
| sequence | string | yes | DNA sequence to analyze |

## Return
JSON with sequence length and percentages of A, T, C, G and GC content.

## Usage example
```
Question: "What is the base composition of ATCGATCG?"
Skill called: base_composition(sequence="ATCGATCG")
Result: {"percentage_A": 0.25, "percentage_T": 0.25, ..., "gc_content": 0.5}
```

# Skill: Translation

## Description
Translates a DNA sequence to its corresponding protein sequence, reading codons 3 at a time.

## Capability
DNA to protein translation using the codon table.

## Internal tools
- `translate` (1:1)

## Parameters
| Name | Type | Required | Description |
|---|---|---|---|
| sequence | string | yes | DNA sequence to translate |
| stop | boolean | no | If true, stops at the first stop codon. Default: false |

## Return
JSON with DNA sequence (preview), resulting protein, length, and stop flag.

## Usage example
```
Question: "Translate ATGATGATG to protein"
Skill called: translation(sequence="ATGATGATG")
Result: {"protein": "MMM", "protein_length": 3}
```

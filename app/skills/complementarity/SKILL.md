# Skill: Complementarity

## Description
Generates the complementary and/or reverse complementary strand of a DNA sequence.

## Capability
DNA complementarity operations (base pairing A<->T, C<->G).

## Internal tools
- `complement` + `reverse_complement` (1:N, related)

## Parameters
| Name | Type | Required | Description |
|---|---|---|---|
| sequence | string | yes | DNA sequence |
| operation | string | yes | "complement", "reverse_complement", or "both" |

## Return
JSON with original sequence and operation result(s).

## Usage example
```
Question: "What is the complementary strand of ATCGATCG?"
Skill called: complementarity(sequence="ATCGATCG", operation="complement")
Result: {"original_sequence": "ATCGATCG", "complement": "TAGCTAGC"}
```

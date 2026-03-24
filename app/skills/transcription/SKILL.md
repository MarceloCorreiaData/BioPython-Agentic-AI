# Skill: Transcription

## Description
Transcribes a DNA sequence to RNA, replacing T with U.

## Capability
Simulation of the biological transcription process (DNA -> RNA).

## Internal tools
- `transcribe` (1:1)

## Parameters
| Name | Type | Required | Description |
|---|---|---|---|
| sequence | string | yes | DNA sequence to transcribe |

## Return
JSON with original DNA sequence and resulting RNA sequence.

## Usage example
```
Question: "Transcribe ATCGATCG to RNA"
Skill called: transcription(sequence="ATCGATCG")
Result: {"dna_sequence": "ATCGATCG", "rna_sequence": "AUCGAUCG"}
```

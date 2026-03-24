# Skill: Read FASTA

## Description
Reads and parses files in FASTA format, returning the list of organisms with id, name, and genomic sequence preview.

## Capability
Reading and parsing of multi-sequence FASTA files.

## Internal tools
- `read_fasta` (1:1)

## Parameters
| Name | Type | Required | Description |
|---|---|---|---|
| file_path | string | yes | Path to the FASTA file |

## Return
JSON with:
- `total_organisms`: number of sequences found
- `organisms`: list with id, name, length, and preview of each sequence

## Usage example
```
Question: "How many organisms are in the FASTA file?"
Skill called: read_fasta(file_path="files/Flaviviridae-genomes.fasta")
```

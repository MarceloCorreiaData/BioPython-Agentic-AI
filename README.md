# BioPython Agentic AI

A bioinformatics AI agent inspired by the BioPython library, built with an Orchestrator + Skills architecture using progressive disclosure via the Claude API.

## Architecture

The agent uses 3 meta-tools instead of registering skills individually:

| Meta-tool | Level | Purpose |
|---|---|---|
| `list_skills` | L1 | Lists names and descriptions of all available skills |
| `load_skill` | L2 | Loads full instructions (SKILL.md) |
| `execute_skill` | L3 | Executes a skill with parameters |

The agent discovers its capabilities dynamically, loading context only when needed (progressive disclosure).

## Available Skills

| Skill | Description |
|---|---|
| `read_fasta` | Reads and parses FASTA files |
| `complementarity` | Generates complement and reverse complement strands |
| `transcription` | Transcribes DNA to RNA (T -> U) |
| `translation` | Translates DNA to protein using the codon table |
| `base_composition` | Calculates percentage of A, T, C, G and GC content |
| `mutation_detection` | Detects point mutations at specific positions |
| `batch_analysis` | Runs any skill across all organisms in a FASTA file |

## Project Structure

```
BioPython-Agentic-AI/
├── app/
│   ├── __init__.py
│   ├── orchestrator.py        # Root agent with SkillToolset (3 meta-tools)
│   └── skills/
│       ├── __init__.py        # Progressive disclosure (list/load/execute)
│       ├── batch_analysis/
│       │   ├── SKILL.md
│       │   └── tools.py
│       ├── base_composition/
│       │   ├── SKILL.md
│       │   └── tools.py
│       ├── complementarity/
│       │   ├── SKILL.md
│       │   └── tools.py
│       ├── mutation_detection/
│       │   ├── SKILL.md
│       │   └── tools.py
│       ├── read_fasta/
│       │   ├── SKILL.md
│       │   └── tools.py
│       ├── transcription/
│       │   ├── SKILL.md
│       │   └── tools.py
│       └── translation/
│           ├── SKILL.md
│           └── tools.py
├── bio/                       # Core library (Sequence, FastaOrganism classes)
├── arquivos/                  # Data files (Flaviviridae-genomes.fasta)
├── .env.example               # Environment variables template
├── main.py                    # Entry point
└── README.md
```

## Setup

```bash
# 1. Clone the repository
git clone https://github.com/MarceloCorreiaData/BioPython-Agentic-AI.git
cd BioPython-Agentic-AI

# 2. Install dependencies
pip install anthropic python-dotenv

# 3. Configure API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 4. Run
python main.py
```

## Usage Examples

```
You: What skills do you have?
You: Read the FASTA file and tell me how many organisms it contains
You: What is the GC content of the sequence ATCGATCG?
You: Translate ATGATGATG to protein
You: Detect A->G mutation at position 1000 in the first virus
You: Read the FASTA file and determine which organism has the most stable DNA
```

## Execution Flow

```
User asks a question
    |
    v
Orchestrator sends to Claude with 3 meta-tools
    |
    v
Claude calls list_skills (L1) -> lists available skills
    |
    v
Claude calls load_skill (L2) -> reads skill instructions
    |
    v
Claude calls execute_skill (L3) -> executes with parameters
    |
    v
Result returns to Claude -> formulates final response
    |
    v
Response displayed to user
```

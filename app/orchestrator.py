"""
Root Agent: Orchestrator agent with progressive disclosure of skills.

Uses 3 meta-tools (list_skills, load_skill, execute_skill) instead of
registering each skill individually. The agent discovers its capabilities
dynamically.
"""

import json
from anthropic import Anthropic
from app.skills import SKILLS_REGISTRY, TOOLS_DEFINITIONS


SYSTEM_PROMPT = """\
You are a bioinformatics agent specialized in DNA sequence analysis.

You have access to a SkillToolset with 3 meta-tools:
1. list_skills: lists all available skills (use FIRST)
2. load_skill: loads complete instructions for a skill
3. execute_skill: executes a skill with parameters

## CRITICAL RULES

1. NEVER answer questions about genomic data using your general knowledge.
   ALWAYS use skills to analyze the actual data from the FASTA file.
   You do NOT know which organisms are in the file or their sequences until you load them with fasta_reader.

2. If the question involves comparing organisms, analyzing sequences, or any biological data:
   - FIRST: load the organisms with fasta_reader
   - THEN: use the necessary skills to analyze the data
   - ONLY THEN: respond based on the actual results

3. Examples of correct reasoning:
   - "Which organism is most stable?" -> fasta_reader -> base_composition for each -> compare GC -> respond with data
   - "What is the GC content of the first virus?" -> fasta_reader -> base_composition with the first sequence -> respond
   - "Is there a mutation at position 1000?" -> fasta_reader -> mutation_detection for each organism -> report
   - "Translate the sequence of virus X" -> fasta_reader -> find virus X -> translation with its sequence -> respond

4. You may use your general knowledge ONLY to:
   - Explain biology concepts (what is GC content, what is a mutation, etc.)
   - Interpret results AFTER obtaining them via skills
   - Never to substitute actual data analysis

## MANDATORY WORKFLOW

- Always start by calling list_skills to know which capabilities you have
- Before executing a skill, call load_skill to understand its parameters
- Only then call execute_skill with the correct parameters
- To analyze multiple organisms, use the batch_analysis skill instead of calling a skill repeatedly
- The batch_analysis skill executes any other skill for all organisms in the FASTA at once

## DATA

The default FASTA file is located at: arquivos/Flaviviridae-genomes.fasta
It contains 159 genomes of viruses from the Flaviviridae family.
You do NOT know the contents of this file until you load it via fasta_reader.

Always respond in English.
"""


class Agent:

    def __init__(self, api_key: str = None, model: str = "claude-sonnet-4-20250514"):
        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.messages = []

    def _execute_meta_tool(self, tool_name: str, tool_input: dict) -> str:
        """Execute one of the 3 meta-tools."""
        if tool_name not in SKILLS_REGISTRY:
            return json.dumps({"error": f"Meta-tool '{tool_name}' not found"})

        try:
            meta_fn = SKILLS_REGISTRY[tool_name]
            return meta_fn(**tool_input)
        except Exception as e:
            return json.dumps({"error": f"Failed to execute '{tool_name}': {str(e)}"})

    def chat(self, user_message: str) -> str:
        """Process a user message and return the agent's response."""
        self.messages.append({"role": "user", "content": user_message})

        while True:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                tools=TOOLS_DEFINITIONS,
                messages=self.messages,
            )

            if response.stop_reason == "tool_use":
                self.messages.append({
                    "role": "assistant",
                    "content": response.content,
                })

                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        print(f"  [{block.name}({json.dumps(block.input, ensure_ascii=False)[:80]})]")
                        result = self._execute_meta_tool(block.name, block.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result,
                        })

                self.messages.append({
                    "role": "user",
                    "content": tool_results,
                })

            else:
                self.messages.append({
                    "role": "assistant",
                    "content": response.content,
                })

                text_parts = []
                for block in response.content:
                    if hasattr(block, "text"):
                        text_parts.append(block.text)

                return "\n".join(text_parts)

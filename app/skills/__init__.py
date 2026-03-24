"""
SkillToolset: Progressive disclosure of skills.

3 meta-tools:
  - list_skills (L1): returns names + descriptions (~50 tokens per skill)
  - load_skill (L2): loads complete SKILL.md (~500 tokens)
  - execute_skill (L3): executes the skill with parameters

The agent sees only L1 automatically. Loads L2 on demand.
Executes L3 when it decides to use a skill.
"""

import os
import json
import importlib

SKILLS_DIR = os.path.dirname(__file__)

# Automatic skill discovery (subdirectories with SKILL.md)
def _discover_skills() -> dict:
    """Discovers all available skills from the filesystem."""
    skills = {}
    for entry in os.listdir(SKILLS_DIR):
        skill_path = os.path.join(SKILLS_DIR, entry)
        skill_md = os.path.join(skill_path, "SKILL.md")
        if os.path.isdir(skill_path) and os.path.exists(skill_md):
            # Extract first content line from SKILL.md as description
            with open(skill_md, "r", encoding="utf-8") as f:
                lines = f.readlines()
                name = entry
                description = ""
                for line in lines:
                    line = line.strip()
                    if line.startswith("## Description"):
                        continue
                    if line and not line.startswith("#"):
                        description = line
                        break
            skills[name] = {
                "name": name,
                "description": description,
                "path": skill_path,
            }
    return skills


# --- L1: list_skills ---
def list_skills() -> str:
    """L1: Returns names and short descriptions of all skills."""
    skills = _discover_skills()
    result = []
    for name, info in skills.items():
        result.append({
            "name": name,
            "description": info["description"],
        })
    return json.dumps(result, ensure_ascii=False)


# --- L2: load_skill ---
def load_skill(skill_name: str) -> str:
    """L2: Loads the complete SKILL.md of a skill."""
    skills = _discover_skills()
    if skill_name not in skills:
        return json.dumps({"error": f"Skill '{skill_name}' not found"})

    skill_md_path = os.path.join(skills[skill_name]["path"], "SKILL.md")
    with open(skill_md_path, "r", encoding="utf-8") as f:
        content = f.read()

    return json.dumps({
        "name": skill_name,
        "instructions": content,
    }, ensure_ascii=False)


# --- L3: execute_skill ---
def execute_skill(skill_name: str, parameters: dict) -> str:
    """L3: Executes a skill with the provided parameters."""
    skills = _discover_skills()
    if skill_name not in skills:
        return json.dumps({"error": f"Skill '{skill_name}' not found"})

    # Dynamically import the skill's tools.py module
    try:
        module = importlib.import_module(f"app.skills.{skill_name}.tools")
    except ModuleNotFoundError:
        return json.dumps({"error": f"Module tools.py not found in '{skill_name}'"})

    # Find the executable function (first public function of the module)
    skill_fn = None
    for attr_name in dir(module):
        if not attr_name.startswith("_"):
            attr = getattr(module, attr_name)
            if callable(attr) and attr.__module__ == module.__name__:
                skill_fn = attr
                break

    if skill_fn is None:
        return json.dumps({"error": f"No function found in '{skill_name}/tools.py'"})

    try:
        return skill_fn(**parameters)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


# --- Tool definitions for the Claude API (3 meta-tools) ---
TOOLS_DEFINITIONS = [
    {
        "name": "list_skills",
        "description": (
            "Lists all available skills with names and short descriptions. "
            "Use this tool FIRST to know which capabilities you have."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "load_skill",
        "description": (
            "Loads the complete instructions for a specific skill. "
            "Use AFTER list_skills to understand a skill's parameters and behavior."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "skill_name": {
                    "type": "string",
                    "description": "Name of the skill (returned by list_skills)",
                },
            },
            "required": ["skill_name"],
        },
    },
    {
        "name": "execute_skill",
        "description": (
            "Executes a skill with the specified parameters. "
            "Use AFTER load_skill to know which parameters to pass."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "skill_name": {
                    "type": "string",
                    "description": "Name of the skill to execute",
                },
                "parameters": {
                    "type": "object",
                    "description": "Skill parameters (see SKILL.md via load_skill)",
                },
            },
            "required": ["skill_name", "parameters"],
        },
    },
]

# Registry: meta-tool name -> function
SKILLS_REGISTRY = {
    "list_skills": lambda **kwargs: list_skills(),
    "load_skill": lambda **kwargs: load_skill(kwargs["skill_name"]),
    "execute_skill": lambda **kwargs: execute_skill(kwargs["skill_name"], kwargs.get("parameters", {})),
}

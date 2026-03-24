"""
Entry point for the bioinformatics agent.
Interactive loop with progressive disclosure of skills.
"""

import os
import sys

from dotenv import load_dotenv
load_dotenv()

from app.orchestrator import Agent


def main():
    print("=" * 60)
    print("  Bioinformatics Agent")
    print("  Progressive Disclosure with SkillToolset")
    print("=" * 60)
    print()
    print("The agent discovers its skills automatically.")
    print("Example questions:")
    print('  "What skills do you have?"')
    print('  "Read the FASTA file and tell me how many organisms there are"')
    print('  "What is the GC content of the sequence ATCGATCG?"')
    print('  "Translate ATGATGATG to protein"')
    print('  "Detect mutation A->G at position 1000 of the first virus"')
    print()
    print("Type 'exit' to quit.")
    print("=" * 60)
    print()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: Set ANTHROPIC_API_KEY in the .env file")
        sys.exit(1)

    agent = Agent(api_key=api_key)

    while True:
        try:
            question = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            break

        if not question:
            continue

        if question.lower() in ("sair", "exit", "quit"):
            print("Exiting...")
            break

        print()
        try:
            response = agent.chat(question)
            print(f"\nAgent: {response}")
        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    main()

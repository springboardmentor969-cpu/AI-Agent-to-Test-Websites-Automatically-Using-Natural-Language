import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agent.parser import InstructionParser
import json

parser = InstructionParser()

test = """Go to https://www.amazon.in/
Type "Iphone pro max" in search
Select first product
View details
Add to cart"""

with open("parser_output.txt", "w") as f:
    f.write("Input:\n")
    f.write(test + "\n\n")
    f.write("Actions:\n")
    actions = parser.parse(test)
    for i, act in enumerate(actions, 1):
        f.write(f"{i}. {json.dumps(act, indent=2)}\n")
    f.write(f"\nTotal actions: {len(actions)}\n")

print(f"Generated {len(actions)} actions. See parser_output.txt for details.")

"""
Debug: Show exactly what gets parsed
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.parser import InstructionParser

# Exact input
instructions_input = """Go to https://www.amazon.in/
Type "Iphone pro max" in search
Select first product
View details
Add to cart"""

print("INPUT (as entered in UI):")
print(repr(instructions_input))
print()

# What app.py does
instructions_text = instructions_input.strip()
tests = [instructions_text]

print(f"Number of tests created: {len(tests)}")
print()

# What graph_batch.py does
parser = InstructionParser()
parsed_sets = [parser.parse(test) for test in tests]

print(f"Number of parsed sets: {len(parsed_sets)}")
print()

for i, actions in enumerate(parsed_sets, 1):
    print(f"Test #{i} - Number of actions: {len(actions)}")
    for j, action in enumerate(actions, 1):
        print(f"  Action {j}: {action}")

# Write to file for easy viewing
with open("parse_debug.txt", "w") as f:
    f.write(f"Tests: {len(tests)}\n")
    f.write(f"Parsed sets: {len(parsed_sets)}\n")
    f.write(f"Actions in first set: {len(parsed_sets[0]) if parsed_sets else 0}\n\n")
    
    if parsed_sets and parsed_sets[0]:
        f.write("Actions:\n")
        for j, action in enumerate(parsed_sets[0], 1):
            f.write(f"{j}. {action}\n")

print("\nWrote details to parse_debug.txt")

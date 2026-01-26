"""
Direct test of the parser and executor to debug the issue
"""
import sys
import os

# Clear any cached imports
if 'agent.parser' in sys.modules:
    del sys.modules['agent.parser']
if 'agent.executor' in sys.modules:
    del sys.modules['agent.executor']

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.parser import InstructionParser
from agent.executor import Executor

print("=" * 60)
print("DIRECT MODULE TEST")
print("=" * 60)

instruction = """Go to https://www.amazon.in/
Type "Iphone pro max" in search
Select first product
View details
Add to cart"""

print("\nInput instruction:")
print(instruction)
print("\n" + "=" * 60)

parser = InstructionParser()
actions = parser.parse(instruction)

print(f"\nParser generated {len(actions)} actions:")
for i, action in enumerate(actions, 1):
    print(f"{i}. {action}")

print("\n" + "=" * 60)
print("\nIf you see 5 actions above, the code is working!")
print("If you see only 1 action, there's a caching issue.")
print("=" * 60)

# Test just the normalization
print("\n\nDEBUG: Testing normalization:")
normalized = instruction.replace('\n', ' then ').replace('\r', '')
print(f"Normalized: {normalized}")

import re
steps = re.split(r' then |\.(?:\s|$)', normalized.lower())
print(f"\nSplit into {len(steps)} steps:")
for i, step in enumerate(steps, 1):
    if step.strip():
        print(f"  {i}. '{step.strip()}'")

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

print("Input:")
print(test)
print("\nActions:")
actions = parser.parse(test)
for i, act in enumerate(actions, 1):
    print(f"{i}. {json.dumps(act, indent=2)}")

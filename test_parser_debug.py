"""
Debug script to test the parser with Amazon instructions
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.parser import InstructionParser

# Test the exact instruction
parser = InstructionParser()

# Test single line instruction
instruction1 = "Go to https://www.amazon.in/ then type 'Iphone pro max' in search then select first product then view details then add to cart"

print("=" * 60)
print("Testing Instruction:")
print(instruction1)
print("=" * 60)
print("\nParsed Actions:")
actions = parser.parse(instruction1)
for i, action in enumerate(actions, 1):
    print(f"{i}. {action}")

print("\n" + "=" * 60)
print("\nTesting Multi-line instruction:")
instruction2 = """Go to https://www.amazon.in/
Type "Iphone pro max" in search
Select first product
View details
Add to cart"""

print(instruction2)
print("=" * 60)
print("\nParsed Actions:")
actions2 = parser.parse(instruction2)
for i, action in enumerate(actions2, 1):
    print(f"{i}. {action}")

print("\n" + "=" * 60)

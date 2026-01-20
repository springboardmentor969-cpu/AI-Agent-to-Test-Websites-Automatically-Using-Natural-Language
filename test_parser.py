from src.instruction_parser.instruction_parser import InstructionParser

parser = InstructionParser()
result = parser.parse("open login page, enter mahi in username, enter 1234 in password, click login")
print("Parsed actions:", result)

from src.assertion_generator.assertion_generator import AssertionGenerator
generator = AssertionGenerator()
assertions = generator.generate(result)
print("Generated assertions:", assertions)

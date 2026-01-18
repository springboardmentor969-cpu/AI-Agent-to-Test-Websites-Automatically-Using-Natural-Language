import yaml
from instruction_parser import parse_instruction

def test_instruction_parser():
    with open("tests/sample_test_cases.yaml") as f:
        cases = yaml.safe_load(f)

    for case in cases:
        parsed = parse_instruction(case["instruction"])
        assert parsed["commands"] == case["expected_commands"]

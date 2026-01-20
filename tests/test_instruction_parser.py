import unittest
from src.instruction_parser.instruction_parser import InstructionParser

class TestInstructionParser(unittest.TestCase):
    def setUp(self):
        self.parser = InstructionParser()

    def test_navigate(self):
        result = self.parser.parse("open youtube")
        expected = [{"action": "navigate", "url": "https://www.youtube.com"}]
        self.assertEqual(result, expected)

    def test_fill(self):
        result = self.parser.parse("enter test in username")
        expected = [{"action": "fill", "field": "username", "value": "test"}]
        self.assertEqual(result, expected)

    def test_click(self):
        result = self.parser.parse("click login")
        expected = [{"action": "click", "element": "login"}]
        self.assertEqual(result, expected)

    def test_assert(self):
        result = self.parser.parse("verify success message")
        expected = [{"action": "assert", "text": "success message"}]
        self.assertEqual(result, expected)

    def test_wait(self):
        result = self.parser.parse("wait for results")
        expected = [{"action": "wait", "element": "results"}]
        self.assertEqual(result, expected)

    def test_multiple_actions(self):
        result = self.parser.parse("open login page, enter user in username, click login")
        expected = [
            {"action": "navigate", "url": "http://127.0.0.1:5000/static/login.html"},
            {"action": "fill", "field": "username", "value": "user"},
            {"action": "click", "element": "login"}
        ]
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
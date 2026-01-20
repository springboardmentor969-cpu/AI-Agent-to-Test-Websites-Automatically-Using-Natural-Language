import unittest
from src.assertion_generator.assertion_generator import AssertionGenerator

class TestAssertionGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = AssertionGenerator()

    def test_navigate_assertion(self):
        actions = [{"action": "navigate", "url": "https://www.youtube.com"}]
        result = self.generator.generate(actions)
        expected = [{"type": "url_contains", "value": "youtube"}]
        self.assertEqual(result, expected)

    def test_fill_assertion(self):
        actions = [{"action": "fill", "field": "username", "value": "test"}]
        result = self.generator.generate(actions)
        expected = [{"type": "field_value", "field": "username", "value": "test"}]
        self.assertEqual(result, expected)

    def test_click_login_assertion(self):
        actions = [{"action": "click", "element": "login"}]
        result = self.generator.generate(actions)
        expected = [{"type": "url_contains", "value": "agent"}]
        self.assertEqual(result, expected)

    def test_assert_action(self):
        actions = [{"action": "assert", "text": "welcome"}]
        result = self.generator.generate(actions)
        expected = [{"type": "text_contains", "value": "welcome"}]
        self.assertEqual(result, expected)

    def test_multiple_assertions(self):
        actions = [
            {"action": "navigate", "url": "https://www.google.com"},
            {"action": "fill", "field": "search", "value": "query"},
            {"action": "click", "element": "login"}
        ]
        result = self.generator.generate(actions)
        expected = [
            {"type": "url_contains", "value": "google"},
            {"type": "field_value", "field": "search", "value": "query"},
            {"type": "url_contains", "value": "agent"}
        ]
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
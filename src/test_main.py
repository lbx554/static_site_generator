from main import extract_title
import unittest

class TestExtractTitle(unittest.TestCase):
    def test_basic_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_title_with_spaces(self):
        self.assertEqual(extract_title("#   Welcome to Boot.dev   "), "Welcome to Boot.dev")

    def test_no_h1_header(self):
        with self.assertRaises(Exception):
            extract_title("This is not a header\n## Subtitle")

    def test_ignores_h2(self):
        with self.assertRaises(Exception):
            extract_title("## Sub Header")

    def test_picks_first_h1(self):
        self.assertEqual(extract_title("# First\n# Second"), "First")

if __name__ == '__main__':
    unittest.main()

import unittest
from blocktype import block_to_block_type, BlockType

class TestBlockToBlockType(unittest.TestCase):

    # --- Test Cases for Paragraph Blocks ---
    def test_paragraph_simple(self):
        self.assertEqual(block_to_block_type("This is a simple paragraph."), BlockType.paragraph)

    def test_paragraph_empty_string(self):
        self.assertEqual(block_to_block_type(""), BlockType.paragraph)

    def test_paragraph_with_numbers(self):
        self.assertEqual(block_to_block_type("123 Some text."), BlockType.paragraph)

    # --- Test Cases for Heading Blocks ---
    def test_heading_h1(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.heading)

    def test_heading_h6(self):
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.heading)

    def test_heading_no_space(self):
        # Should not be a heading if no space after hashes
        self.assertEqual(block_to_block_type("#Heading"), BlockType.paragraph)

    def test_heading_more_than_six_hashes(self):
        self.assertEqual(block_to_block_type("####### Not a heading"), BlockType.paragraph)

    def test_heading_only_hashes(self):
        # Should not be a heading if only hashes and no content/space
        self.assertEqual(block_to_block_type("###"), BlockType.paragraph)

    # --- Test Cases for Code Blocks ---
    def test_code_block_simple(self):
        code_block = "```\nprint('Hello, world!')\n```"
        self.assertEqual(block_to_block_type(code_block), BlockType.code)

    def test_code_block_empty(self):
        self.assertEqual(block_to_block_type("```\n```"), BlockType.code)

    def test_code_block_only_start_delimiter(self):
        # Should not be code if only starts with ``` but doesn't end
        self.assertEqual(block_to_block_type("```code"), BlockType.paragraph)

    def test_code_block_only_end_delimiter(self):
        # Should not be code if only ends with ``` but doesn't start
        self.assertEqual(block_to_block_type("code```"), BlockType.paragraph)

    # --- Test Cases for Quote Blocks ---
    def test_quote_single_line(self):
        self.assertEqual(block_to_block_type("> This is a quote."), BlockType.quote)

    def test_quote_multi_line(self):
        # Assuming your implementation handles multi-line checks
        multi_line_quote = "> First line\n> Second line\n> Third line"
        self.assertEqual(block_to_block_type(multi_line_quote), BlockType.quote)

    def test_quote_mixed_with_non_quote_line(self):
        # If any line doesn't start with '>', it's not a quote block
        mixed_quote = "> Line 1\nNot a quote line\n> Line 3"
        self.assertEqual(block_to_block_type(mixed_quote), BlockType.paragraph) # Or whatever you determine for mixed content

    # --- Test Cases for Unordered List Blocks ---
    def test_unordered_list_single_item(self):
        self.assertEqual(block_to_block_type("- Item 1"), BlockType.unordered_list)

    def test_unordered_list_multi_item(self):
        # Assuming your implementation handles multi-line checks
        ul_block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(ul_block), BlockType.unordered_list)

    def test_unordered_list_mixed_with_non_list_item(self):
        # If any line doesn't start with '- ', it's not an unordered list block
        mixed_ul = "- Item 1\nNot a list item\n- Item 3"
        self.assertEqual(block_to_block_type(mixed_ul), BlockType.paragraph) # Or whatever you determine for mixed content

    # --- Test Cases for Ordered List Blocks ---
    def test_ordered_list_single_item(self):
        self.assertEqual(block_to_block_type("1. Item 1"), BlockType.ordered_list)

    def test_ordered_list_multi_item_correct_sequence(self):
        # Assuming your implementation handles multi-line checks and sequence
        ol_block = "1. Item 1\n2. Item 2\n3. Item 3"
        self.assertEqual(block_to_block_type(ol_block), BlockType.ordered_list)

    def test_ordered_list_multi_item_incorrect_sequence(self):
        # If numbers are not sequential or don't start at 1, it's not an ordered list
        ol_block_bad_seq = "1. Item 1\n3. Item 3\n2. Item 2"
        self.assertEqual(block_to_block_type(ol_block_bad_seq), BlockType.paragraph) # Or whatever you determine for mixed content

    def test_ordered_list_multi_item_starts_at_zero(self):
        ol_block_bad_start = "0. Item 0\n1. Item 1"
        self.assertEqual(block_to_block_type(ol_block_bad_start), BlockType.paragraph)

    def test_ordered_list_mixed_with_non_list_item(self):
        # If any line doesn't conform, it's not an ordered list block
        mixed_ol = "1. Item 1\nNot a list item\n3. Item 3"
        self.assertEqual(block_to_block_type(mixed_ol), BlockType.paragraph)

if __name__ == '__main__':
    unittest.main()

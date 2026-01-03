import unittest
from split_node import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    
    def test_basic_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_bold_delimiter(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_italic_delimiter(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_multiple_delimiters(self):
        node = TextNode("Text with `code1` and `code2` here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code1", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("code2", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_no_delimiters(self):
        node = TextNode("This is just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("This is just plain text", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)
    
    def test_non_text_nodes_unchanged(self):
        nodes = [
            TextNode("Regular text", TextType.TEXT),
            TextNode("Bold text", TextType.BOLD),
            TextNode("Italic text", TextType.ITALIC),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("Regular text", TextType.TEXT),
            TextNode("Bold text", TextType.BOLD),
            TextNode("Italic text", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_unmatched_delimiter_raises_exception(self):
        node = TextNode("This has `unclosed delimiter", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)
    
    def test_empty_delimiter_content(self):
        node = TextNode("This has `` empty delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("", TextType.CODE),
            TextNode(" empty delimiters", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_delimiter_at_start_and_end(self):
        node = TextNode("`start` middle `end`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("start", TextType.CODE),
            TextNode(" middle ", TextType.TEXT),
            TextNode("end", TextType.CODE),
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

#-----------------------------------------------------------------------------------------------------

    def test_split_nodes_image_single_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_nodes_image_multiple_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_nodes_image_no_images(self):
        node = TextNode("This is just plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_nodes_image_image_at_start(self):
        node = TextNode("![start image](https://example.com) followed by text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start image", TextType.IMAGE, "https://example.com"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_image_image_at_end(self):
        node = TextNode("Text before ![end image](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("end image", TextType.IMAGE, "https://example.com"),
            ],
            new_nodes,
        )

    def test_split_nodes_image_only_image(self):
        node = TextNode("![only image](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("only image", TextType.IMAGE, "https://example.com")],
            new_nodes,
        )


class TestTextToTextnodes(unittest.TestCase):

    def test_text_to_textnodes_bold(self):
        text = "This is **bold** text"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_text_to_textnodes_italic(self):
        text = "This is _italic_ text"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_text_to_textnodes_code(self):
        text = "This is `code` text"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT)
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_text_to_textnodes_link(self):
        text = "This is a [link](https://boot.dev)"
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)


    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


if __name__ == "__main__":
    unittest.main()

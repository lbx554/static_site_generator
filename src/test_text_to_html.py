import unittest

from htmlnode import LeafNode, TextNode, text_node_to_html_node
from textnode import TextType



class TestTextToHTMLNode(unittest.TestCase):
    def test_text_node_to_html_node(self):

        # Test textnode values
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

if __name__ == "__main__":
    unittest.main()

import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node2", TextType.BOLD)
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", TextType.BOLD, url="https://www.boot.dev/")
        node2 = TextNode("This is a text node", TextType.BOLD, url="https://www.boot.dev/")
        self.assertEqual(node, node2)

if __name__ == "__main__":
    unittest.main()

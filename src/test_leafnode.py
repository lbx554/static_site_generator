import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leafnode(self):

        # Same paragraph
        node = LeafNode("p", "Hello World")
        self.assertEqual(node.to_html(), "<p>Hello World</p>")

if __name__ == "__main__":
    unittest.main()

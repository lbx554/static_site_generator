import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_htmlnode(self):

        # Simple paragraph with text
        paragraph_node = HTMLNode("p", "This is a paragraph of text")
        self.assertEqual(paragraph_node.tag, "p")
        self.assertEqual(paragraph_node.value, "This is a paragraph of text")
        self.assertIsNone(paragraph_node.children)
        self.assertIsNone(paragraph_node.props)

        # A link with attributes
        link_node = HTMLNode("a", "Click me!", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(link_node.tag, "a")
        self.assertEqual(link_node.value, "Click me!")
        self.assertIsNone(link_node.children)
        self.assertEqual(link_node.props, {"href": "https://www.google.com", "target": "_blank"})

        # A heading
        heading_node = HTMLNode("h1", "Welcome to my website")
        self.assertEqual(heading_node.tag, "h1")
        self.assertEqual(heading_node.value, "Welcome to my website")
        self.assertIsNone(heading_node.children)
        self.assertIsNone(heading_node.props)

        # An image (self-closing tag)
        img_node = HTMLNode("img", None, None, {"src": "image.jpg", "alt": "A beautiful sunset"})
        self.assertEqual(img_node.tag, "img")
        self.assertIsNone(img_node.value)
        self.assertIsNone(img_node.children)
        self.assertEqual(img_node.props, {"src": "image.jpg", "alt": "A beautiful sunset"})


if __name__ == "__main__":
    unittest.main()

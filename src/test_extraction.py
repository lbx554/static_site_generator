import unittest

from htmlnode import LeafNode
from main import extract_markdown_images, extract_markdown_links

class TestExtraction(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        text = "Here's ![first](http://example.com/1.jpg) and ![second](http://example.com/2.png)"
        matches = extract_markdown_images(text)
        expected = [("first", "http://example.com/1.jpg"), ("second", "http://example.com/2.png")]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_images_empty_alt(self):
        text = "Image with empty alt: ![](http://example.com/image.jpg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("", "http://example.com/image.jpg")], matches)

    def test_extract_markdown_images_no_images(self):
        text = "This text has no images at all"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_links_multiple(self):
        text = "Check out [Google](https://google.com) and [GitHub](https://github.com)"
        matches = extract_markdown_links(text)
        expected = [("Google", "https://google.com"), ("GitHub", "https://github.com")]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_links_with_images_mixed(self):
        text = "Here's a [link](https://example.com) and an ![image](https://example.com/pic.jpg)"
        link_matches = extract_markdown_links(text)
        image_matches = extract_markdown_images(text)
        self.assertListEqual([("link", "https://example.com")], link_matches)
        self.assertListEqual([("image", "https://example.com/pic.jpg")], image_matches)

    def test_extract_markdown_links_no_links(self):
        text = "This text has no links"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_images_complex_alt_text(self):
        text = "![Alt with spaces and numbers 123](https://example.com/image.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("Alt with spaces and numbers 123", "https://example.com/image.png")], matches)

if __name__ == "__main__":
    unittest.main()

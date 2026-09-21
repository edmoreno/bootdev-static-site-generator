import unittest

from helpers import extract_markdown_images

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        """Verify extraction of an image alt-text and URL pair."""
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

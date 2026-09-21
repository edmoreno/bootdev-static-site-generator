import unittest
from helpers import text_to_textnodes
from textnode import TextNode, TextType

class TestTextToTextNodes(unittest.TestCase):
    def test_all_text_types_split(self):
        """Verify parsing of plain text, bold, italic, code, images, and links together."""
        text = 'This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        processed = text_to_textnodes(text)
        self.assertEqual(
            processed,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )

    def test_empty_string(self):
        """Verify that empty inline Markdown produces no text nodes."""
        text = ''
        processed = text_to_textnodes(text)
        self.assertEqual(
            processed,
            []
        )

    def test_all_text(self):
        """Verify that unformatted text produces a single plain-text node."""
        text = 'This is text with a word.'
        processed = text_to_textnodes(text)
        self.assertEqual(
            processed,
            [
                TextNode("This is text with a word.", TextType.TEXT),
            ]
        )

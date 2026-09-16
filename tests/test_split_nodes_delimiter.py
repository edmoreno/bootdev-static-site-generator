import unittest

from helpers import split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual([node.text_type for node in new_nodes],
                         [TextType.TEXT, TextType.CODE, TextType.TEXT])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[2].text, " word")

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual([node.text_type for node in new_nodes],
                         [TextType.TEXT, TextType.BOLD, TextType.TEXT])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text, "bold block")
        self.assertEqual(new_nodes[2].text, " word")

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is text with a *italic block* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual([node.text_type for node in new_nodes],
                         [TextType.TEXT, TextType.ITALIC, TextType.TEXT])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text, "italic block")
        self.assertEqual(new_nodes[2].text, " word")

    def test_split_nodes_delimiter_no_delim_preserves_text(self):
        node = TextNode("This is text with a italic block word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.CODE)
        self.assertEqual(new_nodes, [node])

    def test_split_nodes_delimiter_unmatched_delim_raises(self):
        node = TextNode("This has **unclosed bold text", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

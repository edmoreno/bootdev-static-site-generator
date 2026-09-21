import unittest

from helpers import split_nodes_link
from textnode import TextNode, TextType


class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link(self):
        """Verify splitting of multiple links while preserving text, labels, URLs, and order."""
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertEqual(
            [node.text_type for node in new_nodes],
            [TextType.TEXT, TextType.LINK, TextType.TEXT, TextType.LINK],
        )
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "This is text with a link ")
        self.assertEqual(new_nodes[1].text, "to boot dev")
        self.assertEqual(new_nodes[1].url, "https://www.boot.dev")
        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[3].text, "to youtube")
        self.assertEqual(new_nodes[3].url, "https://www.youtube.com/@bootdotdev")

    def test_split_nodes_link_no_link(self):
        """Verify that text without links is preserved."""
        node = TextNode("This is some plain text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [node])

    def test_split_nodes_link_ignores_image_markdown(self):
        """Verify that link splitting leaves image Markdown as text."""
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and [link](https://www.boot.dev)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertEqual([node.text_type for node in new_nodes], [TextType.TEXT, TextType.LINK])
        self.assertEqual(new_nodes[0].text, "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ")
        self.assertEqual(new_nodes[1].text, "link")
        self.assertEqual(new_nodes[1].url, "https://www.boot.dev")

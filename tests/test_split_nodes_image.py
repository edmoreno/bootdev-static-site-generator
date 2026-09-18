import unittest

from helpers import split_nodes_image
from textnode import TextNode, TextType


class TestSplitNodesImage(unittest.TestCase):
    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertEqual(
            [node.text_type for node in new_nodes],
            [TextType.TEXT, TextType.IMAGE, TextType.TEXT, TextType.IMAGE],
        )
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "This is text with an ")
        self.assertEqual(new_nodes[1].text, "image")
        self.assertEqual(new_nodes[1].url, "https://i.imgur.com/zjjcJKZ.png")
        self.assertEqual(new_nodes[2].text, " and another ")
        self.assertEqual(new_nodes[3].text, "second image")
        self.assertEqual(new_nodes[3].url, "https://i.imgur.com/3elNhQu.png")

    def test_split_nodes_image_no_image(self):
        node = TextNode("This is some plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [node])

    def test_split_nodes_image_ignores_links(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertEqual(new_nodes, [node])

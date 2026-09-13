import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_is_not_none(self):
        node = TextNode("text node", TextType.LINK, "www.cnn.com")
        node2 = TextNode("text node", TextType.LINK, "www.cnn.com")
        self.assertEqual(node, node2)

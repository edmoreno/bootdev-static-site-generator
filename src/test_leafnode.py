import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(
            node.to_html(),
            "<p>Hello, world!</p>"
        )

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.to_html)

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(
            node.to_html(),
            "Hello, world!"
        )

    def test_leaf_to_html_return_no_props(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(
            node.to_html(),
            "<p>This is a paragraph of text.</p>"
        )

    def test_leaf_to_html_return_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_to_html_empty_value(self):
        node = LeafNode("p", "")
        self.assertEqual(node.to_html(), "<p></p>")

    def test_leaf_to_html_empty_value_no_tag(self):
        node = LeafNode(None, "")
        self.assertEqual(node.to_html(), "")

    def test_leaf_to_html_no_tag_or_value(self):
        node = LeafNode(None, None)
        self.assertRaises(ValueError, node.to_html)

    def test_leaf_to_html_empty_props(self):
        node = LeafNode("p", "Hello, world!", {})
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_multiple_props(self):
        node = LeafNode("a", "About", {"href": "/about", "target": "_blank"})
        self.assertEqual(
            node.to_html(),
            '<a href="/about" target="_blank">About</a>'
        )

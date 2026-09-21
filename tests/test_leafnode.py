import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        """Verify that a paragraph leaf wraps its text in paragraph tags."""
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(
            node.to_html(),
            "<p>Hello, world!</p>"
        )

    def test_leaf_to_html_no_value(self):
        """Verify that a leaf with a None value raises ValueError."""
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.to_html)

    def test_leaf_to_html_no_tag(self):
        """Verify that an untagged leaf renders as bare text."""
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(
            node.to_html(),
            "Hello, world!"
        )

    def test_leaf_to_html_return_no_props(self):
        """Verify rendering of a leaf without HTML attributes."""
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(
            node.to_html(),
            "<p>This is a paragraph of text.</p>"
        )

    def test_leaf_to_html_return_with_props(self):
        """Verify that a link leaf includes its href attribute."""
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_to_html_empty_value(self):
        """Verify that empty text is allowed inside a tag."""
        node = LeafNode("p", "")
        self.assertEqual(node.to_html(), "<p></p>")

    def test_leaf_to_html_empty_value_no_tag(self):
        """Verify that an untagged empty leaf renders as an empty string."""
        node = LeafNode(None, "")
        self.assertEqual(node.to_html(), "")

    def test_leaf_to_html_no_tag_or_value(self):
        """Verify that a missing value raises even when the tag is also missing."""
        node = LeafNode(None, None)
        self.assertRaises(ValueError, node.to_html)

    def test_leaf_to_html_empty_props(self):
        """Verify that an empty attribute dictionary adds no spaces or attributes."""
        node = LeafNode("p", "Hello, world!", {})
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_multiple_props(self):
        """Verify that all leaf attributes appear in the opening tag."""
        node = LeafNode("a", "About", {"href": "/about", "target": "_blank"})
        self.assertEqual(
            node.to_html(),
            '<a href="/about" target="_blank">About</a>'
        )

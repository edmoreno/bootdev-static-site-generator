import unittest
from textnode import TextNode, TextType, text_node_to_html
from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        """Verify that nodes with matching fields compare equal."""
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_text_node_to_html_text_types(self):
        """Verify leaf tags and values for plain, bold, italic, and code text."""
        cases = [
            (TextType.TEXT, None),
            (TextType.BOLD, "b"),
            (TextType.ITALIC, "i"),
            (TextType.CODE, "code"),
        ]
        for text_type, expected_tag in cases:
            with self.subTest(text_type=text_type):
                node = TextNode("Some text", text_type)
                result = text_node_to_html(node)
                self.assertIsInstance(result, LeafNode)
                self.assertEqual(result.tag, expected_tag)
                self.assertEqual(result.value, "Some text")
                self.assertIsNone(result.props)
                self.assertIsNone(result.children)

    def test_text_node_to_html_link(self):
        """Verify conversion of link text and its href attribute."""
        node = TextNode("About", TextType.LINK, "https://example.com/about")
        result = text_node_to_html(node)
        self.assertIsInstance(result, LeafNode)
        self.assertEqual(result.tag, "a")
        self.assertEqual(result.value, "About")
        self.assertEqual(result.props, {"href": "https://example.com/about"})

    def test_text_node_to_html_image(self):
        """Verify conversion of an image URL and alt text to an empty-valued leaf."""
        node = TextNode("A mountain", TextType.IMAGE, "/images/mountain.png")
        result = text_node_to_html(node)
        self.assertIsInstance(result, LeafNode)
        self.assertEqual(result.tag, "img")
        self.assertEqual(result.value, "")
        self.assertEqual(
            result.props,
            {"src": "/images/mountain.png", "alt": "A mountain"},
        )

    def test_text_node_to_html_empty_text(self):
        """Verify that empty plain text renders as an empty string."""
        node = TextNode("", TextType.TEXT)
        result = text_node_to_html(node)
        self.assertIsNone(result.tag)
        self.assertEqual(result.value, "")
        self.assertEqual(result.to_html(), "")

    def test_text_node_to_html_invalid_type(self):
        """Verify that an unsupported text type raises ValueError."""
        node = TextNode("Some text", "invalid")
        self.assertRaises(ValueError, text_node_to_html, node)

    def test_not_eq(self):
        """Verify that nodes with different text compare unequal."""
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_is_not_none(self):
        """Verify equality for nodes with the same nonempty URL."""
        node = TextNode("text node", TextType.LINK, "www.cnn.com")
        node2 = TextNode("text node", TextType.LINK, "www.cnn.com")
        self.assertEqual(node, node2)

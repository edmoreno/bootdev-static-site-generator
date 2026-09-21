import unittest
from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        """Verify rendering of a parent with one leaf child."""
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        """Verify recursive rendering of nested parent nodes."""
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_preserves_child_order(self):
        """Verify that plain text and tagged children retain their order."""
        node = ParentNode("p", [
            LeafNode(None, "Hello "),
            LeafNode("b", "world"),
            LeafNode(None, "!"),
        ])
        self.assertEqual(node.to_html(), "<p>Hello <b>world</b>!</p>")

    def test_to_html_mixed_leaf_and_parent_children(self):
        """Verify rendering of a mixture of leaf and parent children."""
        node = ParentNode("div", [
            LeafNode("h1", "Title"),
            ParentNode("p", [
                LeafNode(None, "Some "),
                LeafNode("em", "text"),
            ]),
            LeafNode(None, "End"),
        ])
        self.assertEqual(
            node.to_html(),
            "<div><h1>Title</h1><p>Some <em>text</em></p>End</div>",
        )

    def test_to_html_with_parent_and_child_props(self):
        """Verify that parent and child attributes stay on their respective tags."""
        node = ParentNode(
            "div",
            [LeafNode("a", "About", {"href": "/about"})],
            {"class": "navigation", "id": "menu"},
        )
        self.assertEqual(
            node.to_html(),
            '<div class="navigation" id="menu"><a href="/about">About</a></div>',
        )

    def test_to_html_with_empty_props(self):
        """Verify parent rendering with an empty attribute dictionary."""
        node = ParentNode("div", [LeafNode("span", "child")], {})
        self.assertEqual(node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_empty_text_child(self):
        """Verify that an empty text child produces an empty parent element."""
        node = ParentNode("div", [LeafNode(None, "")])
        self.assertEqual(node.to_html(), "<div></div>")

    def test_to_html_without_tag(self):
        """Verify that a None parent tag raises ValueError."""
        node = ParentNode(None, [LeafNode("span", "child")])
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_with_empty_tag(self):
        """Verify that an empty parent tag raises ValueError."""
        node = ParentNode("", [LeafNode("span", "child")])
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_without_children(self):
        """Verify that a None children collection raises ValueError."""
        node = ParentNode("div", None)
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_with_empty_children(self):
        """Verify that an empty children list raises ValueError."""
        node = ParentNode("div", [])
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_propagates_child_error(self):
        """Verify that a child rendering error propagates through the parent."""
        node = ParentNode("div", [LeafNode("span", None)])
        self.assertRaises(ValueError, node.to_html)

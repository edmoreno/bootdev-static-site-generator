import unittest
from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_preserves_child_order(self):
        node = ParentNode("p", [
            LeafNode(None, "Hello "),
            LeafNode("b", "world"),
            LeafNode(None, "!"),
        ])
        self.assertEqual(node.to_html(), "<p>Hello <b>world</b>!</p>")

    def test_to_html_mixed_leaf_and_parent_children(self):
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
        node = ParentNode("div", [LeafNode("span", "child")], {})
        self.assertEqual(node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_empty_text_child(self):
        node = ParentNode("div", [LeafNode(None, "")])
        self.assertEqual(node.to_html(), "<div></div>")

    def test_to_html_without_tag(self):
        node = ParentNode(None, [LeafNode("span", "child")])
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_with_empty_tag(self):
        node = ParentNode("", [LeafNode("span", "child")])
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_without_children(self):
        node = ParentNode("div", None)
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_with_empty_children(self):
        node = ParentNode("div", [])
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_propagates_child_error(self):
        node = ParentNode("div", [LeafNode("span", None)])
        self.assertRaises(ValueError, node.to_html)

import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_no_args(self):
        node = HTMLNode()
        html_str = node.props_to_html()
        self.assertEqual(html_str, '')

    def test_props_to_html_empty_dict(self):
        node = HTMLNode(props={})
        html_str = node.props_to_html()
        self.assertEqual(html_str, '')

    def test_props_to_html_one_attribute(self):
        node = HTMLNode(props={"href": "www.google.com"})
        html_str = node.props_to_html()
        self.assertEqual(html_str, ' href="www.google.com"')

    def test_props_to_html_multi_attribute(self):
        node = HTMLNode(props={"href": "www.google.com", "target": "_blank"})
        html_str = node.props_to_html()
        self.assertEqual(
            html_str,
            ' href="www.google.com" target="_blank"'
        )

    def test_constructor_defaults_are_none(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)
        self.assertEqual(node.value, None)

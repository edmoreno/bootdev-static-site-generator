from __future__ import annotations
from enum import Enum
from leafnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        """Store inline text, its formatting type, and an optional link or image URL."""
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: TextNode) -> bool:
        """Compare two text nodes by text, formatting type value, and URL."""
        return (self.text == other.text) and \
        (self.text_type.value == other.text_type.value) and \
        (self.url == other.url)

    def __repr__(self) -> str:
        """Return a debugging representation of the text, formatting type, and URL."""
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html(text_node: TextNode) -> LeafNode:
    """Convert a text node to the corresponding HTML leaf node.

    Use an untagged leaf for plain text and attributes for links and images.
    Raise ValueError for an unsupported text type.
    """
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": f"{text_node.url}"})
        case TextType.IMAGE:
            return LeafNode("img", '', {"src": f"{text_node.url}", "alt": f"{text_node.text}"})
        case _:
            raise ValueError("Invalid TextType.")

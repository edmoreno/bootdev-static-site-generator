from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str | None, props: dict[str, str] | None = None) -> None:
        """Create a node with text and optional attributes, but no children."""
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        """Render text inside its tag, or return bare text when the tag is None.

        Raise ValueError if the value is None; an empty string is allowed.
        """
        if self.value is None:
            raise ValueError

        if self.tag is None:
            return self.value

        opening_tag = f"<{self.tag}{self.props_to_html()}>"
        closing_tag = f"</{self.tag}>"
        return f"{opening_tag}{self.value}{closing_tag}"

    def __repr__(self):
        """Return a debugging representation of the leaf tag, value, and attributes."""
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"

from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self,
        tag: str,
        children: list[HTMLNode],
        props: dict[str, str] | None = None
    ) -> None:
        """Create a node with a tag, child nodes, and optional HTML attributes."""
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        """Render children in order inside the parent tag.

        Raise ValueError for a missing or empty tag or children collection.
        Propagate errors raised while rendering a child.
        """
        if self.tag is None or self.tag == '':
            raise ValueError("tag is required")

        if self.children is None or not self.children:
            raise ValueError("children is required")

        opening_tag = f"<{self.tag}{self.props_to_html()}>"
        closing_tag = f"</{self.tag}>"
        str_to_return = f"{opening_tag}"
        for child_node in self.children:
            str_to_return += child_node.to_html()

        str_to_return += f"{closing_tag}"

        return str_to_return

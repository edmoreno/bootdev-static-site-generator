from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str | None, props: dict[str, str] | None = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError

        if self.tag is None:
            return self.value

        opening_tag = f"<{self.tag}{self.props_to_html()}>"
        closing_tag = f"</{self.tag}>"
        return f"{opening_tag}{self.value}{closing_tag}"

    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"

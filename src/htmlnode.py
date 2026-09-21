from ast import Not


class HTMLNode:
    def __init__(self,
        tag: str | None = None,
        value: str | None = None,
        children: list[HTMLNode] | None = None,
        props: dict[str, str] | None = None) -> None:
        """Store the optional tag, value, children, and HTML attributes for a node."""
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """Raise NotImplementedError; subclasses must implement HTML rendering."""
        raise NotImplementedError

    def props_to_html(self) -> str:
        """Format attributes as space-prefixed HTML key-value pairs, or return an empty string."""
        if self.props is None or not self.props:
            return ''

        formatted_str = ''
        for key, value in self.props.items():
            formatted_str += f' {key}="{value}"'
        return formatted_str

    def __repr__(self):
        """Return a debugging representation of the node and its fields."""
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

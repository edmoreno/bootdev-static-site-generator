from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        if delimiter not in old_node.text or old_node.text.count(delimiter) < 2:
            raise Exception(f"Delimiter '{delimiter}' not found in text: {old_node.text}")

        split_text = old_node.text.split(delimiter)

        for index, text in enumerate(split_text):
            if index % 2 == 0:
                new_nodes.append(TextNode(text, TextType.TEXT))
            else:
                new_nodes.append(TextNode(text, text_type))

    return new_nodes

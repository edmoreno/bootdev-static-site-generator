from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        if delimiter not in old_node.text:
            new_nodes.append(old_node)
            continue
        if old_node.text.count(delimiter) % 2 != 0:
            raise Exception(f"Delimiter '{delimiter}' not found in text: {old_node.text}")

        split_text = old_node.text.split(delimiter)

        for index, text in enumerate(split_text):
            if index % 2 == 0 and text:
                new_nodes.append(TextNode(text, TextType.TEXT))
            elif index % 2 == 1:
                new_nodes.append(TextNode(text, text_type))

    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)
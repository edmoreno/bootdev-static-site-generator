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
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        image_tuples = extract_markdown_images(old_node.text)
        original_text = old_node.text

        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        if not image_tuples:
            new_nodes.append(old_node)
            continue

        for image_tuple in image_tuples:
            sections = original_text.split(f"![{image_tuple[0]}]({image_tuple[1]})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_tuple[0], TextType.IMAGE, image_tuple[1]))
            original_text = sections[1]

        if original_text:
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        matches = list(re.finditer(r"(?<!\!)\[(.*?)\]\((.*?)\)", old_node.text))
        if not matches:
            new_nodes.append(old_node)
            continue

        last_index = 0
        for match in matches:
            start, end = match.span()
            if start > last_index:
                new_nodes.append(TextNode(old_node.text[last_index:start], TextType.TEXT))
            new_nodes.append(TextNode(match.group(1), TextType.LINK, match.group(2)))
            last_index = end

        if last_index < len(old_node.text):
            new_nodes.append(TextNode(old_node.text[last_index:], TextType.TEXT))

    return new_nodes

node = TextNode(
    "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
    TextType.TEXT,
)
new_nodes = split_nodes_image([node])
print(new_nodes)
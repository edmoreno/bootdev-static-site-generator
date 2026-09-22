from block import BlockType, block_to_blocktype
from htmlnode import HTMLNode
from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    """Split plain-text nodes around paired delimiters into plain and formatted nodes.

    Preserve non-text nodes and text without delimiters. Raise an exception
    when a text node contains an unmatched delimiter.
    """
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
    """Return Markdown image alt-text and URL pairs in order of appearance."""
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    """Return Markdown link label and URL pairs, excluding image syntax."""
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    """Split image Markdown in plain-text nodes into text and image nodes.

    Preserve non-text nodes and nodes without images. Raise ValueError if
    a matched image cannot be separated from the remaining text.
    """
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """Split link Markdown in plain-text nodes into text and link nodes.

    Preserve non-text nodes and nodes without links. Raise ValueError if
    a matched link cannot be separated from the remaining text.
    """
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    """Parse inline images, links, bold, italic, and code into ordered text nodes.

    Return an empty list for empty input. Unmatched formatting delimiters
    raise an exception.
    """
    if not text:
        return []
    seed_node = TextNode(text, TextType.TEXT)
    processed_nodes = split_nodes_image([seed_node])
    processed_nodes = split_nodes_link(processed_nodes)
    processed_nodes = split_nodes_delimiter(processed_nodes, '**', TextType.BOLD)
    processed_nodes = split_nodes_delimiter(processed_nodes, '_', TextType.ITALIC)
    processed_nodes = split_nodes_delimiter(processed_nodes, '`', TextType.CODE)
    return processed_nodes

def markdown_to_blocks(markdown: str) -> list[str]:
    """Split Markdown on double newlines, trim each block, and discard empty blocks."""
    split_string = markdown.split('\n\n')
    trimmed_strings = map(lambda x: x.strip(), split_string)
    filtered_strings = list(filter(lambda x: x != '', trimmed_strings))
    return filtered_strings

def markdown_to_html_node(markdown: str) -> list[HTMLNode]:
    markdown_block_list = markdown_to_blocks(markdown)
    block_nodes = []

    for markdown_block in markdown_block_list:
        block_type = block_to_blocktype(markdown_block)
        header_level = determine_header_level(markdown_block)
        block_markdown_clean = clean_block_markdown_syntax(markdown_block, block_type)

        if block_type == BlockType.CODE:
            code_node = TextNode(block_markdown_clean, TextType.CODE)
            html_code_node = [text_node_to_html(code_node)]
            html_node = ParentNode("pre", html_code_node)
        elif block_type == BlockType.UNORDERED_LIST or block_type == BlockType.ORDERED_LIST:
            lines = block_markdown_clean.split("\n")
            child_nodes = []
            for line in lines:
                children = text_to_children(line)
                parent_node = ParentNode("li", children=children)
                child_nodes.append(parent_node)
            html_node = ParentNode(
                tag=blocktype_to_html_tag(block_type, header_level),
                children=child_nodes
            )
        else:
            child_nodes = text_to_children(block_markdown_clean)
            html_node = ParentNode(
                tag=blocktype_to_html_tag(block_type, header_level),
                children=child_nodes
            )

        block_nodes.append(html_node)

    return ParentNode("div", children=block_nodes)


def blocktype_to_html_tag(blocktype: BlockType, header_level: int) -> str:
    if blocktype == BlockType.PARAGRAPH:
        return "p"
    if blocktype == BlockType.HEADING:
        return f"h{header_level}"
    if blocktype == BlockType.QUOTE:
        return "blockquote"
    if blocktype == BlockType.UNORDERED_LIST:
        return "ul"
    if blocktype == BlockType.ORDERED_LIST:
        return "ol"
    if blocktype == BlockType.CODE:
        return "code"

def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    html_nodes = []

    for text_node in text_nodes:
        html_nodes.append(text_node_to_html(text_node))

    return html_nodes

def determine_header_level(markdown: str) -> int:
    return len(markdown) - len(markdown.lstrip("#"))

def clean_block_markdown_syntax(markdown: str, blocktype: BlockType) -> str:
    if blocktype == BlockType.PARAGRAPH:
        lines = markdown.split("\n")
        stripped_lines = [line.strip() for line in lines]
        return " ".join(stripped_lines)
    if blocktype == BlockType.HEADING:
        hash_count = determine_header_level(markdown)
        return markdown[hash_count:].lstrip().rstrip()
    if blocktype == BlockType.QUOTE:
        list_items = markdown.split("\n")
        replaced_items = []
        for item in list_items:
            replaced_items.append(item.replace("> ", "", 1))
        return "\n".join(replaced_items)
    if blocktype == BlockType.UNORDERED_LIST:
        list_items = markdown.split("\n")
        replaced_items = []
        for item in list_items:
            replaced_items.append(item.replace("- ", "", 1))
        return "\n".join(replaced_items)
    if blocktype == BlockType.ORDERED_LIST:
        list_items = markdown.split("\n")
        replaced_items = []
        for number, line in enumerate(list_items):
            replaced_items.append(line.replace(f"{number+1}. ", "", 1))
        return "\n".join(replaced_items)
    if blocktype == BlockType.CODE:
        if not markdown.startswith("```"):
            return markdown

        content = markdown[4:-3]
        lines = content.split("\n")
        non_empty_lines = [line for line in lines if line.strip()]
        if non_empty_lines:
            min_indent = min(len(line) - len(line.lstrip(" ")) for line in non_empty_lines)
            if min_indent:
                lines = [line[min_indent:] if line.strip() else "" for line in lines]
        return "\n".join(lines)
    return markdown

def extract_title(markdown: str) -> str:
    match = re.search(r"^# (.*)", markdown)

    if match:
        return match.group(1)
    else:
        raise Exception("No h1 header found!")

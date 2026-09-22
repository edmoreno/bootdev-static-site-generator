
from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_blocktype(markdown_block: str) -> BlockType:
    """Classify a Markdown block, defaulting to paragraph when no other pattern matches."""
    if re.match(r"^#{1,6}(?:[ \t]+.*|$)", markdown_block):
        return BlockType.HEADING
    elif re.search(r"^```\n.*```\Z", markdown_block, flags=re.DOTALL):
        return BlockType.CODE
    elif re.fullmatch(r">[^\n]*(?:\n>[^\n]*)*\n?", markdown_block):
        return BlockType.QUOTE
    elif re.fullmatch(r"- [^\n]*(?:\n- [^\n]*)*", markdown_block):
        return BlockType.UNORDERED_LIST
    elif all(line.startswith(f"{number}. ")
        for number, line in enumerate(markdown_block.split("\n"), start=1)
    ):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

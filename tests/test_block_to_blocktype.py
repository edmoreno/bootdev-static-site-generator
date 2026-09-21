import unittest
from block import BlockType, block_to_blocktype
from src import block

class TestBlockToBlocktype(unittest.TestCase):
    def test_no_text(self):
        """Verify that an empty block is classified as a paragraph."""
        markdown = ""
        blocktype = block_to_blocktype(markdown)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

    def test_paragraph(self):
        """Verify that ordinary text is classified as a paragraph."""
        markdown = "this is regular text"
        blocktype = block_to_blocktype(markdown)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

    def test_heading_one(self):
        """Verify recognition of a level-one heading."""
        markdown = "# this is regular text"
        blocktype = block_to_blocktype(markdown)
        self.assertEqual(blocktype, BlockType.HEADING)

    def test_heading_six(self):
        """Verify recognition of a level-six heading."""
        markdown = "###### this is regular text"
        blocktype = block_to_blocktype(markdown)
        self.assertEqual(blocktype, BlockType.HEADING)

    def test_heading_missing_space(self):
        """Verify that a heading marker without a space is treated as a paragraph."""
        markdown = "##this is regular text"
        blocktype = block_to_blocktype(markdown)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

    def test_code_block(self):
        """Verify recognition of a block enclosed in code fences."""
        markdown = "```\nthis is regular text```"
        blocktype = block_to_blocktype(markdown)
        self.assertEqual(blocktype, BlockType.CODE)

    def test_code_block_missing_newline(self):
        """Verify that a code fence without an opening newline is treated as a paragraph."""
        markdown = "```this is regular text```"
        blocktype = block_to_blocktype(markdown)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

    def test_code_block_missing_closing_backticks(self):
        """Verify that an unclosed code fence is treated as a paragraph."""
        markdown = "```\nthis is regular text"
        blocktype = block_to_blocktype(markdown)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

    def test_quote_block(self):
        """Verify recognition of a block with a quote marker on every line."""
        markdown = ">this is regular text\n> this is a second line"
        blocktype = block_to_blocktype(markdown)
        self.assertEqual(blocktype, BlockType.QUOTE)

    def test_quote_block_missing_newline_delimiter(self):
        """Verify that a block with an unmarked quote line is treated as a paragraph."""
        markdown = ">this is regular text\nthis is a second line"
        blocktype = block_to_blocktype(markdown)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

    def test_ordered_list_block(self):
        """Verify recognition of a sequentially numbered list."""
        markdown = "1. this is regular text\n2. this is a second line"
        blocktype = block_to_blocktype(markdown)
        self.assertEqual(blocktype, BlockType.ORDERED_LIST)

    def test_ordered_list_block_missing_space(self):
        """Verify that a numbered item without a space prevents list recognition."""
        markdown = "1.this is regular text\n2. this is a second line"
        blocktype = block_to_blocktype(markdown)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

    def test_ordered_list_block_incorrect_increment(self):
        """Verify that malformed numbering and spacing produce a paragraph."""
        markdown = "1.this is regular text\n3. this is a second line"
        blocktype = block_to_blocktype(markdown)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

    def test_ordered_list_block_missing_period(self):
        """Verify that a numbered item without a period prevents list recognition."""
        markdown = "1 this is regular text\n3. this is a second line"
        blocktype = block_to_blocktype(markdown)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

    def test_unordered_list_block(self):
        """Verify recognition of a block with dash-prefixed list items."""
        markdown = "- this is regular text\n- this is a second line"
        blocktype = block_to_blocktype(markdown)
        self.assertEqual(blocktype, BlockType.UNORDERED_LIST)

    def test_unordered_list_block_missing_space(self):
        """Verify that a dash without a following space prevents list recognition."""
        markdown = "-this is regular text\n- this is a second line"
        blocktype = block_to_blocktype(markdown)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

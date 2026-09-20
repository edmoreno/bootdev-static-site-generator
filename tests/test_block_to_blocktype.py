import unittest
from block import BlockType, block_to_blocktype
from src import block

class TestBlockToBlocktype(unittest.TestCase):
    def test_no_text(self):
        markdown = ""
        blocktype = block_to_blocktype(markdown)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

    def test_paragraph(self):
        markdown = "this is regular text"
        blocktype = block_to_blocktype(markdown)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

    def test_heading_one(self):
        markdown = "# this is regular text"
        blocktype = block_to_blocktype(markdown)
        self.assertEqual(blocktype, BlockType.HEADING)

    def test_heading_six(self):
        markdown = "###### this is regular text"
        blocktype = block_to_blocktype(markdown)
        self.assertEqual(blocktype, BlockType.HEADING)

    def test_heading_missing_space(self):
        markdown = "##this is regular text"
        blocktype = block_to_blocktype(markdown)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

    def test_code_block(self):
        markdown = "```\nthis is regular text```"
        blocktype = block_to_blocktype(markdown)
        self.assertEqual(blocktype, BlockType.CODE)

    def test_code_block_missing_newline(self):
        markdown = "```this is regular text```"
        blocktype = block_to_blocktype(markdown)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

    def test_code_block_missing_closing_backticks(self):
        markdown = "```\nthis is regular text"
        blocktype = block_to_blocktype(markdown)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

    def test_quote_block(self):
        markdown = ">this is regular text\n> this is a second line"
        blocktype = block_to_blocktype(markdown)
        self.assertEqual(blocktype, BlockType.QUOTE)

    def test_quote_block_missing_newline_delimiter(self):
        markdown = ">this is regular text\nthis is a second line"
        blocktype = block_to_blocktype(markdown)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

    def test_ordered_list_block(self):
        markdown = "1. this is regular text\n2. this is a second line"
        blocktype = block_to_blocktype(markdown)
        self.assertEqual(blocktype, BlockType.ORDERED_LIST)

    def test_ordered_list_block_missing_space(self):
        markdown = "1.this is regular text\n2. this is a second line"
        blocktype = block_to_blocktype(markdown)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

    def test_ordered_list_block_incorrect_increment(self):
        markdown = "1.this is regular text\n3. this is a second line"
        blocktype = block_to_blocktype(markdown)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

    def test_ordered_list_block_missing_period(self):
        markdown = "1 this is regular text\n3. this is a second line"
        blocktype = block_to_blocktype(markdown)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

    def test_unordered_list_block(self):
        markdown = "- this is regular text\n- this is a second line"
        blocktype = block_to_blocktype(markdown)
        self.assertEqual(blocktype, BlockType.UNORDERED_LIST)

    def test_unordered_list_block_missing_space(self):
        markdown = "-this is regular text\n- this is a second line"
        blocktype = block_to_blocktype(markdown)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

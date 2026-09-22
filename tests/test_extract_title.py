import unittest
from helpers import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title_successfully(self):
        markdown = "# this is the h1 header"
        extracted = extract_title(markdown)
        self.assertEqual(extracted, "this is the h1 header")
    
    def test_extract_title_no_h1_header(self):
        markdown = "## this is the h2 header"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_extract_title_empty_string(self):
            markdown = ""
            with self.assertRaises(Exception):
                extract_title(markdown)
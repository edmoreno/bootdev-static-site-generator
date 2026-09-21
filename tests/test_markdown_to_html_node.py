import unittest
from helpers import markdown_to_html_node


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_plain_paragraph(self):
        """Render plain text inside a paragraph and a root div."""
        node = markdown_to_html_node("Hello, world!")
        self.assertEqual(node.to_html(), "<div><p>Hello, world!</p></div>")

    def test_heading_levels(self):
        """Render all six heading levels without Markdown markers or separator spaces."""
        for level in range(1, 7):
            with self.subTest(level=level):
                node = markdown_to_html_node("#" * level + " Heading")
                self.assertEqual(
                    node.to_html(),
                    f"<div><h{level}>Heading</h{level}></div>",
                )

    def test_heading_with_inline_formatting(self):
        """Parse bold and italic text within a heading."""
        node = markdown_to_html_node("## A **bold** and _italic_ heading")
        self.assertEqual(
            node.to_html(),
            "<div><h2>A <b>bold</b> and <i>italic</i> heading</h2></div>",
        )

    def test_quote_with_inline_formatting(self):
        """Remove the quote marker and parse inline formatting."""
        node = markdown_to_html_node("> A **bold** quote with `code`.")
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>A <b>bold</b> quote with <code>code</code>.</blockquote></div>",
        )

    def test_unordered_list(self):
        """Render each unordered list item with its own inline children."""
        node = markdown_to_html_node("- First **bold** item\n- Second _italic_ item")
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>First <b>bold</b> item</li><li>Second <i>italic</i> item</li></ul></div>",
        )

    def test_ordered_list_with_ten_items(self):
        """Remove both single-digit and double-digit ordered list markers."""
        markdown = "\n".join(f"{number}. Item {number}" for number in range(1, 11))
        node = markdown_to_html_node(markdown)
        self.assertEqual(
            node.to_html(),
            "<div><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li>"
            "<li>Item 4</li><li>Item 5</li><li>Item 6</li><li>Item 7</li>"
            "<li>Item 8</li><li>Item 9</li><li>Item 10</li></ol></div>",
        )

    def test_links_and_images_in_paragraph(self):
        """Preserve link labels, image alt text, and URLs in their HTML attributes."""
        node = markdown_to_html_node("Visit [About](/about) and ![A cat](/cat.png).")
        self.assertEqual(
            node.to_html(),
            '<div><p>Visit <a href="/about">About</a> and '
            '<img src="/cat.png" alt="A cat"></img>.</p></div>',
        )

    def test_mixed_blocks_preserve_order(self):
        """Keep paragraphs, lists, and quotes in their original document order."""
        node = markdown_to_html_node("Intro\n\n- One\n- Two\n\n> Quote\n\nEnd")
        self.assertEqual(
            node.to_html(),
            "<div><p>Intro</p><ul><li>One</li><li>Two</li></ul>"
            "<blockquote>Quote</blockquote><p>End</p></div>",
        )

    def test_extra_blank_lines(self):
        """Ignore leading, trailing, and repeated blank block separators."""
        node = markdown_to_html_node("\n\nFirst\n\n\n\nSecond\n\n")
        self.assertEqual(node.to_html(), "<div><p>First</p><p>Second</p></div>")

    def test_codeblock_keeps_link_and_image_syntax(self):
        """Keep links, images, and unmatched inline markers literal inside code fences."""
        node = markdown_to_html_node("```\n[label](/url) ![alt](/image) ** _ `\n```")
        self.assertEqual(
            node.to_html(),
            "<div><pre><code>[label](/url) ![alt](/image) ** _ `\n</code></pre></div>",
        )

    def test_codeblock_preserves_indentation(self):
        """Preserve meaningful indentation inside an unindented fenced code block."""
        node = markdown_to_html_node("```\nif ready:\n    run()\n```")
        self.assertEqual(
            node.to_html(),
            "<div><pre><code>if ready:\n    run()\n</code></pre></div>",
        )

    def test_unmatched_inline_delimiter_raises(self):
        """Propagate invalid inline Markdown errors from paragraph conversion."""
        with self.assertRaises(Exception):
            markdown_to_html_node("A **bold phrase without a closing delimiter")

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

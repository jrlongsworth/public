import unittest
from markdown_blocks import (    
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_unordered,
    block_type_ordered,
)

class TestMarkdownBlocks(unittest.TestCase):
    def test_split_blocks_simple(self):
        text = "This\n\nis an example\n\nof blocked text"
        blocks = ["This", "is an example", "of blocked text"]
        self.assertEqual(markdown_to_blocks(text), blocks)

    def test_split_blocs(self):
        text = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        blocks = ["# This is a heading", "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", "* This is the first list item in a list block\n* This is a list item\n* This is another list item"]
        self.assertEqual(markdown_to_blocks(text), blocks)

    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("# heading "), block_type_heading)
        self.assertEqual(block_to_block_type("```\ncode\n```"), block_type_code)
        self.assertEqual(block_to_block_type("> quote\n> quote\n> quote"), block_type_quote)
        self.assertEqual(block_to_block_type("* unordered\n* list\n* here"), block_type_unordered)
        self.assertEqual(block_to_block_type("- unordered\n- list\n- again"), block_type_unordered)
        self.assertEqual(block_to_block_type("1. ordered\n2. list\n3. here"), block_type_ordered)
        self.assertEqual(block_to_block_type("any old thing"), block_type_paragraph)

    def test_paragraph(self):
        md = """This is **bolded** paragraph\ntext in a p\ntag here\n\n"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """This is **bolded** paragraph\ntext in a p\ntag here\n\nThis is another paragraph with *italic* text and `code` here\n\n"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """\n- This is a list\n- with items\n- and *more* items\n\n1. This is an `ordered` list\n2. with items\n3. and more items\n\n"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """\n# this is an h1\n\nthis is paragraph text\n\n## this is an h2\n"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """\n> This is a\n> blockquote block\n\nthis is paragraph text\n\n"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_blockquote(self):
        md = """\n> This is a\n> blockquote block\n\nthis is paragraph text\n\n"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

if __name__ == "__main__":
    unittest.main()
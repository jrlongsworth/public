import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from markdown_blocks import (    
    markdown_to_blocks,
)
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)

class TestInlineMarkdown(unittest.TestCase):
    def test_bold(self):
        node = TextNode("This is text with **bold** in it", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertEqual(
            [
                TextNode("This is text with ", text_type_text),
                TextNode("bold", text_type_bold),
                TextNode(" in it", text_type_text)
            ],
            new_nodes,
        )

    def test_italic(self):
        node = TextNode("This is text with *italic* in it", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertEqual(
            [
                TextNode("This is text with ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" in it", text_type_text)
            ],
            new_nodes,
        )

    def test_code(self):
        node = TextNode("This is text with `code` in it", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertEqual(
            [
                TextNode("This is text with ", text_type_text),
                TextNode("code", text_type_code),
                TextNode(" in it", text_type_text)
            ],
            new_nodes,
        )

    def test_nontext(self):
        node = TextNode("This is text with @nontext@ in it", "nontext")
        new_nodes = split_nodes_delimiter([node], "@", "nontext")
        self.assertEqual(
            [TextNode("This is text with @nontext@ in it", "nontext")], new_nodes
        )

    def test_images(self):
        images = extract_markdown_images("This is text with an ![funImage](https://www.imageline.com/123) and another ![2ndImage](https://www.moreimages.com/haha)")
        self.assertEqual([("funImage", "https://www.imageline.com/123"), ("2ndImage", "https://www.moreimages.com/haha")], images)

    def test_links(self):
        links = extract_markdown_links("This is text with a link [my link](https://www.mylink.com/abc) and another [link again](https://www.linx.com/fun)")
        self.assertEqual([("my link", "https://www.mylink.com/abc"), ("link again", "https://www.linx.com/fun")], links)

    def test_split_image(self):
        node = TextNode("This is text with an ![funImage](https://www.imageline.com/123)", text_type_text)
        new_nodes = split_nodes_image([node])
        self.assertEqual([TextNode("This is text with an ", text_type_text), TextNode("funImage", text_type_image, "https://www.imageline.com/123")], new_nodes)

    def test_split_link(self):
        node = TextNode("This is text with a link [my link](https://www.mylink.com/abc)", text_type_text)
        new_nodes = split_nodes_link([node])
        self.assertEqual([TextNode("This is text with a link ", text_type_text), TextNode("my link", text_type_link, "https://www.mylink.com/abc")], new_nodes)

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
            ],
            nodes
        )
    
if __name__ == "__main__":
    unittest.main()
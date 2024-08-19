import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_single_prop(self):
        htmlnode = HTMLNode("TEST", "TEST", "TEST", {"target": "_blank"})
        html_string = ' target="_blank"'
        self.assertEqual(htmlnode.props_to_html(), html_string)

    def test_props_to_html(self):
        htmlnode = HTMLNode("TEST", "TEST", "TEST", {"href": "https://www.google.com", "target": "_blank", })
        html_string = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(htmlnode.props_to_html(), html_string)

    def test_empty_props(self):
        htmlnode = HTMLNode("TEST", "TEST", "TEST")
        html_string = ''
        self.assertEqual(htmlnode.props_to_html(), html_string)
    
class TestLeafNode(unittest.TestCase):
    def test_value_reqd(self):
        leaf = LeafNode(None, None)
        with self.assertRaises(ValueError):
            leaf.to_html()
            
    def test_no_tag_gets_raw_text(self):
        leaf = LeafNode(None, "This is a test")
        raw_text = "This is a test"
        self.assertEqual(leaf.to_html(), raw_text)
    
    def test_all_provided(self):
        leaf = LeafNode("p", "This is a test")
        html = "<p>This is a test</p>"
        self.assertEqual(leaf.to_html(), html)

class TestParentNode(unittest.TestCase):
    def test_tag_reqd(self):
        parent = ParentNode(None, [LeafNode("b", "Bold text"),])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_children_reqd(self):
        parent = ParentNode("p", None)
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_correct_html_with_one_level(self):
        parent = ParentNode("p", [LeafNode("b", "Bold text"), ])
        html = "<p><b>Bold text</b></p>"
        self.assertEqual(parent.to_html(), html)
    
    def test_nested_children(self):
        parent = ParentNode("div", [ParentNode("p", [LeafNode("b", "Bold text"), LeafNode(None, "Normal text")]), ParentNode("p", [LeafNode("i", "Italic text")])])
        html = "<div><p><b>Bold text</b>Normal text</p><p><i>Italic text</i></p></div>"
        self.assertEqual(parent.to_html(), html)

if __name__ == "__main__":
    unittest.main()
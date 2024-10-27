import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):

    def test_props_multiple(self):
        node = HTMLNode(props={'href': 'https://www.google.com', 'target': '_blank',})
        result = node.props_to_html()

        self.assertIn(' href="https://www.google.com"', result) # type: ignore
        self.assertIn(' target="_blank"', result) # type: ignore
    
    def test_props_none(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_empty(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_single(self):
        node = HTMLNode(props={'href': 'https://www.google.com',})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')
       
    def test_leaf_to_html(self):
        leaf_node = LeafNode(tag="p", value="This is a paragraph")
        result = leaf_node.to_html()

        self.assertIn('<p>This is a paragraph</p>', result)
    
    def test_leaf_to_html_props(self):
        leaf_node = LeafNode(tag="a", value="Click me!", props={'href': 'https://www.google.com'})
        result = leaf_node.to_html()

        self.assertIn(result, "<a href=\"https://www.google.com\">Click me!</a>")

    def test_leaf_to_html_error(self):
        leaf_node = LeafNode(tag="a", value=None)
        with self.assertRaises(ValueError):
            leaf_node.to_html()

    def test_leaf_to_html_notag(self):
        leaf_node = LeafNode(value="This is just plain text")

        self.assertEqual(leaf_node.to_html(), "This is just plain text")

if __name__ == '__main__':
    unittest.main()
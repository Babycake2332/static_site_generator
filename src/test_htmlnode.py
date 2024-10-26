import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    def test_props_multiple(self):
        node = HTMLNode(props={'href': 'https://www.google.com', 'target': '_blank',})
        result = node.props_to_html()

        self.assertIn(' href="https://www.google.com"', result)
        self.assertIn(' target="_blank"', result)
    
    def test_props_none(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_empty(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_single(self):
        node = HTMLNode(props={'href': 'https://www.google.com',})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')
       

if __name__ == '__main__':
    unittest.main()
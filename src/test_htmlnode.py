import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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



class TestLeafNode(unittest.TestCase):

    def test_to_html(self):
        leaf_node = LeafNode(tag="p", value="This is a paragraph")
        result = leaf_node.to_html()

        self.assertIn('<p>This is a paragraph</p>', result)
    
    def test_to_html_props(self):
        leaf_node = LeafNode(tag="a", value="Click me!", props={'href': 'https://www.google.com'})
        result = leaf_node.to_html()

        self.assertIn(result, "<a href=\"https://www.google.com\">Click me!</a>")

    def test_to_html_error(self):
        leaf_node = LeafNode(tag="a", value=None)
        with self.assertRaises(ValueError):
            leaf_node.to_html()

    def test_to_html_notag(self):
        leaf_node = LeafNode(value="This is just plain text")

        self.assertEqual(leaf_node.to_html(), "This is just plain text")


class TestParentNode(unittest.TestCase):
    
    def test_to_html_full(self):
        parent_node = ParentNode(tag="p", children=[
                    LeafNode(tag="b", value="Bold text"), 
                    LeafNode(tag=None, value="Normal text"),
                    ParentNode(tag="div", children=[
                        LeafNode(tag="a", value="Click me!", props={"href": "https://www.google.com", "target": "_blank"},),
                        LeafNode(tag=None, value="Normal Text"),
                            ],
                        ),
                    LeafNode(tag="i", value="italic text"),
                    LeafNode(tag=None, value="Normal text"),
                                ],
                             )

        result = parent_node.to_html()

        # Note leading spaces within attribute tag. 
        self.assertEqual(
                        result, 
                         '<p><b>Bold text</b>Normal text<div><a href="https://www.google.com"'
                         ' target="_blank">Click me!</a>Normal Text</div><i>italic text</i>Normal text</p>'
                        )

    def test_to_html_notag(self):
        parent_node = ParentNode(tag=None, children=[LeafNode(tag="b", value="Bold text")])

        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    def test_to_html_empty(self):
        parent_node = ParentNode(tag="h1", children=[])

        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_object_nochild(self):
        with self.assertRaises(ValueError):
            parent_node = ParentNode(tag="h1", children=None)

    def test_to_html_multichild(self):
        parent_node = ParentNode(tag="p",
                                 children=[
                                     LeafNode(tag="b", value="Bold text"),
                                     ParentNode(tag="h3", children=[
                                         LeafNode(tag="i", value="Italic text"),
                                         LeafNode(tag="a", value="Click me!", props={"href": "https://www.123.com"}),
                                         ParentNode(tag="p", children=[
                                             LeafNode(tag=None, value="Plain text")
                                         ],
                                         ),
                                     ],
                                     ),
                                    ],
                                    )

        result = parent_node.to_html()

        self.assertEqual(
                        result,
                        '<p><b>Bold text</b><h3><i>Italic text</i>'
                        '<a href="https://www.123.com">Click me!</a>'
                        '<p>Plain text</p></h3></p>'
                        )

if __name__ == '__main__':
    unittest.main()
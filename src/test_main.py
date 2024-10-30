import unittest

from main import text_node_to_html_node, split_nodes_delimiter
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode

class TestNodeToHTML(unittest.TestCase):

    def test_text_to_html_link_img(self):
        node_link = TextNode("Click me!", TextType.LINK, "https://www.google.se")
        node_img = TextNode("Alt text", TextType.IMAGE, "https://www.google.se/img123/")

        result_link = text_node_to_html_node(node_link)
        result_img = text_node_to_html_node(node_img)

        expected_link = LeafNode(tag="a", value="Click me!", props={"href": "https://www.google.se"})
        expected_img = LeafNode(tag="img", value="", props={"src": "https://www.google.se/img123/", "alt": "Alt text"})

        self.assertEqual(result_link, expected_link)
        self.assertEqual(result_img, expected_img)
    
    def test_text_to_html_formatting(self):
        node_bold = TextNode("Bold text", TextType.BOLD)
        node_italic = TextNode("Italic text", TextType.ITALIC)
        node_code = TextNode("Code format", TextType.CODE)

        result_bold = text_node_to_html_node(node_bold)
        result_italic = text_node_to_html_node(node_italic)
        result_code = text_node_to_html_node(node_code)

        expected_bold = LeafNode(tag="b", value="Bold text")
        expected_italic = LeafNode(tag="i", value="Italic text")
        expected_code = LeafNode(tag="code", value="Code format")

        self.assertEqual(result_bold, expected_bold)
        self.assertEqual(result_italic, expected_italic)
        self.assertEqual(result_code, expected_code)


    def test_text_to_html_normal_text(self):
        node = TextNode("This is plain text", TextType.TEXT)

        result = text_node_to_html_node(node)
        expected = LeafNode(tag="", value="This is plain text")

        self.assertEqual(result, expected)


    def test_text_to_html_invalid_input(self):
        node_1 = TextNode("Text goes here", "bold")
        node_2 = TextNode("Text goes here", None)
        node_3 = "I am just a string"

        with self.assertRaises(TypeError):
            text_node_to_html_node(node_1)
        with self.assertRaises(TypeError):
            text_node_to_html_node(node_2)
        with self.assertRaises(AttributeError):
            text_node_to_html_node(node_3)

class TestSplitNodes(unittest.TestCase):

    def test_split_node_bold(self):
        node = TextNode("This is **bold** text you know.", TextType.TEXT)
        nodes = split_nodes_delimiter([node],"**", TextType.BOLD)
        assert len(nodes) == 3
        assert nodes[0].text == "This is "
        assert nodes[0].text_type == TextType.TEXT
        assert nodes[1].text == "bold"
        assert nodes[1].text_type == TextType.BOLD
        assert nodes[2].text == " text you know."
        assert nodes[2].text_type == TextType.TEXT

    def test_split_node_italic(self):
        node = TextNode("This text is *italic* you know.", TextType.TEXT)
        nodes = split_nodes_delimiter([node],"*", TextType.ITALIC)
        assert len(nodes) == 3
        assert nodes[0].text == "This text is "
        assert nodes[0].text_type == TextType.TEXT
        assert nodes[1].text == "italic"
        assert nodes[1].text_type == TextType.ITALIC
        assert nodes[2].text == " you know."
        assert nodes[2].text_type == TextType.TEXT
    

    def test_split_node_code(self):
        node = TextNode("This text is `code` you know.", TextType.TEXT)
        nodes = split_nodes_delimiter([node],"`", TextType.CODE)
        assert len(nodes) == 3
        assert nodes[0].text == "This text is "
        assert nodes[0].text_type == TextType.TEXT
        assert nodes[1].text == "code"
        assert nodes[1].text_type == TextType.CODE
        assert nodes[2].text == " you know."
        assert nodes[2].text_type == TextType.TEXT


    def test_split_node_broken_delimiter(self):
        node = TextNode("This text is *broken you know.", TextType.TEXT)
        nodes = split_nodes_delimiter([node],"*", TextType.ITALIC)
        
        self.assertEqual([node], nodes)

    def test_split_node_equal(self):
        node = TextNode("This text is bold", TextType.BOLD)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual([node], nodes)



'''
"This has **two** bold **words**"
"This has ** ** nothing"
[TextNode("Hello", TextType.TEXT), TextNode("**bold** text", TextType.TEXT)]

    What should happen with an invalid delimiter?
    What about empty strings?
    What about multiple pairs of delimiters?

Remember to test both the text content and the text_type of each node!
'''

if __name__ == "__main__":
    unittest.main()
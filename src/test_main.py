import unittest

from main import text_node_to_html_node
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode

class TestMainFunc(unittest.TestCase):

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


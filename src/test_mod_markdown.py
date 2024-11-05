import unittest

from mod_markdown import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from mod_markdown import split_nodes_image, split_nodes_link
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

class TestExtractMD(unittest.TestCase):

    def test_extract_md_correct(self):
        text_img = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        text_link = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        
        self.assertEqual(extract_markdown_images(text_img),
                         [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')])
        self.assertEqual(extract_markdown_links(text_link),
                         [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_extract_md_broken(self):
        text_img = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan(https://i.imgur.com/fJRm4Vk.jpeg)"
        text_link = "This is text with a link to boot dev(https://www.boot.dev) and to youtube(https://www.youtube.com/@bootdotdev)"
        
        assert extract_markdown_images(text_img) == []
        assert extract_markdown_links(text_link) == []

    def test_extract_md_empty(self):
        text_img = ""
        text_link = ""

        assert extract_markdown_images(text_img) == []
        assert extract_markdown_links(text_link) == []

    def test_extract_md_inverted(self):
        text_img = "This is text with a (https://i.imgur.com/aKaOqIh.gif)![rick roll] and (https://i.imgur.com/fJRm4Vk.jpeg)![obi wan]"
        text_link = "This is text with a link to (https://www.boot.dev)[boot dev] and to (https://www.youtube.com/@bootdotdev)[youtube]"

        assert extract_markdown_images(text_img) == []
        assert extract_markdown_links(text_link) == []

    def test_split_nodes(self):
        image_node = [(TextNode("This is plain text ![alt text](www.image-url.com/)", TextType.TEXT))]
        link_node = [(TextNode("This is plain text [anchor text](www.link-url.com/)", TextType.TEXT))]

        expected_img_result = [
            TextNode("This is plain text ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "www.image-url.com/"),
            ]
        
        expected_lnk_result = [
            TextNode("This is plain text ", TextType.TEXT),
            TextNode("anchor text", TextType.LINK, "www.link-url.com/"),
            ]

        self.assertEqual(split_nodes_image(image_node), expected_img_result)
        self.assertEqual(split_nodes_link(link_node), expected_lnk_result)
    
    def test_split_nodes_double(self):
        image_node = [(TextNode("This is plain text ![alt text](www.image-url.com/) and another link ![alt text 2](www.image-url.com/2) more text", TextType.TEXT))]
        link_node = [(TextNode("This is plain text [anchor text](www.link-url.com/) and another link [anchor text 2](www.link-url.com/2) more text", TextType.TEXT))]

        expected_img_result = [
            TextNode("This is plain text ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "www.image-url.com/"),
            TextNode(" and another link ", TextType.TEXT),
            TextNode("alt text 2", TextType.IMAGE, "www.image-url.com/2"),
            TextNode(" more text", TextType.TEXT)
            ]
        
        expected_lnk_result = [
            TextNode("This is plain text ", TextType.TEXT),
            TextNode("anchor text", TextType.LINK, "www.link-url.com/"),
            TextNode(" and another link ", TextType.TEXT),
            TextNode("anchor text 2", TextType.LINK, "www.link-url.com/2"),
            TextNode(" more text", TextType.TEXT)
            ]

        self.assertEqual(split_nodes_image(image_node), expected_img_result)
        self.assertEqual(split_nodes_link(link_node), expected_lnk_result)
    
    def test_split_nodes_empty(self):
        node = []

        assert split_nodes_image(node) == []
        assert split_nodes_link(node) == []
    
    def test_split_nodes_only_md(self):
        image_node = [TextNode("![alt](url)", TextType.TEXT)]
        link_node = [TextNode("[anchor](url)", TextType.TEXT)]

        expected_img_result = [TextNode("alt", TextType.IMAGE, "url")]
        expected_lnk_result = [TextNode("anchor", TextType.LINK, "url")]

        self.assertEqual(split_nodes_image(image_node), expected_img_result)
        self.assertEqual(split_nodes_link(link_node), expected_lnk_result)

    def test_split_nodes_adjacent(self):
        image_node = [TextNode("![alt](url)![alt2](url2)", TextType.TEXT)]
        link_node = [TextNode("[anchor](url)[anchor2](url2)", TextType.TEXT)]

        expected_img_result = [TextNode("alt", TextType.IMAGE, "url"), TextNode("alt2", TextType.IMAGE, "url2")]
        expected_lnk_result = [TextNode("anchor", TextType.LINK, "url"), TextNode("anchor2", TextType.LINK, "url2")]

        self.assertEqual(split_nodes_image(image_node), expected_img_result)
        self.assertEqual(split_nodes_link(link_node), expected_lnk_result)

    def test_split_nodes_malformed_md(self):
        pass

if __name__ == "__main__":
    unittest.main()
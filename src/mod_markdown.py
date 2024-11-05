import re
from textnode import TextNode, TextType
from htmlnode import LeafNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """Converts raw text nodes imported from markdown to new objects.

    Args:
        old_nodes (lst([TextNode])): raw md text nodes
        delimiter (str): md tag symbol
        text_type (TextType): TextType object

    Returns:
        lst([TextNode]): Returns a list of correctly formatted TextNode-objects.
    """
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            first_delimiter = node.text.find(delimiter)
            if first_delimiter == -1:
                new_nodes.append(node)
            else:
                second_delimiter = node.text.find(delimiter, first_delimiter + len(delimiter))
                if second_delimiter == -1:
                    new_nodes.append(node)
                else:
                    first_text = node.text[:first_delimiter]
                    second_text = node.text[second_delimiter + len(delimiter):]
                    middle_text = node.text[first_delimiter + len(delimiter):second_delimiter]
                    new_nodes.append(TextNode(first_text, TextType.TEXT))
                    new_nodes.append(TextNode(middle_text, text_type))
                    new_nodes.append(TextNode(second_text, TextType.TEXT))

    return new_nodes


def text_node_to_html_node(text_node) -> LeafNode:

    if not isinstance(text_node.text_type, TextType):
        raise TypeError("Invalid text type")
    elif not isinstance(text_node, TextNode):
        raise AttributeError("Invalid object")

    tag_value = text_node.text_type.value

    if text_node.text_type == TextType.IMAGE:
        text_node = LeafNode(tag=tag_value, value="", props={"src": text_node.url, "alt": text_node.text})
    elif text_node.text_type == TextType.LINK:
        text_node = LeafNode(tag=tag_value, value=text_node.text, props={"href": text_node.url})
    else:
        text_node = LeafNode(tag=tag_value, value=text_node.text)
    return text_node


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_images(node.text)
        if not matches:
            new_nodes.append(node)
            continue

        current_text = node.text
        for image_alt, image_url in matches:
            sections = current_text.split(f"![{image_alt}]({image_url})", 1)

            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            
            current_text = sections[1]

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    extracted_result = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            extracted_result += extract_markdown_links(node.text)

    for text in extracted_result:
        new_nodes.append(TextNode(text[0], TextType.LINK, text[1]))

    return new_nodes


node = [(TextNode("This is text with an img link ![to imglink](https://www.123.se/wWerx234/) and ![to youtube](https://www.youtube.com) Click it now!", TextType.TEXT)),
        (TextNode("This is a text with another img link ![to google](https://www.google.se/)", TextType.TEXT)),
        (TextNode("123", TextType.TEXT))]

print(split_nodes_image(node))

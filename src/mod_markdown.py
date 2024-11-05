import re
from textnode import TextNode, TextType
from htmlnode import LeafNode

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

        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_links(node.text)
        if not matches:
            new_nodes.append(node)
            continue

        current_text = node.text
        for anchor, url in matches:
            sections = current_text.split(f"[{anchor}]({url})", 1)

            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(anchor, TextType.LINK, url))

            current_text = sections[1]

        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
            
    return new_nodes


def text_to_textnodes(text):
    if text == "" or type(text) != str:
        return

    old_nodes = [TextNode(text, TextType.TEXT)]

    delimiter_map = {
        '**': TextType.BOLD,
        '*': TextType.ITALIC,
        '`': TextType.CODE
    }

    for delimiter, text_type in delimiter_map.items():
            old_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
            old_nodes = split_nodes_image(old_nodes)
            old_nodes = split_nodes_link(old_nodes)

    return old_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def markdown_to_blocks(markdown):
    if markdown == "" or type(markdown) != str:
        return []

    blocks = re.split(r"\n\s*\n", markdown.strip())

    for index, string in enumerate(blocks):
        blocks[index] = string.strip()

    return blocks

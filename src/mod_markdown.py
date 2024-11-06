import re
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def markdown_to_html_node(markdown):
    if type(markdown) != str:
        raise TypeError("Provided markdown format is invalid.")
    # converts full md document to a single html node
    child_nodes = []

    html_node = HTMLNode(tag="div", children=child_nodes)

    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == "heading":
            header_tag = count_header_symbols(block)
            header_text = block.lstrip("# ").rstrip()
            header_text_nodes = text_to_textnodes(header_text)

            header_children = []
            for text_node in header_text_nodes:
                header_children.append(text_node_to_html_node(text_node))
            
            header_node = HTMLNode(tag=header_tag, children=header_children)
            child_nodes.append(header_node)

        elif block_type == "code":
            code_text = block.strip("`")
            code_node = HTMLNode(tag=TextType.CODE.value, value=code_text)
            pre_node = HTMLNode(tag="pre", children=[code_node])
            child_nodes.append(pre_node)

        elif block_type == "quote":
            quote_text = block.strip(">")
            quote_node = HTMLNode(tag="blockquote", value=quote_text) #props: {"cite": "url"}
            child_nodes.append(quote_node)
        
        elif block_type == "unordered list":
            lines = block.splitlines()
            uo_list_node = []

            for line in lines:
                if line.startswith("* ") or line.startswith("- ") or line.startswith("+ "):
                    unordered_text = line[2:]
                    uo_list_node.append(HTMLNode(tag="li", value=unordered_text))
                
            ul_node = HTMLNode(tag="ul", children=uo_list_node)
            child_nodes.append(ul_node)

        elif block_type == "ordered list":
            lines = block.splitlines()
            o_list_node = []

            for line in lines:
                if re.match(r"\d\.\s", line):
                    period_pos = line.find(".")
                    text_start = period_pos + 2
                    ordered_text = line[text_start:]
                    o_list_node.append(HTMLNode(tag="li", value=ordered_text))
                
            ol_node = HTMLNode(tag="ol", children=o_list_node)
            child_nodes.append(ol_node)

        elif block_type == "paragraph":
            p_node = HTMLNode(tag="p", value=block)
            child_nodes.append(p_node)

    return html_node


def count_header_symbols(block):
    count = 0
    header_tag = ""

    for char in block:
        if char == "#":
            count += 1
    if count > 6:
        return ""
    elif count == 1:
        header_tag = "h1"
    elif count == 2:
        header_tag = "h2"
    elif count == 3:
        header_tag = "h3"
    elif count == 4:
        header_tag = "h4"
    elif count == 5:
        header_tag = "h5"
    else:
        header_tag = "h6"
    
    return header_tag

def text_node_to_html_node(text_node) -> HTMLNode:

    if not isinstance(text_node.text_type, TextType):
        raise TypeError("Invalid text type")
    elif not isinstance(text_node, TextNode):
        raise AttributeError("Invalid object")

    tag_value = text_node.text_type.value

    if text_node.text_type == TextType.IMAGE:
        text_node = HTMLNode(tag=tag_value, value="", props={"src": text_node.url, "alt": text_node.text})
    elif text_node.text_type == TextType.LINK:
        text_node = HTMLNode(tag=tag_value, value=text_node.text, props={"href": text_node.url})
    else:
        text_node = HTMLNode(tag=tag_value, value=text_node.text)
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


def block_to_block_type(block):
    heading = re.match(r"^\#{1,6}\s.*$", block, re.MULTILINE)
    code = re.match(r"^(?:`{3})[\s\S]*?(?:`{3})$", block, re.MULTILINE)
    quote = re.match(r"^>.*$", block, re.MULTILINE)

    unordered_pattern = r"^(\*|-|\+)\s.*$"
    unordered_list = re.findall(unordered_pattern, block, re.MULTILINE)

    ordered_pattern = r"^\d+\.\s.*$"
    ordered_list = re.findall(ordered_pattern, block, re.MULTILINE)
    expected_number = 1
    sequence_broken = False

    if heading: 
        return "heading"
    elif code:
        return "code"
    elif quote:
        return "quote"
    elif unordered_list:
        return "unordered list"
    elif ordered_list:
        for item in ordered_list:
            match = re.match(r"^(\d+)\.", item.strip())

            if match:
                number = int(match.group(1))

                if number != expected_number:
                    sequence_broken = True
                expected_number += 1

        if not sequence_broken:  
            return "ordered list"
    
    return "paragraph"

md = None
print(markdown_to_html_node(md))
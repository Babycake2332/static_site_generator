from textnode import TextNode, TextType
from htmlnode import LeafNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
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

def text_node_to_html_node(text_node):

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


def main():
    node = TextNode("This is a **bold** text block", TextType.TEXT)
    node2 = TextNode("This is the **italic** text type", TextType.TEXT)

    nodes = [node, node2]
    split_nodes_delimiter(nodes, "**", TextType.BOLD)



if __name__ == '__main__':
    main()

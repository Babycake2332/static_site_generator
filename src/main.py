from textnode import TextNode, TextType
from htmlnode import LeafNode

def text_node_to_html_node(text_node):
    if not isinstance(text_node.text_type, TextType):
        raise TypeError("Invalid text type")

    if text_node.text_type == TextType.TEXT:
        text_node = LeafNode(value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        text_node = LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        text_node = LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        text_node = LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.IMAGE:
        text_node = LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})


def main():
    node = TextNode(text="hello there", text_type=TextType.BOLD)
    text_node_to_html_node(node)




if __name__ == '__main__':
    main()



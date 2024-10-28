from textnode import TextNode, TextType
from htmlnode import LeafNode

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
    node = TextNode(text="hello there", text_type=TextType.BOLD)
    text_node_to_html_node(node)




if __name__ == '__main__':
    main()

text_node = TextNode("Click me!", TextType.LINK, "https://www.google.se")
print(text_node)
print(text_node_to_html_node(text_node))

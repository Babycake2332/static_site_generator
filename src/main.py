from textnode import TextNode, TextType
from htmlnode import LeafNode
from mod_markdown import split_nodes_delimiter, text_node_to_html_node


def main():
    node = TextNode("This is a **bold** text block", TextType.TEXT)
    node2 = TextNode("This is the **italic** text type", TextType.TEXT)

    nodes = [node, node2]
    split_nodes_delimiter(nodes, "**", TextType.BOLD)



if __name__ == '__main__':
    main()

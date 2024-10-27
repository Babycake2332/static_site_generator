class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self) -> None | str:
        if self.props == None or self.props == {}:
            return ""
        
        props_pairs: str = ""
        for key, value in self.props.items():
            props_pairs = props_pairs + f" {key}=\"{value}\""
        return props_pairs
    
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"




class LeafNode(HTMLNode):

    def __init__(self, value, tag=None, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None or self.value == "":
            raise ValueError("LeafNode is missing required value.")
        elif self.tag == None:
            return f"{self.value}"
        props_attr = super().props_to_html()
        return f"<{self.tag}{props_attr}>{self.value}</{self.tag}>"




class ParentNode(HTMLNode):

    def __init__(self, children, tag=None, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode is missing the required tag")
        elif len(self.children) == 0:
            raise ValueError("ParentNode is missing the required children")
        
        html_string = ""
        for child in self.children:
            html_string += "".join(child.to_html())
        return f"<{self.tag}>{html_string}</{self.tag}>"
            

parent = ParentNode(tag="p", 
                    children=[LeafNode(tag="b", value="Bold text"), 
                           LeafNode(tag=None, value="Normal text"),
                           ParentNode(tag="div",
                                      children=[LeafNode(tag="a", value="Click me!", props={"href": "https://www.google.com", "target": "_blank"},),
                                                LeafNode(tag=None, value="Normal Text"),
                                                ],
                                                ),
                           LeafNode(tag="i", value="italic text"),
                           LeafNode(tag=None, value="Normal text"),
                           ],
                           )

print(parent.to_html())
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
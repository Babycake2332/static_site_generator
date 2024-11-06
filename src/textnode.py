from enum import Enum

class TextType(Enum):
    TEXT = 'text'
    BOLD = 'b'
    ITALIC = 'i'
    CODE = 'code'
    QUOTE = 'blockquote'
    LINK = 'a'
    IMAGE = 'img'

class TextNode:

    def __init__(self, text, text_type, url=None) -> None:
        self.text = text
        self.text_type = text_type
        self.url= url
    
    def __eq__(self, other) -> bool:
        if isinstance(other, TextNode):
            return (self.text == other.text
                    and self.text_type == other.text_type
                    and self.url == other.url) 
        return False
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
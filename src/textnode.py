from enum import Enum

class TextType(Enum): # html-taggar eller klartext??
    NORMAL = 'normal'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    LINKS = 'links'
    IMAGES = 'images'

class TextNode:

    def __init__(self, text, text_type, url):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return self.__init__ == other.__init__
    
    def __repr__(self):
        return list(str(self.text, self.text_type, self.url))
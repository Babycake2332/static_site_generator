from textnode import TextNode

object = TextNode('Hey there folks', 'normal', 'https://123.se')
other_object = TextNode('Haha', 'bold', 'urldefault')
print(object.text)
print(object.text_type)
print(object.url)

print(object.__eq__(other_object))
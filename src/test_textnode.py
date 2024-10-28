import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2) # should return True

    def test_eq_not(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertNotEqual(node, node2) # should return False
    
    def test_eq_none(self):
        node = TextNode("This is a text node", TextType.TEXT, None)
        node2 = TextNode("This is a text node", TextType.TEXT, None)
        self.assertEqual(node, node2) # should return True
    
    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://image.com")
        node2 = TextNode("This is a text node", TextType.IMAGE, "https://image.com")
        self.assertEqual(node, node2) # should return True   

if __name__ == '__main__':
    unittest.main()
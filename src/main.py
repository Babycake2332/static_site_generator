from textnode import TextNode

def main():
    object = TextNode('Hey there folks', 'normal')
    other_object = TextNode('Hey there folks', 'normal')

    print(object.__eq__(other_object))
    print(object)



if __name__ == '__main__':
    main()
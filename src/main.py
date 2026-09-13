from textnode import TextNode, TextType


def main():
    text_node = TextNode("this is dummy text", TextType.BOLD_TEXT, "fake.url")
    print(text_node)

main()

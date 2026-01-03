from textnode import TextType, TextNode

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Error: Not implemented")

    def props_to_html(self):
        if not self.props:
            return ""
        return "".join(f' {key}="{value}"' for key, value in self.props.items())

        def __repr__(self):
            return (
                f"HTMLNode(tag={self.tag}, "
                f"value={self.value}, "
                f"children={self.children}, "
                f"props={self.props})"
            )

class LeafNode(HTMLNode):

    def __init__(self, tag=None, value=None, props=None):
        # Call the parent class constructor using super()
        super().__init__(tag=tag, value=value, children = None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Error: All leaf nodes must have a value")
        elif self.tag is None:
            return self.value
        else:
            props_html = self.props_to_html()
            return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"

        """def __repr__(self):
            return (
                f"HTMLNode(tag={self.tag}, "
                f"value={self.value}, "
                f"children={self.children}, "
                f"props={self.props})"
            )"""

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        # Call the parent class constructor using super()
        super().__init__(tag=tag, value=None, children = children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.children is None:
            raise ValueError("invalid HTML: no children")
        else:
            children_html = ""
            props_html = self.props_to_html()
            for child in self.children:
                children_html += child.to_html()
            return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"

"""
class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
"""


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, props={"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", props={"src":text_node.url, "alt":text_node.text})
    
    raise Exception("Unknown TextType")









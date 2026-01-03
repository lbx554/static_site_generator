
import re
from textnode import TextNode, TextType
# from main import extract_markdown_links, extract_markdown_images
from htmlnode import text_node_to_html_node

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_nodes = node.text.split(delimiter)
            if len(split_nodes) % 2 == 0:
                raise Exception("Invalid markdown: unmatched delimiter")
            for i in range(len(split_nodes)):
                if i % 2 == 0:
                    new_nodes.append(TextNode(split_nodes[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split_nodes[i], text_type))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            images = extract_markdown_links(node.text)
            if len(images) == 0:
                new_nodes.append(node)    
            else:
                current_text = node.text
                for image in images:
                    alt_text, url = image
                    markdown_string = f"[{alt_text}]({url})"
                    sections = current_text.split(markdown_string, 1)

                    if sections[0]:
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))

                    new_nodes.append(TextNode(alt_text, TextType.LINK, url))

                    current_text = sections[1]

                if current_text:
                    new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            images = extract_markdown_images(node.text)
            if len(images) == 0:
                new_nodes.append(node)
            else:
                current_text = node.text
                for image in images:
                    alt_text, url = image
                    markdown_string = f"![{alt_text}]({url})"
                    sections = current_text.split(markdown_string, 1)

                    if sections[0]:
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))

                    new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

                    current_text = sections[1]

                if current_text:
                    new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def text_to_children(text):
    t_list = []
    textn = text_to_textnodes(text)
    for t in textn:
        tn = text_node_to_html_node(t)
        t_list.append(tn)
    return t_list

def markdown_to_blocks(markdown):
    split_mkd = markdown.split("\n\n")
    ans = [x.strip() for x in split_mkd if x.strip()]
    return ans




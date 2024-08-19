import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link
)

def text_to_textnodes(text):
    ret_val = [TextNode(text, text_type_text)]
    ret_val = split_nodes_delimiter(ret_val, "**", text_type_bold)
    ret_val = split_nodes_delimiter(ret_val, "*", text_type_italic)
    ret_val = split_nodes_delimiter(ret_val, "`", text_type_code)
    ret_val = split_nodes_image(ret_val)
    ret_val = split_nodes_link(ret_val)
    return ret_val

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    ret_val = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            ret_val.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError(f"Invalid markdown syntax, formatted section not close: {sections}")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        ret_val.extend(split_nodes)
    return ret_val

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    ret_val = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            ret_val.append(old_node)
            continue
        text_copy = old_node.text
        images = extract_markdown_images(text_copy)
        if len(images) == 0:
            ret_val.append(old_node)
            continue
        for image in images:
            sections = text_copy.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError(f"Invalid markdown, image not closed: {sections}")
            if sections[0] != "":
                ret_val.append(TextNode(sections[0], text_type_text))
            ret_val.append(TextNode(image[0], text_type_image, image[1],))
            text_copy = sections[1]
        if text_copy != "":
            ret_val.append(TextNode(text_copy, text_type_text))
    return ret_val

def split_nodes_link(old_nodes):
    ret_val = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            ret_val.append(old_node)
            continue
        text_copy = old_node.text
        links = extract_markdown_links(text_copy)
        if len(links) == 0:
            ret_val.append(old_node)
            continue
        for link in links:
            sections = text_copy.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError(f"Invalid markdown, link not closed: {sections}")
            if sections[0] != "":
                ret_val.append(TextNode(sections[0], text_type_text))
            ret_val.append(TextNode(link[0], text_type_link, link[1]))
            text_copy = sections[1]
        if text_copy != "":
            ret_val.append(TextNode(text_copy, text_type_text))
    return ret_val
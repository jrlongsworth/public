import re
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node
from htmlnode import ParentNode

block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered = "unordered_list"
block_type_ordered = "ordered_list"
block_type_paragraph = "paragraph"

def markdown_to_blocks(markdown):
    splits = markdown.split('\n\n')
    blocks = []
    for split in splits:
        if split != "":
            blocks.append(split.strip())
    return blocks

def block_to_block_type(markdown):
    lines = markdown.split("\n")
    if len(re.findall(r"#{1,6} .*", markdown)) == 1:
        return block_type_heading
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return block_type_code
    if markdown.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote
    if markdown.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return block_type_paragraph
        return block_type_unordered
    if markdown.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return block_type_paragraph
        return block_type_unordered
    if markdown.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return block_type_paragraph
            i += 1
        return block_type_ordered
    return block_type_paragraph

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    if block_type == block_type_heading:
        return heading_to_html_node(block)
    if block_type == block_type_code:
        return code_to_html_node(block)
    if block_type == block_type_quote:
        return quote_to_html_node(block)
    if block_type == block_type_unordered:
        return unordered_to_html_node(block)
    if block_type == block_type_ordered:
        return ordered_to_html_node(block)
    raise ValueError(f"Invalid block type: {block_type}")
        
def text_to_children(text):
    nodes = text_to_textnodes(text)
    children = []
    for node in nodes:
        html_node = text_node_to_html_node(node)
        children.append(html_node)
    return children

def paragraph_to_html_node(text):
    lines = text.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for character in block:
        if character == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError(f"Invalid code block: {block}")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])

def quote_to_html_node(block):
    lines = block.split("\n")
    ret_val = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError(f"Invalid quote block: {block}")
        ret_val.append(line.lstrip(">").strip())
    content = " ".join(ret_val)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def unordered_to_html_node(block):
    items = block.split("\n")
    ret_val = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        ret_val.append(ParentNode("li", children))
    return ParentNode("ul", ret_val)

def ordered_to_html_node(block):
    items = block.split("\n")
    ret_val = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        ret_val.append(ParentNode("li", children))
    return ParentNode("ol", ret_val)
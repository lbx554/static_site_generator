from blocktype import block_to_block_type, BlockType
from htmlnode import ParentNode, text_node_to_html_node
from textnode import TextNode, TextType
from split_node import text_to_children, markdown_to_blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    list_blocks = []
    
    for block in blocks:
        block_type = block_to_block_type(block)  # Determine what type this block is
        # print(f"DEBUG: Block: '{block}' -> Type: '{block_type}'")

        # Now create an HTMLNode based on the block_type
        if block_type == BlockType.paragraph:
            # print("DEBUG: Processing paragraph")
            children = text_to_children(block)  # Convert the block text to child nodes
            # print(f"DEBUG: Children: {children}")
            paragraph_node = ParentNode("p", children)  # Give it a name
            # print(f"DEBUG: Node HTML: {node.to_html()}")
            list_blocks.append(paragraph_node)

        elif block_type == BlockType.heading:
            # Create heading HTMLNode (you'll need to figure out h1, h2, etc.)
            count = 0
            for char in block:
                if char == '#':
                    count += 1
                else:
                    break  # Stop when you hit the first non-# character
            text_without_hashes = block[count:].strip()  # Skip first 'count' characters, then strip spaces
            lines = block.split()
            inner = "\n".join(lines[1:-1])

            children = text_to_children(text_without_hashes)  # Convert the block text to child nodes
            list_blocks.append(ParentNode(f"h{count}", children))

        elif block_type == BlockType.code:
            # Remove triple backticks from beginning and end
            text_without_backticks = block[3:-3].strip()  # Remove first 3 and last 3 chars

            # Create a TextNode (not HTMLNode!)
            clean_text_node = TextNode(text_without_backticks, TextType.TEXT)

            # Convert TextNode to HTMLNode
            text_html_node = text_node_to_html_node(clean_text_node)

            # Create <code> node with the text as child
            code_node = ParentNode("code", [text_html_node])

            # Create <pre> node with <code> as child
            pre_node = ParentNode("pre", [code_node])

            list_blocks.append(pre_node)

        elif block_type == BlockType.quote:
            lines = block.split("\n")
            clean_lines = []
            for line in lines:
                stripped = line.lstrip()
                if not stripped:
                    continue
                # remove leading ">" or "> "
                if stripped.startswith("> "):
                    clean_lines.append(stripped[2:])
                elif stripped.startswith(">"):
                    clean_lines.append(stripped[1:])
                else:
                    clean_lines.append(stripped)
            text_without_quote_marker = "\n".join(clean_lines)
            children = text_to_children(text_without_quote_marker)
            list_blocks.append(ParentNode("blockquote", children))

        elif block_type == BlockType.unordered_list:
            items = block.split("\n")
            li_nodes = []
            for item in items:
                stripped = item.lstrip()
                if not stripped:
                    continue
                # remove "- "
                if stripped.startswith("- "):
                    text_without_marker = stripped[2:]
                else:
                    text_without_marker = stripped
                children = text_to_children(text_without_marker)
                li_node = ParentNode("li", children)
                li_nodes.append(li_node)
            list_blocks.append(ParentNode("ul", li_nodes))

        elif block_type == BlockType.ordered_list:
            items = block.split("\n")
            li_nodes = []
            for item in items:
                stripped = item.lstrip()
                if not stripped:
                    continue
                space_index = stripped.find(" ")
                if space_index == -1:
                    continue
                text_without_marker = stripped[space_index + 1:]
                children = text_to_children(text_without_marker)
                li_node = ParentNode("li", children)
                li_nodes.append(li_node)
            list_blocks.append(ParentNode("ol", li_nodes))

    # Create the parent div with all blocks as children
    # print(f"DEBUG: Final list_blocks length: {len(list_blocks)}")
    parent_div = ParentNode("div", list_blocks)
    return parent_div

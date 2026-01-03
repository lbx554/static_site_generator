import enum

class BlockType(enum.Enum):
    paragraph = "PARAGRAPH"
    heading = "HEADING"
    code = "CODE"
    quote = "QUOTE"
    unordered_list = "UNORDERED_LIST"
    ordered_list = "ORDERED_LIST"

def block_to_block_type(markdown):
    lines = markdown.splitlines() # Split the entire block into a list of lines

    # Check for Code Block (can span multiple lines, but delimiters are on ends)
    if markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.code

    # Check for Quote Block
    # We need to make sure *every* line starts with '>'
    is_quote = True
    for line in lines:
        if not line.startswith(">"):
            is_quote = False
            break # If any line doesn't start with '>', it's not a quote block
    if is_quote and len(lines) > 0: # Ensure it's a quote and not an empty block
        return BlockType.quote

    # Your existing Heading, Unordered List, Ordered List logic would come here,
    # but they also need to be updated to check *all* lines if they are multi-line.
    # For example, for an unordered list:
    # Check for Unordered List Block
    is_unordered_list = True
    for line in lines:
        if not line.startswith("- "):
            is_unordered_list = False
            break
    if is_unordered_list and len(lines) > 0:
        return BlockType.unordered_list

    # Now, let's consider the Ordered List, which is a bit more complex due to numbering.
    # This logic would go after unordered list check, and before paragraph.
    is_ordered_list = True
    expected_num = 1
    for line in lines:
        # Check if line starts with 'NUMBER. '
        parts = line.split(". ", 1) # Split only at the first '. '
        if len(parts) < 2: # Not enough parts, doesn't match "NUMBER. text"
            is_ordered_list = False
            break
        
        try:
            current_num = int(parts[0]) # Try to convert the first part to an integer
        except ValueError: # If it's not a number, it's not an ordered list item
            is_ordered_list = False
            break
        
        if current_num != expected_num: # Check if the number is what we expect
            is_ordered_list = False
            break
        
        expected_num += 1 # Increment for the next line

    if is_ordered_list and len(lines) > 0:
        return BlockType.ordered_list

    # Your existing Heading check for a single line (or the first line)
    # would still apply. But if a heading was meant to be multi-line,
    # that's a different problem. For typical markdown, headings are single-line.
    if markdown.startswith("#"):
        hash_count = 0
        while hash_count < len(markdown) and markdown[hash_count] == "#":
            hash_count += 1
        if 1 <= hash_count <= 6 and hash_count < len(markdown) and markdown[hash_count] == ' ':
            return BlockType.heading


    # If none of the above conditions are met, it's a paragraph
    return BlockType.paragraph

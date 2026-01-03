import os
import shutil
import re
import sys

from textnode import TextNode, TextType
from converter import markdown_to_html_node
from split_node import extract_markdown_links, extract_markdown_images

def copy_static(source_dir, directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.mkdir(directory)
    copy_source = os.listdir(source_dir)
    for item_name in copy_source:
        source_item_path = os.path.join(source_dir, item_name)
        destination_item_path = os.path.join(directory, item_name)
        if os.path.isfile(source_item_path):
            shutil.copy(source_item_path, destination_item_path)
            print(f"{destination_item_path}\n")
        else:
            copy_static(source_item_path, destination_item_path)

def extract_title(markdown):
    for line in markdown.splitlines():
        # Now 'line' is each line from the markdown, one at a time
            match = re.match(r"^#(?!#)\s*(.*)$", line)
            if match:
                return match.group(1).strip()
            raise Exception("No h1 header found")
            
def generate_page(basepath, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    html_str = markdown_to_html_node(markdown).to_html()
    title_page = extract_title(markdown)
    html = template.replace("{{ Title }}", title_page)
    html = html.replace("{{ Content }}", html_str)

    html = html.replace('href="/', 'href="{basepath}')
    html = html.replace('src="/', 'src="{basepath}')
    
    dir_path = os.path.dirname(dest_path)
    os.makedirs(dir_path, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(html)

def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):
    for name in os.listdir(dir_path_content):
        full_path = os.path.join(dir_path_content, name)

        if os.path.isdir(full_path):
            new_dest_dir = os.path.join(dest_dir_path, name)
            os.makedirs(new_dest_dir, exist_ok=True)
            generate_pages_recursive(basepath, full_path, template_path, new_dest_dir)

        elif os.path.isfile(full_path) and name.endswith(".md"):
            html_name = name.replace(".md", ".html")
            dest_path = os.path.join(dest_dir_path, html_name)
            generate_page(basepath, full_path, template_path, dest_path)



"""def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)
    copy_static("static", "public")
"""

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def main():
    # Delete 'public' directory if it exists
    if os.path.exists("public"):
        shutil.rmtree("public")

    # Copy everything from 'static' to 'public'
    shutil.copytree("static", "public")

    """# Generate the main HTML page
    generate_page("content/index.md", "template.html", "public/index.html")

    # Blog pages
    generate_page(
        "content/blog/glorfindel/index.md",
        "template.html",
        "public/blog/glorfindel/index.html",
    )

    generate_page(
        "content/blog/tom/index.md",
        "template.html",
        "public/blog/tom/index.html",
    )

    generate_page(
        "content/blog/majesty/index.md",
        "template.html",
        "public/blog/majesty/index.html",
    )

    # Contact page
    generate_page(
        "content/contact/index.md",
        "template.html",
        "public/contact/index.html",
    )
    """
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    generate_pages_recursive(basepath, "content", "template.html", "docs")


if __name__ == "__main__":
    main()

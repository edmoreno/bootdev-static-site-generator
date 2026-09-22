import os
import shutil

from helpers import extract_title, markdown_to_html_node


def copy_files_recursive(source_dir: str, destination_dir: str) -> None:
    if not os.path.exists(source_dir):
        raise Exception(f"{source_dir} does not exist!")

    # delete existing destination dir and recreate it
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)
    os.mkdir(destination_dir)

    # copy files over from source to destination recursively
    for file in os.listdir(source_dir):
        full_source_path = os.path.join(source_dir, file)
        full_destination_path = os.path.join(destination_dir, file)
        if os.path.isfile(full_source_path):
            shutil.copy(full_source_path, full_destination_path)
        else:
            copy_files_recursive(full_source_path, full_destination_path)

    return None

def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    with open(from_path, "r", encoding="utf-8") as file:
        markdown = file.read()

    with open(template_path, "r", encoding="utf-8") as file:
        template = file.read()

    html_string = markdown_to_html_node(markdown).to_html()
    page_title = extract_title(markdown)
    template = template.replace("{{ Title }}", page_title)
    template = template.replace("{{ Content }}", html_string)

    parent = os.path.dirname(dest_path)
    if parent:
        os.makedirs(parent, exist_ok=True)

    with open(dest_path, "w", encoding='utf-8') as file:
        file.write(template)

    return None

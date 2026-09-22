from file_helpers import copy_files_recursive, generate_page

def main():
    copy_files_recursive("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

main()

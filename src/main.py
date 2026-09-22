from file_helpers import copy_files_recursive, generate_pages_recursive

def main():
    copy_files_recursive("static", "public")
    generate_pages_recursive("content", "template.html", "public")

main()

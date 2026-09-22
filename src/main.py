import sys

from file_helpers import copy_files_recursive, generate_pages_recursive

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    copy_files_recursive("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()

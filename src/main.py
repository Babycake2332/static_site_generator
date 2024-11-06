import os, shutil, errno
from mod_markdown import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as md:
        markdown = md.read()

    title = extract_title(markdown)
    markdown_node = markdown_to_html_node(markdown)
    html_string = markdown_node.to_html() 

    with open(template_path, "r") as temp:
        template_html = temp.read()

    final_html = template_html.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_string)
 
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    with open(dest_path, "w+") as dest:
        dest.write(final_html)


def copy_files(src, dest):

    if not os.path.exists(src):
        raise Exception("You are trying to access files from the wrong source directory.")

    if os.path.exists(dest):
        shutil.rmtree("./public")

    try:
        shutil.copytree(src, dest)
    except OSError as err:
        if err.errno == errno.ENOTDIR:
            shutil.copy2(src, dest)
        else:
            print("Error % s" % err)


def main():
    src = f"{os.getcwd()}/static"
    dest = f"{os.getcwd()}/public"

    from_path = "content/index.md"
    temp_path = "./template.html"
    dest_path = "public/index.html"
    copy_files(src, dest)
    generate_page(from_path, temp_path, dest_path)



if __name__ == '__main__':
    main()

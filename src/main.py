import os, shutil, errno
from mod_markdown import markdown_to_html_node, extract_title
from pathlib import Path

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def main():

    copy_files(dir_path_static, dir_path_public)
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)



def generate_pages_recursive(dir_path_content, template_path, dest_dir_path): # This function written by boot.dev
    
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)

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



if __name__ == '__main__':
    main()

import os
import glob

# Update index.html template
try:
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    if 'sitemap.xml' in content:
        content = content.replace('sitemap.xml', 'sitemap_index.xml')
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated index.html template.")
except Exception as e:
    print("Error updating index.html:", e)

# Update all .py files to fix BASE_DIR
py_files = glob.glob('*.py')
old_base_dir_str = r'BASE_DIR = "."'
new_base_dir_str = r'BASE_DIR = "."'

for py_file in py_files:
    try:
        with open(py_file, 'r', encoding='utf-8') as f:
            content = f.read()
        if old_base_dir_str in content:
            content = content.replace(old_base_dir_str, new_base_dir_str)
            with open(py_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated BASE_DIR in {py_file}.")
    except Exception as e:
        print(f"Error reading {py_file}: {e}")

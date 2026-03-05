import os
import re

def update_mobile_home(base_dir):
    re_mobile_home = re.compile(r'href="/"(\s*)class="block px-4 py-4 text-xl font-medium text-white hover:text-blue-400')
    count = 0
    errors = 0
    
    for root, dirs, files in os.walk(base_dir):
        rel_path = os.path.relpath(root, base_dir)
        if rel_path == '.':
            continue
            
        parts = rel_path.split(os.sep)
        city_slug = parts[0]
        
        # Only process city folders
        if not city_slug.endswith('-al'):
            continue
            
        for file in files:
            if not file.endswith('.html'):
                continue
                
            filepath = os.path.join(root, file)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                original_content = content
                
                content = re_mobile_home.sub(rf'href="/{city_slug}/"\1class="block px-4 py-4 text-xl font-medium text-white hover:text-blue-400', content)
                
                if content != original_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    count += 1
            except Exception as e:
                errors += 1
                
    print(f"Updated Mobile Home links in {count} HTML files. Errors: {errors}")

if __name__ == '__main__':
    update_mobile_home(r'c:\Users\lucia\Downloads\Zoiris-Cleaning-Services')

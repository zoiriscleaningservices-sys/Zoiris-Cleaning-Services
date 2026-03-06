import os
import re

def update_sitemap_links(base_dir):
    count = 0
    errors = 0
    
    # We are looking for: href="https://www.zoiriscleaningservices.com/sitemap.xml"
    re_sitemap = re.compile(r'href="https://www\.zoiriscleaningservices\.com/sitemap\.xml"')
    replacement = 'href="https://www.zoiriscleaningservices.com/sitemap_index.xml"'

    for root, dirs, files in os.walk(base_dir):
        # Exclude hidden directories and irrelevant caches
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'venv', '__pycache__']]
        
        for file in files:
            if not file.endswith('.html'):
                continue
                
            filepath = os.path.join(root, file)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                original_content = content
                content = re_sitemap.sub(replacement, content)
                
                if content != original_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    count += 1
                    
                if count > 0 and count % 10000 == 0:
                    print(f"Processed {count} files so far...")
                    
            except Exception as e:
                errors += 1
                
    print(f"Updated sitemap links in {count} HTML files. Encountered {errors} errors.")

if __name__ == '__main__':
    update_sitemap_links(".")

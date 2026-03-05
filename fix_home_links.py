import os
import re

def update_home_links(base_dir):
    re_onclick_logo = re.compile(r'onclick="location\.href=[\'"]/[\'"]"')
    re_nav_home = re.compile(r'href="/" class="contact-button text-lg">Home</a>')
    
    # Matches <a ... href="/index.html"><i class="fas fa-home ..."></i> Home</a>
    re_footer_home = re.compile(r'href="/index\.html"(\s*)><i([^>]*fa-home[^>]*)></i>(\s*)Home</a>')
    
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
                
                # Replace exact string: onclick="location.href='/'" -> onclick="location.href='/{city_slug}/'"
                content = re_onclick_logo.sub(f'onclick="location.href=\'/{city_slug}/\'"', content)
                
                # Replace exact string: href="/" class="contact-button text-lg">Home</a>
                content = re_nav_home.sub(f'href="/{city_slug}/" class="contact-button text-lg">Home</a>', content)
                
                # Replace exact string: href="/index.html"><i class="fas fa-home ..."></i> Home</a>
                content = re_footer_home.sub(rf'href="/{city_slug}/"\1><i\2></i>\3Home</a>', content)
                
                if content != original_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    count += 1
            except Exception as e:
                errors += 1
                
    print(f"Updated Home links in {count} HTML files. Encountered {errors} errors.")

if __name__ == '__main__':
    update_home_links(r'c:\Users\lucia\Downloads\Zoiris-Cleaning-Services')

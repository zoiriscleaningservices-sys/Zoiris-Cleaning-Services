import os
from datetime import datetime

BASE_DIR = r"c:\Users\lucia\OneDrive\Desktop\New folder (2)"
BASE_URL = "https://www.zoiriscleaningservices.com"
SITEMAP_FILE = os.path.join(BASE_DIR, "sitemap.xml")

def generate_sitemap():
    print(f"Scanning directory: {BASE_DIR} for index.html files...")
    
    urls = []
    
    for root, dirs, files in os.walk(BASE_DIR):
        # Exclude hidden folders, node_modules, temp builds
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'venv', '__pycache__', 'locations_backup']]
        
        for file in files:
            if file == "index.html":
                # Get the relative path
                rel_path = os.path.relpath(root, BASE_DIR)
                
                # If it's the root directory
                if rel_path == ".":
                    url = f"{BASE_URL}/"
                    priority = "1.0"
                else:
                    # Convert Windows paths to URL paths
                    url_path = rel_path.replace(os.sep, '/')
                    url = f"{BASE_URL}/{url_path}/"
                    
                    # Prioritize Service folders slightly differently
                    if len(url_path.split('/')) == 1:
                        # City hubs e.g. /mobile-al/ 
                        priority = "0.9"
                    else:
                        # Deep service pages e.g. /mobile-al/house-cleaning/
                        priority = "0.8"
                
                urls.append((url, priority))
                
    # Generate XML
    xml_header = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml_footer = '</urlset>'
    
    date_today = datetime.now().strftime("%Y-%m-%d")
    
    with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
        f.write(xml_header)
        for url, priority in urls:
            f.write(f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{date_today}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>{priority}</priority>\n  </url>\n")
        f.write(xml_footer)
        
    print(f"Sitemap generated successfully at {SITEMAP_FILE}")
    print(f"Total URLs indexed: {len(urls)}")

if __name__ == "__main__":
    generate_sitemap()

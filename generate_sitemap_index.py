import os
import datetime
from urllib.parse import quote

BASE_DIR = r"c:\Users\lucia\OneDrive\Desktop\New folder (2)"
DOMAIN = "https://www.zoiriscleaningservices.com"
MAX_URLS_PER_SITEMAP = 45000

def generate_sitemaps():
    print(f"Scanning directory: {BASE_DIR} for index.html files...")
    
    urls = []
    
    # Calculate URLs and Priorities
    for root, dirs, files in os.walk(BASE_DIR):
        # Exclude hidden directories and system folders
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'venv', '__pycache__', 'locations_backup']]
        
        for file in files:
            if file == 'index.html':
                filepath = os.path.join(root, file)
                # Calculate relative path from BASE_DIR
                rel_path = os.path.relpath(filepath, BASE_DIR)
                
                # Convert path separators to forward slashes
                rel_path = rel_path.replace(os.sep, '/')
                
                # Build URL path
                if rel_path == 'index.html':
                    url_path = ''
                else:
                    url_path = rel_path.replace('/index.html', '/')
                
                # Construct absolute URL
                abs_url = f"{DOMAIN}/{url_path}"
                
                # Determine priority based on depth
                depth = url_path.count('/')
                if depth == 0:
                    priority = "1.0"
                elif depth == 1:
                    priority = "0.9" # Main service pages or city hubs
                elif depth == 2:
                    priority = "0.8" # Specific service within city hub
                else:
                    priority = "0.7"
                
                urls.append((abs_url, priority))
                
                if len(urls) % 10000 == 0:
                    print(f"Found {len(urls)} URLs so far...")

    total_urls = len(urls)
    print(f"Extraction complete. Found {total_urls} unique URLs.")
    
    # Chunking into multiple sitemaps
    chunks = [urls[i:i + MAX_URLS_PER_SITEMAP] for i in range(0, total_urls, MAX_URLS_PER_SITEMAP)]
    
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    sitemap_files = []
    
    # Write individual sitemap chunks
    for index, chunk in enumerate(chunks):
        sitemap_filename = f"sitemap-{index + 1}.xml"
        sitemap_path = os.path.join(BASE_DIR, sitemap_filename)
        sitemap_files.append(sitemap_filename)
        
        xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        
        for url, priority in chunk:
            xml_content += '  <url>\n'
            # encode URL to be XML safe
            safe_url = url.replace('&', '&amp;').replace("'", '&apos;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
            xml_content += f'    <loc>{safe_url}</loc>\n'
            xml_content += f'    <lastmod>{today}</lastmod>\n'
            xml_content += '    <changefreq>weekly</changefreq>\n'
            xml_content += f'    <priority>{priority}</priority>\n'
            xml_content += '  </url>\n'
            
        xml_content += '</urlset>'
        
        with open(sitemap_path, "w", encoding="utf-8") as f:
            f.write(xml_content)
            
        print(f"Generated {sitemap_filename} with {len(chunk)} URLs.")

    # Write the Master Sitemap Index
    index_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    index_xml += '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for sf in sitemap_files:
        index_xml += '  <sitemap>\n'
        index_xml += f'    <loc>{DOMAIN}/{sf}</loc>\n'
        index_xml += f'    <lastmod>{today}</lastmod>\n'
        index_xml += '  </sitemap>\n'
        
    index_xml += '</sitemapindex>'
    
    index_path = os.path.join(BASE_DIR, "sitemap_index.xml")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_xml)
        
    print(f"Master Sitemap Index successfully generated at {index_path}.")
    print("WARNING: You can now safely delete the old monolithic 'sitemap.xml' file if it exists.")

if __name__ == "__main__":
    generate_sitemaps()

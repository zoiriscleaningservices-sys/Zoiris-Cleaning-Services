import os
import xml.etree.ElementTree as ET
from datetime import datetime

BASE_URL = "https://www.zoiriscleaningservices.com/"
MAX_URLS_PER_SITEMAP = 45000

def get_html_files(directory):
    html_files = []
    for root, _, files in os.walk(directory):
        # Skip git or other hidden dirs
        if '.git' in root or '.gemini' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                # Get relative path
                rel_dir = os.path.relpath(root, directory)
                if rel_dir == '.':
                    rel_path = file
                else:
                    rel_path = os.path.join(rel_dir, file)
                
                # Convert Windows slashes to forward slashes
                rel_path = rel_path.replace('\\', '/')
                
                # Optional: clean up 'index.html' to just '/' for clean URLs
                # if rel_path.endswith('index.html'):
                #     if rel_path == 'index.html':
                #         rel_path = ''
                #     else:
                #         rel_path = rel_path[:-10] # remove index.html
                
                html_files.append(rel_path)
    return html_files

def generate_sitemaps():
    print("Finding all HTML files...")
    files = get_html_files('.')
    print(f"Found {len(files)} HTML files.")

    # Split into chunks
    chunks = [files[i:i + MAX_URLS_PER_SITEMAP] for i in range(0, len(files), MAX_URLS_PER_SITEMAP)]
    
    sitemap_files = []
    today = datetime.now().strftime('%Y-%m-%d')

    for index, chunk in enumerate(chunks):
        sitemap_filename = f'sitemap_{index}.xml'
        sitemap_files.append(sitemap_filename)
        
        print(f"Generating {sitemap_filename} with {len(chunk)} URLs...")
        
        urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
        
        for file in chunk:
            url_node = ET.SubElement(urlset, "url")
            loc_node = ET.SubElement(url_node, "loc")
            
            # Construct the full URL
            full_url = BASE_URL + file
            loc_node.text = full_url
            
            # Max SEO authority
            priority_node = ET.SubElement(url_node, "priority")
            priority_node.text = "1.0"
            
            changefreq_node = ET.SubElement(url_node, "changefreq")
            changefreq_node.text = "daily"

        # Write the chunk to a file
        tree = ET.ElementTree(urlset)
        # Indent for readability
        ET.indent(tree, space="  ", level=0)
        tree.write(sitemap_filename, encoding='utf-8', xml_declaration=True)

    # Generate Sitemap Index
    print("Generating sitemap_index.xml...")
    sitemapindex = ET.Element("sitemapindex", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    for sitemap_file in sitemap_files:
        sitemap_node = ET.SubElement(sitemapindex, "sitemap")
        loc_node = ET.SubElement(sitemap_node, "loc")
        loc_node.text = BASE_URL + sitemap_file
        
    tree = ET.ElementTree(sitemapindex)
    ET.indent(tree, space="  ", level=0)
    tree.write('sitemap_index.xml', encoding='utf-8', xml_declaration=True)
    print("Done!")

if __name__ == "__main__":
    generate_sitemaps()

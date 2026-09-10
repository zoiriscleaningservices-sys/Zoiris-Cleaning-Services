import os
import json
import xml.etree.ElementTree as ET
from datetime import datetime

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def generate_sitemaps():
    print("Generating comprehensive sitemaps...")
    
    with open(os.path.join(root_dir, 'seo', 'locations.json'), 'r', encoding='utf-8') as f:
        locations = json.load(f)
        
    with open(os.path.join(root_dir, 'seo', 'services.json'), 'r', encoding='utf-8') as f:
        services = json.load(f)
        
    today = datetime.now().strftime("%Y-%m-%d")
    
    # URL list
    urls = []
    
    # 1. Homepage
    urls.append({"loc": "https://www.zoiriscleaningservices.com/", "lastmod": today, "changefreq": "daily", "priority": "1.0"})
    
    # 2. Main static pages
    for page in ["about", "contact", "blog", "locations"]:
        if os.path.exists(os.path.join(root_dir, page, "index.html")) or os.path.exists(os.path.join(root_dir, f"{page}.html")):
            urls.append({"loc": f"https://www.zoiriscleaningservices.com/{page}/", "lastmod": today, "changefreq": "weekly", "priority": "0.9"})
        
    # 3. Location Hubs & Location-Service Pages
    for loc_slug, loc in locations.items():
        loc_dir = os.path.join(root_dir, loc_slug)
        if not os.path.isdir(loc_dir):
            continue
            
        tier = loc.get("tier", "C")
        hub_priority = "0.9" if tier == "A" else ("0.8" if tier == "B" else "0.7")
        urls.append({"loc": f"https://www.zoiriscleaningservices.com/{loc_slug}/", "lastmod": today, "changefreq": "weekly", "priority": hub_priority})
        
        # Location-Service subpages
        srv_priority = "0.8" if tier in ["A", "B"] else "0.6"
        for srv_slug in services.keys():
            srv_file = os.path.join(loc_dir, srv_slug, "index.html")
            if os.path.isfile(srv_file):
                urls.append({"loc": f"https://www.zoiriscleaningservices.com/{loc_slug}/{srv_slug}/", "lastmod": today, "changefreq": "weekly", "priority": srv_priority})
                
    # Build XML
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for u in urls:
        url_el = ET.SubElement(urlset, "url")
        loc_el = ET.SubElement(url_el, "loc")
        loc_el.text = u["loc"]
        lastmod_el = ET.SubElement(url_el, "lastmod")
        lastmod_el.text = u["lastmod"]
        changefreq_el = ET.SubElement(url_el, "changefreq")
        changefreq_el.text = u["changefreq"]
        priority_el = ET.SubElement(url_el, "priority")
        priority_el.text = u["priority"]
        
    tree = ET.ElementTree(urlset)
    out_path = os.path.join(root_dir, "sitemap_0.xml")
    tree.write(out_path, encoding="utf-8", xml_declaration=True)
    
    # Index sitemap
    sitemapindex = ET.Element("sitemapindex", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    sitemap_el = ET.SubElement(sitemapindex, "sitemap")
    loc_el = ET.SubElement(sitemap_el, "loc")
    loc_el.text = "https://www.zoiriscleaningservices.com/sitemap_0.xml"
    lastmod_el = ET.SubElement(sitemap_el, "lastmod")
    lastmod_el.text = today
    
    idx_tree = ET.ElementTree(sitemapindex)
    idx_path = os.path.join(root_dir, "sitemap_index.xml")
    idx_tree.write(idx_path, encoding="utf-8", xml_declaration=True)
    
    print(f"Successfully generated sitemap with {len(urls)} indexable URLs.")

if __name__ == '__main__':
    generate_sitemaps()


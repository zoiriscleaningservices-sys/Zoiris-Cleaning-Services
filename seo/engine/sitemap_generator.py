import os
import json
import xml.etree.ElementTree as ET
from datetime import datetime

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def generate_sitemaps():
    print("Generating sitemaps...")
    
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
        urls.append({"loc": f"https://www.zoiriscleaningservices.com/{page}/", "lastmod": today, "changefreq": "weekly", "priority": "0.8"})
        
    # 3. Location Hubs & Priority Services
    for slug, loc in locations.items():
        priority = "0.9" if loc.get("tier") == "A" else "0.7"
        urls.append({"loc": f"https://www.zoiriscleaningservices.com/{slug}/", "lastmod": today, "changefreq": "weekly", "priority": priority})
        
        # Priority service pages for Tier A locations
        if loc.get("tier") == "A":
            for srv_slug in ["deep-cleaning", "move-in-cleaning", "move-out-cleaning", "commercial-cleaning", "vacation-rental-cleaning", "airbnb-cleaning", "carpet-cleaning"]:
                urls.append({"loc": f"https://www.zoiriscleaningservices.com/{slug}/{srv_slug}/", "lastmod": today, "changefreq": "weekly", "priority": "0.8"})
                
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
    
    print(f"Generated sitemap with {len(urls)} indexable priority URLs.")

if __name__ == '__main__':
    generate_sitemaps()

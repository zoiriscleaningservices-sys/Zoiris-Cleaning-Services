import os
import json
import xml.etree.ElementTree as ET
from datetime import datetime

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Core service territory where Zoiris operates with physical crews
PRIMARY_TERRITORY = {
    "mobile-al", "midtown-mobile-al", "spring-hill-al", "west-mobile-al",
    "daphne-al", "fairhope-al", "spanish-fort-al", "saraland-al", "satsuma-al",
    "semmes-al", "theodore-al", "chickasaw-al", "eight-mile-al", "creola-al",
    "foley-al", "gulf-shores-al", "orange-beach-al", "bay-minette-al",
    "robertsdale-al", "loxley-al", "summerdale-al", "elberta-al",
    "dauphin-island-al", "grand-bay-al", "point-clear-al", "montrose-al"
}

# Major Alabama Metros outside immediate Gulf Coast
MAJOR_METROS = {
    "birmingham-al", "huntsville-al", "montgomery-al", "tuscaloosa-al",
    "auburn-al", "hoover-al", "madison-al", "decatur-al", "dothan-al",
    "florence-al", "gadsden-al", "opelika-al", "pelham-al", "prattville-al",
    "vestavia-hills-al", "albertville-al", "athens-al", "enterprise-al"
}

def create_xml_sitemap(urls, filename):
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
    out_path = os.path.join(root_dir, filename)
    tree.write(out_path, encoding="utf-8", xml_declaration=True)
    print(f"  -> Generated {filename} with {len(urls)} URLs")

def generate_sitemaps():
    print("Generating priority-tiered sitemaps for maximum crawl efficiency...")
    
    with open(os.path.join(root_dir, 'seo', 'locations.json'), 'r', encoding='utf-8') as f:
        locations = json.load(f)
        
    with open(os.path.join(root_dir, 'seo', 'services.json'), 'r', encoding='utf-8') as f:
        services = json.load(f)
        
    today = datetime.now().strftime("%Y-%m-%d")
    
    priority_urls = []
    metro_urls = []
    regional_urls = []
    
    # 1. Homepage & Primary Global Pages -> Priority Sitemap
    priority_urls.append({"loc": "https://www.zoiriscleaningservices.com/", "lastmod": today, "changefreq": "daily", "priority": "1.0"})
    priority_urls.append({"loc": "https://www.zoiriscleaningservices.com/locations/", "lastmod": today, "changefreq": "weekly", "priority": "0.9"})
    
    # Check for core static directories
    for page in ["about", "contact", "blog"]:
        for prefix in ["mobile-al", ""]:
            p = f"{prefix}/{page}" if prefix else page
            if os.path.isdir(os.path.join(root_dir, p)):
                priority_urls.append({"loc": f"https://www.zoiriscleaningservices.com/{p}/", "lastmod": today, "changefreq": "weekly", "priority": "0.85"})
                break

    # 2. Sort Locations into Priority, Metros, and Regional
    for loc_slug, loc in locations.items():
        loc_dir = os.path.join(root_dir, loc_slug)
        if not os.path.isdir(loc_dir):
            continue
            
        if loc_slug in PRIMARY_TERRITORY or loc_slug == "mobile-al":
            target_list = priority_urls
            hub_prio = "0.95" if loc_slug == "mobile-al" else "0.90"
            srv_prio = "0.85"
            cf_hub = "daily" if loc_slug == "mobile-al" else "weekly"
        elif loc_slug in MAJOR_METROS:
            target_list = metro_urls
            hub_prio = "0.80"
            srv_prio = "0.75"
            cf_hub = "weekly"
        else:
            target_list = regional_urls
            hub_prio = "0.65"
            srv_prio = "0.55"
            cf_hub = "monthly"
            
        # Add Location Hub
        target_list.append({"loc": f"https://www.zoiriscleaningservices.com/{loc_slug}/", "lastmod": today, "changefreq": cf_hub, "priority": hub_prio})
        
        # Add Location Services
        for srv_slug in services.keys():
            srv_file = os.path.join(loc_dir, srv_slug, "index.html")
            if os.path.isfile(srv_file):
                target_list.append({"loc": f"https://www.zoiriscleaningservices.com/{loc_slug}/{srv_slug}/", "lastmod": today, "changefreq": "weekly" if target_list is priority_urls else "monthly", "priority": srv_prio})

    # Write Sitemaps
    create_xml_sitemap(priority_urls, "sitemap_priority.xml")
    create_xml_sitemap(metro_urls, "sitemap_metros.xml")
    create_xml_sitemap(regional_urls, "sitemap_regions.xml")
    
    # Also maintain sitemap_0.xml as a combined priority+metro fallback
    create_xml_sitemap(priority_urls + metro_urls, "sitemap_0.xml")
    
    # Generate Master Index Sitemap listing priority first
    sitemapindex = ET.Element("sitemapindex", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    sitemaps_to_index = [
        "https://www.zoiriscleaningservices.com/sitemap_priority.xml",
        "https://www.zoiriscleaningservices.com/sitemap_metros.xml",
        "https://www.zoiriscleaningservices.com/sitemap_regions.xml"
    ]
    
    for sm_loc in sitemaps_to_index:
        sitemap_el = ET.SubElement(sitemapindex, "sitemap")
        loc_el = ET.SubElement(sitemap_el, "loc")
        loc_el.text = sm_loc
        lastmod_el = ET.SubElement(sitemap_el, "lastmod")
        lastmod_el.text = today
        
    idx_tree = ET.ElementTree(sitemapindex)
    idx_path = os.path.join(root_dir, "sitemap_index.xml")
    idx_tree.write(idx_path, encoding="utf-8", xml_declaration=True)
    print(f"  -> Generated sitemap_index.xml with {len(sitemaps_to_index)} priority sitemaps.")

    total = len(priority_urls) + len(metro_urls) + len(regional_urls)
    print(f"\n[DONE] Successfully indexed {total} total URLs across 3 strategic tiers.")
    print(f"  - Tier 1 (Priority Core): {len(priority_urls)} URLs (Mobile & Baldwin County)")
    print(f"  - Tier 2 (Major Metros):  {len(metro_urls)} URLs (Birmingham, Huntsville, etc.)")
    print(f"  - Tier 3 (Regional AL):   {len(regional_urls)} URLs (Statewide coverage)")

if __name__ == '__main__':
    generate_sitemaps()

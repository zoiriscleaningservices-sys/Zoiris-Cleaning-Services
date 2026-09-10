import os
import json

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load datastores
try:
    with open(os.path.join(root_dir, 'seo', 'locations.json'), 'r', encoding='utf-8') as f:
        LOCATIONS = json.load(f)
except Exception:
    LOCATIONS = {}

try:
    with open(os.path.join(root_dir, 'seo', 'services.json'), 'r', encoding='utf-8') as f:
        SERVICES = json.load(f)
except Exception:
    SERVICES = {}

NON_SERVICES = {"about", "contact", "blog", "terms", "privacy", "404", "dashboard", "gallery"}

def classify_page(filepath):
    rel_path = os.path.relpath(filepath, root_dir).replace('\\', '/')
    parts = rel_path.split('/')
    
    classification = {
        "filepath": filepath,
        "rel_path": rel_path,
        "page_type": "unknown",
        "location_slug": "mobile-al",
        "city_name": "Mobile",
        "state": "AL",
        "service_slug": "",
        "service_name": "House Cleaning",
        "tier": "B",
        "is_priority": False,
        "canonical_path": "/"
    }
    
    # Homepage
    if rel_path in ["index.html", ""]:
        classification.update({
            "page_type": "homepage",
            "location_slug": "mobile-al",
            "city_name": "Mobile",
            "service_slug": "house-cleaning",
            "service_name": "House Cleaning & Maid Services",
            "tier": "A",
            "is_priority": True,
            "canonical_path": "/"
        })
        return classification
        
    # Root informational / legal pages
    if len(parts) == 1 and parts[0].endswith('.html'):
        base = parts[0][:-5]
        if base in ["about", "contact", "blog", "privacy", "terms", "dashboard", "gallery", "404"]:
            classification.update({
                "page_type": base,
                "tier": "A",
                "is_priority": True,
                "canonical_path": f"/{base}.html" if base != "index" else "/"
            })
            return classification
            
    # Location folders (e.g. daphne-al/...)
    if parts[0].endswith('-al'):
        loc_slug = parts[0]
        classification["location_slug"] = loc_slug
        if loc_slug in LOCATIONS:
            loc_data = LOCATIONS[loc_slug]
            classification["city_name"] = loc_data.get("city", loc_slug[:-3].replace('-', ' ').title())
            classification["tier"] = loc_data.get("tier", "B")
            classification["is_priority"] = (classification["tier"] == "A")
        else:
            classification["city_name"] = loc_slug[:-3].replace('-', ' ').title()
            
        # City Hub (e.g. daphne-al/index.html)
        if len(parts) == 2 and parts[1] == "index.html":
            classification.update({
                "page_type": "location_hub",
                "service_slug": "house-cleaning",
                "service_name": "House Cleaning & Maid Services",
                "canonical_path": f"/{loc_slug}/"
            })
            return classification
            
        # City Service or Subpage (e.g. daphne-al/deep-cleaning/index.html)
        if len(parts) >= 2:
            sub = parts[1]
            if sub in NON_SERVICES:
                classification.update({
                    "page_type": f"location_{sub}",
                    "service_slug": sub,
                    "service_name": sub.capitalize(),
                    "canonical_path": f"/{loc_slug}/{sub}/"
                })
                return classification
            elif sub.lower().startswith("detailing"):
                classification.update({
                    "page_type": "location_service",
                    "service_slug": "detailing",
                    "service_name": "Detailing",
                    "canonical_path": f"/{loc_slug}/{sub}/"
                })
                return classification
            else:
                # Regular service
                srv_name = SERVICES.get(sub, {}).get("name", " ".join([w.capitalize() for w in sub.split('-')]))
                classification.update({
                    "page_type": "location_service",
                    "service_slug": sub,
                    "service_name": srv_name,
                    "canonical_path": f"/{loc_slug}/{sub}/"
                })
                return classification
                
    # Root subdirectories (e.g. locations/, gallery/)
    if parts[0] == "locations":
        classification.update({
            "page_type": "locations_index",
            "city_name": "Alabama",
            "tier": "A",
            "is_priority": True,
            "canonical_path": "/locations/"
        })
        return classification

    return classification

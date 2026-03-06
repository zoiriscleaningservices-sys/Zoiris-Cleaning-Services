import os
import json
import re
import math

BASE_DIR = "."
DB_FILE = os.path.join(BASE_DIR, "city_coords.json")

# Haversine formula to calculate distance between two lat/lon points
def get_distance(lat1, lon1, lat2, lon2):
    R = 3958.8 # Earth radius in miles
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def inject_dynamic_nav_test():
    print("Loading Geo-Coordinate DB...")
    if not os.path.exists(DB_FILE):
        print(f"Error: {DB_FILE} not found. Run build_geo_db.py first.")
        return
        
    with open(DB_FILE, "r") as f:
        db = json.load(f)
        
    print(f"Loaded {len(db)} cities. Preparing Test execution on Mobile, Huntsville, and Birmingham...")
    
    test_hubs = ['mobile-al', 'huntsville-al', 'birmingham-al']
    count = 0
    modified = 0

    # Read template first to understand what we're replacing
    # The old dropdown looks like this:
    # <div class="absolute left-0 top-full hidden group-hover:flex flex-col w-56 z-50"><a
    # class="contact-button text-lg hover:bg-blue-700" href="/spanish-fort-al/">Spanish Fort</a>...</div>
    old_nav_regex = re.compile(r'<div class="absolute left-0 top-full hidden group-hover:flex flex-col w-56 z-50">.*?</div>', re.DOTALL)

    for hub in test_hubs:
        hub_dir = os.path.join(BASE_DIR, hub)
        if not os.path.exists(hub_dir):
            continue
            
        for root, dirs, files in os.walk(hub_dir):
            for file in files:
                if file == "index.html":
                    count += 1
                    filepath = os.path.join(root, file)
                    
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                        
                    city_match = re.search(r'<title>.*?in (.*?), AL', content)
                    if not city_match:
                        city_match = re.search(r'<title>.*?\| Zoiris Cleaning Services in (.*?), AL', content)
                        
                    current_city = city_match.group(1) if city_match else hub.replace("-al", "").title().replace("-", " ")
                    
                    # Ensure we have coordinates for this city
                    if current_city not in db:
                        # try to find it via slug logic
                        found = False
                        for db_city in db.keys():
                            if db_city.lower().replace(" ", "-").replace("'", "").replace(".", "") == hub.replace("-al", ""):
                                current_city = db_city
                                found = True
                                break
                        if not found:
                            continue # skip if we can't find coords
                            
                    current_coords = db[current_city]
                    
                    # Calculate distances to all other cities
                    distances = []
                    for c_name, c_coords in db.items():
                        if c_name == current_city: continue
                        dist = get_distance(current_coords["lat"], current_coords["lon"], c_coords["lat"], c_coords["lon"])
                        distances.append((c_name, dist))
                        
                    # Sort by distance and grab top 15
                    distances.sort(key=lambda x: x[1])
                    top_15 = distances[:15]
                    
                    # Build new HTML dropdown
                    new_nav_html = '<div class="absolute left-0 top-full hidden group-hover:flex flex-col w-56 z-50">\n'
                    for c_name, dist in top_15:
                        c_slug = c_name.lower().replace(" ", "-").replace("'", "").replace(".", "") + "-al"
                        new_nav_html += f'                    <a class="contact-button text-lg hover:bg-blue-700" href="/{c_slug}/">{c_name}</a>\n'
                    new_nav_html += '                  </div>'
                    
                    # Replace in content
                    if old_nav_regex.search(content):
                        content = old_nav_regex.sub(new_nav_html, content)
                        
                        # Save
                        with open(filepath, "w", encoding="utf-8") as out:
                            out.write(content)
                        modified += 1

    print(f"Dynamic Nav DB Test Complete. Modified {modified} out of {count} files in the 3 test hubs.")
    print(f"Calculated top 15 for {current_city}: {[c[0] for c in top_15]}")

if __name__ == "__main__":
    inject_dynamic_nav_test()

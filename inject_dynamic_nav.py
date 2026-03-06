import os
import json
import re
import math
from multiprocessing import Pool

BASE_DIR = "."
DB_FILE = os.path.join(BASE_DIR, "city_coords.json")

# Haversine formula
def get_distance(lat1, lon1, lat2, lon2):
    R = 3958.8 # miles
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

# Regex to match the dropdown container and links inside
old_nav_regex = re.compile(r'<div class="absolute left-0 top-full hidden group-hover:flex flex-col w-56 z-50">.*?</div>', re.DOTALL)

def process_file_chunk(filepaths_chunk):
    with open(DB_FILE, "r") as f:
        db = json.load(f)
        
    modified_count = 0
    for filepath in filepaths_chunk:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                
            city_match = re.search(r'<title>.*?in (.*?), AL', content)
            if not city_match:
                city_match = re.search(r'<title>.*?\| Zoiris Cleaning Services in (.*?), AL', content)
            
            # Extract folder name to back up city resolving if title matches fail
            hub_dir = os.path.basename(os.path.dirname(os.path.dirname(filepath)))
            if hub_dir == "locations" or "locations" in filepath:
               continue

            current_city = city_match.group(1) if city_match else "Mobile"
            
            if current_city not in db:
                found = False
                for db_city in db.keys():
                    slugified = db_city.lower().replace(" ", "-").replace("'", "").replace(".", "") + "-al"
                    if slugified in filepath:
                        current_city = db_city
                        found = True
                        break
                if not found:
                    current_city = "Mobile" # Fallback
            
            current_coords = db[current_city]
            
            distances = []
            for c_name, c_coords in db.items():
                if c_name == current_city: continue
                dist = get_distance(current_coords["lat"], current_coords["lon"], c_coords["lat"], c_coords["lon"])
                distances.append((c_name, dist))
                
            distances.sort(key=lambda x: x[1])
            top_15 = distances[:15]
            
            new_nav_html = '<div class="absolute left-0 top-full hidden group-hover:flex flex-col w-56 z-50">\n'
            for c_name, dist in top_15:
                c_slug = c_name.lower().replace(" ", "-").replace("'", "").replace(".", "") + "-al"
                new_nav_html += f'                    <a class="contact-button text-lg hover:bg-blue-700" href="/{c_slug}/">{c_name}</a>\n'
            new_nav_html += '                  </div>'
            
            if old_nav_regex.search(content):
                content = old_nav_regex.sub(new_nav_html, content)
                with open(filepath, "w", encoding="utf-8") as out:
                    out.write(content)
                modified_count += 1
                
        except Exception as e:
            pass # ignore parse errors on singleton files
            
    return modified_count


if __name__ == "__main__":
    print("Initiating Multi-Threaded Phase 5 Geo-Navigation Injection across 97,000 documents...")
    all_filepaths = []
    
    # Collect all targeted HTML files
    for root, dirs, files in os.walk(BASE_DIR):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'venv', '__pycache__', 'locations_backup']]
        for file in files:
            if file == "index.html":
                filepath = os.path.join(root, file)
                if "locations" not in filepath: 
                    all_filepaths.append(filepath)

    print(f"Total HTML documents found for DB Injection: {len(all_filepaths)}")
    
    # Use 8 cores
    cores = min(os.cpu_count(), 8)
    chunk_size = len(all_filepaths) // cores
    chunks = [all_filepaths[i:i + chunk_size] for i in range(0, len(all_filepaths), chunk_size)]
    
    with Pool(cores) as p:
        results = p.map(process_file_chunk, chunks)
        
    print(f"Phase 5 Complete! Geo Navigation active across {sum(results)} documents.")

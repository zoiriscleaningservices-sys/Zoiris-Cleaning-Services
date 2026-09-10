import os
import json

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
city_coords_file = os.path.join(root_dir, 'city_coords.json')

with open(city_coords_file, 'r', encoding='utf-8') as f:
    coords_db = json.load(f)

# Priority Tier A markets
TIER_A_CITIES = {
    'mobile-al', 'daphne-al', 'fairhope-al', 'spanish-fort-al', 'foley-al',
    'gulf-shores-al', 'orange-beach-al', 'saraland-al', 'semmes-al',
    'theodore-al', 'satsuma-al', 'grand-bay-al', 'robertsdale-al',
    'bay-minette-al', 'loxley-al', 'elberta-al', 'summerdale-al',
    'dauphin-island-al', 'birmingham-al', 'huntsville-al', 'montgomery-al',
    'tuscaloosa-al', 'auburn-al', 'hoover-al', 'madison-al', 'prattville-al',
    'dothan-al', 'decatur-al', 'florence-al', 'gadsden-al', 'vestavia-hills-al',
    'albertville-al', 'enterprise-al', 'opelika-al', 'athens-al', 'pelham-al'
}

locations = {}

for item in os.listdir(root_dir):
    item_path = os.path.join(root_dir, item)
    if os.path.isdir(item_path) and item.endswith('-al'):
        slug = item
        # e.g. "mobile-al" -> "Mobile", "bay-minette-al" -> "Bay Minette"
        raw_words = slug[:-3].split('-')
        city_name = " ".join([w.capitalize() for w in raw_words])
        
        # Determine coordinates
        lat = 30.6954  # Default Mobile AL
        lon = -88.0399
        if city_name in coords_db:
            lat = coords_db[city_name].get('lat', lat)
            lon = coords_db[city_name].get('lon', lon)
            
        tier = 'A' if slug in TIER_A_CITIES else 'B'
        
        locations[slug] = {
            "slug": slug,
            "city": city_name,
            "state": "AL",
            "country": "US",
            "service_area": True,
            "indexable": True,
            "tier": tier,
            "coordinates": {
                "latitude": lat,
                "longitude": lon
            },
            "display_title": f"{city_name}, AL",
            "county": "Mobile County" if slug in {'mobile-al', 'saraland-al', 'semmes-al', 'theodore-al', 'satsuma-al', 'grand-bay-al', 'dauphin-island-al'} else ("Baldwin County" if slug in {'daphne-al', 'fairhope-al', 'spanish-fort-al', 'foley-al', 'gulf-shores-al', 'orange-beach-al', 'robertsdale-al', 'bay-minette-al', 'loxley-al', 'elberta-al', 'summerdale-al'} else "Alabama")
        }

output_path = os.path.join(root_dir, 'seo', 'locations.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(locations, f, indent=2)

print(f"Generated seo/locations.json with {len(locations)} locations. Tier A: {sum(1 for l in locations.values() if l['tier'] == 'A')}, Tier B: {sum(1 for l in locations.values() if l['tier'] == 'B')}")

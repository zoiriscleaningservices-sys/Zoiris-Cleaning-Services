import urllib.request
import re

url = "https://en.wikipedia.org/wiki/List_of_municipalities_in_Alabama"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')

# Extract cities from the first column of the table
matches = re.findall(r'<th scope="row">.*?<a href="/wiki/[^"]+" title="([^"]+)"', html)

cities = []
seen = set()
for m in matches:
    if "Alabama" in m or "," not in m:
        name = m.split(",")[0].strip()
        
        # Omit generic wikipedia stuff that might get caught
        if "County" in name or name == "Alabama":
            continue
            
        slug = name.lower().replace(" ", "-").replace("'", "").replace(".", "") + "-al"
        
        if slug not in seen:
            seen.add(slug)
            cities.append((slug, name))
        
# Sort alphabetically
cities.sort(key=lambda x: x[1])

print(f"Found {len(cities)} cities.")
with open("all_alabama_cities.txt", "w", encoding="utf-8") as f:
    for slug, name in cities:
        f.write(f'    ("{slug}", "{name}"),\n')

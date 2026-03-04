import os
import shutil
import re

print("Optimizing archive to ensure homepage links work...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Find all explicitly linked locations in index.html
linked_cities = set(re.findall(r'href="/([^/]+-al)/"', html))
print(f"Found {len(linked_cities)} distinct cities linked directly from the homepage.")

# Move all directories back to root first to be safe
archive_dir = "archived_cities"
if os.path.exists(archive_dir):
    for item in os.listdir(archive_dir):
        shutil.move(os.path.join(archive_dir, item), item)

# Re-archive everything EXCEPT what's linked on the homepage
all_cities = [d for d in os.listdir('.') if os.path.isdir(d) and d.endswith('-al')]

cities_to_keep = linked_cities
cities_to_archive = [c for c in all_cities if c not in cities_to_keep]

print(f"Keeping {len(cities_to_keep)} linked cities. Archiving {len(cities_to_archive)} unlinked cities.")

for city in cities_to_archive:
    try:
        shutil.move(city, os.path.join(archive_dir, city))
    except Exception as e:
        print(f"Error moving {city}: {e}")

print("Archive synchronized with homepage links successfully.")

import os
import shutil
import glob

print("Archiving excess cities to get under the 1 GB GitHub limit...")

all_cities = [d for d in os.listdir('.') if os.path.isdir(d) and d.endswith('-al')]
all_cities.sort()

# Keep the first 100 cities for the first push.
cities_to_keep = all_cities[:50]
cities_to_archive = all_cities[50:]

print(f"Keeping {len(cities_to_keep)} cities. Archiving {len(cities_to_archive)} cities.")

for city in cities_to_archive:
    try:
        shutil.move(city, os.path.join('archived_cities', city))
    except Exception as e:
        print(f"Error moving {city}: {e}")

print("Done. Repository size should be reduced.")

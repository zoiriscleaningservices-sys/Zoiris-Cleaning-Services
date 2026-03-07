import os
import glob

BASE_DIR = r"c:\Users\lucia\Downloads\Zoiris-Cleaning-Services"
SKIP_MARKER = "zcs-spintax-injected"
OLD_MARKER = 'id="alternative-to-'  # from inject_merry_maids / inject_normas

cities_injected = 0
cities_missing = 0
pages_injected = 0
pages_missing = 0
sample_missing = []

for item in sorted(os.listdir(BASE_DIR)):
    full = os.path.join(BASE_DIR, item)
    if not (os.path.isdir(full) and item.endswith("-al")):
        continue
    
    html_files = glob.glob(os.path.join(full, "**", "*.html"), recursive=True)
    if not html_files:
        continue
    
    city_has_block = False
    city_missing = 0
    
    for fp in html_files[:5]:  # Check first 5 files per city
        with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        if SKIP_MARKER in content or OLD_MARKER in content:
            city_has_block = True
        else:
            city_missing += 1
    
    if city_has_block:
        cities_injected += 1
        pages_injected += len(html_files)
    else:
        cities_missing += 1
        pages_missing += len(html_files)
        if len(sample_missing) < 5:
            sample_missing.append(item)

print(f"Cities WITH injection:    {cities_injected}")
print(f"Cities WITHOUT injection: {cities_missing}")
print(f"Estimated injected pages: {pages_injected}")
print(f"Estimated missing pages:  {pages_missing}")
print(f"Sample missing cities:    {sample_missing}")

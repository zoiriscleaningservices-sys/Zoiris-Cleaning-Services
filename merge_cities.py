import re

# Read the full file
with open('generate_statewide_full.py', 'r', encoding='utf-8') as f:
    orig_content = f.read()

# Extract the old cities list string block
old_cities_block = re.search(r'cities = \[(.*?)\]', orig_content, re.DOTALL).group(1)

# Extract individual established cities
old_cities = re.findall(r'    \("([^"]+)", "([^"]+)"\)', old_cities_block)
old_city_set = set(slug for slug, name in old_cities)

# Read the new Wikipedia cities
with open('all_alabama_cities.txt', 'r', encoding='utf-8') as f:
    new_cities_raw = f.read()

# Extract the new cities
new_cities = re.findall(r'    \("([^"]+)", "([^"]+)"\)', new_cities_raw)

# Merge ensuring no duplicates (prioritize old ones to be safe)
merged_cities = list(old_cities)
for slug, name in new_cities:
    if slug not in old_city_set:
        merged_cities.append((slug, name))
        old_city_set.add(slug)

# Sort them alphabetically
merged_cities.sort(key=lambda x: x[1])

# Create the new cities block string
new_cities_str = "cities = [\n"
for slug, name in merged_cities:
    new_cities_str += f'    ("{slug}", "{name}"),\n'
# Remove trailing comma on last item
new_cities_str = new_cities_str.rstrip(",\n") + "\n]"

# Inject back into the file
new_content = re.sub(r'cities = \[(.*?)\]', new_cities_str, orig_content, flags=re.DOTALL)

with open('generate_statewide_full.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Successfully merged! The list grew from {len(old_cities)} to {len(merged_cities)} cities.")

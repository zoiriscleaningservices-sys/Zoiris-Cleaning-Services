import os

# Base directory
BASE_DIR = r"c:\Users\lucia\OneDrive\Desktop\New folder (2)"

# The template index file
TEMPLATE_FILE = os.path.join(BASE_DIR, "index.html")

# Read template
with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# Make substitutions targeting just the root's metadata URLs to /mobile-al/
content = content.replace(
    '<link rel="canonical" href="https://www.zoiriscleaningservices.com/" />',
    '<link rel="canonical" href="https://www.zoiriscleaningservices.com/mobile-al/" />'
)
content = content.replace(
    '<meta property="og:url" content="https://www.zoiriscleaningservices.com/" />',
    '<meta property="og:url" content="https://www.zoiriscleaningservices.com/mobile-al/" />'
)

# Write to mobile-al/index.html
out_dir = os.path.join(BASE_DIR, "mobile-al")
os.makedirs(out_dir, exist_ok=True)
out_file = os.path.join(out_dir, "index.html")

with open(out_file, "w", encoding="utf-8") as out:
    out.write(content)

print(f"Successfully copied Main index.html to {out_file} with adjusted canonical/og URLs.")

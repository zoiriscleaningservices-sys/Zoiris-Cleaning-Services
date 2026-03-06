import os
import re
from PIL import Image
import urllib.request

base_dir = "."
index_path = os.path.join(base_dir, "index.html")

# Download the main logo
logo_url = "https://i.ibb.co/gbzKPdnc/Chat-GPT-Image-Aug-31-2025-12-19-42-AM-Picsart-Background-Remover.png"
logo_path = os.path.join(base_dir, "logo.png")
import shutil

logo_path = os.path.join(base_dir, "images", "logo.png")
shutil.copyfile(r"C:\Users\lucia\.gemini\antigravity\brain\034a902f-78cb-433e-a3a1-b0d0ee9cc460\media__1772799578712.png", logo_path)


# Generate favicons
img = Image.open(logo_path)
favicon_dir = os.path.join(base_dir, "favicon")
os.makedirs(favicon_dir, exist_ok=True)

img.resize((16, 16)).save(os.path.join(favicon_dir, "favicon-16x16.png"))
img.resize((32, 32)).save(os.path.join(favicon_dir, "favicon-32x32.png"))
img.resize((180, 180)).save(os.path.join(favicon_dir, "apple-touch-icon.png"))
img.resize((192, 192)).save(os.path.join(favicon_dir, "android-chrome-192x192.png"))
img.resize((512, 512)).save(os.path.join(favicon_dir, "android-chrome-512x512.png"))
img.save(os.path.join(favicon_dir, "favicon.ico"), format="ICO", sizes=[(32, 32)])

with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

# Replace the hero image CSS background
html = html.replace(
    "url('https://i.ibb.co/F4gsMz1c/7e6c60fb-e7da-4ac4-9db4-251daab42a76.png')",
    "url('/images/location_hero.png')"
)

# And also pre-load hero image
html = html.replace(
    '''<link as="image" fetchpriority="high" href="https://i.ibb.co/F4gsMz1c/7e6c60fb-e7da-4ac4-9db4-251daab42a76.png"\n    rel="preload" />''',
    '''<link as="image" fetchpriority="high" href="/images/location_hero.png"\n    rel="preload" />'''
)
html = html.replace(
    '<link as="image" fetchpriority="high" href="https://i.ibb.co/F4gsMz1c/7e6c60fb-e7da-4ac4-9db4-251daab42a76.png" rel="preload" />',
    '<link as="image" fetchpriority="high" href="/images/location_hero.png" rel="preload" />'
)

html = html.replace(
    'https://i.ibb.co/gbzKPdnc/Chat-GPT-Image-Aug-31-2025-12-19-42-AM-Picsart-Background-Remover.png',
    '/images/logo.png'
)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Favicons generated from logo and hero photo updated!")

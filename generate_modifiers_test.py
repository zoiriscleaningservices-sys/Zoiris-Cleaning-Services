import os
import re

BASE_DIR = "."
TEMPLATE_FILE = os.path.join(BASE_DIR, "index.html")

# We only test on Mobile to ensure layout doesn't break
test_cities = [
    ("mobile-al", "Mobile")
]

modifiers = [
    ("best", "Best"),
    ("affordable", "Affordable"),
    ("top-rated", "Top-Rated"),
    ("36602", "36602"),
    ("36608", "36608")
]

services = [
    ("house-cleaning", "House Cleaning"),
    ("deep-cleaning", "Deep Cleaning"),
    ("commercial-cleaning", "Commercial Cleaning"),
    ("move-in-cleaning", "Move-In Cleaning")
]

with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
    template_content = f.read()

count = 0
for slug, city_name in test_cities:
    # 1. Base Localization of the template
    base_content = template_content.replace("/mobile-al/", f"/{slug}/")
    base_content = base_content.replace("mobile-al", f"{slug}")
    base_content = base_content.replace("Mobile, AL", f"{city_name}, AL")
    base_content = base_content.replace("Mobile, Alabama", f"{city_name}, Alabama")
    base_content = base_content.replace("Downtown Mobile", f"Downtown {city_name}")
    base_content = base_content.replace('"addressLocality": "Mobile"', f'"addressLocality": "{city_name}"')
    base_content = base_content.replace("Mobile area", f"{city_name} area")
    base_content = base_content.replace("Mobile, Baldwin County", f"{city_name} & surrounding areas")
    base_content = base_content.replace("Mobile", f"{city_name}")
    
    hub_dir = os.path.join(BASE_DIR, slug)
    target_url = f"https://www.zoiriscleaningservices.com/{slug}/"
    
    # Generate variations
    for m_slug, m_name in modifiers:
        for s_slug, s_name in services:
            count += 1
            mod_slug = f"{m_slug}-{s_slug}"
            
            # Special case for zip codes: use "Best" internally instead of repeating the zip code as an adjective
            # Example: "36602 House Cleaning" sounds weird, so we do "House Cleaning in 36602"
            is_zip = m_slug.isdigit()
            if is_zip:
                title_name = f"Top {s_name} in {m_name}, {city_name}"
                desc_name = f"the best {s_name.lower()} in the {m_name} zip code area"
                h1_name = f"#1 {s_name} in {m_name}, {city_name} AL"
                schema_name = f"the leading {s_name.lower()} provider for {m_name}, {city_name}"
            else:
                title_name = f"Top {m_name} {s_name} in {city_name}, AL"
                desc_name = f"the {m_name.lower()} {s_name.lower()} in the {city_name} area"
                h1_name = f"#1 {m_name} {s_name} in {city_name}, AL"
                schema_name = f"the leading {m_name.lower()} {s_name.lower()} company"

            page_url = f"{target_url}{mod_slug}/"
            
            content = base_content
            # SEO Replacements
            # Title
            content = content.replace(f"<title>#1 Cleaning Service in {city_name}, AL | Zoiris Cleaning Services</title>", f"<title>{title_name} | Zoiris Cleaning Services</title>")
            
            # Meta Description
            content = content.replace(f'content="Cleaning Services in {city_name}, AL. Zoiris Cleaning Services offer the best house cleaning and maid services in the {city_name} area.', f'content="Looking for {desc_name}? Zoiris Cleaning Services guarantees a spotless finish.')
            
            # OG tags
            content = content.replace(f'content="House Cleaning Services in {city_name}, AL. Free Estimate | Zoiris Cleaning Services"', f'content="{title_name} - Free Estimate | Zoiris Cleaning Services"')
            content = content.replace('<meta property="og:url" content="https://www.zoiriscleaningservices.com/" />', f'<meta property="og:url" content="{page_url}" />')
            
            # Canonical
            content = content.replace('<link rel="canonical" href="https://www.zoiriscleaningservices.com/" />', f'<link rel="canonical" href="{page_url}" />')
            
            # Schema
            content = content.replace('"description": "Zoiris Cleaning Service is the leading residential, commercial, and Airbnb cleaning company', f'"description": "Zoiris Cleaning Service is {schema_name}')
            content = content.replace('"@id": "https://www.zoiriscleaningservices.com/#business",', f'"@id": "{page_url}#business",')
            content = content.replace('"url": "https://www.zoiriscleaningservices.com/",', f'"url": "{page_url}",')
            
            # H1
            content = content.replace(f'#1 Cleaning Services in {city_name}, AL', h1_name)
            
            # Hero sub
            if not is_zip:
                content = content.replace('<em>residential & commercial cleaning</em>', f'<em>{m_name.lower()} {s_name.lower()}</em>')
            else:
                content = content.replace('<em>residential & commercial cleaning</em>', f'<em>{s_name.lower()} in {m_name}</em>')

            out_dir = os.path.join(hub_dir, mod_slug)
            os.makedirs(out_dir, exist_ok=True)
            with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as out:
                out.write(content)

print(f"Test Generated {count} modifier/zip clusters for Mobile, AL!")

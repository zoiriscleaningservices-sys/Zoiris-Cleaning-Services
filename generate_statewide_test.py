import os
import re

BASE_DIR = "."
TEMPLATE_FILE = os.path.join(BASE_DIR, "index.html")

cities = [
    ("birmingham-al", "Birmingham"),
    ("montgomery-al", "Montgomery"),
    ("huntsville-al", "Huntsville")
]

# Note: Detailing folder will be "Detailing-Birmingham-AL" after the replace commands!
services = [
    ("house-cleaning", "House Cleaning"),
    ("deep-cleaning", "Deep Cleaning"),
    ("move-in-cleaning", "Move-In Cleaning"),
    ("move-out-cleaning", "Move-Out Cleaning"),
    ("carpet-cleaning", "Carpet Cleaning"),
    ("window-cleaning", "Window Cleaning"),
    ("pressure-washing", "Pressure Washing"),
    ("luxury-estate-cleaning", "Luxury Estate Cleaning"),
    ("laundry-services", "Laundry Services"),
    ("Detailing-{City}-AL", "Detailing"), # We'll handle this in the loop
    
    ("commercial-cleaning", "Commercial Cleaning"),
    ("office-janitorial-services", "Office Janitorial Services"),
    ("janitorial-cleaning-services", "Janitorial Cleaning Services"),
    ("medical-dental-facility-cleaning", "Medical Facility Cleaning"),
    ("industrial-warehouse-cleaning", "Industrial & Warehouse Cleaning"),
    ("floor-stripping-waxing", "Floor Stripping & Waxing"),
    ("gym-fitness-center-cleaning", "Gym & Fitness Center Cleaning"),
    ("school-daycare-cleaning", "School & Daycare Cleaning"),
    ("church-worship-center-cleaning", "Church & Worship Cleaning"),
    ("solar-panel-cleaning", "Solar Panel Cleaning"),
    
    ("vacation-rental-cleaning", "Vacation Rental Cleaning"),
    ("airbnb-cleaning", "Airbnb Cleaning"),
    ("airbnb-vacation-rental-management", "Airbnb & Rental Management"),
    ("post-construction-cleanup", "Post-Construction Cleanup"),
    ("property-management-janitorial", "Property Management Janitorial"),
    ("property-maintenance", "Property Maintenance"),
    ("home-watch-services", "Home Watch Services"),
    ("luxury-estate-management", "Luxury Estate Management"),
    ("gutter-cleaning", "Gutter Cleaning")
]

extras = [
    ("about", "About Us"),
    ("blog", "Cleaning Blog"),
    ("contact", "Contact Us")
]

with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
    template_content = f.read()

for slug, city_name in cities:
    print(f"Generating Hub for {city_name}...")
    
    # 1. Base Localization of the template
    # Convert template specifically to the City
    base_content = template_content.replace("/mobile-al/", f"/{slug}/")
    base_content = base_content.replace("mobile-al", f"{slug}")
    base_content = base_content.replace("Mobile, AL", f"{city_name}, AL")
    base_content = base_content.replace("Mobile, Alabama", f"{city_name}, Alabama")
    base_content = base_content.replace("Downtown Mobile", f"Downtown {city_name}")
    base_content = base_content.replace('"addressLocality": "Mobile"', f'"addressLocality": "{city_name}"')
    base_content = base_content.replace("Mobile area", f"{city_name} area")
    base_content = base_content.replace("Mobile, Baldwin County", f"{city_name} & surrounding areas")
    base_content = base_content.replace("Mobile", f"{city_name}") # Catch any lingering capitalized Mobile like Detailing-Mobile-AL
    
    # Create the hub directory
    hub_dir = os.path.join(BASE_DIR, slug)
    os.makedirs(hub_dir, exist_ok=True)
    
    # Generate the Base Hub index.html
    target_url = f"https://www.zoiriscleaningservices.com/{slug}/"
    hub_content = base_content.replace(
        '<link rel="canonical" href="https://www.zoiriscleaningservices.com/" />',
        f'<link rel="canonical" href="{target_url}" />'
    ).replace(
        '<meta property="og:url" content="https://www.zoiriscleaningservices.com/" />',
        f'<meta property="og:url" content="{target_url}" />'
    ).replace(
        '"@id": "https://www.zoiriscleaningservices.com/#business",',
        f'"@id": "{target_url}#business",'
    ).replace(
        '"url": "https://www.zoiriscleaningservices.com/",',
        f'"url": "{target_url}",'
    )
    
    with open(os.path.join(hub_dir, "index.html"), "w", encoding="utf-8") as base_f:
        base_f.write(hub_content)
        
    # Generate the 29 Services
    for s_slug, service_name in services:
        if "Detailing" in s_slug:
            s_slug = f"Detailing-{city_name}-AL"
            
        content = hub_content
        page_url = f"{target_url}{s_slug}/"
        
        # SEO Replacements
        content = content.replace(
            f"<title>#1 Cleaning Service in {city_name}, AL | Zoiris Cleaning Services</title>",
            f"<title>#1 {service_name} in {city_name}, AL | Zoiris Cleaning Services</title>"
        )
        content = content.replace(
            f'content="Cleaning Services in {city_name}, AL. Zoiris Cleaning Services offer the best house cleaning and maid services in the {city_name} area.',
            f'content="{service_name} in {city_name}, AL. Zoiris Cleaning Services offer the best {service_name.lower()} in the {city_name} area.'
        )
        content = content.replace(
            f'content="House Cleaning Services in {city_name}, AL. Free Estimate | Zoiris Cleaning Services"',
            f'content="{service_name} in {city_name}, AL. Free Estimate | Zoiris Cleaning Services"'
        )
        content = content.replace(
            '"description": "Zoiris Cleaning Service is the leading residential, commercial, and Airbnb cleaning company',
            f'"description": "Zoiris Cleaning Service is the leading {service_name.lower()} company'
        )
        content = content.replace(
            f'#1 Cleaning Services in {city_name}, AL',
            f'#1 {service_name} in {city_name}, AL'
        )
        content = content.replace(
            '<em>residential & commercial cleaning</em>',
            f'<em>{service_name.lower()}</em>'
        )
        
        # Link replacements (since hub_content already has the base hub targeting)
        content = content.replace(
            f'<link rel="canonical" href="{target_url}" />',
            f'<link rel="canonical" href="{page_url}" />'
        )
        content = content.replace(
            f'<meta property="og:url" content="{target_url}" />',
            f'<meta property="og:url" content="{page_url}" />'
        )
        content = content.replace(
            f'"@id": "{target_url}#business",',
            f'"@id": "{page_url}#business",'
        )
        content = content.replace(
            f'"url": "{target_url}",',
            f'"url": "{page_url}",'
        )
        
        out_dir = os.path.join(hub_dir, s_slug)
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as out:
            out.write(content)

    # Generate the 3 Extras
    for e_slug, e_name in extras:
        content = hub_content
        page_url = f"{target_url}{e_slug}/"
        
        content = content.replace(
            f"<title>#1 Cleaning Service in {city_name}, AL | Zoiris Cleaning Services</title>",
            f"<title>{e_name} | Zoiris Cleaning Services in {city_name}, AL</title>"
        )
        content = content.replace(
            f'content="Cleaning Services in {city_name}, AL. Zoiris Cleaning Services offer the best house cleaning and maid services in the {city_name} area.',
            f'content="{e_name} for Zoiris Cleaning Services in {city_name}, AL. We offer the best residential and commercial cleaning in the {city_name} area.'
        )
        content = content.replace(
            f'content="House Cleaning Services in {city_name}, AL. Free Estimate | Zoiris Cleaning Services"',
            f'content="{e_name} | Zoiris Cleaning Services"'
        )
        content = content.replace(
            '"description": "Zoiris Cleaning Service is the leading residential, commercial, and Airbnb cleaning company',
            f'"description": "{e_name} page for Zoiris Cleaning Service, the leading residential, commercial, and Airbnb cleaning company'
        )
        content = content.replace(
            f'#1 Cleaning Services in {city_name}, AL',
            f'{e_name}'
        )
        
        if e_name == "About Us":
            hero_subtext = f"Learn more about <em>Zoiris Cleaning Service</em>, your trusted provider for residential & commercial cleaning across {city_name} and nearby cities."
        elif e_name == "Cleaning Blog":
            hero_subtext = f"Read the latest tips, tricks, and news from <em>Zoiris Cleaning Service</em> on how to maintain a spotless home or business in {city_name}."
        elif e_name == "Contact Us":
            hero_subtext = f"Get in touch with <em>Zoiris Cleaning Service</em> today. We are ready to help with your residential & commercial cleaning needs across {city_name}."
            
        content = content.replace(
            f'<strong>Zoiris Cleaning Service</strong> provides trusted\n          <em>residential & commercial cleaning</em> across\n          <strong>{city_name} & surrounding areas, and nearby cities</strong>.\n          From deep cleans to move-in/out and eco-friendly solutions, we make your home or business spotless.',
            hero_subtext
        )
        
        # Alternate catch for string replace due to lines formatting:
        content = re.sub(
            r'<strong>Zoiris Cleaning Service</strong> provides trusted\s*<em>residential & commercial cleaning</em> across\s*<strong>.*?</strong>.\s*From deep cleans to move-in/out and eco-friendly solutions, we make your home or business spotless.',
            hero_subtext,
            content,
            flags=re.DOTALL
        )
        
        # Link replacements
        content = content.replace(
            f'<link rel="canonical" href="{target_url}" />',
            f'<link rel="canonical" href="{page_url}" />'
        )
        content = content.replace(
            f'<meta property="og:url" content="{target_url}" />',
            f'<meta property="og:url" content="{page_url}" />'
        )
        content = content.replace(
            f'"@id": "{target_url}#business",',
            f'"@id": "{page_url}#business",'
        )
        content = content.replace(
            f'"url": "{target_url}",',
            f'"url": "{page_url}",'
        )

        out_dir = os.path.join(hub_dir, e_slug)
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as out:
            out.write(content)

print("Test generation complete!")

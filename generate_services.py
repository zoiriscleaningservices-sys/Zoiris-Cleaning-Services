import os
import re

# Base directory for the new folders
BASE_DIR = "."

# The template index file
TEMPLATE_FILE = os.path.join(BASE_DIR, "index.html")

# Services list as tuples of (folder_name, service_name)
services = [
    # Residential
    ("mobile-al/house-cleaning", "House Cleaning"),
    ("mobile-al/deep-cleaning", "Deep Cleaning"),
    ("mobile-al/move-in-cleaning", "Move-In Cleaning"),
    ("mobile-al/move-out-cleaning", "Move-Out Cleaning"),
    ("mobile-al/carpet-cleaning", "Carpet Cleaning"),
    ("mobile-al/window-cleaning", "Window Cleaning"),
    ("mobile-al/pressure-washing", "Pressure Washing"),
    ("mobile-al/luxury-estate-cleaning", "Luxury Estate Cleaning"),
    ("mobile-al/laundry-services", "Laundry Services"),
    ("mobile-al/Detailing-Mobile-AL", "Detailing"),
    
    # Commercial
    ("mobile-al/commercial-cleaning", "Commercial Cleaning"),
    ("mobile-al/office-janitorial-services", "Office Janitorial Services"),
    ("mobile-al/janitorial-cleaning-services", "Janitorial Cleaning Services"),
    ("mobile-al/medical-dental-facility-cleaning", "Medical Facility Cleaning"),
    ("mobile-al/industrial-warehouse-cleaning", "Industrial & Warehouse Cleaning"),
    ("mobile-al/floor-stripping-waxing", "Floor Stripping & Waxing"),
    ("mobile-al/gym-fitness-center-cleaning", "Gym & Fitness Center Cleaning"),
    ("mobile-al/school-daycare-cleaning", "School & Daycare Cleaning"),
    ("mobile-al/church-worship-center-cleaning", "Church & Worship Cleaning"),
    ("mobile-al/solar-panel-cleaning", "Solar Panel Cleaning"),
    
    # Property Management
    ("mobile-al/vacation-rental-cleaning", "Vacation Rental Cleaning"),
    ("mobile-al/airbnb-cleaning", "Airbnb Cleaning"),
    ("mobile-al/airbnb-vacation-rental-management", "Airbnb & Rental Management"),
    ("mobile-al/post-construction-cleanup", "Post-Construction Cleanup"),
    ("mobile-al/property-management-janitorial", "Property Management Janitorial"),
    ("mobile-al/property-maintenance", "Property Maintenance"),
    ("mobile-al/home-watch-services", "Home Watch Services"),
    ("mobile-al/luxury-estate-management", "Luxury Estate Management"),
    ("mobile-al/gutter-cleaning", "Gutter Cleaning")
]

with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
    template_content = f.read()

for folder_path, service_name in services:
    # Prepare exact replacements
    content = template_content
    
    # 1. Title tag
    content = content.replace(
        "<title>#1 Cleaning Service in Mobile, AL | Zoiris Cleaning Services</title>",
        f"<title>#1 {service_name} in Mobile, AL | Zoiris Cleaning Services</title>"
    )
    
    # 2. Meta description
    content = content.replace(
        'content="Cleaning Services in Mobile, AL. Zoiris Cleaning Services offer the best house cleaning and maid services in the Mobile area. Call (251) 930 8621 for a free quote today!" />',
        f'content="{service_name} in Mobile, AL. Zoiris Cleaning Services offer the best {service_name.lower()} in the Mobile area. Call (251) 930 8621 for a free quote today!" />'
    )
    
    # 3. OG Title
    content = content.replace(
        '<meta property="og:title" content="House Cleaning Services in Mobile, AL. Free Estimate | Zoiris Cleaning Services" />',
        f'<meta property="og:title" content="{service_name} in Mobile, AL. Free Estimate | Zoiris Cleaning Services" />'
    )
    
    # 4. Schema Description
    content = content.replace(
        '"description": "Zoiris Cleaning Service is the leading residential, commercial, and Airbnb cleaning company in Mobile, Alabama. Offering deep cleaning, move-in/out, post-construction cleaning, office cleaning, and eco-friendly cleaning solutions.",',
        f'"description": "Zoiris Cleaning Service is the leading {service_name.lower()} company in Mobile, Alabama. Offering deep cleaning, move-in/out, post-construction cleaning, office cleaning, and eco-friendly cleaning solutions.",'
    )
    
    # 5. H1 tag
    content = content.replace(
        '#1 Cleaning Services in Mobile, AL',
        f'#1 {service_name} in Mobile, AL'
    )
    
    # 6. Hero subtext
    content = content.replace(
        '<em>residential & commercial cleaning</em>',
        f'<em>{service_name.lower()}</em>'
    )
    
    content = re.sub(r'onclick="location\.href=[\'"]/[\'"]"', 'onclick="location.href=\'/mobile-al/\'"', content)
    content = content.replace('href="/" class="contact-button text-lg">Home</a>', 'href="/mobile-al/" class="contact-button text-lg">Home</a>')
    content = re.sub(r'href="/index\.html"(\s*)><i([^>]*fa-home[^>]*)></i>(\s*)Home</a>', r'href="/mobile-al/"\1><i\2></i>\3Home</a>', content)
    content = re.sub(r'href="/"(\s*)class="block px-4 py-4 text-xl font-medium text-white hover:text-blue-400', r'href="/mobile-al/"\1class="block px-4 py-4 text-xl font-medium text-white hover:text-blue-400', content)

    # Make the directory
    out_dir = os.path.join(BASE_DIR, folder_path)
    os.makedirs(out_dir, exist_ok=True)
    
    # Write the new index file
    out_file = os.path.join(out_dir, "index.html")
    with open(out_file, "w", encoding="utf-8") as out:
        out.write(content)
        
    print(f"Generated {out_file}")

print("Successfully generated all service pages.")

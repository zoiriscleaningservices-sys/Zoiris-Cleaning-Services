import os

# Base directory for the new folders
BASE_DIR = "."

# Services & Extras list (same as previous)
pages = [
    # Residential
    "mobile-al/house-cleaning",
    "mobile-al/deep-cleaning",
    "mobile-al/move-in-cleaning",
    "mobile-al/move-out-cleaning",
    "mobile-al/carpet-cleaning",
    "mobile-al/window-cleaning",
    "mobile-al/pressure-washing",
    "mobile-al/luxury-estate-cleaning",
    "mobile-al/laundry-services",
    "mobile-al/Detailing-Mobile-AL",
    
    # Commercial
    "mobile-al/commercial-cleaning",
    "mobile-al/office-janitorial-services",
    "mobile-al/janitorial-cleaning-services",
    "mobile-al/medical-dental-facility-cleaning",
    "mobile-al/industrial-warehouse-cleaning",
    "mobile-al/floor-stripping-waxing",
    "mobile-al/gym-fitness-center-cleaning",
    "mobile-al/school-daycare-cleaning",
    "mobile-al/church-worship-center-cleaning",
    "mobile-al/solar-panel-cleaning",
    
    # Property Management
    "mobile-al/vacation-rental-cleaning",
    "mobile-al/airbnb-cleaning",
    "mobile-al/airbnb-vacation-rental-management",
    "mobile-al/post-construction-cleanup",
    "mobile-al/property-management-janitorial",
    "mobile-al/property-maintenance",
    "mobile-al/home-watch-services",
    "mobile-al/luxury-estate-management",
    "mobile-al/gutter-cleaning",
    
    # Extras
    "mobile-al/about",
    "mobile-al/blog",
    "mobile-al/contact"
]

for folder_path in pages:
    file_path = os.path.join(BASE_DIR, folder_path, "index.html")
    
    # Ensure the file exists before attempting to read/write
    if not os.path.exists(file_path):
        print(f"Skipping missing file: {file_path}")
        continue
        
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Define dynamic target URL ending with a trailing slash
    target_url = f"https://www.zoiriscleaningservices.com/{folder_path}/"
    
    # 1. Replace hardcoded canonical
    content = content.replace(
        '<link rel="canonical" href="https://www.zoiriscleaningservices.com/" />',
        f'<link rel="canonical" href="{target_url}" />'
    )
    
    # 2. Replace hardcoded og:url
    content = content.replace(
        '<meta property="og:url" content="https://www.zoiriscleaningservices.com/" />',
        f'<meta property="og:url" content="{target_url}" />'
    )
    
    # 3. Replace hardcoded Schema @id and url
    content = content.replace(
        '"@id": "https://www.zoiriscleaningservices.com/#business",',
        f'"@id": "{target_url}#business",'
    )
    content = content.replace(
        '"url": "https://www.zoiriscleaningservices.com/",',
        f'"url": "{target_url}",'
    )

    with open(file_path, "w", encoding="utf-8") as out:
        out.write(content)
        
    print(f"Fixed SEO Links in: {folder_path}")

print("\nSuccessfully updated Canonical URLs, OG URLs, and Schema URLs across all 32 pages!")

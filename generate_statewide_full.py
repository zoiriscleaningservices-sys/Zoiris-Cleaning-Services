import os
import re

BASE_DIR = "."
TEMPLATE_FILE = os.path.join(BASE_DIR, "index.html")

cities = [
    ("birmingham-al", "Birmingham"),
    ("montgomery-al", "Montgomery"),
    ("huntsville-al", "Huntsville"),
    ("mobile-al", "Mobile"), 
    ("tuscaloosa-al", "Tuscaloosa"),
    ("hoover-al", "Hoover"),
    ("dothan-al", "Dothan"),
    ("auburn-al", "Auburn"),
    ("decatur-al", "Decatur"),
    ("madison-al", "Madison"),
    ("florence-al", "Florence"),
    ("phenix-city-al", "Phenix City"),
    ("prattville-al", "Prattville"),
    ("gadsden-al", "Gadsden"),
    ("vestavia-hills-al", "Vestavia Hills"),
    ("alabaster-al", "Alabaster"),
    ("opelika-al", "Opelika"),
    ("enterprise-al", "Enterprise"),
    ("bessemer-al", "Bessemer"),
    ("athens-al", "Athens"),
    ("northport-al", "Northport"),
    ("pelham-al", "Pelham"),
    ("albertville-al", "Albertville"),
    ("oxford-al", "Oxford"),
    ("anniston-al", "Anniston"),
    ("prichard-al", "Prichard"),
    ("trussville-al", "Trussville"),
    ("troy-al", "Troy"),
    ("fairhope-al", "Fairhope"),
    ("daphne-al", "Daphne"),
    ("selma-al", "Selma"),
    ("mountain-brook-al", "Mountain Brook"),
    ("helena-al", "Helena"),
    ("cullman-al", "Cullman"),
    ("foley-al", "Foley"),
    ("talladega-al", "Talladega"),
    ("hueytown-al", "Hueytown"),
    ("center-point-al", "Center Point"),
    ("alexander-city-al", "Alexander City"),
    ("andalusia-al", "Andalusia"),
    ("jasper-al", "Jasper"),
    ("pell-city-al", "Pell City"),
    ("gulf-shores-al", "Gulf Shores"),
    ("spanish-fort-al", "Spanish Fort"),
    ("chelsea-al", "Chelsea"),
    ("saraland-al", "Saraland"),
    ("sylacauga-al", "Sylacauga"),
    ("mccalla-al", "McCalla"),
    ("moody-al", "Moody"),
    ("ozark-al", "Ozark"),
    ("clay-al", "Clay"),
    ("scottsboro-al", "Scottsboro"),
    ("roosevelt-al", "Roosevelt"),
    ("sheffield-al", "Sheffield"),
    ("eufaula-al", "Eufaula"),
    ("fort-payne-al", "Fort Payne"),
    ("calera-al", "Calera"),
    ("boaz-al", "Boaz"),
    ("pinson-al", "Pinson"),
    ("oneonta-al", "Oneonta"),
    ("irondale-al", "Irondale"),
    ("muscle-shoals-al", "Muscle Shoals"),
    ("eight-mile-al", "Eight Mile"),
    ("satsuma-al", "Satsuma"),
    ("montrose-al", "Montrose"),
    ("theodore-al", "Theodore"),
    ("semmes-al", "Semmes"),
    ("creola-al", "Creola"),
    ("stapleton-al", "Stapleton"),
    ("point-clear-al", "Point Clear"),
    ("loxley-al", "Loxley"),
    ("saint-elmo-al", "Saint Elmo"),
    ("irvington-al", "Irvington"),
    ("wilmer-al", "Wilmer"),
    ("bay-minette-al", "Bay Minette"),
    ("coden-al", "Coden"),
    ("chunchula-al", "Chunchula"),
    ("silverhill-al", "Silverhill"),
    ("robertsdale-al", "Robertsdale"),
    ("elberta-al", "Elberta"),
    ("summerdale-al", "Summerdale"),
    ("orange-beach-al", "Orange Beach"),
    ("magnolia-springs-al", "Magnolia Springs")
]

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
    ("Detailing-{City}-AL", "Detailing"),
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

# 1. State-Wide Generation
for slug, city_name in cities:

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
    
    base_content = re.sub(r'onclick="location\.href=[\'"]/[\'"]"', f'onclick="location.href=\'/{slug}/\'"', base_content)
    base_content = base_content.replace('href="/" class="contact-button text-lg">Home</a>', f'href="/{slug}/" class="contact-button text-lg">Home</a>')
    base_content = re.sub(r'href="/index\.html"(\s*)><i([^>]*fa-home[^>]*)></i>(\s*)Home</a>', rf'href="/{slug}/"\1><i\2></i>\3Home</a>', base_content)
    base_content = re.sub(r'href="/"(\s*)class="block px-4 py-4 text-xl font-medium text-white hover:text-blue-400', rf'href="/{slug}/"\1class="block px-4 py-4 text-xl font-medium text-white hover:text-blue-400', base_content)
    
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
        
    for s_slug, service_name in services:
        if "Detailing" in s_slug: s_slug = f"Detailing-{city_name}-AL"
            
        content = hub_content
        page_url = f"{target_url}{s_slug}/"
        
        content = content.replace(f"<title>#1 Cleaning Service in {city_name}, AL | Zoiris Cleaning Services</title>", f"<title>#1 {service_name} in {city_name}, AL | Zoiris Cleaning Services</title>")
        content = content.replace(f'content="Cleaning Services in {city_name}, AL. Zoiris Cleaning Services offer the best house cleaning and maid services in the {city_name} area.', f'content="{service_name} in {city_name}, AL. Zoiris Cleaning Services offer the best {service_name.lower()} in the {city_name} area.')
        content = content.replace(f'content="House Cleaning Services in {city_name}, AL. Free Estimate | Zoiris Cleaning Services"', f'content="{service_name} in {city_name}, AL. Free Estimate | Zoiris Cleaning Services"')
        content = content.replace('"description": "Zoiris Cleaning Service is the leading residential, commercial, and Airbnb cleaning company', f'"description": "Zoiris Cleaning Service is the leading {service_name.lower()} company')
        content = content.replace(f'#1 Cleaning Services in {city_name}, AL', f'#1 {service_name} in {city_name}, AL')
        content = content.replace('<em>residential & commercial cleaning</em>', f'<em>{service_name.lower()}</em>')
        
        content = content.replace(f'<link rel="canonical" href="{target_url}" />', f'<link rel="canonical" href="{page_url}" />')
        content = content.replace(f'<meta property="og:url" content="{target_url}" />', f'<meta property="og:url" content="{page_url}" />')
        content = content.replace(f'"@id": "{target_url}#business",', f'"@id": "{page_url}#business",')
        content = content.replace(f'"url": "{target_url}",', f'"url": "{page_url}",')
        
        out_dir = os.path.join(hub_dir, s_slug)
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as out: out.write(content)

    for e_slug, e_name in extras:
        content = hub_content
        page_url = f"{target_url}{e_slug}/"
        content = content.replace(f"<title>#1 Cleaning Service in {city_name}, AL | Zoiris Cleaning Services</title>", f"<title>{e_name} | Zoiris Cleaning Services in {city_name}, AL</title>")
        content = content.replace(f'content="Cleaning Services in {city_name}, AL. Zoiris Cleaning Services offer the best house cleaning and maid services in the {city_name} area.', f'content="{e_name} for Zoiris Cleaning Services in {city_name}, AL. We offer the best residential and commercial cleaning in the {city_name} area.')
        content = content.replace(f'content="House Cleaning Services in {city_name}, AL. Free Estimate | Zoiris Cleaning Services"', f'content="{e_name} | Zoiris Cleaning Services"')
        content = content.replace('"description": "Zoiris Cleaning Service is the leading residential, commercial, and Airbnb cleaning company', f'"description": "{e_name} page for Zoiris Cleaning Service, the leading residential, commercial, and Airbnb cleaning company')
        content = content.replace(f'#1 Cleaning Services in {city_name}, AL', f'{e_name}')
        
        if e_name == "About Us":
            hero_subtext = f"Learn more about <em>Zoiris Cleaning Service</em>, your trusted provider for residential & commercial cleaning across {city_name} and nearby cities."
        elif e_name == "Cleaning Blog":
            hero_subtext = f"Read the latest tips, tricks, and news from <em>Zoiris Cleaning Service</em> on how to maintain a spotless home or business in {city_name}."
        elif e_name == "Contact Us":
            hero_subtext = f"Get in touch with <em>Zoiris Cleaning Service</em> today. We are ready to help with your residential & commercial cleaning needs across {city_name}."
            
        content = re.sub(r'<strong>Zoiris Cleaning Service</strong> provides trusted\s*<em>residential & commercial cleaning</em> across\s*<strong>.*?</strong>.\s*From deep cleans to move-in/out and eco-friendly solutions, we make your home or business spotless.', hero_subtext, content, flags=re.DOTALL)
        content = content.replace(f'<link rel="canonical" href="{target_url}" />', f'<link rel="canonical" href="{page_url}" />')
        content = content.replace(f'<meta property="og:url" content="{target_url}" />', f'<meta property="og:url" content="{page_url}" />')
        content = content.replace(f'"@id": "{target_url}#business",', f'"@id": "{page_url}#business",')
        content = content.replace(f'"url": "{target_url}",', f'"url": "{page_url}",')

        out_dir = os.path.join(hub_dir, e_slug)
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as out: out.write(content)

print("Generated 80+ Cities Complete!")

# 2. generating the Master Locations Directory /locations/index.html
loc_dir = os.path.join(BASE_DIR, "locations")
os.makedirs(loc_dir, exist_ok=True)

# Generate list items for cities
city_links = ""
for slug, city in sorted(cities, key=lambda x: x[1]):
    city_links += f"""
    <a href="/{slug}/" class="contact-button text-lg block w-full text-center hover:scale-105 transition-transform bg-white/10 backdrop-blur-sm border border-white/20">
      {city}, AL
    </a>"""

# Parse template for locations page
content = template_content
content = content.replace("<title>#1 Cleaning Service in Mobile, AL | Zoiris Cleaning Services</title>", "<title>Service Areas | Zoiris Cleaning Services in Alabama</title>")
content = content.replace('content="Cleaning Services in Mobile, AL. Zoiris Cleaning Services offer the best house cleaning and maid services in the Mobile area. Call (251) 930 8621 for a free quote today!" />', 'content="Service Areas for Zoiris Cleaning Services across Alabama. We offer the best residential and commercial cleaning across the state. Call (251) 930 8621 for a free quote today!" />')
content = content.replace('<meta property="og:title" content="House Cleaning Services in Mobile, AL. Free Estimate | Zoiris Cleaning Services" />', '<meta property="og:title" content="Service Areas | Zoiris Cleaning Services Alabama" />')
content = content.replace('<meta property="og:url" content="https://www.zoiriscleaningservices.com/" />', '<meta property="og:url" content="https://www.zoiriscleaningservices.com/locations/" />')
content = content.replace('<link rel="canonical" href="https://www.zoiriscleaningservices.com/" />', '<link rel="canonical" href="https://www.zoiriscleaningservices.com/locations/" />')
content = content.replace('"@id": "https://www.zoiriscleaningservices.com/#business",', '"@id": "https://www.zoiriscleaningservices.com/locations/#business",')
content = content.replace('"url": "https://www.zoiriscleaningservices.com/",', '"url": "https://www.zoiriscleaningservices.com/locations/",')

# Inject a custom section for the directory grid logic:
custom_hero_section = f"""
    <!-- Locations Directory Grid Section -->
    <section class="min-h-screen pt-32 pb-12 flex flex-col items-center justify-start relative z-10 w-full">
      <div class="relative text-center px-4 sm:px-6 lg:px-8 max-w-5xl w-full">
        <h1 class="text-4xl md:text-5xl font-extrabold text-white leading-tight mb-6 animate-fadeIn text-shadow">
          Alabama Service Areas
        </h1>
        <p class="text-lg md:text-xl text-white font-medium mx-auto mb-8 leading-relaxed max-w-3xl drop-shadow-md">
          Explore the locations we currently provide our top-tier residential and commercial cleaning services across Alabama. Select your city to find your local dedicated Zoiris branch.
        </p>

        <!-- Search Bar -->
        <div class="w-full max-w-2xl mx-auto mb-10 relative">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <i class="fas fa-search text-gray-400"></i>
            </div>
            <input type="text" id="citySearch" onkeyup="filterCities()" placeholder="Search your city... (e.g. Mobile, Gulf Shores)" class="w-full pl-12 pr-4 py-4 rounded-full bg-white/10 backdrop-blur-md border border-white/30 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all shadow-lg text-lg">
        </div>
        
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 w-full" id="cityGrid">
          {city_links}
        </div>
      </div>
    </section>

    <!-- Instant Search Script -->
    <script>
      function filterCities() {{
          var input, filter, grid, items, a, i, txtValue;
          input = document.getElementById("citySearch");
          filter = input.value.toUpperCase();
          grid = document.getElementById("cityGrid");
          items = grid.getElementsByTagName("a");
          
          for (i = 0; i < items.length; i++) {{
              a = items[i];
              txtValue = a.textContent || a.innerText;
              if (txtValue.toUpperCase().indexOf(filter) > -1) {{
                  items[i].style.display = "";
              }} else {{
                  items[i].style.display = "none";
              }}
          }}
      }}
    </script>
"""

# Replace the giant hero/main-content part with custom section instead to avoid duplication.
content = re.sub(
    r'<section class="hero-image min-h-screen pt-24 pb-12 flex items-center justify-center relative" id="home">.*?</section>',
    custom_hero_section,
    content,
    flags=re.DOTALL
)

with open(os.path.join(loc_dir, "index.html"), "w", encoding="utf-8") as out:
    out.write(content)

print("Generated /locations/ master index page successfully!")

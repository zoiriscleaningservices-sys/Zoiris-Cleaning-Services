import os
import re

BASE_DIR = r"c:\Users\lucia\OneDrive\Desktop\New folder (2)"
TEMPLATE_FILE = os.path.join(BASE_DIR, "index.html")

cities_raw = """
Abbeville, Adamsville, Addison, Akron, Alabaster, Albertville, Alexander City, Aliceville, Allgood, Altoona, Andalusia, Anderson, Anniston, Arab, Ardmore, Argo, Ariton, Arley, Ashford, Ashland, Ashville, Athens, Atmore, Attalla, Auburn, Autaugaville, Avon, Babbie, Baileyton, Bakerhill, Banks, Bay Minette, Bayou La Batre, Bear Creek, Beatrice, Beaverton, Belk, Benton, Berry, Bessemer, Billingsley, Birmingham, Black, Blountsville, Blue Springs, Boaz, Boligee, Bon Air, Brantley, Brent, Brewton, Bridgeport, Brighton, Brilliant, Brookside, Brookwood, Brundidge, Butler, Calera, Camden, Camp Hill, Carbon Hill, Cardiff, Carolina, Carrollton, Castleberry, Cedar Bluff, Center Point, Centre, Centreville, Chatom, Chelsea, Cherokee, Chickasaw, Childersburg, Choccolocco, Chunchula, Citronelle, Clanton, Clay, Clayhatchee, Clayton, Cleveland, Clio, Coaling, Coden, Coffee Springs, Coffeeville, Coker, Collinsville, Colony, Columbia, Columbiana, Concord, Coosada, Cordova, Cottonwood, County Line, Courtland, Cowarts, Creola, Crossville, Cuba, Cullman, Cusseta, Dadeville, Daleville, Daphne, Dauphin Island, Daviston, Dayton, Deatsville, Decatur, Demopolis, Detroit, Dodge City, Dora, Dothan, Double Springs, Douglas, Dozier, Dutton, East Brewton, Eclectic, Edwardsville, Eight Mile, Elba, Elberta, Eldridge, Elkmont, Elmore, Emelle, Enterprise, Epes, Ethelsville, Eufaula, Eutaw, Eva, Evergreen, Excel, Fairfield, Fairhope, Fairview, Falkville, Faunsdale, Fayette, Five Points, Flomaton, Florala, Florence, Foley, Forkland, Fort Deposit, Fort Payne, Franklin, Frisco City, Fruithurst, Fulton, Fultondale, Fyffe, Gadsden, Gainesville, Gantt, Garden City, Gardendale, Gaylesville, Geiger, Geneva, Georgiana, Geraldine, Gilbertown, Glen Allen, Glencoe, Glenwood, Goldville, Good Hope, Goodwater, Gordo, Gordon, Gordonville, Goshen, Grand Bay, Grant, Graysville, Greensboro, Greenville, Grimes, Grove Hill, Guin, Gulf Shores, Guntersville, Gurley, Gu-Win, Hackleburg, Haleburg, Haleyville, Hamilton, Hammondville, Hanceville, Harpersville, Hartford, Hartselle, Hayden, Hayneville, Headland, Heath, Heflin, Helena, Henagar, Highland Lake, Hillsboro, Hobson City, Hodges, Hokes Bluff, Holly Pond, Hollywood, Homewood, Hoover, Horn Hill, Hueytown, Huntsville, Hurtsboro, Hytop, Ider, Indian Springs Village, Irondale, Irvington, Jackson, Jackson's Gap, Jacksonville, Jasper, Jemison, Kansas, Kellyton, Kennedy, Killen, Kinsey, Kinston, LaFayette, Lake View, Lakeview, Lanett, Langston, Leeds, Leesburg, Leighton, Lester, Level Plains, Lexington, Libertyville, Lincoln, Linden, Lineville, Lipscomb, Lisman, Littleville, Livingston, Loachapoka, Lockhart, Locust Fork, Loxley, Luverne, Lynn, Madison, Madrid, Magnolia Springs, Malvern, Maplesville, Margaret, Marion, Maytown, McCalla, McIntosh, McKenzie, McMullen, Memphis, Mentone, Midfield, Midland City, Midway, Millbrook, Millport, Millry, Mobile, Monroeville, Montevallo, Montgomery, Montrose, Moody, Mooresville, Morris, Mosses, Moulton, Moundville, Mountain Brook, Mount Vernon, Mulga, Munford, Muscle Shoals, Myrtlewood, Napier Field, Natural Bridge, Nauvoo, Nectar, Needham, Newbern, New Brockton, New Hope, New Site, Newton, Newville, North Courtland, Northport, Notasulga, Oak Grove, Oak Hill, Oakman, Odenville, Ohatchee, Oneonta, Onycha, Opelika, Opp, Orange Beach, Orrville, Owens Cross Roads, Oxford, Ozark, Paint Rock, Parrish, Pelham, Pell City, Pennington, Perdido Beach, Petrey, Phenix City, Phil Campbell, Pickensville, Piedmont, Pike Road, Pinckard, Pine Apple, Pine Hill, Pine Ridge, Pinson, Pisgah, Pleasant Grove, Pleasant Groves, Point Clear, Pollard, Powell, Prattville, Priceville, Prichard, Providence, Ragland, Rainbow City, Rainsville, Ranburne, Red Bay, Red Level, Reece City, Reform, Rehobeth, Repton, Ridgeville, River Falls, Riverside, Riverview, Roanoke, Robertsdale, Rockford, Rogersville, Rosa, Russellville, Rutledge, Saint Elmo, Saint Florian, Saint Stephens, Samson, Sand Rock, Sanford, Saraland, Sardis City, Satsuma, Scottsboro, Section, Selma, Semmes, Sheffield, Shiloh, Shorter, Silas, Silverhill, Sipsey, Skyline, Slocomb, Smiths Station, Snead, Somerville, South Vinemont, Southside, Spanish Fort, Springville, Stapleton, Steele, Stevenson, Sulligent, Sumiton, Summerdale, Susan Moore, Sweet Water, Sylacauga, Sylvan Springs, Sylvania, Talladega, Talladega Springs, Tallassee, Tarrant, Taylor, Thomaston, Thomasville, Thorsby, Tillman's Corner, Town Creek, Toxey, Trafford, Triana, Trinity, Troy, Trussville, Tuscaloosa, Tuscumbia, Tuskegee, Twin, Union Grove, Union Springs, Uniontown, Valley, Valley Grande, Valley Head, Vance, Vernon, Vestavia Hills, Vina, Vincent, Vredenburgh, Wadley, Waldo, Walnut Grove, Warrior, Waterloo, Waverly, Weaver, Webb, Wedowee, West Blocton, West Jefferson, West Point, Weston, Wetumpka, White Hall, Wilmer, Wilsonville, Wilton, Winfield, Woodland, Woodstock, Woodville, Yellow Bluff, York, Gulfcrest, Mount Vernon, Dauphin Island, Orange Beach, Spanish Fort, Daphne, Fairhope, Point Clear, Magnolia Springs, Foley, Gulf Shores, Lillian, Elberta, Robertsdale, Loxley, Silverhill, Summerdale, Bay Minette, Stockton, Tensaw, Rabun, Perdido, Nokomis, Atmore, Flomaton, Brewton, East Brewton, Pollard, Riverview, Castleberry, Evergreen, Repton, Excel, Frisco City, Monroeville, Beatrice, Vredenburgh, Pine Apple, Camden, Yellow Bluff, Oak Hill, Pine Hill, Thomasville, Fulton, Grove Hill, Jackson, McIntosh, Calvert, Mount Vernon, Citronelle, Chunchula, Creola, Axis, Bucks, Satsuma, Saraland, Chickasaw, Prichard, Mobile, Theodore, Irvington, Grand Bay, Bayou La Batre, Coden, Semmes, Wilmer, Eight Mile, Whistler, Toulminville
"""

raw_list = [c.strip() for c in cities_raw.split(",") if c.strip()]
unique_cities = list(set(raw_list))

cities = []
for c in unique_cities:
    slug = c.lower().replace(" ", "-").replace("'", "").replace(".", "") + "-al"
    cities.append((slug, c))

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

# Generate the 530+ Cities
count = 0
for slug, city_name in cities:
    count += 1
    if slug == "mobile-al": continue # Mobile AL was handled deeply in previous batches
    
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
        if "Detailing" in s_slug: s_slug = f"Detailing-{slug}"
            
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

    if count % 20 == 0:
        print(f"Generated {count} cities...")

print(f"Generated {count} Cities Complete! Total Files Gen = {count * 33}")

# 2. generating the Master Locations Directory /locations/index.html
loc_dir = os.path.join(BASE_DIR, "locations")
os.makedirs(loc_dir, exist_ok=True)

# Generate list items for cities
city_links = ""
for slug, city in sorted(cities, key=lambda x: x[1]):
    city_links += f"""
    <a href="/{slug}/" class="contact-button text-sm block w-full text-center hover:scale-105 transition-transform bg-white/10 backdrop-blur-sm border border-white/20 px-2 py-3 rounded-xl m-1">
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
      <div class="relative text-center px-4 sm:px-6 lg:px-8 max-w-[95%] w-full">
        <h1 class="text-4xl md:text-5xl font-extrabold text-white leading-tight mb-6 animate-fadeIn text-shadow">
          Alabama Service Areas Directory
        </h1>
        <p class="text-lg md:text-xl text-white font-medium mx-auto mb-10 leading-relaxed max-w-3xl drop-shadow-md">
          Explore the locations we currently provide our top-tier residential and commercial cleaning services across Alabama. Select your city to find your local dedicated Zoiris cleaning branch.
        </p>
        
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-2 w-full">
          {city_links}
        </div>
      </div>
    </section>
"""

content = re.sub(
    r'<section class="hero-image min-h-screen pt-24 pb-12 flex items-center justify-center relative" id="home">.*?</section>',
    custom_hero_section,
    content,
    flags=re.DOTALL
)

with open(os.path.join(loc_dir, "index.html"), "w", encoding="utf-8") as out:
    out.write(content)

print(f"Generated /locations/ master index page with {count} local SEO hubs successfully!")

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


modifiers = [
    ("best", "Best"),
    ("affordable", "Affordable"),
    ("top-rated", "Top-Rated")
]

# Hardcoding 3 dummy zipcodes for everyone to simulate local indexing. 
zip_modifiers = [
    ("zip1", "Local"), 
    ("zip2", "Local"),
    ("zip3", "Local")
]

all_modifiers = modifiers + zip_modifiers

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

with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
    template_content = f.read()

count = 0
city_num = 0

print("Initiating EXTREME SEO NUKE on all 484 Alabama municipalities. Stand by...")

for slug, city_name in cities:
    city_num += 1
    if slug == "mobile-al": continue # We did this in Phase 3 test.
    
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
    
    # Fake Zip Generator per city based on index hash to randomize
    fake_zip_1 = str(35000 + (len(city_name) * 11) % 999)
    fake_zip_2 = str(36000 + (len(city_name) * 22) % 999) 
    fake_zip_3 = str(37000 + (len(city_name) * 33) % 999)

    current_city_modifiers = []
    for m_slug, m_name in modifiers: current_city_modifiers.append((m_slug, m_name))
    current_city_modifiers.append((fake_zip_1, fake_zip_1))
    current_city_modifiers.append((fake_zip_2, fake_zip_2))
    current_city_modifiers.append((fake_zip_3, fake_zip_3))

    for m_slug, m_name in current_city_modifiers:
        for s_slug, s_name in services:
            count += 1
            mod_slug = f"{m_slug}-{s_slug}"
            
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

    if city_num % 10 == 0:
        print(f"Generated Phase 3 SEO Nuke for {city_num}/484 cities ({count} files so far)...")

print(f"EXTREME SEO NUKE COMPLETE! Gen: {count} NEW Modifier Clusters generated.")

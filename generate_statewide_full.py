import os
import re

BASE_DIR = "."
TEMPLATE_FILE = os.path.join(BASE_DIR, "index.html")

cities = [
    ("adamsville-al", "Adamsville"),
    ("addison-al", "Addison"),
    ("akron-al", "Akron"),
    ("alabaster-al", "Alabaster"),
    ("albertville-al", "Albertville"),
    ("alexander-city-al", "Alexander City"),
    ("aliceville-al", "Aliceville"),
    ("allgood-al", "Allgood"),
    ("altoona-al", "Altoona"),
    ("andalusia-al", "Andalusia"),
    ("anniston-al", "Anniston"),
    ("arab-al", "Arab"),
    ("ardmore-al", "Ardmore"),
    ("argo-al", "Argo"),
    ("ariton-al", "Ariton"),
    ("arley-al", "Arley"),
    ("ashford-al", "Ashford"),
    ("athens-al", "Athens"),
    ("atmore-al", "Atmore"),
    ("attalla-al", "Attalla"),
    ("auburn-al", "Auburn"),
    ("autaugaville-al", "Autaugaville"),
    ("avon-al", "Avon"),
    ("babbie-al", "Babbie"),
    ("baileyton-al", "Baileyton"),
    ("bakerhill-al", "Bakerhill"),
    ("banks-al", "Banks"),
    ("bay-minette-al", "Bay Minette"),
    ("bayou-la-batre-al", "Bayou La Batre"),
    ("bear-creek-al", "Bear Creek"),
    ("beatrice-al", "Beatrice"),
    ("beaverton-al", "Beaverton"),
    ("belk-al", "Belk"),
    ("benton-al", "Benton"),
    ("berlin-al", "Berlin"),
    ("berry-al", "Berry"),
    ("bessemer-al", "Bessemer"),
    ("billingsley-al", "Billingsley"),
    ("birmingham-al", "Birmingham"),
    ("black-al", "Black"),
    ("blountsville-al", "Blountsville"),
    ("blue-springs-al", "Blue Springs"),
    ("boaz-al", "Boaz"),
    ("boligee-al", "Boligee"),
    ("bon-air-al", "Bon Air"),
    ("brantley-al", "Brantley"),
    ("brent-al", "Brent"),
    ("bridgeport-al", "Bridgeport"),
    ("brighton-al", "Brighton"),
    ("brilliant-al", "Brilliant"),
    ("brookside-al", "Brookside"),
    ("brookwood-al", "Brookwood"),
    ("brundidge-al", "Brundidge"),
    ("calera-al", "Calera"),
    ("camp-hill-al", "Camp Hill"),
    ("carbon-hill-al", "Carbon Hill"),
    ("cardiff-al", "Cardiff"),
    ("carolina-al", "Carolina"),
    ("castleberry-al", "Castleberry"),
    ("cedar-bluff-al", "Cedar Bluff"),
    ("center-point-al", "Center Point"),
    ("chelsea-al", "Chelsea"),
    ("cherokee-al", "Cherokee"),
    ("cherokee-ridge-al", "Cherokee Ridge"),
    ("chickasaw-al", "Chickasaw"),
    ("childersburg-al", "Childersburg"),
    ("chunchula-al", "Chunchula"),
    ("citronelle-al", "Citronelle"),
    ("clay-al", "Clay"),
    ("clayhatchee-al", "Clayhatchee"),
    ("cleveland-al", "Cleveland"),
    ("clio-al", "Clio"),
    ("coaling-al", "Coaling"),
    ("coden-al", "Coden"),
    ("coffee-springs-al", "Coffee Springs"),
    ("coffeeville-al", "Coffeeville"),
    ("coker-al", "Coker"),
    ("collinsville-al", "Collinsville"),
    ("colony-al", "Colony"),
    ("columbia-al", "Columbia"),
    ("coosada-al", "Coosada"),
    ("cordova-al", "Cordova"),
    ("cottonwood-al", "Cottonwood"),
    ("courtland-al", "Courtland"),
    ("cowarts-al", "Cowarts"),
    ("creola-al", "Creola"),
    ("crossville-al", "Crossville"),
    ("cuba-al", "Cuba"),
    ("cullman-al", "Cullman"),
    ("cusseta-al", "Cusseta"),
    ("daleville-al", "Daleville"),
    ("daphne-al", "Daphne"),
    ("dauphin-island-al", "Dauphin Island"),
    ("daviston-al", "Daviston"),
    ("dayton-al", "Dayton"),
    ("deatsville-al", "Deatsville"),
    ("decatur-al", "Decatur"),
    ("demopolis-al", "Demopolis"),
    ("detroit-al", "Detroit"),
    ("dodge-city-al", "Dodge City"),
    ("dora-al", "Dora"),
    ("dothan-al", "Dothan"),
    ("douglas-al", "Douglas"),
    ("dozier-al", "Dozier"),
    ("dutton-al", "Dutton"),
    ("east-brewton-al", "East Brewton"),
    ("eclectic-al", "Eclectic"),
    ("edwardsville-al", "Edwardsville"),
    ("eight-mile-al", "Eight Mile"),
    ("elberta-al", "Elberta"),
    ("eldridge-al", "Eldridge"),
    ("elkmont-al", "Elkmont"),
    ("elmore-al", "Elmore"),
    ("emelle-al", "Emelle"),
    ("enterprise-al", "Enterprise"),
    ("epes-al", "Epes"),
    ("ethelsville-al", "Ethelsville"),
    ("eufaula-al", "Eufaula"),
    ("eva-al", "Eva"),
    ("excel-al", "Excel"),
    ("fairfield-al", "Fairfield"),
    ("fairhope-al", "Fairhope"),
    ("fairview-al", "Fairview"),
    ("falkville-al", "Falkville"),
    ("faunsdale-al", "Faunsdale"),
    ("five-points-al", "Five Points"),
    ("flomaton-al", "Flomaton"),
    ("florala-al", "Florala"),
    ("florence-al", "Florence"),
    ("foley-al", "Foley"),
    ("forkland-al", "Forkland"),
    ("fort-deposit-al", "Fort Deposit"),
    ("fort-payne-al", "Fort Payne"),
    ("franklin-al", "Franklin"),
    ("frisco-city-al", "Frisco City"),
    ("fruithurst-al", "Fruithurst"),
    ("fulton-al", "Fulton"),
    ("fultondale-al", "Fultondale"),
    ("fyffe-al", "Fyffe"),
    ("gadsden-al", "Gadsden"),
    ("gainesville-al", "Gainesville"),
    ("gantt-al", "Gantt"),
    ("garden-city-al", "Garden City"),
    ("gardendale-al", "Gardendale"),
    ("gaylesville-al", "Gaylesville"),
    ("geiger-al", "Geiger"),
    ("georgiana-al", "Georgiana"),
    ("geraldine-al", "Geraldine"),
    ("gilbertown-al", "Gilbertown"),
    ("glen-allen-al", "Glen Allen"),
    ("glencoe-al", "Glencoe"),
    ("glenwood-al", "Glenwood"),
    ("goldville-al", "Goldville"),
    ("good-hope-al", "Good Hope"),
    ("goodwater-al", "Goodwater"),
    ("gordo-al", "Gordo"),
    ("gordon-al", "Gordon"),
    ("gordonville-al", "Gordonville"),
    ("goshen-al", "Goshen"),
    ("grant-al", "Grant"),
    ("graysville-al", "Graysville"),
    ("grimes-al", "Grimes"),
    ("gu-win-al", "Gu-Win"),
    ("guin-al", "Guin"),
    ("gulf-shores-al", "Gulf Shores"),
    ("gurley-al", "Gurley"),
    ("hackleburg-al", "Hackleburg"),
    ("haleburg-al", "Haleburg"),
    ("haleyville-al", "Haleyville"),
    ("hammondville-al", "Hammondville"),
    ("hanceville-al", "Hanceville"),
    ("harpersville-al", "Harpersville"),
    ("hartford-al", "Hartford"),
    ("hartselle-al", "Hartselle"),
    ("hayden-al", "Hayden"),
    ("headland-al", "Headland"),
    ("heath-al", "Heath"),
    ("helena-al", "Helena"),
    ("henagar-al", "Henagar"),
    ("highland-lake-al", "Highland Lake"),
    ("hillsboro-al", "Hillsboro"),
    ("hobson-city-al", "Hobson City"),
    ("hodges-al", "Hodges"),
    ("holly-pond-al", "Holly Pond"),
    ("hollywood-al", "Hollywood"),
    ("homewood-al", "Homewood"),
    ("hoover-al", "Hoover"),
    ("horn-hill-al", "Horn Hill"),
    ("hueytown-al", "Hueytown"),
    ("huntsville-al", "Huntsville"),
    ("hurtsboro-al", "Hurtsboro"),
    ("hytop-al", "Hytop"),
    ("ider-al", "Ider"),
    ("indian-springs-village-al", "Indian Springs Village"),
    ("irondale-al", "Irondale"),
    ("irvington-al", "Irvington"),
    ("jackson-al", "Jackson"),
    ("jackson&#39;s-gap-al", "Jackson&#39;s Gap"),
    ("jacksonville-al", "Jacksonville"),
    ("jasper-al", "Jasper"),
    ("jemison-al", "Jemison"),
    ("kansas-al", "Kansas"),
    ("kellyton-al", "Kellyton"),
    ("kennedy-al", "Kennedy"),
    ("killen-al", "Killen"),
    ("kimberly-al", "Kimberly"),
    ("kinsey-al", "Kinsey"),
    ("kinston-al", "Kinston"),
    ("lake-view-al", "Lake View"),
    ("lakeview-al", "Lakeview"),
    ("lanett-al", "Lanett"),
    ("langston-al", "Langston"),
    ("leeds-al", "Leeds"),
    ("leesburg-al", "Leesburg"),
    ("leighton-al", "Leighton"),
    ("lester-al", "Lester"),
    ("level-plains-al", "Level Plains"),
    ("lexington-al", "Lexington"),
    ("libertyville-al", "Libertyville"),
    ("lincoln-al", "Lincoln"),
    ("lineville-al", "Lineville"),
    ("lipscomb-al", "Lipscomb"),
    ("lisman-al", "Lisman"),
    ("littleville-al", "Littleville"),
    ("loachapoka-al", "Loachapoka"),
    ("lockhart-al", "Lockhart"),
    ("locust-fork-al", "Locust Fork"),
    ("louisville-al", "Louisville"),
    ("lowndesboro-al", "Lowndesboro"),
    ("loxley-al", "Loxley"),
    ("lynn-al", "Lynn"),
    ("madison-al", "Madison"),
    ("madrid-al", "Madrid"),
    ("magnolia-springs-al", "Magnolia Springs"),
    ("malvern-al", "Malvern"),
    ("maplesville-al", "Maplesville"),
    ("margaret-al", "Margaret"),
    ("maytown-al", "Maytown"),
    ("mccalla-al", "McCalla"),
    ("mcintosh-al", "McIntosh"),
    ("mckenzie-al", "McKenzie"),
    ("mcmullen-al", "McMullen"),
    ("memphis-al", "Memphis"),
    ("mentone-al", "Mentone"),
    ("midfield-al", "Midfield"),
    ("midland-city-al", "Midland City"),
    ("midway-al", "Midway"),
    ("millbrook-al", "Millbrook"),
    ("millport-al", "Millport"),
    ("millry-al", "Millry"),
    ("mobile-al", "Mobile"),
    ("montevallo-al", "Montevallo"),
    ("montgomery-al", "Montgomery"),
    ("montrose-al", "Montrose"),
    ("moody-al", "Moody"),
    ("mooresville-al", "Mooresville"),
    ("morris-al", "Morris"),
    ("mosses-al", "Mosses"),
    ("moundville-al", "Moundville"),
    ("mount-vernon-al", "Mount Vernon"),
    ("mountain-brook-al", "Mountain Brook"),
    ("mulga-al", "Mulga"),
    ("munford-al", "Munford"),
    ("muscle-shoals-al", "Muscle Shoals"),
    ("myrtlewood-al", "Myrtlewood"),
    ("napier-field-al", "Napier Field"),
    ("natural-bridge-al", "Natural Bridge"),
    ("nauvoo-al", "Nauvoo"),
    ("nectar-al", "Nectar"),
    ("needham-al", "Needham"),
    ("new-brockton-al", "New Brockton"),
    ("new-hope-al", "New Hope"),
    ("new-site-al", "New Site"),
    ("newbern-al", "Newbern"),
    ("newton-al", "Newton"),
    ("newville-al", "Newville"),
    ("north-courtland-al", "North Courtland"),
    ("north-johns-al", "North Johns"),
    ("northport-al", "Northport"),
    ("notasulga-al", "Notasulga"),
    ("oak-grove-al", "Oak Grove"),
    ("oak-hill-al", "Oak Hill"),
    ("oakman-al", "Oakman"),
    ("odenville-al", "Odenville"),
    ("ohatchee-al", "Ohatchee"),
    ("oneonta-al", "Oneonta"),
    ("onycha-al", "Onycha"),
    ("opelika-al", "Opelika"),
    ("opp-al", "Opp"),
    ("orange-beach-al", "Orange Beach"),
    ("orrville-al", "Orrville"),
    ("owens-cross-roads-al", "Owens Cross Roads"),
    ("oxford-al", "Oxford"),
    ("ozark-al", "Ozark"),
    ("paint-rock-al", "Paint Rock"),
    ("parrish-al", "Parrish"),
    ("pelham-al", "Pelham"),
    ("pell-city-al", "Pell City"),
    ("pennington-al", "Pennington"),
    ("perdido-beach-al", "Perdido Beach"),
    ("petrey-al", "Petrey"),
    ("phenix-city-al", "Phenix City"),
    ("phil-campbell-al", "Phil Campbell"),
    ("pickensville-al", "Pickensville"),
    ("piedmont-al", "Piedmont"),
    ("pike-road-al", "Pike Road"),
    ("pinckard-al", "Pinckard"),
    ("pine-apple-al", "Pine Apple"),
    ("pine-hill-al", "Pine Hill"),
    ("pine-level-al", "Pine Level"),
    ("pine-ridge-al", "Pine Ridge"),
    ("pinson-al", "Pinson"),
    ("pisgah-al", "Pisgah"),
    ("pleasant-grove-al", "Pleasant Grove"),
    ("pleasant-groves-al", "Pleasant Groves"),
    ("point-clear-al", "Point Clear"),
    ("pollard-al", "Pollard"),
    ("powell-al", "Powell"),
    ("prattville-al", "Prattville"),
    ("priceville-al", "Priceville"),
    ("prichard-al", "Prichard"),
    ("providence-al", "Providence"),
    ("ragland-al", "Ragland"),
    ("rainbow-city-al", "Rainbow City"),
    ("rainsville-al", "Rainsville"),
    ("ranburne-al", "Ranburne"),
    ("red-bay-al", "Red Bay"),
    ("red-level-al", "Red Level"),
    ("reece-city-al", "Reece City"),
    ("reform-al", "Reform"),
    ("rehobeth-al", "Rehobeth"),
    ("repton-al", "Repton"),
    ("ridgeville-al", "Ridgeville"),
    ("river-falls-al", "River Falls"),
    ("riverside-al", "Riverside"),
    ("riverview-al", "Riverview"),
    ("roanoke-al", "Roanoke"),
    ("robertsdale-al", "Robertsdale"),
    ("rogersville-al", "Rogersville"),
    ("roosevelt-al", "Roosevelt"),
    ("rosa-al", "Rosa"),
    ("rutledge-al", "Rutledge"),
    ("saint-elmo-al", "Saint Elmo"),
    ("samson-al", "Samson"),
    ("sand-rock-al", "Sand Rock"),
    ("sanford-al", "Sanford"),
    ("saraland-al", "Saraland"),
    ("sardis-city-al", "Sardis City"),
    ("satsuma-al", "Satsuma"),
    ("scottsboro-al", "Scottsboro"),
    ("section-al", "Section"),
    ("selma-al", "Selma"),
    ("semmes-al", "Semmes"),
    ("sheffield-al", "Sheffield"),
    ("shiloh-al", "Shiloh"),
    ("shorter-al", "Shorter"),
    ("silas-al", "Silas"),
    ("silverhill-al", "Silverhill"),
    ("sipsey-al", "Sipsey"),
    ("skyline-al", "Skyline"),
    ("slocomb-al", "Slocomb"),
    ("smiths-station-al", "Smiths Station"),
    ("snead-al", "Snead"),
    ("somerville-al", "Somerville"),
    ("south-vinemont-al", "South Vinemont"),
    ("southside-al", "Southside"),
    ("spanish-fort-al", "Spanish Fort"),
    ("springville-al", "Springville"),
    ("st-florian-al", "St. Florian"),
    ("stapleton-al", "Stapleton"),
    ("steele-al", "Steele"),
    ("stevenson-al", "Stevenson"),
    ("sulligent-al", "Sulligent"),
    ("sumiton-al", "Sumiton"),
    ("summerdale-al", "Summerdale"),
    ("susan-moore-al", "Susan Moore"),
    ("sweet-water-al", "Sweet Water"),
    ("sylacauga-al", "Sylacauga"),
    ("sylvan-springs-al", "Sylvan Springs"),
    ("sylvania-al", "Sylvania"),
    ("talladega-al", "Talladega"),
    ("talladega-springs-al", "Talladega Springs"),
    ("tallassee-al", "Tallassee"),
    ("tarrant-al", "Tarrant"),
    ("taylor-al", "Taylor"),
    ("theodore-al", "Theodore"),
    ("thomaston-al", "Thomaston"),
    ("thomasville-al", "Thomasville"),
    ("thorsby-al", "Thorsby"),
    ("town-creek-al", "Town Creek"),
    ("toxey-al", "Toxey"),
    ("trafford-al", "Trafford"),
    ("triana-al", "Triana"),
    ("trinity-al", "Trinity"),
    ("troy-al", "Troy"),
    ("trussville-al", "Trussville"),
    ("tuscaloosa-al", "Tuscaloosa"),
    ("twin-al", "Twin"),
    ("union-al", "Union"),
    ("union-grove-al", "Union Grove"),
    ("uniontown-al", "Uniontown"),
    ("valley-al", "Valley"),
    ("valley-grande-al", "Valley Grande"),
    ("valley-head-al", "Valley Head"),
    ("vance-al", "Vance"),
    ("vestavia-hills-al", "Vestavia Hills"),
    ("vina-al", "Vina"),
    ("vincent-al", "Vincent"),
    ("vredenburgh-al", "Vredenburgh"),
    ("wadley-al", "Wadley"),
    ("waldo-al", "Waldo"),
    ("walnut-grove-al", "Walnut Grove"),
    ("warrior-al", "Warrior"),
    ("waterloo-al", "Waterloo"),
    ("waverly-al", "Waverly"),
    ("weaver-al", "Weaver"),
    ("webb-al", "Webb"),
    ("west-blocton-al", "West Blocton"),
    ("west-jefferson-al", "West Jefferson"),
    ("west-point-al", "West Point"),
    ("westover-al", "Westover"),
    ("white-hall-al", "White Hall"),
    ("wilmer-al", "Wilmer"),
    ("wilsonville-al", "Wilsonville"),
    ("wilton-al", "Wilton"),
    ("winfield-al", "Winfield"),
    ("woodland-al", "Woodland"),
    ("woodstock-al", "Woodstock"),
    ("woodville-al", "Woodville"),
    ("yellow-bluff-al", "Yellow Bluff"),
    ("york-al", "York")
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

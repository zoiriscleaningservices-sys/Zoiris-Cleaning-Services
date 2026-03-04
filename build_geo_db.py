import os
import json
import time
import urllib.request
import urllib.parse
import urllib.error

BASE_DIR = r"c:\Users\lucia\OneDrive\Desktop\New folder (2)"
DB_FILE = os.path.join(BASE_DIR, "city_coords.json")

cities_raw = """
Abbeville, Adamsville, Addison, Akron, Alabaster, Albertville, Alexander City, Aliceville, Allgood, Altoona, Andalusia, Anderson, Anniston, Arab, Ardmore, Argo, Ariton, Arley, Ashford, Ashland, Ashville, Athens, Atmore, Attalla, Auburn, Autaugaville, Avon, Babbie, Baileyton, Bakerhill, Banks, Bay Minette, Bayou La Batre, Bear Creek, Beatrice, Beaverton, Belk, Benton, Berry, Bessemer, Billingsley, Birmingham, Black, Blountsville, Blue Springs, Boaz, Boligee, Bon Air, Brantley, Brent, Brewton, Bridgeport, Brighton, Brilliant, Brookside, Brookwood, Brundidge, Butler, Calera, Camden, Camp Hill, Carbon Hill, Cardiff, Carolina, Carrollton, Castleberry, Cedar Bluff, Center Point, Centre, Centreville, Chatom, Chelsea, Cherokee, Chickasaw, Childersburg, Choccolocco, Chunchula, Citronelle, Clanton, Clay, Clayhatchee, Clayton, Cleveland, Clio, Coaling, Coden, Coffee Springs, Coffeeville, Coker, Collinsville, Colony, Columbia, Columbiana, Concord, Coosada, Cordova, Cottonwood, County Line, Courtland, Cowarts, Creola, Crossville, Cuba, Cullman, Cusseta, Dadeville, Daleville, Daphne, Dauphin Island, Daviston, Dayton, Deatsville, Decatur, Demopolis, Detroit, Dodge City, Dora, Dothan, Double Springs, Douglas, Dozier, Dutton, East Brewton, Eclectic, Edwardsville, Eight Mile, Elba, Elberta, Eldridge, Elkmont, Elmore, Emelle, Enterprise, Epes, Ethelsville, Eufaula, Eutaw, Eva, Evergreen, Excel, Fairfield, Fairhope, Fairview, Falkville, Faunsdale, Fayette, Five Points, Flomaton, Florala, Florence, Foley, Forkland, Fort Deposit, Fort Payne, Franklin, Frisco City, Fruithurst, Fulton, Fultondale, Fyffe, Gadsden, Gainesville, Gantt, Garden City, Gardendale, Gaylesville, Geiger, Geneva, Georgiana, Geraldine, Gilbertown, Glen Allen, Glencoe, Glenwood, Goldville, Good Hope, Goodwater, Gordo, Gordon, Gordonville, Goshen, Grand Bay, Grant, Graysville, Greensboro, Greenville, Grimes, Grove Hill, Guin, Gulf Shores, Guntersville, Gurley, Gu-Win, Hackleburg, Haleburg, Haleyville, Hamilton, Hammondville, Hanceville, Harpersville, Hartford, Hartselle, Hayden, Hayneville, Headland, Heath, Heflin, Helena, Henagar, Highland Lake, Hillsboro, Hobson City, Hodges, Hokes Bluff, Holly Pond, Hollywood, Homewood, Hoover, Horn Hill, Hueytown, Huntsville, Hurtsboro, Hytop, Ider, Indian Springs Village, Irondale, Irvington, Jackson, Jackson's Gap, Jacksonville, Jasper, Jemison, Kansas, Kellyton, Kennedy, Killen, Kinsey, Kinston, LaFayette, Lake View, Lakeview, Lanett, Langston, Leeds, Leesburg, Leighton, Lester, Level Plains, Lexington, Libertyville, Lincoln, Linden, Lineville, Lipscomb, Lisman, Littleville, Livingston, Loachapoka, Lockhart, Locust Fork, Loxley, Luverne, Lynn, Madison, Madrid, Magnolia Springs, Malvern, Maplesville, Margaret, Marion, Maytown, McCalla, McIntosh, McKenzie, McMullen, Memphis, Mentone, Midfield, Midland City, Midway, Millbrook, Millport, Millry, Mobile, Monroeville, Montevallo, Montgomery, Montrose, Moody, Mooresville, Morris, Mosses, Moulton, Moundville, Mountain Brook, Mount Vernon, Mulga, Munford, Muscle Shoals, Myrtlewood, Napier Field, Natural Bridge, Nauvoo, Nectar, Needham, Newbern, New Brockton, New Hope, New Site, Newton, Newville, North Courtland, Northport, Notasulga, Oak Grove, Oak Hill, Oakman, Odenville, Ohatchee, Oneonta, Onycha, Opelika, Opp, Orange Beach, Orrville, Owens Cross Roads, Oxford, Ozark, Paint Rock, Parrish, Pelham, Pell City, Pennington, Perdido Beach, Petrey, Phenix City, Phil Campbell, Pickensville, Piedmont, Pike Road, Pinckard, Pine Apple, Pine Hill, Pine Ridge, Pinson, Pisgah, Pleasant Grove, Pleasant Groves, Point Clear, Pollard, Powell, Prattville, Priceville, Prichard, Providence, Ragland, Rainbow City, Rainsville, Ranburne, Red Bay, Red Level, Reece City, Reform, Rehobeth, Repton, Ridgeville, River Falls, Riverside, Riverview, Roanoke, Robertsdale, Rockford, Rogersville, Rosa, Russellville, Rutledge, Saint Elmo, Saint Florian, Saint Stephens, Samson, Sand Rock, Sanford, Saraland, Sardis City, Satsuma, Scottsboro, Section, Selma, Semmes, Sheffield, Shiloh, Shorter, Silas, Silverhill, Sipsey, Skyline, Slocomb, Smiths Station, Snead, Somerville, South Vinemont, Southside, Spanish Fort, Springville, Stapleton, Steele, Stevenson, Sulligent, Sumiton, Summerdale, Susan Moore, Sweet Water, Sylacauga, Sylvan Springs, Sylvania, Talladega, Talladega Springs, Tallassee, Tarrant, Taylor, Thomaston, Thomasville, Thorsby, Tillman's Corner, Town Creek, Toxey, Trafford, Triana, Trinity, Troy, Trussville, Tuscaloosa, Tuscumbia, Tuskegee, Twin, Union Grove, Union Springs, Uniontown, Valley, Valley Grande, Valley Head, Vance, Vernon, Vestavia Hills, Vina, Vincent, Vredenburgh, Wadley, Waldo, Walnut Grove, Warrior, Waterloo, Waverly, Weaver, Webb, Wedowee, West Blocton, West Jefferson, West Point, Weston, Wetumpka, White Hall, Wilmer, Wilsonville, Wilton, Winfield, Woodland, Woodstock, Woodville, Yellow Bluff, York, Gulfcrest, Mount Vernon, Dauphin Island, Orange Beach, Spanish Fort, Daphne, Fairhope, Point Clear, Magnolia Springs, Foley, Gulf Shores, Lillian, Elberta, Robertsdale, Loxley, Silverhill, Summerdale, Bay Minette, Stockton, Tensaw, Rabun, Perdido, Nokomis, Atmore, Flomaton, Brewton, East Brewton, Pollard, Riverview, Castleberry, Evergreen, Repton, Excel, Frisco City, Monroeville, Beatrice, Vredenburgh, Pine Apple, Camden, Yellow Bluff, Oak Hill, Pine Hill, Thomasville, Fulton, Grove Hill, Jackson, McIntosh, Calvert, Mount Vernon, Citronelle, Chunchula, Creola, Axis, Bucks, Satsuma, Saraland, Chickasaw, Prichard, Mobile, Theodore, Irvington, Grand Bay, Bayou La Batre, Coden, Semmes, Wilmer, Eight Mile, Whistler, Toulminville
"""
raw_list = [c.strip() for c in cities_raw.split(",") if c.strip()]
unique_cities = list(set(raw_list))

# Pre-populated coordinates for major cities to save API calls
hardcoded_coords = {
    "Mobile": (30.6954, -88.0399),
    "Birmingham": (33.5186, -86.8104),
    "Huntsville": (34.7304, -86.5861),
    "Montgomery": (32.3668, -86.3000),
    "Tuscaloosa": (33.2098, -87.5692),
    "Dothan": (31.2232, -85.3905),
    "Decatur": (34.6059, -86.9833),
    "Auburn": (32.6099, -85.4808),
    "Hoover": (33.4054, -86.8058),
    "Florence": (34.7998, -87.6773),
    "Gadsden": (34.0143, -86.0066),
    "Vestavia Hills": (33.4487, -86.7878),
    "Prattville": (32.4640, -86.4597),
    "Phenix City": (32.4710, -85.0016),
    "Alabaster": (33.2443, -86.8164),
    "Bessemer": (33.4018, -86.9544),
    "Enterprise": (31.3152, -85.8552),
    "Opelika": (32.6454, -85.3783),
    "Homewood": (33.4718, -86.7933),
    "Northport": (33.2221, -87.5772),
    "Pelham": (33.2859, -86.8119),
    "Trussville": (33.6198, -86.6089),
    "Fairhope": (30.5229, -87.9032),
    "Daphne": (30.6034, -87.9036),
    "Cullman": (34.1748, -86.8436),
    "Foley": (30.3729, -87.6833),
    "Gulf Shores": (30.2706, -87.7011)
}

db = {}
if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as f:
        db = json.load(f)

print("Building Local Geo-Coordinate Database...")

for city in unique_cities:
    if city in db:
        continue
    
    if city in hardcoded_coords:
        db[city] = {"lat": hardcoded_coords[city][0], "lon": hardcoded_coords[city][1]}
        continue
        
    query = f"{city}, Alabama, USA"
    url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(query)}&format=json&limit=1"
    headers = {"User-Agent": "ZoirisCleaningSEOBot/1.0 (lucia.seo@example.com)"}
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if data:
                db[city] = {"lat": float(data[0]["lat"]), "lon": float(data[0]["lon"])}
            else:
                db[city] = {"lat": 32.3182, "lon": -86.9023} # Fallback to rough geographic center of AL
        time.sleep(1) # Nominatim policy compliant
    except Exception as e:
        print(f"Error fetching {city}: {e}")
        db[city] = {"lat": 32.3182, "lon": -86.9023}

    
    if len(db) % 25 == 0:
        with open(DB_FILE, "w") as f:
            json.dump(db, f, indent=4)
        print(f"Saved {len(db)}/{len(unique_cities)} coordinates...")

with open(DB_FILE, "w") as f:
    json.dump(db, f, indent=4)
print(f"Database Complete! {len(db)} cities mapped.")

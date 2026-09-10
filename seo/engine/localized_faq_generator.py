import os
import json
import re

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load local intelligence database
try:
    with open(os.path.join(root_dir, 'seo', 'local_intelligence.json'), 'r', encoding='utf-8') as f:
        LOCAL_INTEL = json.load(f)
except Exception:
    LOCAL_INTEL = {}

def get_city_profile(city, loc_slug, county):
    loc_clean = loc_slug.lower().strip()
    key = loc_clean.replace('-', '_')
    
    if key == "daphne_al":
        return {
            "region": "eastern_shore",
            "market_name": "Daphne & Eastern Shore",
            "environment_headline": "Daphne Local Environmental Defense & Surface Care",
            "environment_desc": "seasonal live oak pollen, red clay tracking, and Mobile Bay humidity",
            "property_types": "Lake Forest golf enclaves, Sehoy executive homes, Austin Park estates, and Scenic 98 bayfront cottages",
            "neighborhoods": "Lake Forest, Sehoy, Austin Park, Diamante, Historic Old Daphne, and Scenic 98 bluffs",
            "specialty": "Bona-certified hardwood floor care, HEPA live oak pollen extraction, and commuter-flexible housekeeping",
            "local_landmarks": "Lake Forest Yacht Club, Daphne Bayfront Park, and Spanish Fort corridors",
            "about_focus": "From Lake Forest golf course residences and Sehoy executive layouts to historic bluff cottages along Scenic 98, Zoiris Cleaning Services provides dedicated, no-contract residential housekeeping, move turnovers, and commercial janitorial across Daphne and the Eastern Shore.",
            "about_p2": "Our cleaners use Bona-certified pH-neutral hardwood cleaners to protect delicate oak and pine from Baldwin County moisture, paired with multi-stage HEPA filtration that extracts airborne spring live oak pollen and red clay mudroom tracking.",
            "services_intro": "Daphne households balance busy Eastern Shore work commutes with active family schedules. We provide flexible, reliable cleaning protocols designed around your exact routine with zero locked contracts."
        }
    elif key == "fairhope_al":
        return {
            "region": "eastern_shore",
            "market_name": "Fairhope & Point Clear",
            "environment_headline": "Historic Cottage Care & Eco-Safe Surface Protection in Fairhope",
            "environment_desc": "bay moisture, antique architectural dust, and coastal humidity",
            "property_types": "Fruit & Nut District craftsman cottages, Point Clear bayfront estates, Rock Creek golf villas, and Lakewood homes",
            "neighborhoods": "Fruit & Nut District, Downtown Fairhope, Point Clear, Rock Creek, Lakewood, and Sandy Ford",
            "specialty": "historic heart-pine floor preservation, non-toxic hospital-grade disinfectants, and white-glove cottage care",
            "local_landmarks": "Fairhope Municipal Pier, Grand Hotel at Point Clear, and Downtown Fairhope Avenue",
            "about_focus": "Preserving the architectural charm of Fairhope—from 1920s craftsman cottages in the Fruit & Nut District to grand bayfront estates in Point Clear—demands gentle, non-toxic, and white-glove cleaning craftsmanship.",
            "about_p2": "We exclusively apply hospital-grade, EPA-registered eco disinfectants that eliminate 99.9% of bacteria without synthetic VOCs, chlorine fumes, or abrasive chemicals, safely protecting historic heart pine, antique mantels, and luxury marble.",
            "services_intro": "Fairhope homeowners expect discreet, dependable, and non-toxic housekeeping. Our uniformed, in-house W-2 staff delivers spotless results with zero contract commitments."
        }
    elif key == "gulf_shores_al":
        return {
            "region": "gulf_coast",
            "market_name": "Gulf Shores & Orange Beach",
            "environment_headline": "Beachfront Sand Extraction & Coastal Turnover Sanitation in Gulf Shores",
            "environment_desc": "silica beach sand tracking, corrosive salt air mist, and extreme sub-tropical humidity",
            "property_types": "beachfront condominium towers (Phoenix, Crystal Tower), West Beach vacation cottages, Fort Morgan beach homes, and Craft Farms residences",
            "neighborhoods": "West Beach, East Beach, Fort Morgan corridor, Craft Farms, Oyster Bay, and Peninsula",
            "specialty": "10am-3pm vacation rental express turnovers, agitated HEPA sand extraction, and salt-film glass descaling",
            "local_landmarks": "Gulf State Park Pier, Hangout Beach, and Fort Morgan Historic Site",
            "about_focus": "Managing beachfront condominiums, Fort Morgan vacation rentals, and private coastal residences in Craft Farms requires specialized sand extraction and rapid turnover expertise.",
            "about_p2": "Our crews utilize motorized HEPA sand agitation vacuums, salt-film dissolving glass treatments for balcony sliders, and antimicrobial vent sanitizers that keep coastal properties fresh and 5-star guest ready.",
            "services_intro": "Between guest turnarounds and coastal humidity defense, Gulf Shores properties require high-speed, reliable cleaning teams trained in lockbox and resort HOA protocols."
        }
    elif key == "mobile_al":
        return {
            "region": "mobile_metro",
            "market_name": "Mobile & Historic Azalea City",
            "environment_headline": "Historic Ceiling Detail & Sub-Tropical Moisture Defense in Mobile",
            "environment_desc": "heavy Gulf Coast rainfall, high humidity mold risks, and urban port particulate",
            "property_types": "Midtown Victorian homes with 12-ft ceilings, Oakleigh historic district properties, Spring Hill executive estates, and Downtown commercial offices",
            "neighborhoods": "Midtown, Spring Hill, Oakleigh Historic District, De Tonti Square, West Mobile, and Cottage Hill",
            "specialty": "telescoping 12-foot ceiling dusting, antimicrobial grout mold treatment, and Spring Hill recurring housekeeping",
            "local_landmarks": "USS Alabama Battleship Memorial Park, Dauphin Street Historic District, and Mobile Carnival Museum",
            "about_focus": "Serving Midtown Victorian homes, Oakleigh historic properties, Spring Hill estates, and Downtown commercial offices, Zoiris Cleaning Services is Mobile's premier in-house cleaning service.",
            "about_p2": "We deploy telescoping 12-foot extension dusters for historic crown moldings, transoms, and high ceiling fans, alongside antimicrobial surface solutions that combat Mobile's sub-tropical humidity.",
            "services_intro": "Whether you manage a medical practice on Airport Blvd, a historic home in Midtown, or a busy household in West Mobile, our vetted 2-person teams deliver consistent excellence."
        }
    elif key == "spanish_fort_al":
        return {
            "region": "eastern_shore",
            "market_name": "Spanish Fort & TimberCreek",
            "environment_headline": "Multi-Story Foyer Care & Delta Humidity Defense in Spanish Fort",
            "environment_desc": "Mobile-Tensaw Delta dampness, dense pine pollen blooms, and red clay runoff",
            "property_types": "TimberCreek golf villas, Rayne Plantation executive homes, Stonebridge residences, and Spanish Fort Town Center commercial suites",
            "neighborhoods": "TimberCreek, Rayne Plantation, Stonebridge, Blakeley Forest, and Spanish Fort Estates",
            "specialty": "high grand foyer extension dusting, delta moisture odor neutralization, and commuter-convenient scheduling",
            "local_landmarks": "Historic Blakeley State Park, Spanish Fort Town Center, and 5 Rivers Delta Resource Center",
            "about_focus": "Nestled along the Mobile-Tensaw Delta, Spanish Fort executive homes in TimberCreek and Rayne Plantation feature expansive square footage and high two-story foyers requiring coordinated cleaning teams.",
            "about_p2": "We send equipped multi-cleaner teams with commercial HEPA vacuums and extension dusting poles to sanitize multi-tier staircases, open-concept gourmet kitchens, and delta-facing porches.",
            "services_intro": "Designed for busy Eastern Shore commuters, our Spanish Fort services offer seamless digital scheduling, zero locked contracts, and zero reschedule penalty fees."
        }
    elif key == "birmingham_al":
        return {
            "region": "central_alabama",
            "market_name": "Birmingham Metro & Over-the-Mountain",
            "environment_headline": "Over-the-Mountain Estate Housekeeping & Red Clay Defense in Birmingham",
            "environment_desc": "Central Alabama red clay soil, heavy mountain pine pollen, and urban atmospheric soot",
            "property_types": "Mountain Brook luxury estates, Vestavia Hills executive residences, Homewood cottages, Downtown lofts, and Hwy 280 commercial centers",
            "neighborhoods": "Mountain Brook, Vestavia Hills, Homewood, Hoover, Forest Park, Downtown Loft District, and Trussville",
            "specialty": "fine architectural millwork polishing, red clay floor extraction, and corporate office janitorial",
            "local_landmarks": "Vulcan Park & Museum, Birmingham Botanical Gardens, and UAB Medical Center",
            "about_focus": "From sprawling Mountain Brook and Homewood estates to Downtown lofts and Hwy 280 corporate corridors, Zoiris Cleaning Services delivers executive housekeeping and commercial janitorial across the Birmingham metro.",
            "about_p2": "Our teams use specialized HEPA floor extraction systems and non-abrasive microfiber mops to remove sticky Alabama red clay without scratching luxury hardwood, marble, or designer tile.",
            "services_intro": "Birmingham professionals trust our bonded, background-checked staff for flexible weekly maid visits, deposit-guaranteed move turnovers, and after-hours corporate sanitization."
        }
    elif key == "huntsville_al":
        return {
            "region": "north_alabama",
            "market_name": "Huntsville & Rocket City",
            "environment_headline": "Smart Home Surface Care & Aerospace Relocation Turnovers in Huntsville",
            "environment_desc": "Tennessee Valley seasonal allergens, limestone mineral dust, and rapid suburban construction soil",
            "property_types": "Madison modern smart homes, Hampton Cove master-planned residences, Twickenham historic district homes, and Cummings Research Park tech facilities",
            "neighborhoods": "Madison, Hampton Cove, Twickenham Historic District, Monte Sano, Old Town, and Research Park",
            "specialty": "non-static smart display and quartz care, Redstone Arsenal relocation turnovers, and tech park janitorial",
            "local_landmarks": "U.S. Space & Rocket Center, Monte Sano State Park, and Cummings Research Park",
            "about_focus": "Supporting tech engineers, aerospace professionals, and families across Madison, Hampton Cove, and Twickenham, Zoiris Cleaning Services delivers high-precision cleaning across Rocket City.",
            "about_p2": "Our cleaners utilize non-static microfiber equipment safe for smart home displays, quartz surfaces, and modern electronics, alongside deposit-guaranteed turnover cleans for relocating defense contractors.",
            "services_intro": "Huntsville's fast-growing community counts on our reliable in-house teams for customized residential housekeeping and secure after-hours commercial facility care."
        }
    
    if key in LOCAL_INTEL:
        intel = LOCAL_INTEL[key]
        return {
            "region": intel.get("region", "regional_alabama"),
            "market_name": intel.get("market_name", f"{city} Area"),
            "environment_headline": f"{city} Local Environmental Defense & Surface Care",
            "environment_desc": intel.get("local_environment", f"seasonal weather and dust across {county}"),
            "property_types": ", ".join(intel.get("property_profiles", [f"homes and offices in {city}"])),
            "neighborhoods": intel.get("neighborhoods", f"residential subdivisions and commercial districts throughout {city}"),
            "specialty": intel.get("cleaning_challenges", [f"routine housekeeping and deep cleaning in {city}"])[0],
            "local_landmarks": intel.get("local_landmarks", f"the {city} area"),
            "about_focus": f"Serving {city} and {county}, Zoiris Cleaning Services delivers white-glove, no-contract residential housekeeping, move-out turnovers, and commercial janitorial tailored specifically to {intel.get('market_name', city)}.",
            "about_p2": f"Our cleaning specialists deploy commercial HEPA filtration vacuums and hospital-grade eco disinfectants to eliminate {intel.get('local_environment', 'regional dust and allergens')} across {city}.",
            "services_intro": f"From single-family homes to local business offices, we deliver customized cleaning checklists designed around your routine in {city} with zero locked contracts."
        }
        
    # Fallback classifications
    return {
        "region": "regional_alabama",
        "market_name": f"{city} Local Service Area",
        "environment_headline": f"Dependable Local Housekeeping & Sanitization in {city}",
        "environment_desc": f"seasonal weather, red clay dust, and regional pollen across {county}",
        "property_types": f"single-family residences, townhomes, country properties, and local small business offices in {city}",
        "neighborhoods": f"residential homes and local commercial properties throughout {city} and adjacent {county} communities",
        "specialty": f"affordable flat-rate home cleaning, move-in/out sanitization, and dependable maid visits in {city}",
        "local_landmarks": f"the greater {city} area and surrounding {county} communities",
        "about_focus": f"Bringing high-standard cleaning excellence to {city}, Zoiris Cleaning Services offers transparent pricing, vetted in-house cleaners, and customized housekeeping plans with zero locked-in contracts.",
        "about_p2": f"We equip our background-checked crews with commercial HEPA vacuums and EPA-registered sanitizers to protect indoor air quality across {city} and {county}.",
        "services_intro": f"Enjoy a spotless home or workplace in {city} with complete scheduling flexibility and our 100% Re-Clean Guarantee."
    }

def generate_location_faqs(city, loc_slug, county):
    prof = get_city_profile(city, loc_slug, county)
    key = loc_slug.lower().strip().replace('-', '_')
    intel = LOCAL_INTEL.get(key, {})
    
    if key == "daphne_al":
        return [
            {
                "q": "How do your maid services care for delicate hardwood and historic surfaces in Daphne homes?",
                "a": "Many homes throughout Daphne (especially in Lake Forest, Sehoy, and along Scenic 98) feature custom oak, heart pine, or luxury engineered hardwoods. Our cleaners strictly use pH-neutral, manufacturer-recommended hardwood cleaners (following Bona standards) and dedicated microfiber mop pads to safely lift Baldwin County dirt and bay moisture without dulling or warping the wood finish."
            },
            {
                "q": "How do you handle spring live oak pollen and red clay tracking in Daphne residences?",
                "a": "During heavy Eastern Shore pollen seasons, yellow dust coats window sills, screened porches, and intake vents, while Alabama red clay tracks into mudrooms and foyers. We deploy multi-stage HEPA filtration vacuums that trap 99.97% of fine dust particulates down to 0.3 microns and apply non-abrasive clay-lifting solutions to keep your entryway floors spotless."
            },
            {
                "q": "What is the difference between recurring maid service and a deep clean in Daphne, AL?",
                "a": "A recurring clean in Daphne maintains pristine day-to-day cleanliness (bathrooms sanitized, kitchen degreased, floors HEPA vacuumed and mopped, beds dressed). A deep clean is an intensive top-to-bottom scrub that includes hand-washing baseboards, door frames, window blinds, ceiling fan blades, inside microwaves, and removing stubborn scale buildup."
            },
            {
                "q": "Do you require long-term contracts for house cleaning in Daphne?",
                "a": "No, never! All our cleaning services in Daphne are 100% No-Contract. Whether you need weekly, bi-weekly, monthly, or a one-time intensive deep scrub, you maintain complete freedom to start, pause, or reschedule anytime."
            },
            {
                "q": "Are your cleaners background checked, bonded, and insured in Daphne, AL?",
                "a": "Yes, 100%. Zoiris Cleaning Services carries comprehensive general liability insurance and workers' compensation coverage. Every cleaner is an in-house, background-checked W-2 employee (never random gig subcontractors) trained in professional property protection protocols."
            },
            {
                "q": "What neighborhoods in Daphne and Baldwin County do you cover?",
                "a": "We cover all residential enclaves in Daphne, including Lake Forest, Sehoy, Austin Park, Diamante, Historic Old Daphne, Scenic 98 bluffs, and nearby Eastern Shore communities."
            },
            {
                "q": "Can I customize my Daphne cleaning checklist or add interior appliance cleaning?",
                "a": "Yes! You can easily customize your service with add-ons such as inside oven detailing, refrigerator interior sanitization, cabinet interior wipeouts, and patio sweeping."
            },
            {
                "q": "What is your 100% Satisfaction Guarantee policy in Daphne, AL?",
                "a": "Every clean is backed by our 100% Re-Clean Guarantee. If you notice any area that was missed or not up to standard, contact us within 24 hours at (251) 220-2515 and our crew will promptly return to re-clean it at zero extra charge."
            }
        ]
    elif key == "fairhope_al":
        return [
            {
                "q": "How does your cleaning service protect original heart-pine and historic trim in Fairhope cottages?",
                "a": "Historic homes in Fairhope's Fruit & Nut District and Point Clear feature delicate architectural woodwork, antique mantels, and original heart-pine flooring. We use dedicated pH-neutral, non-abrasive cleaners and gentle microfiber cleaning cloths to preserve natural patinas without chemical haze or water damage."
            },
            {
                "q": "Do you use non-toxic, eco-friendly, and pet-safe products in Fairhope homes?",
                "a": "Yes, exclusively. We understand the high standards Fairhope homeowners have for indoor air quality and pet safety. We utilize hospital-grade, EPA-registered eco-friendly disinfectants that neutralize 99.9% of bacteria without harsh chlorine fumes or synthetic fragrances."
            },
            {
                "q": "What is included in a luxury estate or cottage deep clean in Fairhope, AL?",
                "a": "Our Fairhope deep cleaning is a white-glove restorative scrub: hand-washing baseboards, French door frames, high transom windows, ceiling fan blades, descaling luxury bathroom marble, degreasing gourmet ranges, and HEPA vacuuming fine rugs."
            },
            {
                "q": "Do you offer discreet, white-glove recurring housekeeping in Point Clear and Lakewood?",
                "a": "Yes. We provide recurring weekly and bi-weekly housekeeping for executive and bayfront residences throughout Fairhope, Rock Creek, Lakewood, and Point Clear, staffed by uniformed, background-checked professionals."
            },
            {
                "q": "Do you charge fees if I need to reschedule my Fairhope cleaning visit?",
                "a": "No! We never charge rescheduling fees. If your family schedule or travel plans change in Fairhope, simply let us know in advance and we will gladly adjust your date."
            },
            {
                "q": "Are your cleaners full-time employees or third-party contractors?",
                "a": "Every member of our team is a direct in-house W-2 employee who has passed rigorous criminal background checks, drug screenings, and specialized surface-care training."
            },
            {
                "q": "What commercial janitorial services do you provide for Downtown Fairhope businesses?",
                "a": "We provide after-hours cleaning for art galleries, boutique retail storefronts, legal practices, and medical suites throughout Downtown Fairhope with customized sanitization schedules and zero locked contracts."
            },
            {
                "q": "How do I book an initial cleaning or get a quote in Fairhope, AL?",
                "a": "Call our team 24/7 at (251) 220-2515 or submit our quick online quote form to receive an instant, transparent flat-rate estimate tailored to your Fairhope residence."
            }
        ]
    elif key == "gulf_shores_al":
        return [
            {
                "q": "How do you remove embedded beach sand and salt-air film from Gulf Shores condos and homes?",
                "a": "In coastal Gulf Shores, fine silica beach sand penetrates carpet backings, tile grout, and sofa crevices, while salt mist leaves a sticky haze on sliding glass and fixtures. We deploy commercial HEPA filtration vacuum systems designed for sand extraction and non-abrasive glass cleaners that dissolve salt haze without streaking."
            },
            {
                "q": "Do you offer fast same-day turnover cleaning for Gulf Shores vacation rentals and Airbnbs?",
                "a": "Yes! We specialize in the critical 10:00 AM to 3:00 PM turnaround window between guest checkout and check-in for West Beach, East Beach, and Fort Morgan rentals. Our turnover protocol includes bed linen stripping and washing, bathroom disinfection, amenity restocking, and digital photo inspection."
            },
            {
                "q": "Do I need to sign an annual contract for vacation rental cleaning in Gulf Shores?",
                "a": "No! All vacation rental and condo cleaning services in Gulf Shores are 100% No-Contract. You can schedule cleans on-demand or align with your rental calendar with complete flexibility."
            },
            {
                "q": "Are your cleaners insured and bonded to enter Gulf Shores beachfront condominium towers?",
                "a": "Yes, 100%. Zoiris Cleaning Services carries comprehensive liability and workers' compensation coverage. Our cleaners are trained in security keycard handling, lockbox codes, and HOA guidelines for complexes such as Phoenix, Crystal Tower, and Boardwalk."
            },
            {
                "q": "How often should coastal Gulf Shores properties receive a comprehensive deep clean?",
                "a": "We recommend a comprehensive deep clean twice per year for primary coastal residences (spring pre-season and autumn reset). For active short-term rentals, an intensive pre-summer deep clean is essential to earn consistent 5-star guest reviews."
            },
            {
                "q": "What residential neighborhoods in Gulf Shores do you service for private homeowners?",
                "a": "In addition to beachfront condos, we provide routine house cleaning and deep cleaning for private residences in Craft Farms, Peninsula, Oyster Bay, Aventura, and along the Fort Morgan corridor."
            },
            {
                "q": "What cleaning equipment and supplies do your crews bring to Gulf Shores?",
                "a": "Our teams arrive fully equipped with commercial-grade HEPA vacuums, microfiber mop systems, extension poles for high ceilings, and hospital-grade eco-friendly disinfectants."
            },
            {
                "q": "What is your satisfaction guarantee for cleanings in Gulf Shores, AL?",
                "a": "Every clean is backed by our 100% Re-Clean Guarantee. If any area is ever reported not up to standard, contact us within 24 hours and our team will return promptly to re-clean it at zero extra charge."
            }
        ]
    elif key == "mobile_al":
        return [
            {
                "q": "How does your cleaning service handle high ceilings and historic architectural details in Mobile homes?",
                "a": "Historic homes across Midtown, Oakleigh, and De Tonti Square frequently feature 12-foot ceilings, ornate crown moldings, picture rails, and vintage crystal chandeliers. Our teams utilize specialized telescoping HEPA extension dusters and gentle microfiber tools to capture dust and cobwebs without endangering delicate historic plaster."
            },
            {
                "q": "How do your cleaning methods combat Mobile's high sub-tropical humidity and allergen risks?",
                "a": "Mobile receives the highest annual rainfall of any city in the contiguous US, creating prime conditions for dust mites and mildew in air vents and bathroom tile. We deploy multi-stage HEPA filtration vacuums that capture 99.97% of airborne allergens down to 0.3 microns, paired with hospital-grade surface sanitization."
            },
            {
                "q": "What recurring maid schedules do you offer Mobile families and professionals?",
                "a": "We provide weekly, bi-weekly, monthly, or on-demand one-time cleanings with 100% No Contracts. You have total freedom to pause, reschedule, or adjust your schedule whenever needed."
            },
            {
                "q": "Do you provide deposit-guaranteed move-out cleaning in Mobile, AL?",
                "a": "Yes! Our Mobile move-out cleanings follow strict property management checklists—wiping inside all kitchen and bathroom cabinets, detailing interior ovens and refrigerators, scrubbing baseboards, and sanitizing floors."
            },
            {
                "q": "Are your cleaners background-checked and insured to work in Mobile properties?",
                "a": "Yes. Zoiris Cleaning Services is fully licensed, bonded, and insured. Every cleaner is an in-house W-2 employee who has completed comprehensive background checks and hands-on training."
            },
            {
                "q": "What neighborhoods in Mobile and Mobile County do you cover?",
                "a": "We cover all areas of Mobile, including Spring Hill, Midtown, Downtown, Oakleigh, West Mobile, Cottage Hill, Saraland, Semmes, Theodore, and Satsuma."
            },
            {
                "q": "What commercial janitorial services do you offer in Mobile, AL?",
                "a": "We provide after-hours office cleaning, medical suite sanitization, law firm janitorial, and commercial floor care for businesses along Airport Blvd, Dauphin Street, and the Downtown business district."
            },
            {
                "q": "How do I schedule a cleaning service in Mobile, AL?",
                "a": "Call our Mobile dispatch team 24/7 at (251) 220-2515 or request a free estimate online to choose your preferred cleaning date."
            }
        ]
    elif key == "spanish_fort_al":
        return [
            {
                "q": "How do your cleaning teams service large custom homes in Spanish Fort communities like TimberCreek?",
                "a": "Homes in TimberCreek, Rayne Plantation, and Stonebridge often exceed 3,500 square feet with multi-tier foyers and custom finishes. We send coordinated 2-to-3 person professional teams equipped with commercial HEPA vacuums and specialized extension tools to clean every level thoroughly and efficiently."
            },
            {
                "q": "How does your service tackle Mobile-Tensaw Delta humidity and pine pollen in Spanish Fort?",
                "a": "Surrounded by pine canopies and delta waterways, Spanish Fort homes face heavy pine dust and humidity dampness. Our cleaning protocol includes wet-wiping window sills, dusting intake registers, and using moisture-safe floor sanitizers."
            },
            {
                "q": "Do you require contracts for recurring house cleaning in Spanish Fort, AL?",
                "a": "No. All our recurring maid services in Spanish Fort are 100% No-Contract, allowing you to pause or reschedule anytime with zero fees."
            },
            {
                "q": "Are your cleaning professionals insured, bonded, and vetted in Spanish Fort?",
                "a": "Yes, 100%. We carry comprehensive general liability and workers' compensation insurance. Every cleaner is an in-house background-checked employee."
            },
            {
                "q": "What areas of Spanish Fort do you cover?",
                "a": "We cover all of Spanish Fort including TimberCreek, Rayne Plantation, Stonebridge, Historic Blakeley area, Highway 181 corridor, and Spanish Fort Town Center."
            },
            {
                "q": "Can I add inside appliance detailing to my Spanish Fort deep clean?",
                "a": "Yes! Interior oven scrubbing, refrigerator sanitizing, and inside cabinet wipeouts can be added to any deep cleaning visit."
            },
            {
                "q": "What equipment and supplies do you bring to Spanish Fort homes?",
                "a": "Our teams bring commercial HEPA vacuums, microfiber mop pads, and hospital-grade eco-friendly cleaning solutions that are completely safe for children and pets."
            },
            {
                "q": "What is your satisfaction guarantee in Spanish Fort, AL?",
                "a": "We back every job with our 100% Re-Clean Guarantee. If you notice any area that doesn't meet your expectations, let us know within 24 hours and we will re-clean it for free."
            }
        ]
    elif key == "birmingham_al":
        return [
            {
                "q": "Do you provide executive residential housekeeping and commercial office janitorial in Birmingham, AL?",
                "a": "Yes! We offer tailored residential maid service, deep seasonal resets, and after-hours commercial office janitorial across Mountain Brook, Vestavia Hills, Hoover, Homewood, Downtown, and the UAB medical corridor."
            },
            {
                "q": "How do you handle heavy red clay tracking and pine pollen in Birmingham homes?",
                "a": "Central Alabama red clay soil and mountain pine pollen require specialized floor care. We use multi-stage HEPA vacuums and microfiber mopping systems that capture fine clay particulates without scratching hardwood, luxury vinyl plank, or marble."
            },
            {
                "q": "Do you require long-term contracts for cleaning in Birmingham?",
                "a": "Never. All our cleaning plans in Birmingham are 100% No-Contract. You have total freedom to schedule weekly, bi-weekly, or one-time visits and adjust anytime."
            },
            {
                "q": "Are your cleaning professionals licensed, bonded, and insured in Birmingham?",
                "a": "Yes, 100%. Zoiris Cleaning Services carries comprehensive liability insurance and workers' comp. Every cleaner is an in-house vetted employee who has passed rigorous background screening."
            },
            {
                "q": "What is included in a top-to-bottom deep clean in Birmingham, AL?",
                "a": "Our Birmingham deep cleaning covers intensive hand-washing of baseboards, door frames, window sills, blinds, ceiling fans, light switches, kitchen backsplash degreasing, and heavy bathroom lime/soap scum extraction."
            },
            {
                "q": "What neighborhoods and business centers do you cover across Birmingham?",
                "a": "We cover Mountain Brook, Forest Park, Vestavia Hills, Homewood, Hoover, Downtown Birmingham lofts, and Hwy 280 corporate corridors."
            },
            {
                "q": "Can I reschedule or skip a cleaning visit without penalty fees in Birmingham?",
                "a": "Yes! We never charge rescheduling fees. Simply notify our team in advance, and we will happily move your appointment date."
            },
            {
                "q": "How quickly can I get a quote and schedule a cleaning in Birmingham, AL?",
                "a": "Call our dispatch line 24/7 at (251) 220-2515 or submit an online request for an instant flat-rate estimate and rapid booking."
            }
        ]
    elif key == "huntsville_al":
        return [
            {
                "q": "Do you offer move-in sanitization and recurring maid services in Huntsville, AL?",
                "a": "Yes! We provide thorough move-in/move-out sanitization for relocating aerospace and tech professionals, alongside weekly, bi-weekly, and monthly recurring maid services throughout Huntsville and Madison."
            },
            {
                "q": "How do your cleaning teams protect high-tech surfaces and modern smart homes in Huntsville?",
                "a": "Our cleaners are trained in delicate surface protocols—using non-static microfiber dusting tools, non-corrosive eco-safe disinfectants, and specialized vacuum attachments designed to protect electronic displays, custom quartz countertops, and modern LED fixtures."
            },
            {
                "q": "Do I have to commit to an ongoing contract for home cleaning in Huntsville?",
                "a": "No. All cleaning services provided by Zoiris Cleaning Services in Huntsville are 100% No Locked Contracts. You are free to book one-time deep cleanings or recurring visits with zero commitments."
            },
            {
                "q": "What safety and insurance protections cover my Huntsville property during a cleaning?",
                "a": "We maintain full general liability insurance, bond protection, and workers' compensation. Every cleaner is a fully vetted, background-checked W-2 employee who arrives in uniform."
            },
            {
                "q": "What coverage areas and subdivisions do you service around Huntsville?",
                "a": "We service Madison, Hampton Cove, Twickenham Historic District, Monte Sano, Old Town, and the Cummings Research Park corridor."
            },
            {
                "q": "What supplies and equipment do you bring to cleanings in Huntsville, AL?",
                "a": "Our crews arrive fully self-sufficient with commercial-grade HEPA filtration vacuum systems, microfiber mop kits, extension dusters, and hospital-grade, pet-safe non-toxic disinfectants."
            },
            {
                "q": "What if I need to change my cleaning appointment date in Huntsville?",
                "a": "There are zero rescheduling penalty fees. Simply contact us in advance, and our scheduling team will shift your booking to the next available date."
            },
            {
                "q": "How is flat-rate pricing calculated for homes in Huntsville, AL?",
                "a": "We base our transparent flat-rate pricing on your home's total square footage, number of bedrooms and bathrooms, and selected service tier with zero hidden travel fees."
            }
        ]
    else: # Dynamic localized generation for all other AL cities
        return [
            {
                "q": f"Do you provide professional house cleaning and commercial janitorial in {city}, AL?",
                "a": f"Yes! Zoiris Cleaning Services provides comprehensive residential housekeeping, deep restorative cleanings, move-in/move-out turnovers, and commercial janitorial services throughout {city} and {county}."
            },
            {
                "q": f"Is there any travel fee or extra mileage charge for cleaning in {city}?",
                "a": f"No. We provide 100% upfront, transparent flat-rate pricing for homes and businesses in {city} with zero hidden travel fees, mileage surcharges, or unexpected add-ons."
            },
            {
                "q": f"Do you require long-term contracts for cleaning services in {city}?",
                "a": f"Never. All our cleaning plans in {city} are 100% No Locked Contracts. You have total freedom to schedule weekly, bi-weekly, monthly, or one-time cleanings and pause or adjust anytime."
            },
            {
                "q": f"What safety, bonding, and insurance protections cover my {city} property?",
                "a": f"Zoiris Cleaning Services is fully licensed, bonded, and carries general liability insurance and workers' compensation. Every cleaner is an in-house employee who has passed rigorous criminal background checks and professional training."
            },
            {
                "q": f"What equipment and cleaning products do your cleaners bring to {city}?",
                "a": f"Our crews arrive fully equipped with commercial-grade HEPA filtration vacuum systems, microfiber cleaning cloths, mop systems, extension dusters, and hospital-grade, pet-safe non-toxic disinfectants safe for kids and animals."
            },
            {
                "q": f"How long does a standard cleaning appointment take in a {city} home?",
                "a": f"Depending on your home's total square footage and room layout, a typical maintenance visit takes between 1.5 to 3.5 hours with our dedicated 2-person professional cleaning crew working systematically through your checklist."
            },
            {
                "q": f"What specific areas of {city} and surrounding {county} communities do you service?",
                "a": f"We service {prof['neighborhoods']}, covering single-family homes, townhomes, country estates, and local commercial facilities across {city}."
            },
            {
                "q": f"What is your 100% Satisfaction Guarantee policy in {city}, AL?",
                "a": f"If you are not completely delighted with any room or surface we cleaned, notify us within 24 hours of your service in {city}. Our team will promptly return to your property and re-clean the specific area at zero additional charge."
            }
        ]

def get_localized_about_html(city, loc_slug, county):
    prof = get_city_profile(city, loc_slug, county)
    return f"""
    <!-- 🌟 SECTION: ABOUT ZOIRIS CLEANING SERVICES IN {city.upper()} -->
    <section class="py-20 px-4 sm:px-6 lg:px-8 bg-transparent relative z-10" id="about">
      <div class="max-w-7xl mx-auto">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          
          <!-- Image Column -->
          <div class="relative">
            <div class="relative rounded-3xl overflow-hidden shadow-2xl border-4 border-white/20">
              <img src="/images/services_action.png" alt="Zoiris Cleaning Services team serving {city} AL" class="w-full h-full object-cover transform hover:scale-105 transition duration-500">
              <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent"></div>
              <div class="absolute bottom-6 left-6 right-6 text-white">
                <span class="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider mb-2 inline-block">
                  Verified Local Service
                </span>
                <h3 class="text-2xl font-bold">Trusted House &amp; Commercial Cleaning in {city}, AL</h3>
                <p class="text-gray-300 text-sm mt-1">Dedicated in-house staff • Licensed, bonded &amp; insured</p>
              </div>
            </div>
            <!-- Trust Badge Floating -->
            <div class="absolute -bottom-6 -right-6 bg-white p-4 rounded-2xl shadow-xl border border-gray-100 max-w-xs hidden sm:block">
              <div class="flex items-center gap-3">
                <div class="w-12 h-12 rounded-xl bg-blue-600 text-white flex items-center justify-center text-xl font-bold">
                  <i class="fas fa-shield-alt"></i>
                </div>
                <div>
                  <h4 class="font-bold text-gray-900 text-sm">100% Guaranteed</h4>
                  <p class="text-xs text-gray-500">Spotless results or we re-clean for free</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Content Column -->
          <div>
            <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 backdrop-blur-md border border-white/20 text-blue-200 text-sm font-semibold mb-4">
              <i class="fas fa-map-marker-alt text-blue-400"></i> {city}, AL Local Cleaning Authority
            </div>
            <h2 class="text-3xl sm:text-4xl font-extrabold text-white tracking-tight mb-6">
              {prof['environment_headline']}
            </h2>
            <p class="text-purple-100 text-base sm:text-lg mb-4 leading-relaxed">
              {prof['about_focus']}
            </p>
            <p class="text-purple-100 text-base sm:text-lg mb-6 leading-relaxed">
              {prof['about_p2']}
            </p>

            <div class="flex flex-col sm:flex-row gap-4 mt-8">
              <a href="tel:2512202515" class="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold py-3.5 px-8 rounded-full shadow-lg shadow-blue-500/30 text-center transition duration-300">
                <i class="fas fa-phone-alt mr-2"></i> Call (251) 220-2515
              </a>
              <a href="#quote" class="bg-white/10 hover:bg-white/20 text-white font-semibold py-3.5 px-8 rounded-full border border-white/30 text-center backdrop-blur-md transition duration-300">
                Get a Free Estimate
              </a>
            </div>

          </div>

        </div>
      </div>
    </section>
    """

def get_localized_city_services_html(city, loc_slug, county):
    key = loc_slug.lower().strip().replace('-', '_')
    prof = get_city_profile(city, loc_slug, county)
    
    if key == "daphne_al":
        cards = [
            ("Eastern Shore Deep Clean", "fas fa-sparkles", "bg-purple-100 text-purple-600", "Hand-scrubbed baseboards, door frames, inside microwaves, and deep live oak pollen extraction across Lake Forest, Sehoy, and Austin Park floor plans."),
            ("Hardwood & Pine Preservation", "fas fa-tree", "bg-amber-100 text-amber-600", "Bona-certified pH-neutral floor care and damp microfiber mops that lift Mobile Bay moisture and Baldwin County clay without clouding custom oak or heart pine."),
            ("Executive Move-In / Move-Out", "fas fa-truck-moving", "bg-blue-100 text-blue-600", "Turnkey empty-home turnovers meeting strict landlord inspections: interior cabinets, refrigerator/oven detailing, and full bathroom scale extraction."),
            ("Zero-Contract Maid Service", "fas fa-calendar-check", "bg-green-100 text-green-600", "Weekly, bi-weekly, or monthly recurring housekeeping with vetted W-2 staff, zero locked contracts, and zero fees for schedule adjustments.")
        ]
        subtitle = "Tailored Residential & Commercial Cleaning Protocols for Daphne, AL"
    elif key == "fairhope_al":
        cards = [
            ("Historic Cottage Deep Clean", "fas fa-home", "bg-pink-100 text-pink-600", "Gentle preservation-grade cleaning for Fruit & Nut District cottages, vintage French doors, high transom glass, and original heart pine flooring."),
            ("100% Non-Toxic & Pet-Safe Maid Care", "fas fa-leaf", "bg-green-100 text-green-600", "Hospital-grade, EPA-registered eco disinfectants free from synthetic fragrances, chlorine fumes, or harsh VOCs for pristine indoor air purity."),
            ("Bayfront Estate Housekeeping", "fas fa-water", "bg-blue-100 text-blue-600", "White-glove recurring housekeeping for Point Clear and Lakewood bayfront homes: anti-static salt air glass polishing and luxury marble descaling."),
            ("Downtown Commercial Janitorial", "fas fa-briefcase", "bg-purple-100 text-purple-600", "Discreet after-hours cleaning for Fairhope art galleries, boutique storefronts, medical suites, and legal offices with zero contract lock-ins.")
        ]
        subtitle = "Delicate Architectural Care & Eco-Safe Protocols for Fairhope & Point Clear"
    elif key == "gulf_shores_al":
        cards = [
            ("Vacation Rental Turnover Blitz", "fas fa-umbrella-beach", "bg-blue-100 text-blue-600", "Fast-turn 10am-3pm checkout-to-checkin turnovers: linen laundering, refrigerator sanitization, amenity restocking, and photo proof verification."),
            ("Silica Sand Extraction Deep Clean", "fas fa-wind", "bg-amber-100 text-amber-600", "Agitated commercial HEPA vacuums engineered to lift coarse beach sand from carpet backing, upholstery crevices, and tile grout lines."),
            ("Salt-Air Mist & Glass Descaling", "fas fa-tint", "bg-cyan-100 text-cyan-600", "Specialized anti-static treatments that dissolve sticky coastal salt-film from sliding balcony doors, glass railings, and outdoor fixtures."),
            ("Condo HOA & Keycard Compliant", "fas fa-key", "bg-purple-100 text-purple-600", "Uniformed, insured in-house staff experienced with lockbox codes, keycards, and property management rules across West Beach and Fort Morgan.")
        ]
        subtitle = "Coastal Sand Abatement & Vacation Rental Turnovers in Gulf Shores, AL"
    elif key == "mobile_al":
        cards = [
            ("Midtown Historic Deep Clean", "fas fa-landmark", "bg-indigo-100 text-indigo-600", "Telescoping HEPA dusters reaching 12-foot ceilings, crown moldings, ceiling fans, and vintage transoms in Oakleigh and Midtown homes."),
            ("Sub-Tropical Humidity & Mold Defense", "fas fa-shield-virus", "bg-green-100 text-green-600", "Antimicrobial surface disinfection targeting high-moisture bathroom tile, window sills, and AC intake registers across Mobile County."),
            ("Spring Hill & West Mobile Maid Care", "fas fa-house-user", "bg-purple-100 text-purple-600", "Structured 2-cleaner team routines for expansive suburban family residences, playrooms, and gourmet kitchens with zero locked contracts."),
            ("Corporate & Industrial Janitorial", "fas fa-building", "bg-blue-100 text-blue-600", "Reliable after-hours cleaning for Downtown Mobile corporate offices, port facilities, legal firms, and Airport Blvd healthcare suites.")
        ]
        subtitle = "High-Ceiling Historic Detail & Humidity Defense Across Mobile, AL"
    elif key == "spanish_fort_al":
        cards = [
            ("TimberCreek Multi-Story Detail", "fas fa-layer-group", "bg-amber-100 text-amber-600", "Multi-cleaner teams equipped with extension tools for two-story foyers, grand staircases, banisters, and high-ceiling living spaces."),
            ("Delta Humidity & Pine Pollen Scrub", "fas fa-tree", "bg-green-100 text-green-600", "Specialized HEPA air filtration and moisture-neutralizing hard floor solutions protecting indoor air from delta dampness and pine dust."),
            ("Commuter Flexible Housekeeping", "fas fa-clock", "bg-blue-100 text-blue-600", "Convenient scheduling with zero lock-in contracts and no fees for date adjustments, tailored for active Eastern Shore commuters."),
            ("Move-Out Deposit Turnover", "fas fa-clipboard-check", "bg-purple-100 text-purple-600", "Thorough empty-property scrubbing meeting strict rental management standards to ensure 100% security deposit returns.")
        ]
        subtitle = "Executive Multi-Story Care & Pine Defense in Spanish Fort, AL"
    elif key == "birmingham_al":
        cards = [
            ("Over-the-Mountain Estate Care", "fas fa-crown", "bg-purple-100 text-purple-600", "White-glove housekeeping for Mountain Brook, Vestavia Hills, and Homewood estates: custom millwork dusting and luxury surface care."),
            ("Red Clay & Pollen Abatement", "fas fa-shoe-prints", "bg-red-100 text-red-600", "Multi-stage HEPA filtration and microfiber floor washing that captures sticky Alabama red clay without dulling hardwoods or tile."),
            ("Downtown Loft & High-Rise Turnovers", "fas fa-city", "bg-blue-100 text-blue-600", "Turnkey move-in/move-out sanitization for urban condominiums and lofts with flexible key-drop and deposit-ready standards."),
            ("Commercial & Medical Janitorial", "fas fa-stethoscope", "bg-teal-100 text-teal-600", "After-hours sanitization for Hwy 280 corporate parks, UAB medical corridor offices, law practices, and commercial retail.")
        ]
        subtitle = "Estate Care, Red Clay Defense & Commercial Janitorial in Birmingham, AL"
    elif key == "huntsville_al":
        cards = [
            ("Tech Corridor Smart Home Care", "fas fa-laptop-house", "bg-cyan-100 text-cyan-600", "Non-static microfiber dusting and non-corrosive eco-safe cleaners protecting smart displays, quartz surfaces, and modern electronics."),
            ("Aerospace & Defense Relocation Turnovers", "fas fa-plane-departure", "bg-blue-100 text-blue-600", "Fast turnaround move-in/move-out sanitization for Redstone Arsenal personnel and tech contractors with deposit-back guarantees."),
            ("Madison & Hampton Cove Maid Service", "fas fa-home", "bg-indigo-100 text-indigo-600", "Recurring weekly and bi-weekly housekeeping for expansive suburban floor plans with multi-cleaner teams and zero contracts."),
            ("Commercial Facility & Janitorial", "fas fa-microchip", "bg-purple-100 text-purple-600", "Secure, background-checked after-hours office cleaning for Cummings Research Park suites, engineering firms, and labs.")
        ]
        subtitle = "Smart Home Housekeeping & Relocation Turnovers in Huntsville, AL"
    else:
        cards = [
            (f"Intensive Deep Restorative Clean", "fas fa-sparkles", "bg-purple-100 text-purple-600", f"Hand-washed baseboards, detailed window sills, inside microwaves, and deep sanitization across {prof['property_types']} in {city}."),
            (f"Recurring No-Contract Housekeeping", "fas fa-calendar-check", "bg-green-100 text-green-600", f"Weekly, bi-weekly, or monthly maid visits tailored to your routine with zero locked contracts and zero fees for schedule changes in {city}."),
            (f"Move-In / Move-Out Turnover Blitz", "fas fa-truck-moving", "bg-blue-100 text-blue-600", f"Thorough empty-property scrubbing meeting Alabama rental standards: interior cabinets, appliances, and floor sanitization in {county}."),
            (f"Commercial Office & Business Janitorial", "fas fa-building", "bg-amber-100 text-amber-600", f"Dependable after-hours cleaning, trash removal, restroom disinfection, and floor care for local businesses and offices throughout {city}.")
        ]
        subtitle = f"Customized Residential Housekeeping & Commercial Janitorial in {city}, AL"

    cards_html = ""
    for title, icon, bg, desc in cards:
        cards_html += f"""
          <!-- Service Card -->
          <div class="bg-white/95 rounded-2xl p-6 sm:p-8 shadow-xl border border-white/20 hover:scale-[1.02] transition-transform duration-300">
            <div class="w-12 h-12 rounded-xl {bg} flex items-center justify-center text-2xl mb-5">
              <i class="{icon}"></i>
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-3">{title}</h3>
            <p class="text-sm text-gray-700 leading-relaxed">
              {desc}
            </p>
          </div>
"""

    return f"""
    <!-- 🧼 SECTION: LOCAL SERVICE HIGHLIGHTS & PROPERTY PROTOCOLS -->
    <section class="py-20 px-4 sm:px-6 lg:px-8 bg-transparent relative z-10" id="services-overview">
      <div class="max-w-7xl mx-auto">
        
        <div class="text-center max-w-3xl mx-auto mb-16">
          <span class="text-sm font-bold uppercase tracking-wider text-blue-100 bg-white/10 backdrop-blur-md border border-white/20 px-4 py-1.5 rounded-full">
            ✦ Local Cleaning Excellence in {city}, AL ✦
          </span>
          <h2 class="text-3xl md:text-4xl font-extrabold text-white mt-4 tracking-tight">
            {subtitle}
          </h2>
          <div class="mt-3 h-1 w-24 bg-gradient-to-r from-blue-400 to-indigo-400 mx-auto rounded"></div>
          <p class="mt-4 text-purple-100 text-base md:text-lg leading-relaxed">
            {prof['services_intro']}
          </p>
        </div>

        <!-- Local Service Cards Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
{cards_html}
        </div>

      </div>
    </section>
    """


def get_localized_faq_html(city, loc_slug, county):
    prof = get_city_profile(city, loc_slug, county)
    faqs = generate_location_faqs(city, loc_slug, county)
    items_html = ""
    icon_list = [
        "fas fa-file-signature", "fas fa-calendar-alt", "fas fa-shield-alt", "fas fa-calculator",
        "fas fa-spray-can", "fas fa-layer-group", "fas fa-map-marked-alt", "fas fa-award"
    ]
    for i, item in enumerate(faqs):
        icon = icon_list[i % len(icon_list)]
        items_html += f"""
          <!-- FAQ {i+1} -->
          <div class="bg-white rounded-2xl border border-white/20 shadow-xl overflow-hidden transition-all duration-200">
            <button class="w-full px-6 py-5 text-left font-bold text-lg text-gray-900 flex justify-between items-center hover:bg-slate-50 transition" onclick="toggleFaq(this)">
              <span class="flex items-center gap-3">
                <i class="{icon} text-blue-600"></i>
                {item['q']}
              </span>
              <i class="fas fa-chevron-down text-gray-400 transition-transform duration-300"></i>
            </button>
            <div class="faq-answer px-6 pb-6 pt-2 text-gray-700 text-sm sm:text-base leading-relaxed hidden border-t border-gray-100">
              <p>
                {item['a']}
              </p>
            </div>
          </div>
"""
    return f"""
    <!-- ❓ SECTION: FREQUENTLY ASKED QUESTIONS (ACCORDION & RICH SEO) -->
    <section class="py-20 px-4 sm:px-6 lg:px-8 bg-transparent relative z-10" id="faq">
      <div class="max-w-5xl mx-auto">
        
        <div class="text-center max-w-3xl mx-auto mb-14">
          <span class="text-sm font-bold uppercase tracking-wider text-blue-100 bg-white/10 backdrop-blur-md border border-white/20 px-4 py-1.5 rounded-full">
            ✦ {prof['market_name']} Housekeeping &amp; Janitorial FAQs ✦
          </span>
          <h2 class="text-3xl md:text-4xl font-extrabold text-white mt-4 tracking-tight">
            Frequently Asked Questions About Cleaning Services in {city}, AL
          </h2>
          <div class="mt-3 h-1 w-24 bg-gradient-to-r from-blue-400 to-indigo-400 mx-auto rounded"></div>
          <p class="mt-4 text-purple-100 text-base md:text-lg leading-relaxed">
            Essential answers on our {prof['specialty']}, flexible scheduling, and surface care guarantees across {city} and {county}.
          </p>
        </div>

        <!-- Accordion Items -->
        <div class="space-y-4">
{items_html}
        </div>

        <!-- FAQ CTA -->
        <div class="mt-12 text-center bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl p-6 sm:p-8 text-white shadow-xl">
          <h3 class="text-xl sm:text-2xl font-bold mb-2">Have a specific question about your {city} property?</h3>
          <p class="text-blue-100 text-sm sm:text-base mb-6 max-w-xl mx-auto">
            Our friendly customer care team is available 24/7 to discuss your cleaning needs and provide an instant, customized quote.
          </p>
          <div class="flex flex-col sm:flex-row justify-center gap-4">
            <a href="tel:2512202515" class="bg-white text-blue-700 font-bold px-6 py-3 rounded-full hover:bg-gray-100 transition shadow-md">
              <i class="fas fa-phone-alt mr-2"></i> Call (251) 220-2515
            </a>
            <a href="#quote" class="bg-black/30 hover:bg-black/50 text-white font-bold px-6 py-3 rounded-full border border-white/30 transition">
              <i class="fas fa-file-invoice mr-2"></i> Request A Free Estimate
            </a>
          </div>
        </div>

      </div>
    </section>

    <script>
      function toggleFaq(button) {{
        const answer = button.nextElementSibling;
        const icon = button.querySelector('.fa-chevron-down');
        const isOpen = !answer.classList.contains('hidden');

        document.querySelectorAll('.faq-answer').forEach(el => {{
          el.classList.add('hidden');
        }});
        document.querySelectorAll('#faq .fa-chevron-down').forEach(el => {{
          el.classList.remove('rotate-180');
        }});

        if (!isOpen) {{
          answer.classList.remove('hidden');
          icon.classList.add('rotate-180');
        }}
      }}
    </script>
"""

import os
import json
import re

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Geographical and Economic Regional Classifications for Alabama
COASTAL_CITIES = {
    'gulf-shores-al', 'orange-beach-al', 'dauphin-island-al', 'fort-morgan-al', 'foley-al',
    'elberta-al', 'summerdale-al', 'lillian-al', 'perdido-beach-al', 'bayou-la-batre-al',
    'coden-al', 'magnolia-springs-al', 'bon-secour-al'
}

EASTERN_SHORE_CITIES = {
    'daphne-al', 'fairhope-al', 'spanish-fort-al', 'point-clear-al', 'montrose-al',
    'loxley-al', 'robertsdale-al', 'bay-minette-al', 'silverhill-al', 'stapleton-al',
    'stockton-al', 'eastern-shore-al', 'perdido-al', 'rabun-al', 'tensaw-al'
}

MOBILE_METRO_CITIES = {
    'mobile-al', 'midtown-mobile-al', 'downtown-mobile-al', 'west-mobile-al', 'spring-hill-al',
    'cottage-hill-al', 'saraland-al', 'semmes-al', 'theodore-al', 'satsuma-al', 'grand-bay-al',
    'creola-al', 'axis-al', 'chunchula-al', 'citronelle-al', 'eight-mile-al', 'irvington-al',
    'saint-elmo-al', 'wilmer-al', 'tillmans-corner-al', 'toulminville-al', 'prichard-al',
    'chickasaw-al', 'bucks-al', 'calvert-al', 'mount-vernon-al', 'whistler-al',
    'maid-service-mobile-al-al', 'dog-river-al', 'gulfcrest-al'
}

BIRMINGHAM_METRO_CITIES = {
    'birmingham-al', 'hoover-al', 'vestavia-hills-al', 'homewood-al', 'mountain-brook-al',
    'alabaster-al', 'bessemer-al', 'pelham-al', 'trussville-al', 'gardendale-al', 'leeds-al',
    'fairfield-al', 'center-point-al', 'fultondale-al', 'irondale-al', 'chelsea-al',
    'calera-al', 'helena-al', 'montevallo-al', 'hueytown-al', 'midfield-al', 'pleasant-grove-al',
    'tarrant-al', 'adamsville-al', 'forestdale-al', 'clay-al', 'pinson-al', 'moody-al'
}

HUNTSVILLE_TENNESSEE_VALLEY = {
    'huntsville-al', 'madison-al', 'decatur-al', 'athens-al', 'florence-al', 'muscle-shoals-al',
    'sheffield-al', 'tuscumbia-al', 'hartselle-al', 'scottsboro-al', 'fort-payne-al',
    'albertville-al', 'boaz-al', 'guntersville-al', 'arab-al', 'cullman-al', 'bridgeport-al',
    'rainsville-al', 'stevenson-al', 'elkmont-al', 'rogersville-al', 'killen-al'
}

MONTGOMERY_RIVER_REGION = {
    'montgomery-al', 'prattville-al', 'wetumpka-al', 'millbrook-al', 'pike-road-al',
    'tallassee-al', 'selma-al', 'tuskegee-al', 'deatsville-al', 'coosada-al', 'clanton-al',
    'alexander-city-al', 'dadeville-al', 'hayneville-al'
}

COLLEGE_TOWN_METROS = {
    'tuscaloosa-al', 'northport-al', 'auburn-al', 'opelika-al', 'troy-al',
    'jacksonville-al', 'livingston-al', 'marion-al'
}

WIREGRASS_SOUTHEAST = {
    'dothan-al', 'enterprise-al', 'ozark-al', 'daleville-al', 'andalusia-al', 'eufaula-al',
    'headland-al', 'geneva-al', 'hartford-al', 'slocomb-al', 'opp-al', 'abbeville-al',
    'flomaton-al', 'atmore-al', 'brewton-al', 'monroeville-al', 'evergreen-al'
}

def get_city_profile(city, loc_slug, county):
    loc_clean = loc_slug.lower().strip()
    
    if loc_clean in COASTAL_CITIES:
        return {
            "region": "coastal",
            "environment_headline": "Coastal Salt Air, Sand & Humidity Defense",
            "environment_desc": f"beach sand, high coastal humidity, and saltwater air common along the {city} coastline",
            "property_types": "beachfront condominiums, luxury vacation rental cottages, private coastal estates, and family beach residences",
            "neighborhoods": f"all beachfront strips, Gulf-front condo towers, and residential communities across {city} and South Baldwin County",
            "specialty": "rapid same-day turnover cleaning for vacation rentals & Airbnbs, HEPA sand extraction, and humidity moisture defense",
            "local_landmarks": f"the {city} beach shoreline, coastal rental developments, and nearby Gulf waters",
            "about_focus": f"Specializing in coastal property care across {city}, we help homeowners, property managers, and vacation hosts maintain 5-star clean standards despite rigorous beach sand and Gulf Coast humidity."
        }
    elif loc_clean in EASTERN_SHORE_CITIES:
        return {
            "region": "eastern_shore",
            "environment_headline": "Historic Bayfront Care & Hardwood Floor Preservation",
            "environment_desc": f"coastal bay breezes, seasonal Southern live oak pollen, and red-clay dust across the Eastern Shore",
            "property_types": "historic bayfront residences, custom golf community homes, private estates, and modern single-family subdivisions",
            "neighborhoods": f"established bayside neighborhoods, scenic bluffs, and vibrant residential enclaves throughout {city} and {county}",
            "specialty": "delicate hardwood floor preservation (Bona standards), high-detail dusting, and customizable recurring maid service",
            "local_landmarks": f"Mobile Bay coastline, downtown {city} boutique districts, and scenic Eastern Shore parkways",
            "about_focus": f"From scenic bayfront properties to quiet residential subdivisions in {city}, our dedicated cleaning crews deliver white-glove housekeeping tailored to delicate surfaces, custom woodwork, and busy family lifestyles."
        }
    elif loc_clean in MOBILE_METRO_CITIES:
        return {
            "region": "mobile_metro",
            "environment_headline": "Gulf Coast Allergen Control & Deep Sanitization",
            "environment_desc": f"deep Southern humidity, heavy pollen seasons, and everyday dust in {county}",
            "property_types": "historic district homes, suburban family properties, modern townhomes, and commercial office suites",
            "neighborhoods": f"all residential subdivisions, historic corridors, and commercial business districts across {city}",
            "specialty": "multi-stage HEPA vacuum allergen extraction, 100% deposit-ready move-out cleans, and flexible recurring maid schedules",
            "local_landmarks": f"historic {city} avenues, suburban neighborhoods, and downtown commercial corridors",
            "about_focus": f"As your trusted local cleaning team in {city}, we bring top-tier sanitation, commercial-grade HEPA allergen removal, and dependable no-contract maid visits to homes and commercial spaces throughout {county}."
        }
    elif loc_clean in BIRMINGHAM_METRO_CITIES:
        return {
            "region": "birmingham_metro",
            "environment_headline": "Metropolitan Executive Maid & Commercial Janitorial",
            "environment_desc": f"urban particulate dust, seasonal pine pollen, and variable weather across the greater {city} area",
            "property_types": "executive residences, multi-level suburban estates, modern condos, and corporate commercial facilities",
            "neighborhoods": f"all metro districts, residential suburbs, and commercial centers throughout {city} and surrounding areas",
            "specialty": "after-hours commercial janitorial, executive deep housekeeping, and recurring residential maid visits",
            "local_landmarks": f"the {city} metro center, executive residential communities, and surrounding commercial corridors",
            "about_focus": f"Serving discerning homeowners and business leaders in {city}, Zoiris Cleaning Services delivers impeccable sanitation, flexible scheduling, and dependable bonded staff with zero lock-in contracts."
        }
    elif loc_clean in HUNTSVILLE_TENNESSEE_VALLEY:
        return {
            "region": "north_alabama",
            "environment_headline": "High-Tech Executive Residence & Valley Allergen Care",
            "environment_desc": f"Tennessee Valley humidity, mountain pollen, and fast-growing community dust in {city}",
            "property_types": "executive aerospace residences, modern smart homes, suburban subdivisions, and medical/tech facilities",
            "neighborhoods": f"residential communities, mountain-view neighborhoods, and tech business corridors across {city}",
            "specialty": "detailed move-in sanitization for relocating professionals, HEPA air particulate vacuuming, and commercial facility maintenance",
            "local_landmarks": f"the {city} tech corridor, mountain valley communities, and surrounding residential growth centers",
            "about_focus": f"Supporting busy professionals and families throughout {city}, we provide rigorous, systematic cleaning protocols that keep your living and work spaces pristine, healthy, and inviting."
        }
    elif loc_clean in MONTGOMERY_RIVER_REGION:
        return {
            "region": "river_region",
            "environment_headline": "Capital Region Housekeeping & Commercial Care",
            "environment_desc": f"River Region humidity, seasonal allergens, and everyday urban dust in {county}",
            "property_types": "historic antebellum homes, modern suburban family houses, government offices, and multi-family developments",
            "neighborhoods": f"historic neighborhoods, quiet residential subdivisions, and commercial business districts across {city}",
            "specialty": "comprehensive move-in/move-out cleans, reliable recurring maid service, and customized office janitorial",
            "local_landmarks": f"historic {city} landmarks, riverfront areas, and established residential suburbs",
            "about_focus": f"Delivering trusted cleaning services across {city}, our vetted and insured cleaners bring reliability, eco-friendly supplies, and detailed room-by-room care to every job."
        }
    elif loc_clean in COLLEGE_TOWN_METROS:
        return {
            "region": "college_metro",
            "environment_headline": "Fast-Paced Campus Turnover & Residential Detailing",
            "environment_desc": f"high-traffic living wear, student lease transition dust, and seasonal climate factors in {city}",
            "property_types": "student rental apartments, executive faculty homes, modern lofts, and local retail storefronts",
            "neighborhoods": f"campus neighborhoods, student housing communities, and quiet residential suburbs across {city}",
            "specialty": "deposit-guaranteed student move turnovers, game-day/event post-cleanups, and bi-weekly residential upkeep",
            "local_landmarks": f"the {city} campus district, student living corridors, and surrounding residential subdivisions",
            "about_focus": f"Whether you need a rapid lease-end turnover clean or weekly maintenance for a family home in {city}, Zoiris Cleaning Services ensures spotless, worry-free results backed by our 100% guarantee."
        }
    elif loc_clean in WIREGRASS_SOUTHEAST:
        return {
            "region": "wiregrass",
            "environment_headline": "Wiregrass Family Maid Service & Dust Mitigation",
            "environment_desc": f"Southeast Alabama humidity, agricultural dust, and strong summer pollen in {county}",
            "property_types": "single-family family homes, rural properties, military relocation residences, and commercial facilities",
            "neighborhoods": f"established family neighborhoods, quiet country acreage, and commercial districts throughout {city}",
            "specialty": "flat-rate residential maid care, military family move-out inspections, and commercial office cleaning",
            "local_landmarks": f"downtown {city}, regional agricultural hubs, and surrounding Wiregrass communities",
            "about_focus": f"Providing dependable cleaning solutions across {city}, our local crews take immense pride in honest, hard work, leaving your home spotless and sanitized every single time."
        }
    else:
        return {
            "region": "regional_alabama",
            "environment_headline": "Dependable Local Housekeeping & Sanitization",
            "environment_desc": f"seasonal Alabama weather, red clay dust, and regional pollen across {county}",
            "property_types": "single-family homes, country properties, rental units, and local small business offices",
            "neighborhoods": f"residential homes and local commercial properties throughout {city} and adjacent {county} communities",
            "specialty": "affordable flat-rate home cleaning, move-in/out sanitization, and dependable maid visits with zero travel surcharges",
            "local_landmarks": f"the greater {city} area and surrounding {county} communities",
            "about_focus": f"Bringing high-standard cleaning excellence to {city}, Zoiris Cleaning Services offers transparent pricing, vetted in-house cleaners, and customized housekeeping plans with zero locked-in contracts."
        }

def generate_location_faqs(city, loc_slug, county):
    prof = get_city_profile(city, loc_slug, county)
    reg = prof["region"]
    
    if reg == "coastal":
        return [
            {
                "q": f"How do you handle beach sand, salt air, and high humidity when cleaning homes in {city}, AL?",
                "a": f"In coastal {city}, beach sand and salt-laden humidity easily penetrate tile grout, baseboards, and carpets. We deploy commercial-grade HEPA filtration vacuum systems to extract embedded silica sand without scratching delicate surfaces, combined with non-abrasive, moisture-neutralizing sanitizers that prevent mildew growth in humid beach environments."
            },
            {
                "q": f"Do you offer fast turnaround cleaning for {city} vacation rentals and Airbnb properties?",
                "a": f"Yes! We specialize in rapid 10:00 AM to 3:00 PM turnover windows for vacation rentals, beach cottages, and VRBO/Airbnb properties in {city}. Our dedicated turnover protocol includes stripping and washing linens, complete kitchen and bathroom disinfection, guest amenity restocking, and digital photo verification so your property is 5-star guest ready."
            },
            {
                "q": f"Do I have to sign a seasonal or long-term contract for house cleaning in {city}?",
                "a": f"No, never. At Zoiris Cleaning Services, all residential and vacation rental cleaning services in {city} are 100% No-Contract. Whether you need bi-weekly housekeeping for your primary residence, a seasonal deep spring clean, or scheduled weekend turnovers during peak summer months, you maintain total scheduling freedom."
            },
            {
                "q": f"Are your cleaners licensed, bonded, and insured to work in {city} condos and private homes?",
                "a": f"Yes, absolutely. Zoiris Cleaning Services carries comprehensive general liability insurance and workers' compensation coverage. Every team member is an in-house, background-checked W-2 employee (never random third-party contractors) trained in strict safety, key handling, and property protection protocols."
            },
            {
                "q": f"What specific areas and complexes do you service across {city} and {county}?",
                "a": f"We cover {prof['neighborhoods']}, including beachfront condo complexes, private island communities, inland family subdivisions, and commercial storefronts throughout {city} and neighboring Alabama coastal areas."
            },
            {
                "q": f"How is pricing determined for house and condo cleaning in {city}, AL?",
                "a": f"We provide clear, upfront flat-rate pricing based on your property's square footage, bedroom and bathroom count, and chosen cleaning scope (standard maintenance, comprehensive deep clean, or vacation turnover). We never charge surprise mileage fees or hidden travel surcharges."
            },
            {
                "q": f"What professional equipment and supplies do your cleaners bring to {city} cleanings?",
                "a": f"Our teams arrive fully equipped with commercial HEPA vacuum systems, microfiber mop technology for hardwood and tile, extension dusters for vaulted ceilings, and hospital-grade, pet-safe non-toxic disinfectants safe for families and rental guests."
            },
            {
                "q": f"What is your 100% Satisfaction Guarantee policy in {city}?",
                "a": f"Your satisfaction is backed by our 100% Re-Clean Guarantee. If any area does not meet your high standards, simply notify us within 24 hours of your service in {city}. We will promptly dispatch our team back to re-clean the specific area at zero additional charge."
            }
        ]
    elif reg == "eastern_shore":
        return [
            {
                "q": f"How do your maid services care for delicate hardwood and historic surfaces in {city} homes?",
                "a": f"Many homes throughout {city} feature premium heart pine, oak, or custom engineered hardwoods. Our cleaners strictly use pH-neutral, manufacturer-recommended hardwood cleaners (following Bona standards) and dedicated microfiber mop pads to safely lift dirt and bay moisture without dulling or warping the wood finish."
            },
            {
                "q": f"What is the difference between recurring maid service and a deep clean in {city}?",
                "a": f"A recurring clean in {city} maintains pristine day-to-day cleanliness (bathrooms sanitized, kitchen degreased, floors HEPA vacuumed and mopped, beds dressed). A deep clean is an intensive top-to-bottom scrub that includes hand-washing baseboards, door frames, window blinds, ceiling fan blades, inside microwaves, and removing stubborn scale buildup."
            },
            {
                "q": f"Can I customize my cleaning checklist for my residence in {city}, AL?",
                "a": f"Absolutely. We work directly with you to prioritize key rooms, focus areas, or custom add-ons (such as interior oven detailing, refrigerator sanitizing, patio sweeping, or laundry folding) tailored precisely to your family's routine and lifestyle in {city}."
            },
            {
                "q": f"Do you charge penalty fees if I need to reschedule my cleaning visit in {city}?",
                "a": f"No! We never charge rescheduling fees. We understand that family commitments, travel, or unexpected events can change your schedule in {city}. Simply give us advance notice, and our friendly team will gladly move your appointment to the next convenient day without penalty."
            },
            {
                "q": f"Are your cleaners full-time vetted employees or independent subcontractors?",
                "a": f"100% of our staff are direct, in-house employees who have undergone thorough criminal background checks, drug screenings, and rigorous classroom and hands-on sanitization training. We never send unvetted third-party gig workers into your {city} home."
            },
            {
                "q": f"What neighborhoods and communities do you cover throughout {city} and {county}?",
                "a": f"We provide complete coverage across {prof['neighborhoods']}, from historic downtown and scenic bayfront roads to master-planned golf communities and new subdivisions across {city} and the Eastern Shore."
            },
            {
                "q": f"Do I need to provide vacuums, mops, or cleaning chemicals?",
                "a": f"No, our cleaning professionals arrive with all commercial-grade HEPA filtration vacuum equipment, microfiber cleaning tools, extension poles, and eco-friendly disinfectants. If you have specialized heirloom stone or custom wood products you prefer us to apply, we are happy to use them."
            },
            {
                "q": f"How do I request a free, customized quote for my {city}, AL home?",
                "a": f"You can call our team directly 24/7 at (251) 220-2515 or submit our quick online quote form on this page to receive an instant, transparent flat-rate estimate tailored to your home."
            }
        ]
    elif reg == "mobile_metro":
        return [
            {
                "q": f"What recurring cleaning frequencies do you offer homeowners in {city}, AL?",
                "a": f"We provide weekly, bi-weekly (every two weeks), tri-weekly, monthly, or on-demand one-time cleanings in {city}. All recurring housekeeping plans come with 100% No Locked Contracts, giving you complete freedom to pause, reschedule, or adjust frequency anytime."
            },
            {
                "q": f"How do your cleaning methods help with high humidity and dust allergens in {city}?",
                "a": f"Due to Gulf Coast humidity across {county}, dust mites and airborne allergens thrive in soft surfaces and duct registers. We utilize commercial-grade HEPA filtration vacuum systems capable of trapping 99.97% of particles down to 0.3 microns, paired with hospital-grade surface sanitization to keep your indoor air fresh and allergen-free."
            },
            {
                "q": f"Do you provide move-out deposit cleaning for renters and realtors in {city}?",
                "a": f"Yes! Our {city} move-out cleaning service follows strict property management inspection criteria—scrubbing inside kitchen cabinets, detailing appliances, hand-wiping baseboards, removing bathroom scale, and deep vacuuming closets to help ensure 100% deposit return."
            },
            {
                "q": f"Are your cleaners fully insured and background-checked in {city}, AL?",
                "a": f"Yes. Zoiris Cleaning Services is fully licensed, bonded, and carries general liability insurance and workers' compensation. Every cleaner is an in-house employee who has passed rigorous multi-state criminal background verification and hands-on sanitization training."
            },
            {
                "q": f"How long does a standard cleaning appointment take in a {city} home?",
                "a": f"Depending on your home's total square footage and room layout, a typical maintenance visit takes between 1.5 to 3 hours with our dedicated 2-person professional cleaning crew working systematically through your customized checklist."
            },
            {
                "q": f"What specific areas of {city} and surrounding communities do you service?",
                "a": f"We service {prof['neighborhoods']}, including Midtown, Downtown, West Mobile, Spring Hill, Cottage Hill, Saraland, Semmes, Theodore, Satsuma, Grand Bay, and adjacent Mobile County communities."
            },
            {
                "q": f"Are the cleaning solutions you use safe for children and household pets?",
                "a": f"Yes, 100%. We exclusively use commercial-grade, eco-friendly, non-toxic cleaning products that effectively eliminate 99.9% of harmful bacteria, grease, and grime without releasing harsh chemical fumes or toxic residues into your {city} home."
            },
            {
                "q": f"What is your 100% Satisfaction Guarantee policy in {city}, AL?",
                "a": f"If you are not completely delighted with any room or surface we cleaned, notify us within 24 hours. Our team will promptly return to your {city} property and re-clean the specific area at zero additional charge."
            }
        ]
    elif reg == "birmingham_metro":
        return [
            {
                "q": f"Do you provide both executive residential maid service and commercial office janitorial in {city}, AL?",
                "a": f"Yes! Zoiris Cleaning Services provides comprehensive residential housekeeping, deep restorative cleaning, and after-hours commercial office janitorial across {city} and the greater Birmingham metropolitan area."
            },
            {
                "q": f"Do you require long-term binding service contracts in {city}?",
                "a": f"Never. All our residential and commercial cleaning packages in {city} are 100% No-Contract. You have total freedom to schedule recurring cleanings, adjust frequency, or pause service at any time without cancellation penalties."
            },
            {
                "q": f"How do you handle heavy red clay tracking and seasonal pollen in {city} homes?",
                "a": f"Central Alabama red clay soil and heavy spring pine pollen require specialized care. We utilize multi-stage HEPA filtration vacuums and specialized microfiber mopping systems that capture fine clay particulates without scratching hardwood, luxury vinyl plank, or tile."
            },
            {
                "q": f"Are your cleaning professionals insured, bonded, and background checked?",
                "a": f"Yes, 100%. Zoiris Cleaning Services is fully licensed, bonded, and carries comprehensive general liability and workers' compensation coverage. Every team member is an in-house vetted employee who has passed rigorous background screening."
            },
            {
                "q": f"What is included in a top-to-bottom deep clean in {city}, AL?",
                "a": f"Our {city} deep cleaning covers intensive hand-washing of baseboards, door frames, window sills, blinds, ceiling fans, light switches, exterior and interior microwave detailing, kitchen backsplash degreasing, and heavy bathroom lime/soap scum extraction."
            },
            {
                "q": f"What neighborhoods and business centers do you cover across {city}?",
                "a": f"We cover {prof['neighborhoods']}, servicing executive estates, suburban master-planned communities, downtown lofts, and corporate office parks throughout {city}."
            },
            {
                "q": f"Can I reschedule or skip a cleaning visit without fees?",
                "a": f"Yes! We never charge rescheduling fees. We understand busy executive and family schedules in {city}. Simply notify our team in advance, and we will happily move your appointment date without hassle."
            },
            {
                "q": f"How quickly can I get a quote and schedule a cleaning in {city}, AL?",
                "a": f"Call our dispatch line 24/7 at (251) 220-2515 or submit an online request. We typically provide instant flat-rate estimates within minutes and can frequently accommodate same-week or next-day bookings."
            }
        ]
    elif reg == "north_alabama":
        return [
            {
                "q": f"Do you offer move-in sanitization and recurring maid services in {city}, AL?",
                "a": f"Yes! We provide thorough move-in/move-out sanitization for relocating professionals and families, alongside weekly, bi-weekly, and monthly recurring maid services throughout {city} and the Tennessee Valley region."
            },
            {
                "q": f"How do your cleaning teams protect high-tech and modern smart homes in {city}?",
                "a": f"Our professional cleaners are trained in delicate surface protocols—using non-static microfiber dusting tools, non-corrosive eco-safe disinfectants, and specialized vacuum attachments designed to protect electronic displays, custom stone countertops, and modern high-end finishes."
            },
            {
                "q": f"Do I have to commit to an ongoing contract for home cleaning in {city}?",
                "a": f"No. All cleaning services provided by Zoiris Cleaning Services in {city} are 100% No Locked Contracts. You are free to book one-time deep cleanings or recurring visits with zero lock-in commitments."
            },
            {
                "q": f"What safety and insurance protections cover my {city} property during a cleaning?",
                "a": f"We maintain full general liability insurance, bond protection, and workers' compensation. Every cleaner is a fully vetted, background-checked W-2 employee who arrives in uniform with professional equipment."
            },
            {
                "q": f"What coverage areas and subdivisions do you service around {city}?",
                "a": f"We service {prof['neighborhoods']}, including residential master-planned communities, executive subdivisions, and commercial business districts across {city} and North Alabama."
            },
            {
                "q": f"What supplies and equipment do you bring to cleanings in {city}, AL?",
                "a": f"Our crews arrive fully self-sufficient with commercial-grade HEPA filtration vacuum systems, microfiber mop kits, extension dusters, and hospital-grade, pet-safe non-toxic disinfectants that leave your home smelling naturally clean."
            },
            {
                "q": f"What if I need to change my cleaning appointment date in {city}?",
                "a": f"There are zero rescheduling penalty fees. Simply contact us in advance, and our scheduling team will happily shift your booking to the next available date that fits your calendar."
            },
            {
                "q": f"How is flat-rate pricing calculated for homes in {city}, AL?",
                "a": f"We base our transparent flat-rate pricing on your home's total square footage, number of bedrooms and bathrooms, and selected service tier (standard maintenance, intensive deep clean, or move turnover) with zero hidden travel fees."
            }
        ]
    elif reg == "college_metro":
        return [
            {
                "q": f"Do you provide move-out cleaning with security deposit guarantees for student housing and rentals in {city}, AL?",
                "a": f"Yes! Our {city} move-out cleaning service strictly follows landlord and property manager turnover checklists—scrubbing inside refrigerators, ovens, kitchen cabinets, deep-sanitizing bathrooms, and wiping baseboards to help guarantee full deposit refunds."
            },
            {
                "q": f"What residential housekeeping services do you offer permanent {city} homeowners and faculty?",
                "a": f"We offer weekly, bi-weekly, and monthly recurring maid services, deep restorative cleans, post-renovation cleanup, and custom housekeeping tailored to busy faculty, professionals, and families in {city}."
            },
            {
                "q": f"Do you require locked-in annual or semester contracts in {city}?",
                "a": f"No! All cleaning services in {city} are 100% No-Contract. Whether you need a one-time semester turnover clean, event cleanup, or routine bi-weekly visits, you have full flexibility to start, pause, or cancel anytime."
            },
            {
                "q": f"Are your cleaners background checked, licensed, and insured in {city}?",
                "a": f"Yes, 100%. Zoiris Cleaning Services carries comprehensive general liability and workers' compensation coverage. Every team member undergoes criminal background verification and hands-on professional cleaning training."
            },
            {
                "q": f"What parts of {city} and surrounding neighborhoods do you cover?",
                "a": f"We cover {prof['neighborhoods']}, including campus-area housing complexes, private student apartments, established residential subdivisions, and local commercial storefronts throughout {city}."
            },
            {
                "q": f"What products and vacuums do your teams bring to {city} cleanings?",
                "a": f"We supply all professional tools, including commercial HEPA filtration vacuum systems, microfiber mop pads, and hospital-grade, pet-safe non-toxic disinfectants that eliminate 99.9% of bacteria without harsh toxic odors."
            },
            {
                "q": f"Are there fees for rescheduling my cleaning service in {city}?",
                "a": f"No. We never charge rescheduling fees. If your exam schedule, move date, or travel plans change, simply notify us in advance and we will reschedule your cleaning date with zero hassle."
            },
            {
                "q": f"How do I get an instant estimate for my {city}, AL apartment or house?",
                "a": f"Call our team directly 24/7 at (251) 220-2515 or submit our simple quote form to receive a fast, customized flat-rate estimate tailored to your space."
            }
        ]
    else: # regional_alabama, river_region, wiregrass
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
                "q": f"What is the difference between a standard clean and a deep clean in {city}?",
                "a": f"A standard clean covers routine maintenance (kitchens degreased, bathrooms disinfected, floors vacuumed and mopped, dusting). A deep clean adds intensive hand-scrubbing of baseboards, door frames, window blinds, ceiling fan blades, inside microwaves, and heavy lime/scale removal."
            },
            {
                "q": f"Can I reschedule my cleaning appointment in {city} without penalty?",
                "a": f"Yes! There are zero rescheduling fees. Simply let us know in advance, and our scheduling team will happily work with you to move your cleaning date without any penalty."
            },
            {
                "q": f"How do I receive a fast, free estimate for my home or business in {city}, AL?",
                "a": f"Call our friendly team 24/7 at (251) 220-2515 or submit a quick request on our website to receive an instant, customized flat-rate quote."
            }
        ]

def get_localized_about_html(city, loc_slug, county):
    prof = get_city_profile(city, loc_slug, county)
    
    return f"""
    <!-- About Section – {city} & {county} Cleaning Authority -->
    <section class="px-6 py-20 bg-transparent relative z-10" id="about">
      <div class="max-w-6xl mx-auto">
        
        <div class="text-center max-w-3xl mx-auto mb-12">
          <span class="text-sm font-bold uppercase tracking-wider text-blue-100 bg-white/10 backdrop-blur-md border border-white/20 px-4 py-1.5 rounded-full">
            ✦ {city}, AL Local Cleaning Authority ✦
          </span>
          <h2 class="text-3xl md:text-4xl font-extrabold text-white mt-4 sm:text-4xl">
            Why {city} &amp; {county} Homeowners Choose Zoiris
          </h2>
          <div class="mt-3 h-1 w-20 bg-blue-400 mx-auto rounded"></div>
          <p class="mt-4 text-purple-100 text-base md:text-lg leading-relaxed">
            At <strong>Zoiris Cleaning Services</strong>, we believe <em>little things make the difference</em>. Whether you need ongoing weekly maid service, a thorough seasonal deep clean, or an immaculate move-out turnover, we deliver reliable, personalized care with <strong>zero locked-in contracts</strong> and complete peace of mind across {city} and surrounding Alabama communities.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-12 items-center mb-16">
          <!-- About Image & Highlights -->
          <div class="relative">
            <img alt="Professional eco-friendly cleaning in {city} Alabama by Zoiris team"
              class="rounded-2xl shadow-2xl w-full h-auto object-cover border-4 border-white/20" src="/images/services_action.png" />
            <div class="absolute -bottom-6 -right-4 sm:right-6 bg-white p-4 rounded-xl shadow-xl border border-gray-100 max-w-xs hidden sm:block">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold text-lg">
                  <i class="fas fa-award"></i>
                </div>
                <div>
                  <h4 class="font-bold text-gray-900 text-sm">100% Guaranteed</h4>
                  <p class="text-xs text-gray-600">Spotless results or we re-clean for free</p>
                </div>
              </div>
            </div>
          </div>

          <!-- About Content -->
          <div>
            <h3 class="text-2xl md:text-3xl font-bold text-white mb-4">{prof['environment_headline']}</h3>
            <p class="text-purple-100 text-base md:text-lg mb-4 leading-relaxed">
              {prof['about_focus']}
            </p>
            <p class="text-purple-100 text-base md:text-lg mb-6 leading-relaxed">
              We service {prof['property_types']} across {prof['neighborhoods']}. We never use unvetted subcontractors—every member of our team is an in-house employee, thoroughly background checked, drug screened, and rigorously trained in room-by-room sanitation routines and HEPA vacuum standards.
            </p>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div class="flex items-start bg-white/95 rounded-xl shadow-lg p-4 border border-white/20">
                <div class="flex-shrink-0 bg-blue-100 rounded-lg p-2.5 text-blue-600 mr-3">
                  <i class="fas fa-handshake text-xl"></i>
                </div>
                <div>
                  <h4 class="font-bold text-gray-900 text-sm">No Contracts</h4>
                  <p class="text-xs text-gray-600 mt-0.5">Freedom to start, pause, or adjust anytime.</p>
                </div>
              </div>

              <div class="flex items-start bg-white/95 rounded-xl shadow-lg p-4 border border-white/20">
                <div class="flex-shrink-0 bg-green-100 rounded-lg p-2.5 text-green-600 mr-3">
                  <i class="fas fa-shield-alt text-xl"></i>
                </div>
                <div>
                  <h4 class="font-bold text-gray-900 text-sm">Bonded &amp; Insured</h4>
                  <p class="text-xs text-gray-600 mt-0.5">Full liability &amp; workers' compensation protection.</p>
                </div>
              </div>

              <div class="flex items-start bg-white/95 rounded-xl shadow-lg p-4 border border-white/20">
                <div class="flex-shrink-0 bg-purple-100 rounded-lg p-2.5 text-purple-600 mr-3">
                  <i class="fas fa-users-cog text-xl"></i>
                </div>
                <div>
                  <h4 class="font-bold text-gray-900 text-sm">Vetted Employees</h4>
                  <p class="text-xs text-gray-600 mt-0.5">Background checked, uniform, trained teams of 2+.</p>
                </div>
              </div>

              <div class="flex items-start bg-white/95 rounded-xl shadow-lg p-4 border border-white/20">
                <div class="flex-shrink-0 bg-amber-100 rounded-lg p-2.5 text-amber-600 mr-3">
                  <i class="fas fa-leaf text-xl"></i>
                </div>
                <div>
                  <h4 class="font-bold text-gray-900 text-sm">Eco &amp; Pet-Safe</h4>
                  <p class="text-xs text-gray-600 mt-0.5">Non-toxic supplies safe for your kids &amp; pets.</p>
                </div>
              </div>
            </div>

          </div>
        </div>

        <!-- 3 Core Advantages Grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="bg-white/95 p-6 rounded-2xl shadow-xl border border-white/20 hover:scale-[1.02] transition-transform">
            <div class="w-12 h-12 rounded-xl bg-blue-100 text-blue-600 flex items-center justify-center text-2xl mb-4">
              <i class="fas fa-sliders-h"></i>
            </div>
            <h4 class="text-lg font-bold text-gray-900 mb-2">Tailored for {city} Properties</h4>
            <p class="text-sm text-gray-700 leading-relaxed">
              Every home is unique. We build a personalized cleaning checklist matching your specific floor types, room priorities, and lifestyle in {city} without exceeding your budget.
            </p>
          </div>

          <div class="bg-white/95 p-6 rounded-2xl shadow-xl border border-white/20 hover:scale-[1.02] transition-transform">
            <div class="w-12 h-12 rounded-xl bg-purple-100 text-purple-600 flex items-center justify-center text-2xl mb-4">
              <i class="fas fa-tools"></i>
            </div>
            <h4 class="text-lg font-bold text-gray-900 mb-2">Commercial-Grade Equipment</h4>
            <p class="text-sm text-gray-700 leading-relaxed">
              We equip our cleaners with high-performance HEPA vacuum filtration for thorough allergen and particulate extraction, plus dedicated microfiber systems for hardwood.
            </p>
          </div>

          <div class="bg-white/95 p-6 rounded-2xl shadow-xl border border-white/20 hover:scale-[1.02] transition-transform">
            <div class="w-12 h-12 rounded-xl bg-green-100 text-green-600 flex items-center justify-center text-2xl mb-4">
              <i class="fas fa-history"></i>
            </div>
            <h4 class="text-lg font-bold text-gray-900 mb-2">Zero Rescheduling Fees</h4>
            <p class="text-sm text-gray-700 leading-relaxed">
              Life happens. If unexpected plans or travel arise in {city}, simply notify us in advance. We will happily reschedule your cleaning with zero hassle or penalty fees.
            </p>
          </div>
        </div>

      </div>
    </section>
"""

def get_localized_faq_html(city, loc_slug, county):
    faqs = generate_location_faqs(city, loc_slug, county)
    
    faq_items_html = ""
    icon_list = [
        "fas fa-file-signature",
        "fas fa-calendar-alt",
        "fas fa-shield-alt",
        "fas fa-calculator",
        "fas fa-spray-can",
        "fas fa-layer-group",
        "fas fa-map-marked-alt",
        "fas fa-award"
    ]
    
    for i, item in enumerate(faqs):
        icon = icon_list[i % len(icon_list)]
        faq_items_html += f"""
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
            ✦ Got Questions? We Have Answers ✦
          </span>
          <h2 class="text-3xl md:text-4xl font-extrabold text-white mt-4 tracking-tight">
            Frequently Asked Questions About {city} AL Cleaning Services
          </h2>
          <div class="mt-3 h-1 w-24 bg-gradient-to-r from-blue-400 to-indigo-400 mx-auto rounded"></div>
          <p class="mt-4 text-purple-100 text-base md:text-lg leading-relaxed">
            Everything you need to know about our cleaning standards, flexible scheduling, pricing, and safety protections in {city} and surrounding Alabama areas.
          </p>
        </div>

        <!-- Accordion Items -->
        <div class="space-y-4">
{faq_items_html}
        </div>

        <!-- FAQ CTA -->
        <div class="mt-12 text-center bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl p-6 sm:p-8 text-white shadow-xl">
          <h3 class="text-xl sm:text-2xl font-bold mb-2">Have a specific question about your home or office in {city}?</h3>
          <p class="text-blue-100 text-sm sm:text-base mb-6 max-w-xl mx-auto">
            Our friendly local team is available 24/7 to help structure the perfect cleaning plan for your space.
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

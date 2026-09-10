import os
import json
import re
import sys

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from localized_faq_generator import get_city_profile, LOCAL_INTEL

try:
    with open(os.path.join(root_dir, 'seo', 'services.json'), 'r', encoding='utf-8') as f:
        SERVICES = json.load(f)
except Exception:
    SERVICES = {}

def get_service_meta(service_slug):
    srv = SERVICES.get(service_slug, {})
    name = srv.get("name", service_slug.replace('-', ' ').title())
    category = srv.get("category", "residential")
    return name, category, srv

def generate_bespoke_service_faqs(city, loc_slug, county, service_slug):
    """Generates 8 completely unique, localized FAQs specifically for this service and city."""
    prof = get_city_profile(city, loc_slug, county)
    key = loc_slug.lower().strip().replace('-', '_')
    srv_name, category, srv_data = get_service_meta(service_slug)
    srv_lower = srv_name.lower()
    
    if key == "daphne_al":
        if "deep" in service_slug:
            return [
                {
                    "q": "How does your Daphne deep clean protect custom hardwoods in Lake Forest and Sehoy?",
                    "a": "Daphne homes often feature heart pine or custom oak floors vulnerable to moisture and abrasive dirt. Our deep clean uses Bona-certified, pH-neutral solutions and soft microfiber damp pads to scrub baseboards and floors without clouding delicate sealants."
                },
                {
                    "q": "What steps remove Eastern Shore live oak pollen during a Daphne deep cleaning?",
                    "a": "Spring oak pollen clings to window tracks, intake registers, and ceiling fans across Daphne. We hand-wipe all horizontal trim, wet-clean window frames, and deploy multi-stage HEPA vacuums trapping 99.97% of airborne spores."
                },
                {
                    "q": "How does deep cleaning differ from routine maid visits in Daphne, AL?",
                    "a": "Routine visits maintain daily hygiene (counters, showers, floors). A deep clean is an intensive scrub covering hand-washed baseboards, interior microwave detailing, descaling stubborn grout scale, and degreasing range hoods."
                },
                {
                    "q": "Can I reschedule my Daphne deep clean if my work or family plans change?",
                    "a": "Yes, always. We never charge rescheduling penalties. If your family routine shifts in Daphne, notify us in advance and we will move your appointment seamlessly."
                },
                {
                    "q": "Are your cleaning technicians in-house employees or third-party contractors?",
                    "a": "Every cleaner is a direct, in-house W-2 employee who has undergone multi-state background screening, drug testing, and rigorous hands-on surface-care training."
                },
                {
                    "q": "How do you calculate deep cleaning quotes for residences in Daphne, AL?",
                    "a": "Estimates reflect total square footage, bathroom/bedroom count, and specific home condition. We give upfront flat-rate rates with zero travel surcharges."
                },
                {
                    "q": "Which neighborhoods across Daphne and Baldwin County do your teams service?",
                    "a": "We service Lake Forest, Sehoy, Austin Park, Diamante, Historic Old Daphne, Scenic 98 bluffs, and nearby Eastern Shore residential communities."
                },
                {
                    "q": "How do I secure an appointment for deep cleaning in Daphne, AL?",
                    "a": "Call our local dispatch desk 24/7 at (251) 220-2515 or submit our online form to select your preferred date and receive an instant estimate."
                }
            ]
        elif "move" in service_slug:
            return [
                {
                    "q": "What tasks are completed during a Daphne move-out cleaning service?",
                    "a": "Our move-out checklist satisfies Alabama property management inspection standards: wiping interior/exterior cabinets, deep-degreasing ovens and refrigerators, washing baseboards, and sanitizing all flooring."
                },
                {
                    "q": "Does your move-out service help secure 100% deposit return in Daphne?",
                    "a": "Yes! Our thorough empty-property turnover protocol leaves rentals and apartments turnkey ready for landlord walkthroughs."
                },
                {
                    "q": "When is the optimal time to schedule my Daphne move clean?",
                    "a": "Schedule your clean once all moving boxes and furniture are cleared out, allowing our crew unobstructed access to closets, baseboards, and cabinet interiors."
                },
                {
                    "q": "Do you enforce binding contracts for move-related cleanings in Daphne?",
                    "a": "Never. All move-in and move-out appointments are provided on a one-time flat-rate basis with zero contract obligations."
                },
                {
                    "q": "Are your move turnover cleaners fully insured and bonded in Daphne, AL?",
                    "a": "Yes, 100%. We carry general liability coverage and workers' compensation, protecting your property throughout the turnover process."
                },
                {
                    "q": "Do your teams bring all required vacuum systems and cleaning agents?",
                    "a": "Yes. We arrive fully equipped with commercial-grade HEPA filtration vacuums, microfiber mop kits, extension dusters, and eco-safe disinfectants."
                },
                {
                    "q": "What is the typical duration of a move-out clean in Daphne, AL?",
                    "a": "Most empty home move cleans take between 3 to 5 hours depending on square footage, executed by our dedicated multi-cleaner crew."
                },
                {
                    "q": "How can I request an instant estimate for move cleaning in Daphne?",
                    "a": "Contact our dispatch team 24/7 at (251) 220-2515 or request an estimate online for rapid flat-rate pricing."
                }
            ]
    elif key == "fairhope_al":
        if "deep" in service_slug:
            return [
                {
                    "q": "How do your technicians preserve antique millwork and heart-pine in Fairhope cottages?",
                    "a": "Historic craftsman cottages across Fairhope's Fruit & Nut District require non-abrasive care. We apply specialized pH-balanced cleaners and plush microfiber cloths to lift grime without compromising vintage wood wax or natural patinas."
                },
                {
                    "q": "Are your Fairhope deep cleaning products safe for pets and children?",
                    "a": "Yes, 100%. We strictly apply EPA-registered, hospital-grade non-toxic disinfectants that eliminate 99.9% of bacteria without volatile organic compounds (VOCs) or synthetic scents."
                },
                {
                    "q": "What specialized architectural details are scrubbed during a Fairhope deep clean?",
                    "a": "We hand-wash high transoms, vintage fireplace mantels, French door lites, deep window sills, and descale natural marble in luxury bathrooms."
                },
                {
                    "q": "Can Fairhope homeowners transition to routine maid visits after a deep clean?",
                    "a": "Yes! Many clients begin with an intensive restorative clean and transition into weekly or bi-weekly housekeeping with total scheduling freedom."
                },
                {
                    "q": "What is your policy on rescheduling cleaning dates in Fairhope, AL?",
                    "a": "Zero fees. Simply contact our scheduling team in advance and we will adjust your service date to match your calendar."
                },
                {
                    "q": "Are your cleaners direct employees covered by workers' compensation?",
                    "a": "Yes. 100% of our staff are vetted W-2 employees who undergo extensive background checks, drug screenings, and fine-surface training."
                },
                {
                    "q": "Which Fairhope neighborhoods are included in your service territory?",
                    "a": "We service Fruit & Nut District cottages, Point Clear bayfront estates, Rock Creek golf villas, Lakewood, and Downtown Fairhope properties."
                },
                {
                    "q": "How do I book a restorative deep clean in Fairhope, AL?",
                    "a": "Call us 24/7 at (251) 220-2515 or submit an online request for a personalized, transparent flat-rate estimate."
                }
            ]
    elif key == "gulf_shores_al":
        if "deep" in service_slug or "airbnb" in service_slug or "vacation" in service_slug:
            return [
                {
                    "q": "How do you extract deep-set silica beach sand from Gulf Shores vacation rentals?",
                    "a": "Coastal sand embeds deep beneath carpet backing and into tile grout lines. We utilize motorized commercial HEPA vacuums with high-frequency brush agitators to lift sand grains without scratching flooring surfaces."
                },
                {
                    "q": "Can your team meet strict 10:00 AM to 3:00 PM turnover windows in Gulf Shores?",
                    "a": "Yes! Our vacation turnover teams specialize in same-day checkout-to-checkin turnarounds along West Beach and Fort Morgan, completing linen laundering, sanitization, and staging on schedule."
                },
                {
                    "q": "Do you provide photo inspection reports after Gulf Shores cleanings?",
                    "a": "Yes. Upon request, cleaners document completed rooms, sparkling bathrooms, and staged amenities via digital inspection photos for property managers."
                },
                {
                    "q": "Are your cleaners cleared to enter beachfront high-rise condo towers in Gulf Shores?",
                    "a": "Yes, 100%. We are insured, bonded, and trained on complex lockbox systems, security keycards, and HOA turnover protocols across Phoenix and Crystal Tower."
                },
                {
                    "q": "How do your solutions combat salt-air film on sliding glass doors in Gulf Shores?",
                    "a": "We use anti-static glass descaling agents that break down sticky marine salt mist on balcony sliders and railings, leaving streak-free clarity."
                },
                {
                    "q": "What essential guest amenities can your turnover crew restock in Gulf Shores?",
                    "a": "Our staff restocks hand soaps, shampoo bottles, toilet tissue, paper towels, and trash bags according to your host checklist."
                },
                {
                    "q": "What happens if an arriving guest notes a cleaning issue in Gulf Shores?",
                    "a": "Our 100% Re-Clean Guarantee applies immediately: contact us within 24 hours and a crew will promptly return to re-clean the reported area at zero charge."
                },
                {
                    "q": "How do I receive a turnover cleaning quote in Gulf Shores, AL?",
                    "a": "Call our coastal dispatch line 24/7 at (251) 220-2515 or submit your property details online for flat-rate per-turn pricing."
                }
            ]
    elif key == "mobile_al":
        return [
            {
                "q": "How do your teams reach 12-foot ceilings and crown molding in historic Mobile homes?",
                "a": "Midtown and Oakleigh residences feature towering ceilings, picture rails, and historic transoms. We deploy telescoping micro-dusters and HEPA vacuum wands to clear dust without touching vintage plaster."
            },
            {
                "q": "How do your cleaning protocols address Mobile's sub-tropical humidity and mildew risks?",
                "a": "With high regional rainfall across Mobile County, bathroom grout lines and shaded entries require antimicrobial care. We apply EPA-registered surface treatments that eliminate mold and mildew spores."
            },
            {
                "q": "What recurring housekeeping plans are available in Spring Hill and West Mobile?",
                "a": "We offer weekly, bi-weekly, and monthly maid visits with zero binding contracts, ideal for busy medical professionals, executives, and families."
            },
            {
                "q": "Do you provide deposit-guaranteed move-out sanitization in Mobile, AL?",
                "a": "Yes! Our move-out service includes interior oven/refrigerator detailing, cabinet wipeouts, and full floor disinfection to satisfy landlord checklists."
            },
            {
                "q": "Are your cleaners licensed, bonded, and background-verified in Mobile?",
                "a": "Yes, 100%. Zoiris Cleaning Services carries general liability and workers' compensation coverage for all in-house employees."
            },
            {
                "q": "What commercial office janitorial services do you offer in Downtown Mobile?",
                "a": "We provide after-hours janitorial for law offices, medical clinics, and corporate suites along Dauphin Street and Airport Blvd."
            },
            {
                "q": "Can I add inside appliance scrubbing to my Mobile cleaning visit?",
                "a": "Yes! Oven interior degreasing, refrigerator sanitizing, and cabinet interior wipeouts are available add-ons."
            },
            {
                "q": "What is your satisfaction guarantee policy in Mobile, AL?",
                "a": "We back every service with our 100% Re-Clean Guarantee. Notify us within 24 hours if any area does not meet expectations, and we will return to re-clean it for free."
            }
        ]

    # Dynamic fallback for all other AL markets
    return [
        {
            "q": f"What is included in {srv_lower} in {city}, AL?",
            "a": f"Our {srv_lower} in {city} is customized for your property layout, floor types, and local environmental conditions. Our vetted 2+ person teams work through a detailed checklist with commercial HEPA vacuums."
        },
        {
            "q": f"Do I need to sign a contract for {srv_lower} in {city}?",
            "a": f"No! All {srv_lower} services in {city} are 100% No-Contract. You can schedule one-time visits or recurring maintenance with total freedom."
        },
        {
            "q": f"Are your cleaning professionals insured and bonded in {city}?",
            "a": f"Yes, 100%. Zoiris Cleaning Services carries full general liability insurance and workers' compensation coverage for all staff."
        },
        {
            "q": f"What equipment do your cleaners bring to {city} properties?",
            "a": f"Our crews bring commercial-grade HEPA filtration vacuum systems, microfiber mop kits, extension dusters, and hospital-grade eco-friendly disinfectants."
        },
        {
            "q": f"How long does a standard {srv_lower} visit take in {city}?",
            "a": f"Depending on total square footage and room layout, an appointment takes between 2 to 4.5 hours with our multi-cleaner crew."
        },
        {
            "q": f"What neighborhoods in {city} and {county} do you cover?",
            "a": f"We cover {prof['neighborhoods']}, servicing single-family residences, townhomes, and local commercial properties throughout {city}."
        },
        {
            "q": f"Are there penalty fees if I reschedule my {srv_lower} in {city}?",
            "a": f"No. We never charge rescheduling fees. Simply let our team know in advance and we will move your appointment date."
        },
        {
            "q": f"What is your 100% Satisfaction Guarantee policy in {city}, AL?",
            "a": f"If any area does not meet your expectations, contact us within 24 hours at (251) 220-2515 and our crew will return to re-clean it for free."
        }
    ]

def get_bespoke_location_service_html(city, loc_slug, county, service_slug):
    """Builds a rich, completely unique landing page for a specific location-service combination."""
    prof = get_city_profile(city, loc_slug, county)
    srv_name, category, srv_data = get_service_meta(service_slug)
    srv_lower = srv_name.lower()
    key = loc_slug.lower().strip().replace('-', '_')
    
    # Granular city narratives, trust pillars, and advantages
    if key == "daphne_al":
        service_focus_headline = f"Dedicated {srv_name} for Daphne Homes & Estates"
        service_intro_p1 = f"In Daphne, properties ranging from Lake Forest golf enclaves to custom homes in Sehoy face distinct environmental challenges—including seasonal live oak pollen, red clay entryway tracking, and coastal Mobile Bay moisture. Our specialized {srv_lower} is engineered specifically to protect your interior air quality and delicate hardwood finishes."
        service_intro_p2 = f"Our uniformed in-house crews utilize manufacturer-approved pH-neutral floor care (following Bona standards) and commercial HEPA filtration to eliminate embedded dirt, sanitize high-touch fixtures, and restore your space to immaculate standards."
        pillar_1_title, pillar_1_desc = "Eastern Shore Family Care", "Systematic top-to-bottom scrub designed for active suburban commuter households."
        pillar_2_title, pillar_2_desc = "Bona Floor Protocol", "Manufacturer-approved pH-neutral solutions protecting custom oak and heart pine."
        pillar_3_title, pillar_3_desc = "In-House Uniformed Crews", "Background-checked W-2 employees trained in fine property protection."
        pillar_4_title, pillar_4_desc = "Total Booking Freedom", "Start, pause, or adjust service dates anytime with zero contracts or penalties."
        adv_1_title, adv_1_desc = "Lake Forest & Sehoy Priority", "Customized checklists adapted for Eastern Shore suburban floor plans, high-traffic mudrooms, and family lifestyles."
        adv_2_title, adv_2_desc = "Live Oak Pollen Extraction", "Multi-stage HEPA filtration traps 99.97% of fine pollen particles, protecting indoor air during heavy spring blooms."
        adv_3_title, adv_3_desc = "Commuter Schedule Flexibility", "Convenient scheduling with zero lock-in contracts and no fees for date adjustments for busy commuters."
    elif key == "fairhope_al":
        service_focus_headline = f"White-Glove {srv_name} in Fairhope & Point Clear"
        service_intro_p1 = f"Fairhope's architectural charm—from 1920s craftsman cottages in the Fruit & Nut District to sprawling bayfront estates in Point Clear—demands a delicate, preservation-minded approach. Standard abrasive methods risk damaging historic heart pine, custom millwork, and antique heirlooms."
        service_intro_p2 = f"Zoiris Cleaning Services delivers discreet, meticulous {srv_lower} using hospital-grade, eco-friendly, and non-toxic formulas. Every surface is cleaned by background-checked, trained professionals who respect the historic integrity of your home."
        pillar_1_title, pillar_1_desc = "Fine Millwork & Transom Detailing", "Gentle non-abrasive hand-washing of vintage trim, French doors, and transoms."
        pillar_2_title, pillar_2_desc = "Hospital-Grade Eco Disinfection", "100% pet-safe non-toxic disinfectants free from synthetic fragrances or harsh fumes."
        pillar_3_title, pillar_3_desc = "Discreet White-Glove Staff", "Vetted in-house professionals dedicated to quiet, meticulous estate care."
        pillar_4_title, pillar_4_desc = "Bespoke Room Focus", "Tailored cleaning priorities structured around your historic home's layout."
        adv_1_title, adv_1_desc = "Heart Pine & Antique Safe", "Gentle, non-abrasive techniques tailored specifically for original heart pine, antique trim, and luxury natural marble."
        adv_2_title, adv_2_desc = "Hospital-Grade Eco Purity", "100% non-toxic, pet-safe, and fragrance-free disinfectants ensuring exceptional indoor air purity."
        adv_3_title, adv_3_desc = "Point Clear & Downtown Detail", "Meticulous surface polishing for bayfront verandas, French doors, and boutique studio spaces."
    elif key == "gulf_shores_al":
        service_focus_headline = f"Coastal {srv_name} for Gulf Shores Condos & Beach Homes"
        service_intro_p1 = f"Living or hosting guests on the Gulf Coast means battling constant silica sand tracking, sticky salt-spray air, and extreme summer humidity. Standard house cleaning methods simply push sand deeper into carpet backing and leave smears on balcony glass."
        service_intro_p2 = f"Our Gulf Shores {srv_lower} uses motorized HEPA sand extraction vacuums, anti-static glass descaling treatments, and antimicrobial sanitizers that prevent coastal mildew, ensuring your beachfront property remains 5-star guest ready."
        pillar_1_title, pillar_1_desc = "Silica Sand Extraction", "Motorized agitation lifting coarse beach sand from carpets, rugs, and tile grout."
        pillar_2_title, pillar_2_desc = "Salt-Film Dissolving Care", "Anti-static glass solutions removing stubborn salt mist from balcony sliders."
        pillar_3_title, pillar_3_desc = "10am-3pm Turnover Blitz", "Turnkey checkout-to-checkin speed for West Beach and Fort Morgan hosts."
        pillar_4_title, pillar_4_desc = "Photo Proof Verification", "Digital staging inspections provided for remote owners and rental managers."
        adv_1_title, adv_1_desc = "Deep Sand Purge Protocol", "Commercial-grade HEPA vacuuming with specialized agitators to lift embedded sand from carpets, rugs, and tile grout."
        adv_2_title, adv_2_desc = "Salt-Mist Glass & Fixture Care", "Dissolves stubborn coastal salt haze on sliding glass doors, balcony railings, and exterior light fixtures."
        adv_3_title, adv_3_desc = "Condo HOA & Keybox Trained", "Experienced with security lockboxes, keycards, and beachfront HOA protocols across Phoenix and Crystal Tower."
    elif key == "mobile_al":
        service_focus_headline = f"Professional {srv_name} in Mobile, AL & Historic Districts"
        service_intro_p1 = f"Mobile's distinct architectural heritage—from Midtown Victorian cottages with 12-foot ceilings to executive homes in Spring Hill—requires specialized cleaning protocols. Mobile's high sub-tropical humidity creates unique allergen and moisture challenges."
        service_intro_p2 = f"Our professional crews utilize telescoping HEPA extension dusters, commercial grout scrubbers, and hospital-grade surface sanitizers to deliver thorough, hygienic results backed by our 100% Re-Clean Guarantee."
        pillar_1_title, pillar_1_desc = "12-Ft Ceiling Telescoping", "Extended HEPA reach for historic Midtown crown molding and ceiling fans."
        pillar_2_title, pillar_2_desc = "Gulf Moisture Defense", "Antimicrobial sanitizers targeting bathroom tile grout and shaded doorways."
        pillar_3_title, pillar_3_desc = "Spring Hill Executive Care", "Structured multi-cleaner routines for expansive suburban family residences."
        pillar_4_title, pillar_4_desc = "Shift & Executive Flexibility", "Convenient scheduling designed around Mobile healthcare and professional shifts."
        adv_1_title, adv_1_desc = "Historic Detail & Transom Dusting", "Specialized telescoping dusters reach 12+ foot ceilings, crown moldings, ceiling fans, and vintage light fixtures safely."
        adv_2_title, adv_2_desc = "Sub-Tropical Mold/Mildew Control", "Antimicrobial surface treatments that eliminate mildew spores in tile bathrooms and shaded exterior entries."
        adv_3_title, adv_3_desc = "Healthcare & Executive Scheduling", "Flexible scheduling for busy healthcare workers, historic homeowners, and suburban families with zero locked contracts."
    elif key == "spanish_fort_al":
        service_focus_headline = f"Executive {srv_name} in Spanish Fort & TimberCreek"
        service_intro_p1 = f"Surrounded by the Mobile-Tensaw Delta and pine canopies, Spanish Fort homes in TimberCreek, Rayne Plantation, and Stonebridge face heavy pine pollen and wetland moisture. Large multi-level floor plans demand structured, coordinated cleaning teams."
        service_intro_p2 = f"Zoiris Cleaning Services sends multi-cleaner teams equipped with commercial HEPA systems to detail two-story foyers, open-concept kitchens, and expansive living areas with unmatched efficiency."
        pillar_1_title, pillar_1_desc = "Two-Story Foyer Detailing", "Equipped for high staircases, banisters, and grand entryway fixtures."
        pillar_2_title, pillar_2_desc = "Delta Humidity Mitigation", "Moisture-neutralizing hard floor cleaners preventing damp odors."
        pillar_3_title, pillar_3_desc = "Multi-Cleaner Team Power", "Coordinated in-house teams ensuring large square footages are finished fast."
        pillar_4_title, pillar_4_desc = "I-10 Commuter Convenience", "Zero reschedule penalties and seamless digital booking for busy commuters."
        adv_1_title, adv_1_desc = "TimberCreek Multi-Story Focus", "Structured multi-cleaner teams equipped to handle high-staircase dusting, banisters, and high-ceiling fans."
        adv_2_title, adv_2_desc = "Delta Humidity & Pine Defense", "Moisture-safe cleaning products and HEPA filtration protecting indoor air from delta dampness and pine dust."
        adv_3_title, adv_3_desc = "Relocation & Deposit Readiness", "Fast, deposit-guaranteed move turnovers and flexible recurring schedules with zero lock-in terms."
    else:
        service_focus_headline = f"Professional {srv_name} in {city}, AL"
        service_intro_p1 = f"Keeping your property in {city} pristine, healthy, and welcoming is seamless with Zoiris Cleaning Services. We offer tailored {srv_lower} solutions structured specifically for {prof['neighborhoods']} with zero locked contracts."
        service_intro_p2 = f"Our in-house, background-checked cleaning professionals use commercial HEPA filtration equipment and hospital-grade eco-friendly disinfectants to deliver consistent, spotless results backed by our 100% Satisfaction Guarantee."
        pillar_1_title, pillar_1_desc = "Zero Locked Contracts", "Total freedom to schedule weekly, bi-weekly, or one-time cleanings on demand."
        pillar_2_title, pillar_2_desc = "No Reschedule Penalties", f"Flexible bookings designed around your calendar in {city}."
        pillar_3_title, pillar_3_desc = "Bonded & Insured In-House Staff", "Comprehensive liability and workers' compensation protection on every appointment."
        pillar_4_title, pillar_4_desc = "Eco-Safe Sanitation", "EPA-registered non-toxic disinfectants safe for kids and household pets."
        adv_1_title, adv_1_desc = f"Tailored for {city} Properties", f"Custom checklists structured specifically for your square footage, room count, and flooring materials in {city}."
        adv_2_title, adv_2_desc = "Commercial HEPA Systems", "High-efficiency vacuums capturing 99.97% of fine dust and allergens down to 0.3 microns, protecting indoor air."
        adv_3_title, adv_3_desc = "Transparent Upfront Pricing", f"Clear, flat-rate pricing with zero surprise travel surcharges across {county}."

    # Build unique FAQs
    faqs = generate_bespoke_service_faqs(city, loc_slug, county, service_slug)
    faq_items_html = ""
    icon_list = [
        "fas fa-file-signature", "fas fa-calendar-alt", "fas fa-shield-alt", "fas fa-calculator",
        "fas fa-spray-can", "fas fa-layer-group", "fas fa-map-marked-alt", "fas fa-award"
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
    <!-- 🌟 SECTION: SERVICE OVERVIEW & LOCAL AUTHORITY -->
    <section class="px-6 py-20 bg-transparent relative z-10" id="service-overview">
      <div class="max-w-6xl mx-auto">
        
        <div class="text-center max-w-3xl mx-auto mb-12">
          <span class="text-sm font-bold uppercase tracking-wider text-blue-100 bg-white/10 backdrop-blur-md border border-white/20 px-4 py-1.5 rounded-full">
            ✦ {city}, AL {srv_name} Authority ✦
          </span>
          <h2 class="text-3xl md:text-4xl font-extrabold text-white mt-4 sm:text-4xl">
            {service_focus_headline}
          </h2>
          <div class="mt-3 h-1 w-20 bg-blue-400 mx-auto rounded"></div>
          <p class="mt-4 text-purple-100 text-base md:text-lg leading-relaxed">
            {service_intro_p1}
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-12 items-center mb-16">
          <!-- Service Action Image & Badge -->
          <div class="relative">
            <img alt="Professional {srv_lower} in {city} AL by Zoiris Cleaning Services team"
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

          <!-- Service Content Column -->
          <div>
            <h3 class="text-2xl md:text-3xl font-bold text-white mb-4">{prof['environment_headline']}</h3>
            <p class="text-purple-100 text-base md:text-lg mb-4 leading-relaxed">
              {service_intro_p2}
            </p>
            <p class="text-purple-100 text-base md:text-lg mb-6 leading-relaxed">
              We service {prof['property_types']} throughout {prof['neighborhoods']}. With our dedicated in-house staff, you never have to worry about unvetted subcontractors or binding annual contracts.
            </p>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div class="flex items-start bg-white/95 rounded-xl shadow-lg p-4 border border-white/20">
                <div class="flex-shrink-0 bg-blue-100 rounded-lg p-2.5 text-blue-600 mr-3">
                  <i class="fas fa-handshake text-xl"></i>
                </div>
                <div>
                  <h4 class="font-bold text-gray-900 text-sm">{pillar_1_title}</h4>
                  <p class="text-xs text-gray-600 mt-0.5">{pillar_1_desc}</p>
                </div>
              </div>

              <div class="flex items-start bg-white/95 rounded-xl shadow-lg p-4 border border-white/20">
                <div class="flex-shrink-0 bg-green-100 rounded-lg p-2.5 text-green-600 mr-3">
                  <i class="fas fa-shield-alt text-xl"></i>
                </div>
                <div>
                  <h4 class="font-bold text-gray-900 text-sm">{pillar_2_title}</h4>
                  <p class="text-xs text-gray-600 mt-0.5">{pillar_2_desc}</p>
                </div>
              </div>

              <div class="flex items-start bg-white/95 rounded-xl shadow-lg p-4 border border-white/20">
                <div class="flex-shrink-0 bg-purple-100 rounded-lg p-2.5 text-purple-600 mr-3">
                  <i class="fas fa-users-cog text-xl"></i>
                </div>
                <div>
                  <h4 class="font-bold text-gray-900 text-sm">{pillar_3_title}</h4>
                  <p class="text-xs text-gray-600 mt-0.5">{pillar_3_desc}</p>
                </div>
              </div>

              <div class="flex items-start bg-white/95 rounded-xl shadow-lg p-4 border border-white/20">
                <div class="flex-shrink-0 bg-amber-100 rounded-lg p-2.5 text-amber-600 mr-3">
                  <i class="fas fa-leaf text-xl"></i>
                </div>
                <div>
                  <h4 class="font-bold text-gray-900 text-sm">{pillar_4_title}</h4>
                  <p class="text-xs text-gray-600 mt-0.5">{pillar_4_desc}</p>
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
            <h4 class="text-lg font-bold text-gray-900 mb-2">{adv_1_title}</h4>
            <p class="text-sm text-gray-700 leading-relaxed">
              {adv_1_desc}
            </p>
          </div>

          <div class="bg-white/95 p-6 rounded-2xl shadow-xl border border-white/20 hover:scale-[1.02] transition-transform">
            <div class="w-12 h-12 rounded-xl bg-purple-100 text-purple-600 flex items-center justify-center text-2xl mb-4">
              <i class="fas fa-tools"></i>
            </div>
            <h4 class="text-lg font-bold text-gray-900 mb-2">{adv_2_title}</h4>
            <p class="text-sm text-gray-700 leading-relaxed">
              {adv_2_desc}
            </p>
          </div>

          <div class="bg-white/95 p-6 rounded-2xl shadow-xl border border-white/20 hover:scale-[1.02] transition-transform">
            <div class="w-12 h-12 rounded-xl bg-green-100 text-green-600 flex items-center justify-center text-2xl mb-4">
              <i class="fas fa-history"></i>
            </div>
            <h4 class="text-lg font-bold text-gray-900 mb-2">{adv_3_title}</h4>
            <p class="text-sm text-gray-700 leading-relaxed">
              {adv_3_desc}
            </p>
          </div>
        </div>

      </div>
    </section>

    <!-- ❓ SECTION: FREQUENTLY ASKED QUESTIONS (ACCORDION & RICH SEO) -->
    <section class="py-20 px-4 sm:px-6 lg:px-8 bg-transparent relative z-10" id="faq">
      <div class="max-w-5xl mx-auto">
        
        <div class="text-center max-w-3xl mx-auto mb-14">
          <span class="text-sm font-bold uppercase tracking-wider text-blue-100 bg-white/10 backdrop-blur-md border border-white/20 px-4 py-1.5 rounded-full">
            ✦ Got Questions About {srv_name}? We Have Answers ✦
          </span>
          <h2 class="text-3xl md:text-4xl font-extrabold text-white mt-4 tracking-tight">
            Frequently Asked Questions About {srv_name} in {city}, AL
          </h2>
          <div class="mt-3 h-1 w-24 bg-gradient-to-r from-blue-400 to-indigo-400 mx-auto rounded"></div>
          <p class="mt-4 text-purple-100 text-base md:text-lg leading-relaxed">
            Everything you need to know about our {srv_lower} protocols, transparent pricing, flexible scheduling, and guarantees in {city} and {county}.
          </p>
        </div>

        <!-- Accordion Items -->
        <div class="space-y-4">
{faq_items_html}
        </div>

        <!-- FAQ CTA -->
        <div class="mt-12 text-center bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl p-6 sm:p-8 text-white shadow-xl">
          <h3 class="text-xl sm:text-2xl font-bold mb-2">Ready for a spotless space in {city}?</h3>
          <p class="text-blue-100 text-sm sm:text-base mb-6 max-w-xl mx-auto">
            Our friendly local team is available 24/7 to provide an instant, customized flat-rate estimate.
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

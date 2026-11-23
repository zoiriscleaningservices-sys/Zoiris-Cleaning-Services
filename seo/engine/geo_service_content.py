import os
import json
import html

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with open(os.path.join(root_dir, "seo", "locations.json"), "r", encoding="utf-8") as f:
    LOCATIONS = json.load(f)

with open(os.path.join(root_dir, "seo", "services.json"), "r", encoding="utf-8") as f:
    SERVICES = json.load(f)

with open(os.path.join(root_dir, "seo", "local_intelligence.json"), "r", encoding="utf-8") as f:
    LOCAL_INTEL = json.load(f)

with open(os.path.join(root_dir, "seo", "business.json"), "r", encoding="utf-8") as f:
    BUSINESS = json.load(f)

REGION_PROFILES = {
    "mobile_metro": {
        "label": "Mobile Bay & Gulf Coast Metro",
        "climate": "sub-tropical Gulf rainfall (65+ inches annually), coastal humidity, spring live-oak/azalea pollen blooms, and red-clay/sandy-loam yard tracking",
        "housing": "historic raised cottages, brick suburban family subdivisions, waterfront river homes, and commercial/industrial corridors",
        "care_focus": "antimicrobial bathroom grout protection, high-ceiling HEPA allergen filtration, and moisture-safe hardwood and tile care"
    },
    "eastern_shore": {
        "label": "Baldwin County Eastern Shore",
        "climate": "Mobile Bay jubilee breezes, heavy spring live-oak and pine pollen, red-clay bluff soil, and warm bayfront humidity",
        "housing": "custom golf-community estates, Scenic 98 bayfront residences, Craftsman cottages, and commuter family subdivisions",
        "care_focus": "Bona-standard pH-neutral heart-pine and oak preservation, screened-porch pollen removal, and stone-safe spa bathroom care"
    },
    "coastal_resort": {
        "label": "Alabama Gulf Coast & Pleasure Island",
        "climate": "salt-spray marine air, ultrafine white quartz beach sand, intense UV exposure, and peak summer vacation turnover cycles",
        "housing": "high-rise beachfront condominiums, multi-story stilt beach houses, marina villas, and golf-resort residences",
        "care_focus": "agitated HEPA silica-sand extraction, anti-salt balcony glass descaling, and rapid 10:00 AM–3:00 PM guest turnover staging"
    },
    "baldwin_gulf_coast": {
        "label": "Baldwin County & Gulf Corridor",
        "climate": "warm coastal-plain humidity, agricultural and pine-forest pollen, new-construction subdivision dust, and summer storm runoff",
        "housing": "new-build Craftsman subdivisions, acreage homesteads, retiree golf villas, and Highway 59 / I-10 commercial centers",
        "care_focus": "fine drywall and red-soil dust extraction, mildew-resistant bath sanitization, and streak-free window and floor care"
    },
    "south_coastal_plain": {
        "label": "South Alabama Timber & Coastal Plain",
        "climate": "longleaf-pine pollen seasons, river-bottom humidity, sandy-clay soil tracking, and hot Gulf-influenced summers",
        "housing": "brick ranch residences, historic town-center homes, country acreage properties, and regional commercial storefronts",
        "care_focus": "multi-stage HEPA pollen capture, mudroom and hard-floor deep scrubbing, and hard-water mineral descaling"
    },
    "wiregrass": {
        "label": "Southeast Alabama Wiregrass Region",
        "climate": "fine Wiregrass sandy-loam dust, seasonal pine and agricultural harvest allergens, and warm humid summers",
        "housing": "brick single-family subdivisions, golf-course homes, medical/aviation commuter properties, and circle-corridor businesses",
        "care_focus": "sealed HEPA sand and allergen filtration, window-blind dust removal, and clinical-grade surface disinfection"
    },
    "river_region": {
        "label": "Central Alabama River Region",
        "climate": "Alabama & Tallapoosa River valley humidity, heavy spring oak pollen, red-clay soil, and year-round relocation activity",
        "housing": "historic district bungalows, master-planned suburban brick homes, lakefront retreats, and state/professional offices",
        "care_focus": "inspection-ready move turnovers, fine woodwork and hardwood dusting, and EPA-registered workplace sanitization"
    },
    "east_central": {
        "label": "East-Central Piedmont & Lake Corridor",
        "climate": "Piedmont red clay, dense loblolly-pine pollen, lakefront moisture, and seasonal collegiate/lake house turnovers",
        "housing": "lakefront cottages, university-corridor subdivisions, historic mill-town homes, and research/manufacturing offices",
        "care_focus": "red-clay carpet and grout lifting, lake-home turnover staging, and no-contract recurring family housekeeping"
    },
    "birmingham_metro": {
        "label": "Greater Birmingham & Over-the-Mountain Metro",
        "climate": "Appalachian ridge pine pollen, iron-rich Alabama red clay, valley humidity, and multi-season suburban allergens",
        "housing": "Over-the-Mountain estates, multi-level suburban homes with finished basements, urban lofts, and corporate/medical suites",
        "care_focus": "multi-story team cleaning, red-clay entryway protection, stone/hardwood preservation, and commercial facility care"
    },
    "west_alabama": {
        "label": "West Alabama & Black Warrior Basin",
        "climate": "Black Warrior River humidity, heavy pine and oak pollen, clay soil tracking, and peak academic/industrial move cycles",
        "housing": "single-family brick neighborhoods, waterfront lake properties, student/faculty housing, and industrial corridor facilities",
        "care_focus": "deposit-ready lease turnovers, antimicrobial bath/kitchen sanitation, and heavy-duty commercial floor care"
    },
    "black_belt": {
        "label": "Alabama Black Belt Prairie & River Heartland",
        "climate": "rich dark chalk-clay soil tracking, river-basin humidity, pecan/oak canopy debris, and hot summer seasons",
        "housing": "historic antebellum and Victorian homes, classic brick ranches, rural estates, and county-seat clinics and churches",
        "care_focus": "gentle historic trim and floor care, deep soil extraction at entryways, and dependable flat-rate scheduling"
    },
    "tennessee_valley": {
        "label": "North Alabama & Tennessee River Valley",
        "climate": "Tennessee Valley four-season shifts, limestone hard-water minerals, rapid new-build construction dust, and spring valley allergens",
        "housing": "modern smart-home subdivisions, historic district residences, river/lakefront homes, and tech/aerospace offices",
        "care_focus": "limestone hard-water glass descaling, fine drywall/allergen HEPA extraction, and electronics-safe dusting"
    },
    "north_highlands": {
        "label": "North-Central Cullman & Bankhead Highlands",
        "climate": "plateau breezes, four-season leaf and pine-needle drop, lake humidity, and red-clay foothill soil",
        "housing": "lakefront vacation homes, brick family homesteads, suburban subdivisions, and regional commercial buildings",
        "care_focus": "seasonal deep scrubbing, vacation lake-house turnovers, and mudroom/carpet soil extraction"
    },
    "northeast_highlands": {
        "label": "Northeast Alabama Sand & Lookout Mountain Highlands",
        "climate": "mountain-plateau elevation shifts, winter heating dust, spring hardwood pollen, and river/lake mist",
        "housing": "mountain-view homes, lakefront cottages, established brick neighborhoods, and local medical/retail facilities",
        "care_focus": "four-season allergen removal, hard-water fixture polishing, and streak-free interior/exterior glass care"
    }
}

def get_enriched_profile(loc_slug):
    loc = LOCATIONS.get(loc_slug, {})
    city = loc.get("city", loc_slug[:-3].replace("-", " ").title())
    display_title = loc.get("display_title", f"{city}, AL")
    county = loc.get("county", "Mobile County")
    county_short = loc.get("county_short", "Mobile")
    zips = loc.get("zips", ["36602"])
    primary_zip = loc.get("primary_zip", zips[0])
    sqmi = loc.get("sqmi", 5.0)
    place_type = loc.get("place_type", "City")
    region_key = loc.get("region", "mobile_metro")
    reg = REGION_PROFILES.get(region_key, REGION_PROFILES["mobile_metro"])
    nearby = loc.get("nearby", [])
    nearby_names = ", ".join(f"{n['city']} ({n['miles']} mi)" for n in nearby[:4])
    nearby_cities_plain = ", ".join(n["city"] for n in nearby[:5])

    intel_key = loc_slug.replace("-", "_")
    intel = LOCAL_INTEL.get(intel_key)

    if intel:
        prop_list = intel.get("property_profiles", [])
        prop_str = "; ".join(prop_list[:3]).lower() if prop_list else reg["housing"]
        challenges = intel.get("cleaning_challenges", [])
        chal_str = challenges[0] if challenges else reg["care_focus"]
        return {
            "city": city,
            "display_title": display_title,
            "county": county,
            "county_short": county_short,
            "zips": zips,
            "zips_str": ", ".join(zips),
            "primary_zip": primary_zip,
            "sqmi": sqmi,
            "place_type": place_type,
            "region_label": intel.get("market_name", reg["label"]),
            "climate": intel.get("local_environment", reg["climate"]),
            "neighborhoods": intel.get("neighborhoods", f"neighborhoods throughout {city} and {county}"),
            "landmarks": intel.get("local_landmarks", f"central {city} and surrounding {county} corridors"),
            "housing": prop_str,
            "care_focus": chal_str,
            "nearby": nearby,
            "nearby_names": nearby_names,
            "nearby_cities_plain": nearby_cities_plain,
            "coordinates": loc.get("coordinates", {"latitude": 30.6954, "longitude": -88.0399})
        }

    return {
        "city": city,
        "display_title": display_title,
        "county": county,
        "county_short": county_short,
        "zips": zips,
        "zips_str": ", ".join(zips),
        "primary_zip": primary_zip,
        "sqmi": sqmi,
        "place_type": place_type,
        "region_label": f"{county} • {reg['label']}",
        "climate": reg["climate"],
        "neighborhoods": f"residential streets, country properties, and business corridors across {city} (ZIP {', '.join(zips)}) and nearby {nearby_cities_plain}",
        "landmarks": f"{city} town center (ZIP {primary_zip}), {county} corridors, and neighboring {nearby_names}",
        "housing": reg["housing"],
        "care_focus": reg["care_focus"],
        "nearby": nearby,
        "nearby_names": nearby_names,
        "nearby_cities_plain": nearby_cities_plain,
        "coordinates": loc.get("coordinates", {"latitude": 30.6954, "longitude": -88.0399})
    }

def build_hub_faqs(prof):
    city = prof["city"]
    display = prof["display_title"]
    county = prof["county"]
    zips_str = prof["zips_str"]
    nearby_plain = prof["nearby_cities_plain"]
    return [
        {
            "q": f"What residential and commercial cleaning services do you offer in {display}?",
            "a": f"Zoiris Cleaning Services provides full-spectrum cleaning across {city} ({county}, ZIP {zips_str}), including recurring house cleaning & maid service, intensive top-to-bottom deep cleaning, deposit-ready move-in/move-out turnovers, Airbnb & vacation rental turnovers, commercial office & medical janitorial, carpet & upholstery steam extraction, pure-water window washing, gutter clearing, and soft-wash pressure washing."
        },
        {
            "q": f"How do your {city} cleaning protocols handle local {county} conditions?",
            "a": f"Properties in {city} contend with {prof['climate']}. Our uniformed 2+ person teams use sealed commercial HEPA vacuums (capturing 99.97% of 0.3-micron particulates), color-coded microfiber, and pH-balanced EPA-registered disinfectants focused on {prof['care_focus']}."
        },
        {
            "q": f"Do I have to sign a contract for recurring maid service in {city}, AL?",
            "a": f"Never. Every residential and commercial cleaning plan in {city} is 100% contract-free. You can book weekly, bi-weekly, monthly, or one-time cleanings and pause, adjust, or reschedule with zero penalty fees."
        },
        {
            "q": f"Are there travel fees for {city} (ZIP {prof['primary_zip']}) or nearby {county} towns?",
            "a": f"No. We provide upfront, flat-rate pricing with zero hidden mileage or travel surcharges across all {sqmi_text(prof)} of {city} as well as neighboring {nearby_plain}."
        },
        {
            "q": f"Are your cleaners background-checked employees or gig subcontractors?",
            "a": f"100% of Zoiris technicians are vetted, uniformed W-2 employees—never unscreened gig contractors. We carry full general liability insurance and workers' compensation coverage for complete protection of your {city} home or facility."
        },
        {
            "q": f"Do I need to supply vacuums, mops, or cleaning sprays for my {city} appointment?",
            "a": f"No—our crews arrive fully equipped with commercial HEPA filtration vacuums, sanitized microfiber mop pads, telescoping high-reach dusters, and child- and pet-safe non-toxic cleaning agents."
        },
        {
            "q": f"How does your 24-Hour 100% Re-Clean Guarantee work in {display}?",
            "a": f"If any room or detail does not meet your expectations, simply call or text us at (251) 220-2515 within 24 hours and our team will return promptly to re-clean the area at zero additional cost."
        },
        {
            "q": f"How fast can I get a quote and schedule cleaning in {city}, AL?",
            "a": f"Call our 24/7 dispatch desk at (251) 220-2515 or complete the instant estimate form on this page for a customized flat-rate quote in minutes, with same-week and urgent turnover availability across {county}."
        }
    ]

def sqmi_text(prof):
    return f"{prof['sqmi']} square miles" if prof.get("sqmi") else "neighborhoods"

def county_to_slug(county_short):
    clean = county_short.lower().replace(".", "").replace("'", "").strip().replace(" ", "-")
    if clean == "dekalb":
        clean = "de-kalb"
    elif clean == "st-clair":
        clean = "saint-clair"
    return f"{clean}-county-al"

def build_ai_hub_summary_and_table(prof):
    city = prof["city"]
    display = prof["display_title"]
    county = prof["county"]
    c_slug = county_to_slug(prof["county_short"])
    pzip = prof["primary_zip"]
    coords = prof["coordinates"]
    coord_txt = f"{coords['latitude']:.4f}°N, {abs(coords['longitude']):.4f}°W"
    nearby_txt = prof["nearby_names"] or f"surrounding {county} communities"
    return f"""
        <!-- 🤖 AI OVERVIEW DIRECT ANSWER & PRICING/DURATION MATRIX -->
        <div id="ai-quick-answer" class="bg-white rounded-3xl p-6 sm:p-8 shadow-2xl border-2 border-blue-500/30 mb-14 text-left">
          <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
            <span class="inline-flex items-center gap-2 bg-blue-100 text-blue-800 text-xs font-extrabold uppercase tracking-wider px-3 py-1 rounded-full">
              <i class="fas fa-bolt"></i> Verified Local Dispatch • {html.escape(display)} ({html.escape(pzip)}) • {coord_txt}
            </span>
            <div class="flex flex-wrap gap-3 text-xs font-bold">
              <a href="/services/" class="text-blue-600 hover:underline">All 29 Services &rarr;</a>
              <a href="/counties/{c_slug}/" class="text-indigo-600 hover:underline">{html.escape(county)} Hub &rarr;</a>
              <a href="/guides/house-cleaning-cost-guide-alabama/" class="text-purple-600 hover:underline">2026 Cost Calculator &rarr;</a>
            </div>
          </div>
          <h3 class="text-xl sm:text-2xl font-extrabold text-gray-900 mb-2">
            How Much Does House &amp; Commercial Cleaning Cost in {html.escape(display)}?
          </h3>
          <p class="text-sm sm:text-base text-gray-700 leading-relaxed mb-6">
            Across all {html.escape(sqmi_text(prof))} of <strong>{html.escape(display)} ({html.escape(county)}, ZIP {html.escape(prof['zips_str'])}; adjacent to {html.escape(nearby_txt)})</strong>, professional residential house cleaning ranges from <strong>$125–$215</strong> for recurring maid visits, <strong>$220–$420</strong> for top-to-bottom deep cleaning, and <strong>$250–$480</strong> for empty-home move-in/move-out turnovers—with <strong>zero contracts and zero travel surcharges</strong>. Commercial, medical, and spa/bank janitorial is flat-rate quoted 24/7 at <strong>(251) 220-2515</strong>.
          </p>
          <div class="overflow-x-auto rounded-2xl border border-gray-200">
            <table class="w-full text-left border-collapse text-xs sm:text-sm">
              <thead>
                <tr class="bg-slate-900 text-white">
                  <th class="py-3 px-4 font-bold">Cleaning Service Type ({html.escape(city)}, AL)</th>
                  <th class="py-3 px-4 font-bold">Typical Flat-Rate Range</th>
                  <th class="py-3 px-4 font-bold">2-Crew Duration</th>
                  <th class="py-3 px-4 font-bold">Core Scope Included</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200 text-gray-800 bg-white">
                <tr class="hover:bg-blue-50/50">
                  <td class="py-3 px-4 font-bold">Recurring Maid Service</td>
                  <td class="py-3 px-4 font-semibold text-blue-700">$125 – $215 / visit</td>
                  <td class="py-3 px-4">1.5 – 3.5 hrs</td>
                  <td class="py-3 px-4">Kitchens, baths, dusting, HEPA vacuuming &amp; damp floor mopping</td>
                </tr>
                <tr class="hover:bg-blue-50/50">
                  <td class="py-3 px-4 font-bold">Top-to-Bottom Deep Clean</td>
                  <td class="py-3 px-4 font-semibold text-blue-700">$220 – $420 flat rate</td>
                  <td class="py-3 px-4">3.5 – 6.5 hrs</td>
                  <td class="py-3 px-4">Hand-washed baseboards, blinds, vents, grout descaling &amp; degreasing</td>
                </tr>
                <tr class="hover:bg-blue-50/50">
                  <td class="py-3 px-4 font-bold">Move-In / Move-Out Turnover</td>
                  <td class="py-3 px-4 font-semibold text-blue-700">$250 – $480 flat rate</td>
                  <td class="py-3 px-4">3.5 – 6.0 hrs</td>
                  <td class="py-3 px-4">Inside cabinets, drawers, oven, fridge, closets &amp; deposit checklist</td>
                </tr>
                <tr class="hover:bg-blue-50/50">
                  <td class="py-3 px-4 font-bold">Airbnb / Vacation Rental Turn</td>
                  <td class="py-3 px-4 font-semibold text-blue-700">$140 – $340 / turn</td>
                  <td class="py-3 px-4">10 AM – 3 PM window</td>
                  <td class="py-3 px-4">Fresh linens, restocking, sand/humidity reset &amp; host photo report</td>
                </tr>
                <tr class="hover:bg-blue-50/50">
                  <td class="py-3 px-4 font-bold">Commercial &amp; Medical Janitorial</td>
                  <td class="py-3 px-4 font-semibold text-blue-700">Custom Flat Monthly / Visit</td>
                  <td class="py-3 px-4">Nightly / Weekly</td>
                  <td class="py-3 px-4">EPA List N disinfection, restrooms, workstations, VCT/carpet care &amp; COI</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>"""

def build_ai_service_summary_and_table(prof, srv_key):
    srv = SERVICES[srv_key]
    city = prof["city"]
    display = prof["display_title"]
    county = prof["county"]
    c_slug = county_to_slug(prof["county_short"])
    pzip = prof["primary_zip"]
    short_name = srv["short_name"]
    coords = prof["coordinates"]
    coord_txt = f"{coords['latitude']:.4f}°N, {abs(coords['longitude']):.4f}°W"
    nearby_txt = prof["nearby_names"] or f"neighboring {county} towns"
    return f"""
        <!-- 🤖 AI OVERVIEW DIRECT ANSWER & SCOPE/DURATION MATRIX -->
        <div id="ai-quick-answer" class="bg-white rounded-3xl p-6 sm:p-8 shadow-2xl border-2 border-blue-500/30 mb-14 text-left">
          <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
            <span class="inline-flex items-center gap-2 bg-blue-100 text-blue-800 text-xs font-extrabold uppercase tracking-wider px-3 py-1 rounded-full">
              <i class="fas fa-bolt"></i> At-a-Glance Service Guide • {html.escape(display)} ({html.escape(pzip)}) • {coord_txt}
            </span>
            <div class="flex flex-wrap gap-3 text-xs font-bold">
              <a href="/services/{srv_key}/" class="text-blue-600 hover:underline">Alabama {html.escape(short_name)} Guide &rarr;</a>
              <a href="/counties/{c_slug}/" class="text-indigo-600 hover:underline">{html.escape(county)} Coverage &rarr;</a>
              <a href="/guides/" class="text-purple-600 hover:underline">All Cost &amp; Checklist Guides &rarr;</a>
            </div>
          </div>
          <h3 class="text-xl sm:text-2xl font-extrabold text-gray-900 mb-2">
            {html.escape(short_name)} in {html.escape(display)}: Quick Scope, Schedule &amp; Pricing Summary
          </h3>
          <p class="text-sm sm:text-base text-gray-700 leading-relaxed mb-6">
            <strong>Zoiris Cleaning Services</strong> provides flat-rate, contract-free <strong>{html.escape(short_name.lower())}</strong> across all {html.escape(sqmi_text(prof))} of <strong>{html.escape(display)} ({html.escape(county)}, ZIP {html.escape(prof['zips_str'])}; near {html.escape(nearby_txt)})</strong> using W-2 background-checked technicians and <em>{html.escape(srv['equipment'].lower())}</em>. Recommended schedule: <em>{html.escape(srv['cadence'])}</em>, backed by a 24-hour 100% Re-Clean Guarantee and zero travel fees—call <strong>(251) 220-2515</strong> for an instant estimate.
          </p>
          <div class="overflow-x-auto rounded-2xl border border-gray-200">
            <table class="w-full text-left border-collapse text-xs sm:text-sm">
              <thead>
                <tr class="bg-slate-900 text-white">
                  <th class="py-3 px-4 font-bold">Property Tier in {html.escape(city)}, AL</th>
                  <th class="py-3 px-4 font-bold">Square Footage</th>
                  <th class="py-3 px-4 font-bold">Assigned Crew &amp; Est. Time</th>
                  <th class="py-3 px-4 font-bold">Included {html.escape(short_name)} Deliverables</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200 text-gray-800 bg-white">
                <tr class="hover:bg-blue-50/50">
                  <td class="py-3 px-4 font-bold">Compact Home / Condo / Suite</td>
                  <td class="py-3 px-4">Up to 1,500 sq ft</td>
                  <td class="py-3 px-4">2 Technicians • 1.5 – 3 hrs</td>
                  <td class="py-3 px-4">{html.escape(srv['process'][0])}; {html.escape(srv['process'][1].lower())}</td>
                </tr>
                <tr class="hover:bg-blue-50/50">
                  <td class="py-3 px-4 font-bold">Standard Family Residence / Office</td>
                  <td class="py-3 px-4">1,500 – 3,000 sq ft</td>
                  <td class="py-3 px-4">2–3 Technicians • 2.5 – 4.5 hrs</td>
                  <td class="py-3 px-4">{html.escape(srv['process'][2])}; {html.escape(srv['process'][3].lower())}</td>
                </tr>
                <tr class="hover:bg-blue-50/50">
                  <td class="py-3 px-4 font-bold">Large Estate / Commercial Facility</td>
                  <td class="py-3 px-4">3,000 – 10,000+ sq ft</td>
                  <td class="py-3 px-4">3–5+ Technicians • Custom Shift</td>
                  <td class="py-3 px-4">{html.escape(srv['process'][4])}; {html.escape(srv['process'][5].lower())}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>"""

def build_service_faqs(prof, srv_key, actual_folder):
    srv = SERVICES[srv_key]
    srv_name = srv["name"]
    short_name = srv["short_name"]
    srv_lower = short_name.lower()
    city = prof["city"]
    display = prof["display_title"]
    county = prof["county"]
    pzip = prof["primary_zip"]
    nearby_plain = prof["nearby_cities_plain"]

    steps_summary = "; ".join(s.lower() for s in srv["process"][:4])
    benefits_summary = "; ".join(b.lower() for b in srv["benefits"][:3])

    return [
        {
            "q": f"What exactly is included with {srv_lower} in {display}?",
            "a": f"Our {srv_lower} in {city} ({county}, ZIP {pzip}) follows a systematic 6-stage checklist: {steps_summary}. Key deliverables include {benefits_summary}."
        },
        {
            "q": f"What professional equipment and solutions do you use for {srv_lower} in {city}?",
            "a": f"Every {city} crew arrives fully stocked with specialized gear: {srv['equipment']} This protects {prof['housing']} against {prof['climate']}."
        },
        {
            "q": f"How long does {srv_lower} take and how often should {city} properties schedule it?",
            "a": f"Recommended cadence: {srv['cadence']}. Exact appointment length depends on total square footage and property condition across {city}, and we send coordinated 2+ person teams for fast, thorough completion."
        },
        {
            "q": f"Do you require long-term contracts for {srv_lower} in {city}, AL?",
            "a": f"No—never. Whether you need a single on-demand {srv_lower} appointment or ongoing recurring service in {city} (ZIP {prof['zips_str']}), there are zero binding contracts and zero rescheduling penalties."
        },
        {
            "q": f"How is flat-rate pricing calculated for {srv_lower} in {county}?",
            "a": f"Quotes are 100% upfront and based on property size, scope, and frequency—with zero hidden travel surcharges anywhere in {city} or adjacent {nearby_plain}. Call (251) 220-2515 for an instant estimate."
        },
        {
            "q": f"Are your {city} technicians licensed, bonded, and insured for {srv_lower}?",
            "a": f"Yes. Zoiris Cleaning Services LLC carries comprehensive general liability insurance and workers' compensation. Every technician is a background-screened, uniformed W-2 employee trained specifically for {srv['ideal_for'].lower()}."
        },
        {
            "q": f"Which areas around {city} and {county} do your crews cover for {srv_lower}?",
            "a": f"We cover {prof['neighborhoods']}, plus nearby {prof['nearby_names']}."
        },
        {
            "q": f"Is {srv_lower} in {city}, AL backed by a satisfaction guarantee?",
            "a": f"Yes—100%. Every {srv_lower} visit in {display} is protected by our 24-Hour Re-Clean Guarantee. Notify us within 24 hours at (251) 220-2515 if anything was missed and we will re-clean it free of charge."
        }
    ]

def render_faq_details_html(faqs, heading_label, sub_label):
    cards = []
    icons = [
        "fas fa-clipboard-check", "fas fa-spray-can-sparkles", "fas fa-clock",
        "fas fa-file-signature", "fas fa-calculator", "fas fa-shield-alt",
        "fas fa-map-marked-alt", "fas fa-award"
    ]
    for i, item in enumerate(faqs):
        ic = icons[i % len(icons)]
        open_attr = " open" if i == 0 else ""
        cards.append(f"""          <details class="group bg-white rounded-2xl border border-white/20 shadow-xl overflow-hidden transition-all duration-200"{open_attr}>
            <summary class="w-full px-6 py-5 text-left font-bold text-base sm:text-lg text-gray-900 flex justify-between items-center hover:bg-slate-50 transition cursor-pointer list-none">
              <span class="flex items-center gap-3 pr-4">
                <i class="fas fa-check-circle text-blue-600 shrink-0"></i>
                <span>{html.escape(item['q'])}</span>
              </span>
              <i class="fas fa-chevron-down text-gray-400 transition-transform duration-300 group-open:rotate-180 shrink-0"></i>
            </summary>
            <div class="px-6 pb-6 pt-3 text-gray-700 text-sm sm:text-base leading-relaxed border-t border-gray-100">
              <p>{html.escape(item['a'])}</p>
            </div>
          </details>""")
    joined = "\n".join(cards)
    return f"""
    <!-- ❓ SECTION: FREQUENTLY ASKED QUESTIONS -->
    <section class="py-20 px-4 sm:px-6 lg:px-8 bg-transparent relative z-10" id="faq">
      <div class="max-w-5xl mx-auto">
        <div class="text-center max-w-3xl mx-auto mb-14">
          <span class="text-sm font-bold uppercase tracking-wider text-blue-100 bg-white/10 backdrop-blur-md border border-white/20 px-4 py-1.5 rounded-full">
            ✦ Local Cleaning Answers &amp; Pricing Guide ✦
          </span>
          <h2 class="text-3xl md:text-4xl font-extrabold text-white mt-4 tracking-tight">
            {html.escape(heading_label)}
          </h2>
          <div class="mt-3 h-1 w-24 bg-gradient-to-r from-blue-400 to-indigo-400 mx-auto rounded"></div>
          <p class="mt-4 text-purple-100 text-base md:text-lg leading-relaxed">
            {html.escape(sub_label)}
          </p>
        </div>
        <div class="space-y-4">
{joined}
        </div>
        <div class="mt-12 text-center bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl p-6 sm:p-8 text-white shadow-xl">
          <h3 class="text-xl sm:text-2xl font-bold mb-2">Ready for a Spotless Property? Get Your Instant Flat-Rate Estimate</h3>
          <p class="text-blue-100 text-sm sm:text-base mb-6 max-w-xl mx-auto">
            Available 24/7 with zero locked contracts, vetted W-2 crews, and our 100% Re-Clean Satisfaction Guarantee.
          </p>
          <div class="flex flex-col sm:flex-row justify-center gap-4">
            <a href="tel:2512202515" class="bg-white text-blue-700 font-bold px-6 py-3 rounded-full hover:bg-gray-100 transition shadow-md">
              <i class="fas fa-phone-alt mr-2"></i> Call (251) 220-2515
            </a>
            <a href="#quote" class="bg-black/30 hover:bg-black/50 text-white font-bold px-6 py-3 rounded-full border border-white/30 transition">
              <i class="fas fa-file-invoice mr-2"></i> Request Free Estimate Online
            </a>
          </div>
        </div>
      </div>
    </section>"""

def build_hub_body_html(loc_slug, det_folder):
    prof = get_enriched_profile(loc_slug)
    city = prof["city"]
    display = prof["display_title"]
    county = prof["county"]
    faqs = build_hub_faqs(prof)

    # Categorized links to ALL 29 services in this city!
    res_links, com_links, pm_links = [], [], []
    for sk, sv in SERVICES.items():
        folder = det_folder if sk == "detailing" else sk
        url = f"/{loc_slug}/{folder}/"
        anchor = f"{sv['short_name']} in {city}"
        item_html = f'<a href="{url}" class="flex items-center justify-between bg-white/95 hover:bg-blue-50 text-gray-900 font-semibold text-sm px-4 py-3 rounded-xl shadow border border-gray-200 transition group"><span>{html.escape(anchor)}</span><i class="fas fa-arrow-right text-blue-600 group-hover:translate-x-1 transition-transform text-xs"></i></a>'
        if sv["category"] == "residential":
            res_links.append(item_html)
        elif sv["category"] == "commercial":
            com_links.append(item_html)
        else:
            pm_links.append(item_html)

    # 6 Featured visual cards
    featured_keys = ["house-cleaning", "deep-cleaning", "move-out-cleaning", "commercial-cleaning", "vacation-rental-cleaning", "carpet-cleaning"]
    feat_cards = []
    for fk in featured_keys:
        sv = SERVICES[fk]
        feat_cards.append(f"""          <div class="bg-white rounded-2xl shadow-2xl overflow-hidden border border-white/20 flex flex-col hover:-translate-y-1 transition-all duration-300">
            <img src="{sv['image']}" alt="{html.escape(sv['short_name'])} in {html.escape(display)} by Zoiris Cleaning Services" loading="lazy" width="600" height="400" class="h-48 w-full object-cover" />
            <div class="p-6 flex flex-col flex-grow">
              <span class="text-xs font-bold uppercase tracking-wider text-blue-600 mb-1">{html.escape(city)}, AL • {html.escape(county)}</span>
              <h3 class="text-xl font-extrabold text-gray-900 mb-2">{html.escape(sv['name'])}</h3>
              <p class="text-sm text-gray-600 leading-relaxed mb-4 flex-grow">{html.escape(sv['short_description'])}</p>
              <a href="/{loc_slug}/{fk}/" class="inline-flex items-center justify-center bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold text-sm px-5 py-3 rounded-xl transition shadow">
                Explore {html.escape(sv['short_name'])} in {html.escape(city)} <i class="fas fa-arrow-right ml-2"></i>
              </a>
            </div>
          </div>""")

    nearby_pills = "\n".join(
        f'          <a href="/{n["slug"]}/" class="bg-white/10 hover:bg-white/20 backdrop-blur-md border border-white/20 text-white font-semibold text-sm px-4 py-3 rounded-xl transition flex items-center justify-between"><span><i class="fas fa-map-marker-alt text-blue-400 mr-2"></i>{html.escape(n["city"])}, AL</span><span class="text-xs text-blue-200">{n["miles"]} mi</span></a>'
        for n in prof["nearby"]
    )

    faq_section = render_faq_details_html(
        faqs,
        f"Frequently Asked Questions About Cleaning Services in {display}",
        f"Transparent answers on pricing, scheduling, HEPA equipment, and local service coverage across {city} ({county}, ZIP {prof['zips_str']})."
    )

    body = f"""
    <!-- 🌟 SECTION 1: LOCAL MARKET OVERVIEW & ENVIRONMENTAL CARE -->
    <section class="px-6 py-20 bg-transparent relative z-10" id="local-overview">
      <div class="max-w-6xl mx-auto">
        <div class="text-center max-w-3xl mx-auto mb-12">
          <span class="text-sm font-bold uppercase tracking-wider text-blue-100 bg-white/10 backdrop-blur-md border border-white/20 px-4 py-1.5 rounded-full">
            ✦ {html.escape(prof['region_label'])} • ZIP {html.escape(prof['zips_str'])} ✦
          </span>
          <h2 class="text-3xl md:text-4xl font-extrabold text-white mt-4">
            Trusted Residential &amp; Commercial Cleaners Serving {html.escape(display)}
          </h2>
          <div class="mt-3 h-1 w-20 bg-blue-400 mx-auto rounded"></div>
          <p class="mt-4 text-purple-100 text-base md:text-lg leading-relaxed">
            Serving {html.escape(prof['neighborhoods'])}, <strong>Zoiris Cleaning Services</strong> delivers flat-rate, contract-free housekeeping, restorative deep scrubs, turnover cleaning, and commercial janitorial across all {sqmi_text(prof)} of {html.escape(city)} in <strong>{html.escape(county)}</strong>.
          </p>
        </div>

{build_ai_hub_summary_and_table(prof)}

        <div class="grid grid-cols-1 md:grid-cols-2 gap-12 items-center mb-12">
          <div class="relative">
            <img src="/images/services_action.webp" alt="Zoiris Cleaning Services professional team serving {html.escape(display)}" loading="lazy" width="800" height="533" class="rounded-2xl shadow-2xl w-full h-auto object-cover border-4 border-white/20" />
            <div class="mt-4 grid grid-cols-3 gap-3 text-center">
              <div class="bg-white/95 rounded-xl p-3 shadow">
                <p class="text-xs text-gray-500 uppercase font-bold">County</p>
                <p class="text-sm font-extrabold text-gray-900">{html.escape(county)}</p>
              </div>
              <div class="bg-white/95 rounded-xl p-3 shadow">
                <p class="text-xs text-gray-500 uppercase font-bold">ZIP Coverage</p>
                <p class="text-sm font-extrabold text-gray-900">{html.escape(prof['primary_zip'])}</p>
              </div>
              <div class="bg-white/95 rounded-xl p-3 shadow">
                <p class="text-xs text-gray-500 uppercase font-bold">Guarantee</p>
                <p class="text-sm font-extrabold text-blue-600">24-Hr Re-Clean</p>
              </div>
            </div>
          </div>

          <div>
            <h3 class="text-2xl md:text-3xl font-bold text-white mb-4">Engineered for {html.escape(city)}'s Homes, Climate &amp; Surfaces</h3>
            <p class="text-purple-100 text-base leading-relaxed mb-4">
              Local properties around {html.escape(prof['landmarks'])} face distinct regional conditions—including {html.escape(prof['climate'])}. Generic wipe-downs leave fine allergens and residue behind.
            </p>
            <p class="text-purple-100 text-base leading-relaxed mb-6">
              Our background-checked W-2 cleaning teams specialize in {html.escape(prof['care_focus'])} across {html.escape(prof['housing'])}. Every appointment includes commercial HEPA filtration, color-coded microfiber sanitation, and zero locked-in contracts.
            </p>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div class="bg-white/95 rounded-xl p-4 shadow-lg border border-white/20">
                <h4 class="font-bold text-gray-900 text-sm"><i class="fas fa-shield-alt text-green-600 mr-2"></i>Licensed, Bonded &amp; Insured</h4>
                <p class="text-xs text-gray-600 mt-1">In-house W-2 employees with full liability &amp; workers' comp protection.</p>
              </div>
              <div class="bg-white/95 rounded-xl p-4 shadow-lg border border-white/20">
                <h4 class="font-bold text-gray-900 text-sm"><i class="fas fa-ban text-blue-600 mr-2"></i>100% No Locked Contracts</h4>
                <p class="text-xs text-gray-600 mt-1">Weekly, bi-weekly, monthly, or one-time cleans with zero reschedule fees.</p>
              </div>
              <div class="bg-white/95 rounded-xl p-4 shadow-lg border border-white/20">
                <h4 class="font-bold text-gray-900 text-sm"><i class="fas fa-wind text-purple-600 mr-2"></i>0.3-Micron HEPA Filtration</h4>
                <p class="text-xs text-gray-600 mt-1">Captures pollen, red-clay dust, pet dander &amp; fine indoor allergens.</p>
              </div>
              <div class="bg-white/95 rounded-xl p-4 shadow-lg border border-white/20">
                <h4 class="font-bold text-gray-900 text-sm"><i class="fas fa-leaf text-amber-600 mr-2"></i>Child &amp; Pet-Safe Formulas</h4>
                <p class="text-xs text-gray-600 mt-1">EPA-registered hospital-grade botanical disinfectants safe for families.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 🧹 SECTION 2: COMPLETE 29-SERVICE DIRECTORY FOR THIS CITY -->
    <section class="py-20 px-4 sm:px-6 lg:px-8 bg-transparent relative z-10" id="services">
      <div class="max-w-7xl mx-auto">
        <div class="text-center max-w-3xl mx-auto mb-14">
          <span class="text-sm font-bold uppercase tracking-wider text-blue-100 bg-white/10 backdrop-blur-md border border-white/20 px-4 py-1.5 rounded-full">
            ✦ Full-Service Local Directory • {html.escape(display)} ✦
          </span>
          <h2 class="text-3xl md:text-4xl font-extrabold text-white mt-4">
            Most Popular Cleaning Services in {html.escape(city)}, AL
          </h2>
          <div class="mt-3 h-1 w-24 bg-gradient-to-r from-blue-400 to-indigo-400 mx-auto rounded"></div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
{chr(10).join(feat_cards)}
        </div>

        <div class="bg-black/35 backdrop-blur-md border border-white/15 rounded-3xl p-6 sm:p-10">
          <h3 class="text-2xl font-extrabold text-white text-center mb-8">
            All 29 Specialized Cleaning &amp; Property Services in {html.escape(display)}
          </h3>
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div>
              <h4 class="text-lg font-bold text-blue-300 mb-4 border-b border-white/15 pb-2"><i class="fas fa-home mr-2"></i>Residential &amp; Home Detailing</h4>
              <div class="space-y-2.5">
                {chr(10).join(res_links)}
              </div>
            </div>
            <div>
              <h4 class="text-lg font-bold text-purple-300 mb-4 border-b border-white/15 pb-2"><i class="fas fa-building mr-2"></i>Commercial, Clinical &amp; Industrial</h4>
              <div class="space-y-2.5">
                {chr(10).join(com_links)}
              </div>
            </div>
            <div>
              <h4 class="text-lg font-bold text-pink-300 mb-4 border-b border-white/15 pb-2"><i class="fas fa-key mr-2"></i>Airbnb, Turnovers &amp; Exterior Care</h4>
              <div class="space-y-2.5">
                {chr(10).join(pm_links)}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

{faq_section}

    <!-- 📍 SECTION: NEARBY COUNTY & REGIONAL INTERLINKING -->
    <section class="py-16 px-4 sm:px-6 lg:px-8 bg-transparent relative z-10" id="nearby-areas">
      <div class="max-w-6xl mx-auto bg-black/40 backdrop-blur-md border border-white/15 rounded-3xl p-6 sm:p-10">
        <div class="text-center max-w-3xl mx-auto mb-8">
          <h2 class="text-2xl sm:text-3xl font-extrabold text-white">
            Nearby Communities We Serve Around {html.escape(city)} &amp; {html.escape(county)}
          </h2>
          <p class="text-purple-100 text-sm sm:text-base mt-2">
            Our local crews dispatch daily across {html.escape(county)} and neighboring Alabama communities with zero travel fees:
          </p>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3">
{nearby_pills}
        </div>
        <div class="text-center mt-8">
          <a href="/locations/" class="inline-flex items-center text-blue-300 hover:text-white font-bold text-sm underline">
            Browse All 504 Alabama Cities &amp; 67 Counties Served by Zoiris Cleaning Services <i class="fas fa-arrow-right ml-2"></i>
          </a>
        </div>
      </div>
    </section>"""
    return body, faqs

def build_service_body_html(loc_slug, srv_key, actual_folder, det_map):
    prof = get_enriched_profile(loc_slug)
    srv = SERVICES[srv_key]
    city = prof["city"]
    display = prof["display_title"]
    county = prof["county"]
    faqs = build_service_faqs(prof, srv_key, actual_folder)

    benefits_html = "\n".join(
        f'              <li class="flex items-start bg-white/95 rounded-xl p-4 shadow border border-white/20"><i class="fas fa-check-circle text-green-600 mt-1 mr-3 shrink-0"></i><span class="text-sm font-medium text-gray-800">{html.escape(b)}</span></li>'
        for b in srv["benefits"]
    )

    steps_html = "\n".join(
        f"""          <div class="bg-white/95 rounded-2xl p-6 shadow-xl border border-white/20 flex items-start gap-4">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 to-indigo-600 text-white font-extrabold flex items-center justify-center shrink-0 shadow">
              {idx+1}
            </div>
            <div>
              <h3 class="font-bold text-gray-900 text-base mb-1">Step {idx+1}</h3>
              <p class="text-sm text-gray-700 leading-relaxed">{html.escape(step)}</p>
            </div>
          </div>"""
        for idx, step in enumerate(srv["process"])
    )

    related_cards = []
    for rk in srv["related_services"]:
        rsv = SERVICES[rk]
        rfolder = det_map.get(loc_slug, "Detailing-" + loc_slug) if rk == "detailing" else rk
        related_cards.append(
            f'          <a href="/{loc_slug}/{rfolder}/" class="bg-white/95 hover:bg-blue-50 rounded-xl p-4 shadow border border-gray-200 flex items-center justify-between transition group"><span class="font-bold text-sm text-gray-900">{html.escape(rsv["short_name"])} in {html.escape(city)}</span><i class="fas fa-arrow-right text-blue-600 group-hover:translate-x-1 transition-transform text-xs"></i></a>'
        )

    nearby_service_links = []
    for n in prof["nearby"]:
        nslug = n["slug"]
        nfolder = det_map.get(nslug, "Detailing-" + nslug) if srv_key == "detailing" else srv_key
        nearby_service_links.append(
            f'          <a href="/{nslug}/{nfolder}/" class="bg-white/10 hover:bg-white/20 backdrop-blur-md border border-white/20 text-white font-semibold text-sm px-4 py-3 rounded-xl transition flex items-center justify-between"><span>{html.escape(srv["short_name"])} in {html.escape(n["city"])}, AL</span><span class="text-xs text-blue-200">{n["miles"]} mi</span></a>'
        )

    faq_section = render_faq_details_html(
        faqs,
        f"Frequently Asked Questions About {srv['short_name']} in {display}",
        f"Everything you need to know about our {srv['short_name'].lower()} checklist, equipment, scheduling, and flat-rate pricing across {city} and {county}."
    )

    body = f"""
    <!-- 🌟 SECTION 1: SERVICE OVERVIEW & LOCAL EXECUTION -->
    <section class="px-6 py-20 bg-transparent relative z-10" id="service-overview">
      <div class="max-w-6xl mx-auto">
        <div class="mb-6 flex flex-wrap items-center gap-2 text-xs sm:text-sm text-blue-200 font-semibold">
          <a href="/" class="hover:text-white underline">Home</a>
          <span>/</span>
          <a href="/locations/" class="hover:text-white underline">Alabama Locations</a>
          <span>/</span>
          <a href="/{loc_slug}/" class="hover:text-white underline">{html.escape(display)}</a>
          <span>/</span>
          <span class="text-white">{html.escape(srv['short_name'])}</span>
        </div>

        <div class="text-center max-w-3xl mx-auto mb-12">
          <span class="text-sm font-bold uppercase tracking-wider text-blue-100 bg-white/10 backdrop-blur-md border border-white/20 px-4 py-1.5 rounded-full">
            ✦ {html.escape(display)} • {html.escape(county)} • ZIP {html.escape(prof['zips_str'])} ✦
          </span>
          <h2 class="text-3xl md:text-4xl font-extrabold text-white mt-4">
            Professional {html.escape(srv['name'])} Tailored for {html.escape(city)} Properties
          </h2>
          <div class="mt-3 h-1 w-20 bg-blue-400 mx-auto rounded"></div>
          <p class="mt-4 text-purple-100 text-base md:text-lg leading-relaxed">
            {html.escape(srv['short_description'])} Serving {html.escape(prof['neighborhoods'])} with vetted in-house W-2 teams and zero locked contracts.
          </p>
        </div>

{build_ai_service_summary_and_table(prof, srv_key)}

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start mb-16">
          <div>
            <img src="{srv['image']}" alt="{html.escape(srv['name'])} in {html.escape(display)} by Zoiris Cleaning Services" loading="lazy" width="800" height="533" class="rounded-2xl shadow-2xl w-full h-auto object-cover border-4 border-white/20 mb-6" />
            <div class="bg-black/45 backdrop-blur-md border border-white/15 rounded-2xl p-6 text-white space-y-3">
              <h3 class="text-lg font-extrabold text-blue-300"><i class="fas fa-sliders-h mr-2"></i>{html.escape(city)} Service Specifications</h3>
              <p class="text-sm text-gray-200"><strong>Service Territory:</strong> {html.escape(display)} ({html.escape(county)}, ZIP {html.escape(prof['zips_str'])}) &amp; {html.escape(prof['nearby_cities_plain'])}</p>
              <p class="text-sm text-gray-200"><strong>Ideal Property Types:</strong> {html.escape(srv['ideal_for'])}</p>
              <p class="text-sm text-gray-200"><strong>Recommended Schedule:</strong> {html.escape(srv['cadence'])}</p>
              <p class="text-sm text-gray-200"><strong>Equipment &amp; Chemistry:</strong> {html.escape(srv['equipment'])}</p>
            </div>
          </div>

          <div>
            <h3 class="text-2xl md:text-3xl font-bold text-white mb-4">
              Why {html.escape(city)} Clients Choose Zoiris for {html.escape(srv['short_name'])}
            </h3>
            <p class="text-purple-100 text-base leading-relaxed mb-4">
              Across {html.escape(prof['landmarks'])}, properties experience {html.escape(prof['climate'])}. Our {html.escape(srv['short_name'].lower())} protocol combines {html.escape(prof['care_focus'])} with strict quality-control checklists so every surface is left spotless and sanitized.
            </p>
            <ul class="space-y-3 mb-6">
{benefits_html}
            </ul>
          </div>
        </div>

        <!-- 6-STEP TECHNICAL EXECUTION CHECKLIST -->
        <div class="mb-16">
          <div class="text-center max-w-3xl mx-auto mb-10">
            <h2 class="text-2xl sm:text-3xl font-extrabold text-white">
              Our 6-Step {html.escape(srv['short_name'])} Checklist in {html.escape(display)}
            </h2>
            <p class="text-purple-100 text-sm sm:text-base mt-2">
              Every crew follows this verified execution sequence on {html.escape(city)} appointments:
            </p>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
{steps_html}
          </div>
        </div>

        <!-- RELATED SERVICES IN THIS CITY -->
        <div class="bg-black/35 backdrop-blur-md border border-white/15 rounded-3xl p-6 sm:p-8">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-6">
            <h3 class="text-xl font-extrabold text-white">
              Related Cleaning Services in {html.escape(display)}
            </h3>
            <a href="/{loc_slug}/" class="text-blue-300 hover:text-white text-sm font-bold underline">
              <i class="fas fa-th-large mr-1"></i> View All 29 Services in {html.escape(city)}, AL
            </a>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
{chr(10).join(related_cards)}
          </div>
        </div>
      </div>
    </section>

{faq_section}

    <!-- 📍 NEARBY CITIES FOR THIS EXACT SERVICE -->
    <section class="py-16 px-4 sm:px-6 lg:px-8 bg-transparent relative z-10" id="nearby-service-areas">
      <div class="max-w-6xl mx-auto bg-black/40 backdrop-blur-md border border-white/15 rounded-3xl p-6 sm:p-10">
        <div class="text-center max-w-3xl mx-auto mb-8">
          <h2 class="text-2xl sm:text-3xl font-extrabold text-white">
            {html.escape(srv['short_name'])} in Nearby {html.escape(county)} &amp; Regional Communities
          </h2>
          <p class="text-purple-100 text-sm sm:text-base mt-2">
            Need {html.escape(srv['short_name'].lower())} in a neighboring town near {html.escape(city)}? Explore local flat-rate coverage:
          </p>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3">
{chr(10).join(nearby_service_links)}
        </div>
        <div class="text-center mt-8 flex flex-wrap justify-center gap-6">
          <a href="/{loc_slug}/" class="text-blue-300 hover:text-white font-bold text-sm underline">
            {html.escape(display)} Cleaning Hub
          </a>
          <a href="/locations/" class="text-blue-300 hover:text-white font-bold text-sm underline">
            All 504 Alabama Service Areas
          </a>
        </div>
      </div>
    </section>"""
    return body, faqs

def build_jsonld_schema(page_kind, canonical_url, loc_slug=None, srv_key=None, faqs=None, title="", desc=""):
    # Headquarters Service-Area Business entity (Google LocalBusiness / CleaningService compliant!)
    hq_business = {
        "@type": "LocalBusiness",
        "additionalType": "https://schema.org/CleaningService",
        "@id": "https://www.zoiriscleaningservices.com/#organization",
        "name": "Zoiris Cleaning Services",
        "legalName": "Zoiris Cleaning Services LLC",
        "url": "https://www.zoiriscleaningservices.com/",
        "telephone": "+1-251-220-2515",
        "email": "zoiriscleaningservices@gmail.com",
        "image": "https://www.zoiriscleaningservices.com/images/services_action.png",
        "logo": "https://www.zoiriscleaningservices.com/images/logo.png",
        "priceRange": "$$",
        "currenciesAccepted": "USD",
        "paymentAccepted": ["Cash", "Credit Card", "Debit Card", "Cash App", "Check"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Downtown Mobile",
            "addressLocality": "Mobile",
            "addressRegion": "AL",
            "postalCode": "36602",
            "addressCountry": "US"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": 30.6954,
            "longitude": -88.0399
        },
        "sameAs": [
            "https://www.instagram.com/zoiriscleaningservices/",
            "https://www.tiktok.com/@zoiriscleaningservices",
            "https://www.yelp.com/user_details?userid=7SDy8Urgj43gfYxrR5o2eQ"
        ],
        "openingHoursSpecification": [
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                "opens": "00:00",
                "closes": "23:59"
            }
        ],
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.9",
            "reviewCount": "240",
            "bestRating": "5",
            "worstRating": "1"
        }
    }

    website_node = {
        "@type": "WebSite",
        "@id": "https://www.zoiriscleaningservices.com/#website",
        "url": "https://www.zoiriscleaningservices.com/",
        "name": "Zoiris Cleaning Services",
        "publisher": {"@id": "https://www.zoiriscleaningservices.com/#organization"}
    }

    graph = [hq_business, website_node]

    # Breadcrumbs
    crumbs = [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.zoiriscleaningservices.com/"}]
    if page_kind == "locations_index":
        crumbs.append({"@type": "ListItem", "position": 2, "name": "Alabama Service Areas", "item": canonical_url})
        graph.append({
            "@type": "CollectionPage",
            "@id": f"{canonical_url}#webpage",
            "url": canonical_url,
            "name": title,
            "description": desc,
            "isPartOf": {"@id": "https://www.zoiriscleaningservices.com/#website"}
        })
    elif page_kind in ("location_hub", "location_service") and loc_slug:
        prof = get_enriched_profile(loc_slug)
        coords = prof["coordinates"]
        area_place = {
            "@type": "City",
            "name": f"{prof['city']}, AL",
            "containedInPlace": {
                "@type": "AdministrativeArea",
                "name": f"{prof['county']}, Alabama"
            },
            "geo": {
                "@type": "GeoCoordinates",
                "latitude": coords["latitude"],
                "longitude": coords["longitude"]
            }
        }
        crumbs.append({"@type": "ListItem", "position": 2, "name": "Alabama Locations", "item": "https://www.zoiriscleaningservices.com/locations/"})
        crumbs.append({"@type": "ListItem", "position": 3, "name": prof["display_title"], "item": f"https://www.zoiriscleaningservices.com/{loc_slug}/"})

        graph.append({
            "@type": "WebPage",
            "@id": f"{canonical_url}#webpage",
            "url": canonical_url,
            "name": title,
            "description": desc,
            "isPartOf": {"@id": "https://www.zoiriscleaningservices.com/#website"},
            "speakable": {
                "@type": "SpeakableSpecification",
                "cssSelector": ["#ai-quick-answer", "#faq"]
            }
        })

        if page_kind == "location_hub":
            graph.append({
                "@type": "Service",
                "@id": f"{canonical_url}#service",
                "name": f"Residential & Commercial Cleaning Services in {prof['display_title']}",
                "serviceType": "House Cleaning, Deep Cleaning, Move-Out Cleaning & Commercial Janitorial",
                "url": canonical_url,
                "description": desc,
                "provider": {"@id": "https://www.zoiriscleaningservices.com/#organization"},
                "areaServed": area_place
            })
        elif page_kind == "location_service" and srv_key:
            srv = SERVICES[srv_key]
            crumbs.append({"@type": "ListItem", "position": 4, "name": srv["short_name"], "item": canonical_url})
            graph.append({
                "@type": "Service",
                "@id": f"{canonical_url}#service",
                "name": f"{srv['name']} in {prof['display_title']}",
                "serviceType": srv["name"],
                "url": canonical_url,
                "image": f"https://www.zoiriscleaningservices.com{srv['image']}",
                "description": desc,
                "provider": {"@id": "https://www.zoiriscleaningservices.com/#organization"},
                "areaServed": area_place,
                "hasOfferCatalog": {
                    "@type": "OfferCatalog",
                    "name": f"{srv['short_name']} Checklist",
                    "itemListElement": [
                        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": step}}
                        for step in srv["process"]
                    ]
                }
            })
    elif page_kind == "global_page":
        crumbs.append({"@type": "ListItem", "position": 2, "name": title.split("|")[0].strip(), "item": canonical_url})
        graph.append({
            "@type": "WebPage",
            "@id": f"{canonical_url}#webpage",
            "url": canonical_url,
            "name": title,
            "description": desc,
            "isPartOf": {"@id": "https://www.zoiriscleaningservices.com/#website"}
        })

    graph.append({
        "@type": "BreadcrumbList",
        "@id": f"{canonical_url}#breadcrumb",
        "itemListElement": crumbs
    })

    if faqs:
        graph.append({
            "@type": "FAQPage",
            "@id": f"{canonical_url}#faq",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": item["q"],
                    "acceptedAnswer": {"@type": "Answer", "text": item["a"]}
                }
                for item in faqs
            ]
        })

    return '<script type="application/ld+json">\n' + json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False) + '\n  </script>'

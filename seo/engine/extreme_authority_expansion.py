import os
import sys
import re
import json
import html
from datetime import datetime

engine_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(engine_dir))
sys.path.insert(0, engine_dir)

from geo_service_content import (
    LOCATIONS, SERVICES, REGION_PROFILES,
    county_to_slug, render_faq_details_html, build_jsonld_schema
)
from master_overhaul import (
    DET_MAP, HEAD_TO_STYLE_RE, HERO_H1_P_RE, HERO_SECTION_RE,
    QUOTE_SECTION_RE, FOOTER_START_RE, build_clean_head_top,
    sanitize_common_html, write_atomic, TODAY
)

ALL_67_ALABAMA_COUNTIES = [
    "Autauga", "Baldwin", "Barbour", "Bibb", "Blount", "Bullock", "Butler",
    "Calhoun", "Chambers", "Cherokee", "Chilton", "Choctaw", "Clarke", "Clay",
    "Cleburne", "Coffee", "Colbert", "Conecuh", "Coosa", "Covington", "Crenshaw",
    "Cullman", "Dale", "Dallas", "De Kalb", "Elmore", "Escambia", "Etowah",
    "Fayette", "Franklin", "Geneva", "Greene", "Hale", "Henry", "Houston",
    "Jackson", "Jefferson", "Lamar", "Lauderdale", "Lawrence", "Lee", "Limestone",
    "Lowndes", "Macon", "Madison", "Marengo", "Marion", "Marshall", "Mobile",
    "Monroe", "Montgomery", "Morgan", "Perry", "Pickens", "Pike", "Randolph",
    "Russell", "Shelby", "Saint Clair", "Sumter", "Talladega", "Tallapoosa",
    "Tuscaloosa", "Walker", "Washington", "Wilcox", "Winston"
]

INDEXNOW_KEY = "zoiris8f4a2c91e7b34d60a5c1e8f9203b4d71"

def load_shell_template():
    raw = open(os.path.join(root_dir, "mobile-al", "index.html"), "r", encoding="utf-8", errors="replace").read()
    return raw

def render_shell_page(shell_raw, title, desc, canon_url, h1_txt, sub_html, body_html, faqs=None, og_image="/images/services_action.png", extra_article_schema=False):
    schema_block = build_custom_page_schema(canon_url, title, desc, faqs=faqs, is_article=extra_article_schema)
    head_top = build_clean_head_top(title, desc, canon_url, og_image=og_image, schema_block=schema_block)
    out = HEAD_TO_STYLE_RE.sub(lambda _: head_top, shell_raw, count=1)
    out = HERO_H1_P_RE.sub(
        lambda m: f"{m.group(1)}\n          {html.escape(h1_txt)}\n        {m.group(3)}\n          {sub_html}\n        {m.group(5)}",
        out, count=1
    )
    hm = HERO_SECTION_RE.search(out)
    qm = QUOTE_SECTION_RE.search(out)
    fm = FOOTER_START_RE.search(out)
    if hm and qm and fm:
        out = out[:hm.end()] + "\n\n" + body_html + "\n\n    " + qm.group(1) + "\n\n    " + out[fm.start():]
    out = sanitize_common_html(out)
    return out

def build_custom_page_schema(canon_url, title, desc, faqs=None, is_article=False):
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
        "geo": {"@type": "GeoCoordinates", "latitude": 30.6954, "longitude": -88.0399},
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "00:00",
            "closes": "23:59"
        }],
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
    page_node = {
        "@type": "WebPage",
        "@id": f"{canon_url}#webpage",
        "url": canon_url,
        "name": title,
        "description": desc,
        "isPartOf": {"@id": "https://www.zoiriscleaningservices.com/#website"},
        "speakable": {
            "@type": "SpeakableSpecification",
            "cssSelector": ["#ai-quick-answer", "#faq"]
        }
    }
    graph = [hq_business, website_node, page_node]
    if is_article:
        graph.append({
            "@type": "Article",
            "@id": f"{canon_url}#article",
            "headline": title.split("|")[0].strip(),
            "description": desc,
            "datePublished": "2026-09-10",
            "dateModified": TODAY,
            "author": {"@id": "https://www.zoiriscleaningservices.com/#organization"},
            "publisher": {"@id": "https://www.zoiriscleaningservices.com/#organization"},
            "mainEntityOfPage": {"@id": f"{canon_url}#webpage"},
            "image": "https://www.zoiriscleaningservices.com/images/services_action.png"
        })

    path_parts = [p for p in canon_url.replace("https://www.zoiriscleaningservices.com", "").split("/") if p]
    crumbs = [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.zoiriscleaningservices.com/"}]
    if len(path_parts) == 1:
        crumbs.append({"@type": "ListItem", "position": 2, "name": title.split("|")[0].strip(), "item": canon_url})
    elif len(path_parts) >= 2:
        sec_map = {"services": "All Cleaning Services", "counties": "Alabama Counties", "guides": "Cleaning Cost & Checklists"}
        sec_name = sec_map.get(path_parts[0], path_parts[0].capitalize())
        crumbs.append({"@type": "ListItem", "position": 2, "name": sec_name, "item": f"https://www.zoiriscleaningservices.com/{path_parts[0]}/"})
        crumbs.append({"@type": "ListItem", "position": 3, "name": title.split("|")[0].strip(), "item": canon_url})

    graph.append({"@type": "BreadcrumbList", "@id": f"{canon_url}#breadcrumb", "itemListElement": crumbs})
    if faqs:
        graph.append({
            "@type": "FAQPage",
            "@id": f"{canon_url}#faq",
            "mainEntity": [{"@type": "Question", "name": x["q"], "acceptedAnswer": {"@type": "Answer", "text": x["a"]}} for x in faqs]
        })
    return '<script type="application/ld+json">\n' + json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False) + '\n  </script>'

def build_service_pillars(shell):
    print("Building /services/ directory + 29 Statewide Master Service Pillar Pages...")
    pillar_urls = []
    srv_root = os.path.join(root_dir, "services")
    os.makedirs(srv_root, exist_ok=True)

    gulf_locs = sorted([v for v in LOCATIONS.values() if v["sitemap_tier"] == "priority"], key=lambda x: x["city"])
    metro_locs = sorted([v for v in LOCATIONS.values() if v["sitemap_tier"] == "metros"], key=lambda x: x["city"])

    # 1. /services/index.html
    cards = []
    for sk, sv in SERVICES.items():
        cards.append(f"""          <div class="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100 flex flex-col">
            <img src="{sv['image']}" alt="{html.escape(sv['name'])}" loading="lazy" width="600" height="400" class="h-44 w-full object-cover" />
            <div class="p-6 flex flex-col flex-grow">
              <span class="text-xs font-extrabold uppercase tracking-wider text-blue-600 mb-1">{html.escape(sv['category'].replace('-', ' '))}</span>
              <h3 class="text-lg font-extrabold text-gray-900 mb-2">{html.escape(sv['name'])}</h3>
              <p class="text-xs sm:text-sm text-gray-600 mb-4 flex-grow">{html.escape(sv['short_description'])}</p>
              <a href="/services/{sk}/" class="bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-bold text-xs sm:text-sm py-2.5 px-4 rounded-xl text-center hover:opacity-95 transition">
                View Scope, Pricing &amp; Cities &rarr;
              </a>
            </div>
          </div>""")

    idx_faqs = [
        {"q": "What types of residential and commercial cleaning services does Zoiris offer across Alabama?", "a": "Zoiris Cleaning Services offers 29 specialized services across all 67 Alabama counties—including recurring house cleaning & maid service, top-to-bottom deep cleaning, move-in/move-out turnovers, Airbnb & vacation rental turnovers, commercial office & medical janitorial, VCT floor stripping & waxing, carpet & upholstery steam cleaning, pure-water window & solar panel washing, gutter clearing, and soft-wash pressure washing."},
        {"q": "Do any of your 29 cleaning services require a long-term contract?", "a": "No. Every residential, commercial, and vacation-rental service is 100% contract-free with zero cancellation or rescheduling penalties."},
        {"q": "Are all Zoiris cleaning technicians W-2 employees and insured?", "a": "Yes. Every crew member is a background-checked, uniformed W-2 employee covered by comprehensive general liability insurance and workers' compensation."},
        {"q": "How can I get an instant quote for any cleaning service in Alabama?", "a": "Call our 24/7 dispatch line at (251) 220-2515, use our online estimate form, or check our 2026 Alabama Cleaning Cost Calculator for instant flat-rate pricing."}
    ]
    idx_body = f"""
    <section class="px-6 py-20 bg-transparent relative z-10">
      <div class="max-w-7xl mx-auto">
        <div id="ai-quick-answer" class="bg-white rounded-3xl p-6 sm:p-8 shadow-2xl border-2 border-blue-500/30 mb-14">
          <span class="inline-block bg-blue-100 text-blue-800 text-xs font-extrabold uppercase px-3 py-1 rounded-full mb-2">Complete 29-Service Master Directory</span>
          <h2 class="text-2xl sm:text-3xl font-extrabold text-gray-900 mb-3">Complete Residential, Commercial &amp; Turnover Cleaning Catalog</h2>
          <p class="text-sm sm:text-base text-gray-700 leading-relaxed">
            <strong>Zoiris Cleaning Services LLC</strong> executes <strong>29 specialized interior and exterior cleaning protocols</strong> across <strong>Mobile, Semmes, Theodore, Baldwin County, Birmingham, Huntsville, Montgomery, and all 503 Alabama communities</strong>. Every service includes commercial HEPA filtration, EPA-registered disinfectants, flat-rate upfront quotes, zero contracts, and a 24-hour 100% Re-Clean Guarantee.
          </p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-7">
{chr(10).join(cards)}
        </div>
      </div>
    </section>
{render_faq_details_html(idx_faqs, "Frequently Asked Questions About Our 29 Cleaning Services", "Answers on service combinations, commercial COI documentation, equipment, and statewide scheduling.")}"""

    idx_canon = "https://www.zoiriscleaningservices.com/services/"
    idx_html = render_shell_page(
        shell,
        "All 29 Residential & Commercial Cleaning Services in Alabama | Zoiris",
        "Explore all 29 house cleaning, deep cleaning, move-out, Airbnb turnover, medical/commercial janitorial, carpet, window & pressure washing services across Alabama. Call (251) 220-2515!",
        idx_canon,
        "29 Specialized Cleaning Services Across Alabama",
        "Flat-rate, <strong>No-Contract</strong> residential housekeeping, commercial janitorial, vacation-rental turnovers, and exterior washing across all 67 Alabama counties.",
        idx_body,
        faqs=idx_faqs
    )
    write_atomic(os.path.join(srv_root, "index.html"), idx_html)
    pillar_urls.append(idx_canon)

    # 2. Each of the 29 /services/<sk>/index.html pages
    for sk, sv in SERVICES.items():
        sdir = os.path.join(srv_root, sk)
        os.makedirs(sdir, exist_ok=True)
        canon = f"https://www.zoiriscleaningservices.com/services/{sk}/"

        gulf_city_links = "\n".join(
            f'            <a href="/{v["slug"]}/{DET_MAP[v["slug"]] if sk=="detailing" else sk}/" class="bg-white/10 hover:bg-white/20 border border-white/20 rounded-xl px-4 py-2.5 text-white text-xs sm:text-sm font-semibold flex justify-between items-center transition"><span>{html.escape(sv["short_name"])} in {html.escape(v["city"])}, AL</span><span class="text-blue-200 text-xs">{html.escape(v["primary_zip"])}</span></a>'
            for v in gulf_locs
        )
        metro_city_links = "\n".join(
            f'            <a href="/{v["slug"]}/{DET_MAP[v["slug"]] if sk=="detailing" else sk}/" class="bg-white/10 hover:bg-white/20 border border-white/20 rounded-xl px-4 py-2.5 text-white text-xs sm:text-sm font-semibold flex justify-between items-center transition"><span>{html.escape(sv["short_name"])} in {html.escape(v["city"])}, AL</span><span class="text-purple-200 text-xs">{html.escape(v["county_short"])} Co.</span></a>'
            for v in metro_locs
        )
        steps_rows = "\n".join(
            f'                <tr class="hover:bg-blue-50/50"><td class="py-3 px-4 font-bold text-blue-700">Phase {i+1}</td><td class="py-3 px-4 font-semibold">{html.escape(st)}</td><td class="py-3 px-4">{html.escape(sv["benefits"][i % len(sv["benefits"])])}</td></tr>'
            for i, st in enumerate(sv["process"])
        )
        p_faqs = [
            {"q": f"What is included in professional {sv['short_name'].lower()} across Alabama?", "a": f"{sv['short_description']} Every appointment follows our 6-phase checklist: " + "; ".join(sv["process"]) + "."},
            {"q": f"What equipment and cleaning chemistry do you use for {sv['short_name'].lower()}?", "a": sv["equipment"]},
            {"q": f"How often should homeowners or facility managers schedule {sv['short_name'].lower()}?", "a": f"Recommended cadence: {sv['cadence']}. Ideal for {sv['ideal_for'].lower()}."},
            {"q": f"Do you offer {sv['short_name'].lower()} in Mobile, Semmes, Theodore, Gulf Shores, Birmingham, and Huntsville?", "a": f"Yes! Zoiris Cleaning Services dispatches trained W-2 crews for {sv['short_name'].lower()} across Mobile, Semmes, Theodore, Daphne, Fairhope, Gulf Shores, Orange Beach, Birmingham, Huntsville, Montgomery, Tuscaloosa, Auburn, and all 503 Alabama cities with zero travel fees."}
        ]
        p_body = f"""
    <section class="px-6 py-20 bg-transparent relative z-10">
      <div class="max-w-6xl mx-auto">
        <div id="ai-quick-answer" class="bg-white rounded-3xl p-6 sm:p-8 shadow-2xl border-2 border-blue-500/30 mb-14">
          <div class="flex flex-wrap justify-between items-center gap-2 mb-3">
            <span class="bg-blue-100 text-blue-800 text-xs font-extrabold uppercase px-3 py-1 rounded-full">Statewide Service Standard &amp; Checklist</span>
            <a href="/guides/house-cleaning-cost-guide-alabama/" class="text-xs font-bold text-blue-600 hover:underline">Open Instant Cost Estimator &rarr;</a>
          </div>
          <h2 class="text-2xl sm:text-3xl font-extrabold text-gray-900 mb-3">{html.escape(sv['name'])}: Complete Scope, Equipment &amp; Execution Matrix</h2>
          <p class="text-sm sm:text-base text-gray-700 leading-relaxed mb-6">
            <strong>{html.escape(sv['name'])}</strong> by Zoiris Cleaning Services is designed for <em>{html.escape(sv['ideal_for'].lower())}</em> across Mobile, Baldwin County, and all 67 Alabama counties. Using <strong>{html.escape(sv['equipment'].lower())}</strong>, our W-2 insured teams deliver contract-free service ({html.escape(sv['cadence'])}) backed by a 24-hour 100% Re-Clean Guarantee.
          </p>
          <div class="overflow-x-auto rounded-2xl border border-gray-200">
            <table class="w-full text-left border-collapse text-xs sm:text-sm">
              <thead>
                <tr class="bg-slate-900 text-white">
                  <th class="py-3 px-4 font-bold">Execution Stage</th>
                  <th class="py-3 px-4 font-bold">Technical Task Performed</th>
                  <th class="py-3 px-4 font-bold">Verified Quality Outcome</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200 bg-white text-gray-800">
{steps_rows}
              </tbody>
            </table>
          </div>
        </div>

        <div class="bg-black/40 backdrop-blur-md border border-white/15 rounded-3xl p-6 sm:p-8 mb-10">
          <h2 class="text-2xl font-extrabold text-white mb-2">{html.escape(sv['short_name'])} Across Mobile &amp; Baldwin County Gulf Coast ({len(gulf_locs)} Hubs)</h2>
          <p class="text-sm text-purple-200 mb-6">Select your local Gulf Coast branch for neighborhood-specific scheduling &amp; instant quotes:</p>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2.5">
{gulf_city_links}
          </div>
        </div>

        <div class="bg-black/35 backdrop-blur-md border border-white/15 rounded-3xl p-6 sm:p-8">
          <h2 class="text-2xl font-extrabold text-white mb-2">{html.escape(sv['short_name'])} in Major Alabama Metros ({len(metro_locs)} Cities)</h2>
          <p class="text-sm text-purple-200 mb-6">Direct statewide dispatch with zero contracts and upfront flat-rate pricing:</p>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2.5">
{metro_city_links}
          </div>
          <div class="text-center mt-6">
            <a href="/counties/" class="text-blue-300 hover:text-white font-bold text-sm underline">Browse All 67 Alabama Counties &rarr;</a>
          </div>
        </div>
      </div>
    </section>
{render_faq_details_html(p_faqs, f"Frequently Asked Questions About {sv['name']}", f"Statewide technical specifications, safety standards, and booking answers for {sv['short_name'].lower()}.")}"""

        p_title = f"{sv['name']} in Alabama | Checklist, Rates & Local Branches | Zoiris"
        p_desc = f"Professional {sv['short_name'].lower()} across Mobile, Semmes, Theodore, Gulf Shores, Birmingham, Huntsville & all 67 AL counties. See full 6-step checklist & flat rates: (251) 220-2515!"
        p_html = render_shell_page(
            shell, p_title, p_desc, canon,
            f"{sv['name']} Across Alabama",
            f"Vetted W-2 specialists, {html.escape(sv['cadence'].lower())}, zero locked contracts, and 24-hour satisfaction guarantee.",
            p_body, faqs=p_faqs, og_image=sv["image"]
        )
        write_atomic(os.path.join(sdir, "index.html"), p_html)
        pillar_urls.append(canon)

    return pillar_urls

def build_county_hubs(shell):
    print("Building /counties/ directory + All 67 Alabama County Hubs...")
    county_urls = []
    cnt_root = os.path.join(root_dir, "counties")
    os.makedirs(cnt_root, exist_ok=True)

    by_county = {c: [] for c in ALL_67_ALABAMA_COUNTIES}
    for v in LOCATIONS.values():
        cs = v["county_short"]
        if cs == "DeKalb":
            cs = "De Kalb"
        elif cs == "St. Clair":
            cs = "Saint Clair"
        by_county.setdefault(cs, []).append(v)

    cnt_cards = []
    for cname in ALL_67_ALABAMA_COUNTIES:
        cslug = county_to_slug(cname)
        cities = sorted(by_county.get(cname, []), key=lambda x: x["city"])
        sample_names = ", ".join(x["city"] for x in cities[:4]) if cities else f"{cname} County communities"
        cnt_cards.append(
            f'          <a href="/counties/{cslug}/" class="bg-white/95 hover:bg-blue-50 rounded-2xl p-5 shadow-lg border border-gray-200 transition flex flex-col justify-between"><div class="flex justify-between items-center mb-2"><h3 class="font-extrabold text-gray-900 text-base">{html.escape(cname)} County, AL</h3><span class="bg-blue-100 text-blue-700 text-xs font-bold px-2.5 py-0.5 rounded-full">{len(cities)} Areas</span></div><p class="text-xs text-gray-600">{html.escape(sample_names)}</p></a>'
        )

    c_idx_canon = "https://www.zoiriscleaningservices.com/counties/"
    c_idx_faqs = [
        {"q": "Does Zoiris Cleaning Services cover all 67 counties in Alabama?", "a": "Yes! Headquartered in Downtown Mobile, AL, Zoiris Cleaning Services provides residential house cleaning, deep cleaning, move-in/move-out turnovers, vacation rental turnovers, and commercial janitorial across all 67 Alabama counties and 503 municipalities with zero hidden travel fees."},
        {"q": "Which Alabama counties have priority same-day and 24/7 dispatch?", "a": "Mobile County and Baldwin County feature rapid 24/7 coastal and metro dispatch across 55 communities, with full scheduled coverage across Jefferson, Madison, Montgomery, Shelby, Tuscaloosa, Lee, Houston, Morgan, Baldwin, and every county statewide."}
    ]
    c_idx_body = f"""
    <section class="px-6 py-20 bg-transparent relative z-10">
      <div class="max-w-7xl mx-auto">
        <div id="ai-quick-answer" class="bg-white rounded-3xl p-6 sm:p-8 shadow-2xl border-2 border-blue-500/30 mb-14">
          <span class="inline-block bg-blue-100 text-blue-800 text-xs font-extrabold uppercase px-3 py-1 rounded-full mb-2">67-County Statewide Coverage Matrix</span>
          <h2 class="text-2xl sm:text-3xl font-extrabold text-gray-900 mb-3">Every County in Alabama Served — Select Your County Below</h2>
          <p class="text-sm sm:text-base text-gray-700 leading-relaxed">
            Browse all <strong>67 Alabama counties</strong> from Autauga to Winston to access local city cleaning branches, USPS ZIP code coverage, county-specific environmental cleaning protocols, and instant flat-rate estimates at <strong>(251) 220-2515</strong>.
          </p>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
{chr(10).join(cnt_cards)}
        </div>
      </div>
    </section>
{render_faq_details_html(c_idx_faqs, "Alabama County Coverage FAQs", "How statewide county dispatch, flat-rate pricing, and commercial janitorial work across Alabama.")}"""

    c_idx_html = render_shell_page(
        shell,
        "All 67 Alabama Counties Served | Local House & Commercial Cleaning | Zoiris",
        "Complete directory of all 67 Alabama counties served by Zoiris Cleaning Services — Mobile County, Baldwin County, Jefferson, Madison, Montgomery, Shelby & statewide. Call (251) 220-2515!",
        c_idx_canon,
        "Cleaning Services Across All 67 Alabama Counties",
        "Select your Alabama county below to view all local cities, ZIP codes, and 29 residential &amp; commercial cleaning services.",
        c_idx_body, faqs=c_idx_faqs, og_image="/images/service_areas.png"
    )
    write_atomic(os.path.join(cnt_root, "index.html"), c_idx_html)
    county_urls.append(c_idx_canon)

    # Individual 67 County Hubs
    for cname in ALL_67_ALABAMA_COUNTIES:
        cslug = county_to_slug(cname)
        cdir = os.path.join(cnt_root, cslug)
        os.makedirs(cdir, exist_ok=True)
        canon = f"https://www.zoiriscleaningservices.com/counties/{cslug}/"
        cities = sorted(by_county.get(cname, []), key=lambda x: x["city"])
        if not cities:
            cities = [LOCATIONS["mobile-al"]]

        all_zips = sorted({z for c in cities for z in c["zips"]})[:12]
        zips_str = ", ".join(all_zips)
        reg_key = cities[0].get("region", "mobile_metro")
        reg = REGION_PROFILES.get(reg_key, REGION_PROFILES["mobile_metro"])
        lead_city = cities[0]

        city_rows = "\n".join(
            f'                <tr class="hover:bg-blue-50/50"><td class="py-3 px-4 font-bold"><a href="/{c["slug"]}/" class="text-blue-700 hover:underline">{html.escape(c["display_title"])}</a></td><td class="py-3 px-4">{html.escape(", ".join(c["zips"][:3]))}</td><td class="py-3 px-4"><a href="/{c["slug"]}/house-cleaning/" class="text-indigo-600 hover:underline mr-2">Maid</a> • <a href="/{c["slug"]}/deep-cleaning/" class="text-indigo-600 hover:underline mr-2">Deep Clean</a> • <a href="/{c["slug"]}/move-out-cleaning/" class="text-indigo-600 hover:underline mr-2">Move-Out</a> • <a href="/{c["slug"]}/commercial-cleaning/" class="text-indigo-600 hover:underline">Commercial</a></td></tr>'
            for c in cities
        )

        srv_pills = "\n".join(
            f'            <a href="/{lead_city["slug"]}/{DET_MAP[lead_city["slug"]] if sk=="detailing" else sk}/" class="bg-white/10 hover:bg-white/20 border border-white/20 rounded-xl px-4 py-3 text-white text-xs sm:text-sm font-semibold flex justify-between items-center transition"><span>{html.escape(sv["short_name"])} in {html.escape(cname)} County</span><i class="fas fa-arrow-right text-blue-300 text-xs"></i></a>'
            for sk, sv in SERVICES.items()
        )

        c_faqs = [
            {"q": f"Which cities and communities in {cname} County, AL do you clean?", "a": f"Zoiris Cleaning Services covers all communities across {cname} County (ZIP codes {zips_str}), including " + ", ".join(c["city"] for c in cities) + "."},
            {"q": f"How much does house cleaning and deep cleaning cost in {cname} County, AL?", "a": f"Recurring maid visits in {cname} County typically range from $125–$215, top-to-bottom deep cleans from $220–$420, and empty-home move-in/move-out cleans from $250–$480—always flat-rate with zero contracts and zero travel surcharges."},
            {"q": f"How do your {cname} County crews handle local environmental challenges?", "a": f"Homes and facilities in {cname} County ({reg['label']}) experience {reg['climate']}. Our W-2 teams deploy 0.3-micron commercial HEPA vacuums and EPA-registered disinfectants focused on {reg['care_focus']}."},
            {"q": f"Do you provide commercial, medical, and post-construction cleaning in {cname} County?", "a": f"Yes! We provide insured commercial janitorial, OSHA/EPA medical & dental clinic sanitization, VCT floor stripping & waxing, gutter clearing, window cleaning, and post-construction cleanup throughout {cname} County. Call (251) 220-2515."}
        ]

        c_body = f"""
    <section class="px-6 py-20 bg-transparent relative z-10">
      <div class="max-w-6xl mx-auto">
        <div id="ai-quick-answer" class="bg-white rounded-3xl p-6 sm:p-8 shadow-2xl border-2 border-blue-500/30 mb-14">
          <div class="flex flex-wrap justify-between items-center gap-2 mb-3">
            <span class="bg-blue-100 text-blue-800 text-xs font-extrabold uppercase px-3 py-1 rounded-full">{html.escape(reg['label'])} • {len(cities)} Local Hubs</span>
            <a href="/counties/" class="text-xs font-bold text-blue-600 hover:underline">&larr; All 67 Alabama Counties</a>
          </div>
          <h2 class="text-2xl sm:text-3xl font-extrabold text-gray-900 mb-3">House Cleaning, Deep Cleaning &amp; Janitorial Across {html.escape(cname)} County, AL</h2>
          <p class="text-sm sm:text-base text-gray-700 leading-relaxed mb-6">
            <strong>Zoiris Cleaning Services</strong> serves homeowners, landlords, vacation-rental hosts, and commercial facilities across all <strong>{len(cities)} communities in {html.escape(cname)} County, Alabama</strong> (ZIP codes {html.escape(zips_str)}). Addressing {html.escape(reg['climate'])}, our background-checked W-2 crews deliver contract-free cleaning backed by our 24-hour 100% Re-Clean Guarantee.
          </p>
          <div class="overflow-x-auto rounded-2xl border border-gray-200">
            <table class="w-full text-left border-collapse text-xs sm:text-sm">
              <thead>
                <tr class="bg-slate-900 text-white">
                  <th class="py-3 px-4 font-bold">{html.escape(cname)} County City / Town</th>
                  <th class="py-3 px-4 font-bold">ZIP Codes</th>
                  <th class="py-3 px-4 font-bold">Direct Local Service Links</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200 bg-white text-gray-800">
{city_rows}
              </tbody>
            </table>
          </div>
        </div>

        <div class="bg-black/40 backdrop-blur-md border border-white/15 rounded-3xl p-6 sm:p-8">
          <h2 class="text-2xl font-extrabold text-white mb-2">All 29 Services Available in {html.escape(cname)} County, AL</h2>
          <p class="text-sm text-purple-200 mb-6">Flat-rate upfront quotes with zero travel fees anywhere in {html.escape(cname)} County:</p>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2.5">
{srv_pills}
          </div>
        </div>
      </div>
    </section>
{render_faq_details_html(c_faqs, f"Frequently Asked Questions — {cname} County, AL Cleaning", f"Coverage, pricing, and scheduling across {cname} County ({zips_str}).")}"""

        c_title = f"Cleaning Services in {cname} County, AL | Maid, Deep & Commercial | Zoiris"
        c_desc = f"Trusted house cleaning, deep cleaning, move-out turnovers & commercial janitorial across all {len(cities)} cities in {cname} County, AL (ZIP {zips_str[:25]}). No contracts! Call (251) 220-2515!"
        c_html = render_shell_page(
            shell, c_title, c_desc, canon,
            f"House & Commercial Cleaning in {cname} County, AL",
            f"Serving all {len(cities)} communities across {html.escape(cname)} County with vetted W-2 cleaners, HEPA filtration, and zero locked contracts.",
            c_body, faqs=c_faqs, og_image="/images/service_areas.png"
        )
        write_atomic(os.path.join(cdir, "index.html"), c_html)
        county_urls.append(canon)

    return county_urls

GUIDES_DATA = [
    {
        "slug": "house-cleaning-cost-guide-alabama",
        "title": "2026 House Cleaning Cost Guide in Alabama (Sq Ft & Room Rates) | Zoiris",
        "desc": "How much does house cleaning cost in Mobile, Birmingham, Huntsville & Alabama in 2026? Complete flat-rate pricing table by sq ft, bedrooms & service type + instant calculator!",
        "h1": "2026 House Cleaning & Maid Service Cost Guide (Alabama & Gulf Coast)",
        "sub": "Complete flat-rate pricing benchmarks by square footage, bedroom count, and cleaning type—plus an interactive instant estimate calculator.",
        "answer": "In Alabama (including Mobile, Baldwin County, Birmingham, Huntsville, and Montgomery), standard recurring house cleaning costs $125 to $225 per visit ($0.07–$0.12/sq ft), top-to-bottom deep cleaning costs $220 to $440 ($0.14–$0.22/sq ft), and empty-home move-in/move-out cleaning ranges from $250 to $495 depending on home size and bathroom count, with 10%–20% savings on weekly or bi-weekly plans.",
        "headers": ["Home Size / Layout", "Recurring Maid Visit", "Deep Cleaning", "Move-In / Move-Out", "2-Person Crew Time"],
        "rows": [
            ["1–2 Bed / 1–2 Bath (< 1,200 sq ft)", "$120 – $155", "$210 – $275", "$240 – $310", "1.5 – 3.0 Hours"],
            ["3 Bed / 2 Bath (1,200 – 2,000 sq ft)", "$145 – $190", "$265 – $350", "$295 – $390", "2.5 – 4.5 Hours"],
            ["4 Bed / 2.5–3 Bath (2,000 – 3,000 sq ft)", "$185 – $240", "$340 – $440", "$380 – $495", "3.5 – 5.5 Hours"],
            ["5+ Bed / Luxury Estate (3,200+ sq ft)", "$245 – $360+", "$450 – $680+", "$495 – $750+", "5.0 – 8.0 Hours"]
        ],
        "calculator": True,
        "related_srv": ["house-cleaning", "deep-cleaning", "move-out-cleaning", "move-in-cleaning"],
        "faqs": [
            {"q": "Is flat-rate house cleaning better than hourly maid pricing?", "a": "Yes. Flat-rate pricing guarantees you know the exact cost upfront before cleaning begins and ensures technicians clean until the entire room-by-room checklist is 100% finished rather than watching the clock."},
            {"q": "Why does the first cleaning cost more than recurring bi-weekly visits?", "a": "An initial deep clean removes months of accumulated baseboard dust, bathroom scale, blind dust, and kitchen grease. Once your home reaches maintenance standard, weekly or bi-weekly visits take half the time and cost significantly less."},
            {"q": "Are supplies, HEPA vacuums, and insurance included in Zoiris flat rates?", "a": "Yes—100%. Every Zoiris Cleaning Services quote includes commercial HEPA vacuums, sanitized microfiber pads, EPA-registered child/pet-safe cleaners, W-2 workers' comp, general liability insurance, and zero travel fees."}
        ]
    },
    {
        "slug": "ultimate-move-out-cleaning-checklist",
        "title": "Ultimate Move-Out Cleaning Checklist (Landlord Deposit Guide) | Zoiris",
        "desc": "Room-by-room landlord & property manager move-out cleaning checklist to get 100% of your security deposit back. Kitchens, ovens, fridges, baths, baseboards & floors!",
        "h1": "The Ultimate Landlord-Approved Move-Out Cleaning Checklist",
        "sub": "Every exact inspection point Alabama landlords, apartment managers, and realtors check before releasing your full security deposit.",
        "answer": "To pass a landlord move-out inspection and secure a 100% security deposit refund, tenants must empty and wipe inside all cabinets, drawers, and closets; degrease the oven interior, drip pans, range hood, and refrigerator shelves; descale shower glass, tubs, and toilets; wet-wash all baseboards, blinds, and door frames; remove wall scuffs; and vacuum and mop every floor edge-to-edge.",
        "headers": ["Inspection Zone", "Critical Deposit-Risk Items", "Required Standard to Pass Walkthrough"],
        "rows": [
            ["Kitchen & Appliances", "Inside oven racks/glass, fridge drawers, microwave, hood filter", "Zero baked-on carbon grease, crumbs, food spills, or odors"],
            ["Cabinets & Pantries", "Upper/lower shelves, silverware drawers, under-sink plumbing bay", "Vacuumed crumb-free and wiped with food-safe disinfectant"],
            ["Bathrooms & Grout", "Shower glass soap scum, toilet base/ring, exhaust fan grille, vanity", "Descaled streak-free glass, sanitized porcelain & dust-free fan"],
            ["Walls, Trim & Windows", "Baseboards, door frames, light switches, blinds, window tracks", "Hand-wiped trim, dead bugs vacuumed from sills & scuffs erased"],
            ["Floors, Closets & Garage", "Wire closet racks, carpet edges, laundry hookups, garage sweep", "HEPA-vacuumed tack edges, residue-free mopped hard floors"]
        ],
        "calculator": False,
        "related_srv": ["move-out-cleaning", "move-in-cleaning", "carpet-cleaning", "property-management-janitorial"],
        "faqs": [
            {"q": "What is the #1 reason landlords deduct cleaning fees from security deposits?", "a": "Skipped appliance interiors (baked-on oven grease and sticky refrigerator crisper bins), dusty baseboards/blinds, and bathroom shower soap scum account for over 80% of security deposit cleaning deductions."},
            {"q": "Should move-out cleaning happen before or after movers load the truck?", "a": "Always schedule move-out cleaning after 100% of boxes and furniture are removed so crews have unobstructed access to closet floors, baseboards, wall edges, and cabinet shelves."},
            {"q": "Does Zoiris provide an itemized move-out cleaning receipt for my landlord?", "a": "Yes! We provide an itemized completion invoice documenting appliance interior, cabinet, bathroom, and floor sanitization—backed by our 24-hour Walkthrough Re-Clean Guarantee."}
        ]
    },
    {
        "slug": "deep-cleaning-vs-regular-cleaning",
        "title": "Deep Cleaning vs. Regular House Cleaning: Full Comparison Chart | Zoiris",
        "desc": "What is the difference between a deep clean and a regular clean? Side-by-side 20-point task comparison chart, time differences, pricing & when your home needs each.",
        "h1": "Deep Cleaning vs. Regular House Cleaning: What's the Real Difference?",
        "sub": "A side-by-side room-by-room breakdown of standard recurring maid maintenance versus restorative top-to-bottom deep scrubbing.",
        "answer": "Regular house cleaning maintains weekly or bi-weekly surface hygiene—sanitizing countertops, sinks, toilets, showers, mirrors, and vacuuming/mopping floors. Deep cleaning adds intensive vertical and detail labor: hand-washing baseboards, doors, window frames, and blinds; descaling heavy shower grout and mineral buildup; degreasing range hoods; and dusting ceiling fan blades and HVAC vents.",
        "headers": ["Cleaning Task / Surface", "Regular Recurring Clean", "Top-to-Bottom Deep Clean"],
        "rows": [
            ["Baseboards, Door Frames & Wainscoting", "Dry micro-dusted on rotation", "Hand-scrubbed wet to remove grime & scuffs"],
            ["Window Blinds, Sills & Lock Ledges", "Light surface dusting", "Individual slat wiping & deep sill washing"],
            ["Bathroom Tile Grout & Glass Doors", "Routine disinfectant wipe & rinse", "Acid-free mineral descaling & grout brush scrub"],
            ["Kitchen Stovetop, Range Hood & Microwave", "Exterior wipe + interior microwave", "Heavy hood-filter degreasing, burner & backsplash scrub"],
            ["Ceiling Fans, Light Fixtures & Air Vents", "Reachable cobweb clearing", "Hand-wiped fan blades & HEPA vent register detailing"]
        ],
        "calculator": False,
        "related_srv": ["deep-cleaning", "house-cleaning", "detailing", "carpet-cleaning"],
        "faqs": [
            {"q": "Do I need a deep clean before starting bi-weekly maid service?", "a": "If your home has not been professionally cleaned within the past 45 days, starting with a one-time Deep Clean resets baseboards, grout, and buildup so ongoing bi-weekly visits stay affordable and fast."},
            {"q": "How often does an average Alabama home need a deep clean?", "a": "Most households schedule a comprehensive deep clean twice per year—once in late spring after live-oak/pine pollen season and once before autumn/holiday hosting."}
        ]
    },
    {
        "slug": "airbnb-turnover-cleaning-checklist",
        "title": "5-Star Airbnb & Vacation Rental Turnover Cleaning Checklist | Zoiris",
        "desc": "Complete 10 AM–3 PM Airbnb & VRBO beach/condo turnover cleaning checklist for Superhosts. Zero-hair bathroom protocol, linen staging, sand removal & inventory table!",
        "h1": "5-Star Airbnb & Vacation Rental Turnover Checklist (Superhost Protocol)",
        "sub": "How top Gulf Shores, Orange Beach, Dauphin Island, and Alabama hosts achieve 5.0-star Cleanliness ratings inside tight 10 AM–3 PM windows.",
        "answer": "A 5-star Airbnb turnover requires six synchronized steps between 10:00 AM checkout and 3:00 PM check-in: immediate damage and left-item photo logging, stripping and laundering/swapping par-stock bed and bath linens, food-free refrigerator and dishwasher reset, LED zero-hair bathroom sterilization, HEPA sand and pet-dander floor extraction, and staged welcome amenities verified by timestamped host photos.",
        "headers": ["Turnover Phase (10 AM – 3 PM)", "Superhost Critical Checkpoints", "Guest Review Protection Goal"],
        "rows": [
            ["1. 10:00 AM Arrival Walk", "Check smart lock, thermostat, broken items, smoke odors & under beds", "Immediate claim documentation before cleaning starts"],
            ["2. Linen & Bed Staging", "Inspect mattress protectors, lint-roll pillows, crisp hospital corners", "Hotel-crisp presentation matching hero listing photos"],
            ["3. Bathroom Zero-Hair Audit", "Sanitize tub/toilet/vanity, clear drain hair, polish glass & roll towels", "Eliminates the #1 cause of 3-star Airbnb reviews"],
            ["4. Kitchen & Coffee Reset", "Empty fridge, unload clean dishes, wipe microwave/crumbs, restock pods", "Spotless Move-In-Ready kitchen & starter supplies"],
            ["5. Floors, Patio & Photo Sign-Off", "Agitated HEPA sand extraction, balcony glass wipe & 8 staging photos", "Remote host peace of mind prior to 3:00 PM check-in"]
        ],
        "calculator": False,
        "related_srv": ["airbnb-cleaning", "vacation-rental-cleaning", "airbnb-vacation-rental-management", "laundry-services"],
        "faqs": [
            {"q": "How many sets of sheets and towels should an Airbnb host keep on site?", "a": "Always maintain 3 full par sets per bed and guest (1 on the bed, 1 in wash/turnover rotation, and 1 backup locked in the owner closet) to guarantee fast same-day 10 AM–3 PM turnovers."},
            {"q": "Can Zoiris sync directly with my Airbnb, VRBO, or Guesty calendar?", "a": "Yes! We sync directly with host booking calendars and send timestamped staging photos after every checkout across Gulf Shores, Orange Beach, Fort Morgan, Dauphin Island, Mobile, Fairhope, and statewide."}
        ]
    },
    {
        "slug": "commercial-office-cleaning-checklist-pricing",
        "title": "Commercial Office & Medical Cleaning Pricing & Checklist Guide | Zoiris",
        "desc": "2026 commercial cleaning & office janitorial pricing per sq ft in Alabama + daily, weekly & monthly scope matrix for offices, clinics, banks & warehouses.",
        "h1": "Commercial Cleaning & Office Janitorial Pricing + Scope Matrix",
        "sub": "Facility manager's guide to commercial janitorial rates, OSHA/EPA List N clinical disinfection standards, and daily/weekly custodial schedules.",
        "answer": "Commercial office and facility cleaning in Alabama typically costs $0.08 to $0.20 per square foot per visit (or $250 to $1,800+ per month for recurring 1x–5x weekly schedules), depending on restroom count, foot traffic, floor types (VCT vs. carpet), and whether clinical EPA List N medical disinfection is required.",
        "headers": ["Facility Type", "Recommended Frequency", "Key Sanitation Focus", "Billing Structure"],
        "rows": [
            ["Corporate & Law/CPA Offices", "1x – 5x Weekly (After-Hours)", "Workstations, conference glass, breakrooms & restrooms", "Flat Monthly Rate (No Lock-In)"],
            ["Medical, Dental & Urgent Care", "Nightly Terminal Clean", "EPA List N dwell-time exam room & waiting room disinfection", "Clinical Flat Monthly + Logs"],
            ["Retail, Banks & Dealerships", "3x – 7x Weekly", "Entry glass, showroom VCT/tile shine & customer restrooms", "Flat Monthly + Quarterly Floor Care"],
            ["Industrial & Warehouses", "Weekly / Shift-Window", "Concrete auto-scrubbing, shop locker rooms & shipping offices", "Custom Per-Shift or Monthly"]
        ],
        "calculator": False,
        "related_srv": ["commercial-cleaning", "office-janitorial-services", "janitorial-cleaning-services", "medical-dental-facility-cleaning", "floor-stripping-waxing"],
        "faqs": [
            {"q": "Does Zoiris provide a Certificate of Insurance (COI) and W-9 for commercial properties?", "a": "Yes, same day. Zoiris Cleaning Services LLC carries comprehensive general liability insurance and full workers' compensation for our uniformed W-2 staff."},
            {"q": "Are commercial janitorial agreements locked into 1-year or 3-year contracts?", "a": "Never. Unlike national franchise brokers that trap businesses in punitive auto-renewing contracts, Zoiris earns your business every month with transparent, flexible terms."}
        ]
    },
    {
        "slug": "remove-red-clay-mildew-hard-water-stains",
        "title": "How to Remove Alabama Red Clay, Gulf Mildew & Hard-Water Stains | Zoiris",
        "desc": "Pro cleaning chemistry guide: safely remove iron-rich Alabama red clay from carpet/grout, Gulf Coast bathroom mildew, hard-water shower glass scale & pine pollen.",
        "h1": "Removing Alabama Red Clay, Coastal Mildew, Hard-Water Scale & Pollen",
        "sub": "Field-tested stain chemistry from Zoiris technicians for Alabama's toughest regional soil, humidity, and mineral challenges.",
        "answer": "Iron-rich Alabama red clay requires dry HEPA vacuuming first followed by a neutral detergent and tannin/iron spotter—never hot bleach, which sets iron oxide permanently. Subtropical bathroom mildew responds best to EPA-registered peroxide or botanical thymol disinfectants with a full 10-minute dwell time, while cloudy shower glass requires acid-free mineral descalers rather than abrasive pads.",
        "headers": ["Regional Stain / Buildup", "What NOT to Use (Damages Surface)", "Pro Technician Removal Method"],
        "rows": [
            ["Alabama Red Clay (Carpet & Grout)", "Chlorine bleach or rubbing wet mud deeper", "Dry vacuum loose soil -> iron/surfactant pre-treat -> hot-water rinse"],
            ["Gulf Humidity Shower Mildew", "Painting over damp caulk or quick wipe", "10-min EPA antimicrobial dwell -> nylon grout scrub -> dry airflow"],
            ["Hard-Water Glass & Chrome Scale", "Steel wool or green scouring pads (scratches!)", "Non-abrasive chelated mineral descaler + #0000 bronze wool / squeegee"],
            ["Yellow Pine & Live-Oak Pollen", "Dry feather dusters (launches spores airborne)", "0.3-micron sealed HEPA vacuum + damp microfiber capture"]
        ],
        "calculator": False,
        "related_srv": ["carpet-cleaning", "deep-cleaning", "pressure-washing", "window-cleaning"],
        "faqs": [
            {"q": "Why do red clay stains turn permanent orange when cleaned with household cleaners?", "a": "Alabama red clay gets its color from iron oxide (rust). Alkaline soaps with bleach oxidize and bond iron particles into nylon carpet and porous grout unless treated with a proper iron-reducing stain agent and hot-water extraction."}
        ]
    },
    {
        "slug": "post-construction-cleaning-checklist-phases",
        "title": "3-Phase Post-Construction Cleaning Checklist (Rough, Final & Touch-Up) | Zoiris",
        "desc": "Complete contractor & homeowner post-construction cleaning checklist covering Phase 1 Rough Clean, Phase 2 Final Detail Clean & Phase 3 Owner Walkthrough Polish.",
        "h1": "3-Phase Post-Construction & Renovation Cleaning Checklist",
        "sub": "How general contractors, custom home builders, and remodelers eliminate ultrafine drywall gypsum dust for Certificate of Occupancy & handover.",
        "answer": "Professional post-construction cleanup is executed in three sequential phases: Phase 1 (Rough Clean) removes construction debris, floor ram-board, and window manufacturer stickers; Phase 2 (Final Detail Clean) performs top-down sealed HEPA extraction of drywall dust inside every vent, cabinet hinge, drawer track, baseboard, and fixture; Phase 3 (Touch-Up Clean) polishes glass and floors after final punch-list trades exit.",
        "headers": ["Construction Phase", "Timing on Schedule", "Core Deliverables"],
        "rows": [
            ["Phase 1: Rough Clean", "After framing, drywall & rough trades", "Debris sweep, ram-board removal, sticker/plastic peel & rough HEPA vac"],
            ["Phase 2: Final Detail Clean", "After paint, cabinets, tile & fixtures", "Walls/ceilings dusted, cabinet/drawer interiors HEPA vacuumed, grout-haze buff & glass razor-safe wash"],
            ["Phase 3: Punch-List Touch-Up", "24–48 hrs before owner closing/CO", "Final footprint/dust removal, stainless/mirror polish & white-glove inspection"]
        ],
        "calculator": False,
        "related_srv": ["post-construction-cleanup", "window-cleaning", "floor-stripping-waxing", "pressure-washing"],
        "faqs": [
            {"q": "Why can't regular shop vacs clean post-construction drywall dust?", "a": "Standard shop vacs exhaust ultrafine sub-micron gypsum dust right back into the room air, where it settles back onto cabinets and floors 12 hours later. Sealed 0.3-micron commercial HEPA extractors trap 99.97% of fine dust permanently."}
        ]
    },
    {
        "slug": "carpet-steam-cleaning-vs-shampooing-guide",
        "title": "Carpet Steam Cleaning (Hot-Water Extraction) vs. Shampooing Guide | Zoiris",
        "desc": "Why carpet manufacturers require hot-water extraction (steam cleaning) over rotary shampooing or bonnet cleaning—dry times, pet odor enzymes & upholstery care.",
        "h1": "Hot-Water Extraction Steam Cleaning vs. Carpet Shampooing & Dry Bonnet",
        "sub": "Compare residue levels, allergen removal, drying times, and Shaw/Mohawk carpet warranty requirements.",
        "answer": "Major carpet mills (including Shaw and Mohawk) recommend hot-water extraction ('steam cleaning') because 200°F pressurized water and high-lift vacuum suction flush both deep-embedded grit and cleaning solution out of the carpet pile. Traditional rotary shampooing leaves sticky soap residue that attracts dirt rapidly, while dry bonnet pads only buff the top 15% of fibers.",
        "headers": ["Carpet Method", "Soil & Allergen Depth", "Soap Residue Risk", "Typical Dry Time"],
        "rows": [
            ["Hot-Water Extraction (Steam)", "100% down to primary backing", "Zero residue (pH-balanced rinse)", "3 – 5 Hours"],
            ["Bio-Enzyme + Steam (Pet Odors)", "Penetrates sub-pad urine crystals", "Zero residue + odor molecule breakdown", "4 – 6 Hours"],
            ["Rotary Foam Shampooing", "Top 40% of pile", "High sticky soap re-soiling risk", "8 – 24 Hours"],
            ["Dry Bonnet / Encapsulation", "Surface 15%–25% commercial maintenance", "Low (interim commercial use only)", "1 – 2 Hours"]
        ],
        "calculator": False,
        "related_srv": ["carpet-cleaning", "deep-cleaning", "move-out-cleaning", "detailing"],
        "faqs": [
            {"q": "Can hot-water steam extraction also clean microfiber and linen sofas?", "a": "Yes! Using a low-moisture shear-flow upholstery hand tool and fabric-matched pH solutions, steam extraction lifts body oils, pet dander, and beverage spills from sofas, sectionals, dining chairs, and mattresses without over-wetting cushions."}
        ]
    },
    {
        "slug": "soft-washing-vs-pressure-washing-guide",
        "title": "Soft Washing vs. Pressure Washing: Safe Exterior PSI Chart | Zoiris",
        "desc": "Never blast vinyl siding or stucco with 3,000 PSI! See the complete Soft Washing vs. Pressure Washing PSI & biodegradable algaecide chart for homes & driveways.",
        "h1": "Soft Washing vs. Pressure Washing: Safe PSI Chart by Exterior Surface",
        "sub": "Protect vinyl siding, Hardie plank, brick mortar, stucco, and wood decks while eliminating green algae and black mildew at the root.",
        "answer": "High-pressure washing (2,500–3,500 PSI with a rotary surface cleaner) should only be used on cured concrete driveways, sidewalks, and commercial aprons. House siding (vinyl, Hardie plank, painted brick, stucco, and soffits) must be soft-washed at under 100 PSI using biodegradable algaecide surfactants that kill mold and Gloeocapsa algae spores without forcing water behind siding or etching paint.",
        "headers": ["Exterior Surface", "Safe Method", "Operating Pressure", "Why It Matters"],
        "rows": [
            ["Vinyl, Hardie Plank & Stucco Siding", "Low-Pressure Soft Wash", "60 – 100 PSI", "Prevents blown window seals, oxidation streaks & water intrusion"],
            ["Concrete Driveways & Sidewalks", "Rotary Surface Pressure Wash", "2,500 – 3,500 PSI", "Lifts embedded black algae, tire marks & red clay without wand stripes"],
            ["Wood Decks & Privacy Fences", "Gentle Wash + Brightener", "500 – 800 PSI", "Cleans gray weathered fibers without splintering soft pine/cedar"],
            ["Rooftop Solar Panels & Windows", "0-TDS Deionized Pure Water", "Garden-pressure brush", "Zero mineral spots & 100% manufacturer warranty compliance"]
        ],
        "calculator": False,
        "related_srv": ["pressure-washing", "window-cleaning", "gutter-cleaning", "solar-panel-cleaning"],
        "faqs": [
            {"q": "Is soft-wash solution safe around azaleas, camellias, and coastal landscaping?", "a": "Yes—when performed by trained technicians who pre-saturate all surrounding foliage and soil with fresh water before application, apply targeted low-drift nozzles, and perform a thorough post-rinse."}
        ]
    },
    {
        "slug": "home-cleaning-frequency-schedule-chart",
        "title": "Home Cleaning Schedule Chart: Daily, Weekly, Monthly & Seasonal | Zoiris",
        "desc": "How often should you clean sheets, bathrooms, baseboards, carpets, gutters & windows? Printable room-by-room cleaning frequency chart for healthy homes.",
        "h1": "How Often Should Everything in Your Home Be Cleaned? (Master Chart)",
        "sub": "Evidence-based hygiene and indoor-air-quality schedule covering daily touchpoints, weekly maid tasks, monthly upkeep, and seasonal deep care.",
        "answer": "For healthy indoor air quality and surface hygiene, kitchen counters and dishes require daily wiping; bathrooms, bed sheets, high-touch handles, and HEPA vacuuming/mopping should be completed weekly (or bi-weekly for lower-traffic homes); microwaves, fridge shelves, and ceiling fans monthly; baseboards, blinds, and ovens quarterly; and carpet steam extraction, window washing, and gutter clearing every 6 months.",
        "headers": ["Frequency Tier", "Surfaces & Items Included", "Professional Zoiris Service Match"],
        "rows": [
            ["Weekly / Bi-Weekly", "Toilets, showers, sinks, mirrors, kitchen counters, bed sheets, HEPA floors", "Recurring House Cleaning & Maid Service"],
            ["Monthly", "Appliance exteriors, microwave interior, ceiling fans, intake vents & laundry closets", "Recurring Maid + Rotational Detail"],
            ["Every 3–6 Months", "Wet-washed baseboards, window blinds, grout descaling, oven & fridge interiors", "Top-to-Bottom Deep Cleaning"],
            ["Twice Per Year (Spring & Fall)", "Hot-water carpet/rug steam clean, interior/exterior windows, gutters & soft wash", "Carpet, Window, Gutter & Soft-Wash Bundle"]
        ],
        "calculator": False,
        "related_srv": ["house-cleaning", "deep-cleaning", "carpet-cleaning", "gutter-cleaning", "window-cleaning"],
        "faqs": [
            {"q": "Is weekly or bi-weekly maid service better for homes with pets or allergies?", "a": "Households with indoor dogs/cats, young children, or seasonal pollen allergies benefit strongly from weekly 0.3-micron HEPA vacuuming and damp microfiber dusting, while couples and smaller households often prefer bi-weekly service."}
        ]
    }
]

CALC_WIDGET_HTML = """
        <div class="bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 rounded-3xl p-6 sm:p-8 text-white shadow-2xl border border-blue-400/30 mb-14">
          <h2 class="text-2xl sm:text-3xl font-extrabold mb-2"><i class="fas fa-calculator text-blue-400 mr-2"></i>Interactive Instant Cleaning Price &amp; Time Estimator</h2>
          <p class="text-sm text-purple-200 mb-6">Adjust your home size and service type for an instant ballpark flat-rate range (no email required):</p>
          <div class="grid grid-cols-1 sm:grid-cols-4 gap-4 mb-6">
            <div>
              <label class="block text-xs uppercase font-bold text-blue-300 mb-1" for="calcBeds">Bedrooms</label>
              <select id="calcBeds" onchange="runCostCalc()" class="w-full rounded-xl bg-white text-gray-900 font-bold p-3 text-sm">
                <option value="1">1 Bedroom</option>
                <option value="2">2 Bedrooms</option>
                <option value="3" selected>3 Bedrooms</option>
                <option value="4">4 Bedrooms</option>
                <option value="5">5+ Bedrooms</option>
              </select>
            </div>
            <div>
              <label class="block text-xs uppercase font-bold text-blue-300 mb-1" for="calcBaths">Bathrooms</label>
              <select id="calcBaths" onchange="runCostCalc()" class="w-full rounded-xl bg-white text-gray-900 font-bold p-3 text-sm">
                <option value="1">1 Bathroom</option>
                <option value="2" selected>2 Bathrooms</option>
                <option value="3">3 Bathrooms</option>
                <option value="4">4+ Bathrooms</option>
              </select>
            </div>
            <div>
              <label class="block text-xs uppercase font-bold text-blue-300 mb-1" for="calcType">Service Type</label>
              <select id="calcType" onchange="runCostCalc()" class="w-full rounded-xl bg-white text-gray-900 font-bold p-3 text-sm">
                <option value="1.0" selected>Recurring Maid Clean</option>
                <option value="1.75">Top-to-Bottom Deep Clean</option>
                <option value="1.95">Empty Move-In / Move-Out</option>
                <option value="1.3">Airbnb / Vacation Turnover</option>
              </select>
            </div>
            <div>
              <label class="block text-xs uppercase font-bold text-blue-300 mb-1" for="calcFreq">Frequency Discount</label>
              <select id="calcFreq" onchange="runCostCalc()" class="w-full rounded-xl bg-white text-gray-900 font-bold p-3 text-sm">
                <option value="0.85">Weekly (Save 15%)</option>
                <option value="0.92" selected>Bi-Weekly (Save 8%)</option>
                <option value="0.96">Monthly (Save 4%)</option>
                <option value="1.0">One-Time Clean</option>
              </select>
            </div>
          </div>
          <div class="bg-white/10 border border-white/20 rounded-2xl p-5 flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
              <p class="text-xs uppercase font-bold text-blue-300">Estimated Flat-Rate Range (Zero Contracts)</p>
              <p id="calcOutPrice" class="text-3xl font-extrabold text-white mt-1">$145 – $185</p>
              <p id="calcOutTime" class="text-xs text-purple-200 mt-1">Est. 2-Person Crew Duration: 2.5 – 3.5 Hours • All Supplies &amp; HEPA Vacuums Included</p>
            </div>
            <div class="flex gap-3">
              <a href="tel:2512202515" class="bg-white text-blue-800 font-extrabold px-5 py-3 rounded-xl text-sm shadow hover:bg-gray-100 transition">Lock Exact Rate: (251) 220-2515</a>
              <a href="#quote" class="bg-blue-600 text-white font-extrabold px-5 py-3 rounded-xl text-sm shadow hover:bg-blue-500 transition">Book Online &rarr;</a>
            </div>
          </div>
          <script>
            function runCostCalc() {
              var beds = parseInt(document.getElementById('calcBeds').value, 10);
              var baths = parseInt(document.getElementById('calcBaths').value, 10);
              var mult = parseFloat(document.getElementById('calcType').value);
              var freq = parseFloat(document.getElementById('calcFreq').value);
              var base = 85 + (beds * 18) + (baths * 22);
              var low = Math.round((base * mult * freq) / 5) * 5;
              var high = Math.round((low * 1.24) / 5) * 5;
              var hrsLow = Math.max(1.5, ((1.1 + beds * 0.35 + baths * 0.35) * (mult > 1.5 ? 1.55 : 1.0))).toFixed(1);
              var hrsHigh = (parseFloat(hrsLow) + 1.2).toFixed(1);
              document.getElementById('calcOutPrice').textContent = '$' + low + ' – $' + high;
              document.getElementById('calcOutTime').textContent = 'Est. 2-Person Crew Duration: ' + hrsLow + ' – ' + hrsHigh + ' Hours • All Supplies & HEPA Vacuums Included';
            }
          </script>
        </div>"""

def build_guides_and_blog(shell):
    print("Building /guides/ hub + 10 AI-Overview Authority Guides + upgrading /mobile-al/blog/...")
    guide_urls = []
    g_root = os.path.join(root_dir, "guides")
    os.makedirs(g_root, exist_ok=True)

    cards = []
    for g in GUIDES_DATA:
        cards.append(f"""          <a href="/guides/{g['slug']}/" class="bg-white rounded-2xl p-6 shadow-xl border border-gray-100 hover:-translate-y-1 transition flex flex-col justify-between">
            <div>
              <span class="inline-block bg-indigo-100 text-indigo-800 text-xs font-extrabold uppercase px-3 py-1 rounded-full mb-3">Expert Guide &amp; Matrix</span>
              <h3 class="text-xl font-extrabold text-gray-900 mb-2">{html.escape(g['h1'])}</h3>
              <p class="text-sm text-gray-600 leading-relaxed mb-4">{html.escape(g['sub'])}</p>
            </div>
            <span class="text-blue-600 font-bold text-sm">Read Full Guide &amp; Chart &rarr;</span>
          </a>""")

    g_idx_canon = "https://www.zoiriscleaningservices.com/guides/"
    g_idx_body = f"""
    <section class="px-6 py-20 bg-transparent relative z-10">
      <div class="max-w-6xl mx-auto">
        <div id="ai-quick-answer" class="bg-white rounded-3xl p-6 sm:p-8 shadow-2xl border-2 border-blue-500/30 mb-12">
          <h2 class="text-2xl sm:text-3xl font-extrabold text-gray-900 mb-2">Alabama Cleaning Cost Calculators, Checklists &amp; Pro Stain Guides</h2>
          <p class="text-sm sm:text-base text-gray-700">
            Published by the field supervisors at <strong>Zoiris Cleaning Services LLC</strong>—explore transparent 2026 cleaning pricing tables, landlord move-out inspection sheets, Superhost Airbnb protocols, and safe PSI/stain chemistry charts.
          </p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
{chr(10).join(cards)}
        </div>
      </div>
    </section>"""

    g_idx_html = render_shell_page(
        shell,
        "Cleaning Cost Guides, Checklists & Stain Charts | Zoiris Cleaning",
        "2026 house cleaning cost calculator, landlord move-out checklists, deep vs regular cleaning tables, Airbnb turnover guides & Alabama stain removal charts.",
        g_idx_canon,
        "Cleaning Pricing Guides, Checklists & Expert Charts",
        "Transparent cost benchmarks, printable inspection matrices, and technician-tested surface care guides.",
        g_idx_body
    )
    write_atomic(os.path.join(g_root, "index.html"), g_idx_html)
    guide_urls.append(g_idx_canon)

    # Also upgrade /mobile-al/blog/index.html so it showcases all 10 authority guides!
    blog_canon = "https://www.zoiriscleaningservices.com/mobile-al/blog/"
    blog_html = render_shell_page(
        shell,
        "Cleaning Tips, Pricing Guides & Checklists | Zoiris Cleaning Blog",
        "Official Zoiris Cleaning Services resource hub: 2026 house cleaning cost guide, move-out checklists, Airbnb turnover systems & Gulf Coast humidity care.",
        blog_canon,
        "Zoiris Cleaning Resource Center & Expert Blog",
        "Actionable checklists, transparent pricing guides, and Alabama surface-care expertise from our professional cleaning crews.",
        g_idx_body
    )
    write_atomic(os.path.join(root_dir, "mobile-al", "blog", "index.html"), blog_html)

    # Build each of the 10 individual guides
    for g in GUIDES_DATA:
        gdir = os.path.join(g_root, g["slug"])
        os.makedirs(gdir, exist_ok=True)
        canon = f"https://www.zoiriscleaningservices.com/guides/{g['slug']}/"

        ths = "".join(f'<th class="py-3.5 px-4 font-bold">{html.escape(h)}</th>' for h in g["headers"])
        trs = []
        for row in g["rows"]:
            tds = "".join(
                f'<td class="py-3.5 px-4 {"font-bold text-gray-900" if idx==0 else "text-gray-700"}">{html.escape(cell)}</td>'
                for idx, cell in enumerate(row)
            )
            trs.append(f'                <tr class="hover:bg-blue-50/50">{tds}</tr>')

        rel_srv_links = "\n".join(
            f'            <a href="/services/{sk}/" class="bg-white/95 hover:bg-blue-50 rounded-xl p-4 shadow font-bold text-sm text-gray-900 flex justify-between items-center"><span>{html.escape(SERVICES[sk]["name"])}</span><i class="fas fa-arrow-right text-blue-600"></i></a>'
            for sk in g["related_srv"] if sk in SERVICES
        )
        other_guides = "\n".join(
            f'            <a href="/guides/{og["slug"]}/" class="bg-white/10 hover:bg-white/20 border border-white/20 rounded-xl p-4 text-white text-sm font-semibold flex justify-between items-center"><span>{html.escape(og["h1"])}</span><i class="fas fa-arrow-right text-blue-300 shrink-0 ml-2"></i></a>'
            for og in GUIDES_DATA if og["slug"] != g["slug"]
        )
        city_jump = "\n".join(
            f'            <a href="/{cslug}/" class="bg-blue-600/30 hover:bg-blue-600/50 border border-blue-300/30 text-white text-xs font-bold px-3.5 py-2 rounded-full transition">{cname}</a>'
            for cslug, cname in [
                ("mobile-al", "Mobile, AL"), ("semmes-al", "Semmes, AL"), ("theodore-al", "Theodore, AL"),
                ("saraland-al", "Saraland, AL"), ("daphne-al", "Daphne, AL"), ("fairhope-al", "Fairhope, AL"),
                ("foley-al", "Foley, AL"), ("gulf-shores-al", "Gulf Shores, AL"), ("orange-beach-al", "Orange Beach, AL"),
                ("birmingham-al", "Birmingham, AL"), ("huntsville-al", "Huntsville, AL"), ("montgomery-al", "Montgomery, AL"),
                ("tuscaloosa-al", "Tuscaloosa, AL"), ("auburn-al", "Auburn, AL"), ("dothan-al", "Dothan, AL")
            ]
        )

        calc_block = CALC_WIDGET_HTML if g.get("calculator") else ""
        g_body = f"""
    <article class="px-6 py-20 bg-transparent relative z-10">
      <div class="max-w-5xl mx-auto">
        <div class="mb-6 text-xs sm:text-sm text-blue-200 font-semibold flex flex-wrap gap-2">
          <a href="/" class="hover:text-white underline">Home</a><span>/</span>
          <a href="/guides/" class="hover:text-white underline">Cleaning Guides</a><span>/</span>
          <span class="text-white">{html.escape(g['h1'])}</span>
        </div>

        <div id="ai-quick-answer" class="bg-white rounded-3xl p-6 sm:p-8 shadow-2xl border-2 border-blue-500/30 mb-12">
          <span class="inline-flex items-center gap-2 bg-blue-100 text-blue-800 text-xs font-extrabold uppercase px-3 py-1 rounded-full mb-3">
            <i class="fas fa-bolt"></i> Key Takeaway &amp; Direct Answer (Updated {TODAY})
          </span>
          <h2 class="text-2xl sm:text-3xl font-extrabold text-gray-900 mb-3">{html.escape(g['h1'])} — Quick Summary</h2>
          <p class="text-base text-gray-800 leading-relaxed mb-6">
            {html.escape(g['answer'])}
          </p>
          <div class="overflow-x-auto rounded-2xl border border-gray-200">
            <table class="w-full text-left border-collapse text-xs sm:text-sm">
              <thead>
                <tr class="bg-slate-900 text-white">{ths}</tr>
              </thead>
              <tbody class="divide-y divide-gray-200 bg-white">
{chr(10).join(trs)}
              </tbody>
            </table>
          </div>
        </div>

{calc_block}

        <div class="bg-black/40 backdrop-blur-md border border-white/15 rounded-3xl p-6 sm:p-8 mb-12">
          <h2 class="text-2xl font-extrabold text-white mb-4">Book Matching Professional Cleaning Services</h2>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-6">
{rel_srv_links}
          </div>
          <h3 class="text-sm font-bold uppercase tracking-wider text-blue-300 mb-3">Instant Local Dispatch Across Alabama:</h3>
          <div class="flex flex-wrap gap-2">
{city_jump}
            <a href="/locations/" class="bg-white text-blue-900 text-xs font-extrabold px-3.5 py-2 rounded-full">All 503 AL Cities &rarr;</a>
          </div>
        </div>

        <div class="bg-black/30 backdrop-blur-md border border-white/15 rounded-3xl p-6 sm:p-8">
          <h2 class="text-xl font-extrabold text-white mb-4">More Cleaning Pricing &amp; Checklist Guides</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
{other_guides}
          </div>
        </div>
      </div>
    </article>
{render_faq_details_html(g['faqs'], f"Frequently Asked Questions: {g['h1']}", "Direct expert answers from Zoiris Cleaning Services field supervisors.")}"""

        g_html = render_shell_page(
            shell, g["title"], g["desc"], canon, g["h1"], html.escape(g["sub"]),
            g_body, faqs=g["faqs"], extra_article_schema=True
        )
        write_atomic(os.path.join(gdir, "index.html"), g_html)
        guide_urls.append(canon)

    return guide_urls

def build_ai_llms_rss_indexnow_and_sitemaps(pillar_urls, county_urls, guide_urls):
    print("Generating /llms.txt, /llms-full.txt, /feed.xml, IndexNow key file, robots.txt, and 5-tier sitemaps...")

    # 1. /llms.txt & /llms-full.txt (AI Search / Gemini / ChatGPT / Perplexity / Claude Grounding Standard)
    llms_txt = f"""# Zoiris Cleaning Services LLC

> Zoiris Cleaning Services LLC is a licensed, bonded, and insured residential and commercial cleaning company headquartered in Downtown Mobile, Alabama (ZIP 36602), serving Mobile, Semmes, Theodore, Saraland, Baldwin County (Daphne, Fairhope, Spanish Fort, Foley, Gulf Shores, Orange Beach, Fort Morgan), Birmingham, Huntsville, Montgomery, Tuscaloosa, Auburn, and all 67 counties / 503 municipalities across the State of Alabama.

## Core Facts & Contact
- **Phone (24/7 Dispatch & Instant Flat-Rate Quotes):** (251) 220-2515 (`+1-251-220-2515`)
- **Email:** zoiriscleaningservices@gmail.com
- **Website:** https://www.zoiriscleaningservices.com/
- **Contract Policy:** 100% No Locked Contracts, Zero Rescheduling Penalties, Zero Travel Surcharges
- **Staffing & Safety:** Vetted, background-checked W-2 employees (never unscreened gig subcontractors); Commercial 0.3-micron HEPA filtration vacuums; EPA-registered child- and pet-safe disinfectants; Full General Liability & Workers' Compensation Insurance
- **Guarantee:** 24-Hour 100% Re-Clean Satisfaction Guarantee

## Typical Alabama Flat-Rate Cleaning Benchmarks (2026)
- **Recurring House Cleaning & Maid Service:** $125–$225 per visit (Weekly, Bi-Weekly, Monthly)
- **Top-to-Bottom Deep Cleaning:** $220–$440 flat rate
- **Move-In / Move-Out Empty-Home Turnover:** $250–$495 flat rate (Landlord Deposit Checklist)
- **Airbnb & Vacation Rental Same-Day Turnover (10 AM–3 PM):** $140–$340 per turnover
- **Commercial, Office & Medical/Dental Janitorial:** Custom flat monthly or per-visit pricing ($0.08–$0.20/sq ft)

## Primary Hubs & Directories
- [Homepage — Mobile, AL House Cleaning & Maid Service](https://www.zoiriscleaningservices.com/)
- [All 29 Cleaning Services Master Catalog](https://www.zoiriscleaningservices.com/services/)
- [All 67 Alabama Counties Directory](https://www.zoiriscleaningservices.com/counties/)
- [All 503 Alabama Cities & ZIP Codes Directory](https://www.zoiriscleaningservices.com/locations/)
- [Cleaning Cost Calculator, Checklists & Stain Guides](https://www.zoiriscleaningservices.com/guides/)

## High-Demand Pricing & Checklist Guides
""" + "\n".join(f"- [{g['h1']}](https://www.zoiriscleaningservices.com/guides/{g['slug']}/): {g['answer']}" for g in GUIDES_DATA) + "\n"

    write_atomic(os.path.join(root_dir, "llms.txt"), llms_txt)

    llms_full = llms_txt + "\n## Complete 29 Specialized Cleaning Services\n" + "\n".join(
        f"- **{sv['name']}** (`https://www.zoiriscleaningservices.com/services/{sk}/`): {sv['short_description']} Equipment: {sv['equipment']}"
        for sk, sv in SERVICES.items()
    ) + "\n\n## All 67 Alabama County Hubs\n" + "\n".join(
        f"- [{c} County, AL Cleaning Services](https://www.zoiriscleaningservices.com/counties/{county_to_slug(c)}/)"
        for c in ALL_67_ALABAMA_COUNTIES
    ) + "\n"
    write_atomic(os.path.join(root_dir, "llms-full.txt"), llms_full)

    # 2. IndexNow Verification Key File
    write_atomic(os.path.join(root_dir, f"{INDEXNOW_KEY}.txt"), INDEXNOW_KEY)

    # 3. Valid RSS 2.0 Feed (/feed.xml) for Rapid Googlebot Feed/WebSub Discovery!
    rss_items = []
    rss_sources = [
        ("House Cleaning & Maid Service in Mobile, AL | Zoiris Cleaning Services", "https://www.zoiriscleaningservices.com/", "24/7 flat-rate, no-contract house cleaning, deep cleaning, move turnovers & commercial janitorial across Mobile, Baldwin County & Alabama."),
        ("All 29 Residential & Commercial Cleaning Services in Alabama", "https://www.zoiriscleaningservices.com/services/", "Complete catalog of 29 cleaning services across all 67 Alabama counties."),
        ("All 67 Alabama Counties Cleaning Coverage Directory", "https://www.zoiriscleaningservices.com/counties/", "County-by-county cleaning service directory across Alabama."),
        ("All 503 Alabama Cities & Service Areas", "https://www.zoiriscleaningservices.com/locations/", "Searchable A-Z directory of all 503 Alabama cities and USPS ZIP codes served by Zoiris.")
    ]
    for g in GUIDES_DATA:
        rss_sources.append((g["title"], f"https://www.zoiriscleaningservices.com/guides/{g['slug']}/", g["answer"]))
    for sk, sv in SERVICES.items():
        rss_sources.append((f"{sv['name']} in Alabama", f"https://www.zoiriscleaningservices.com/services/{sk}/", sv["short_description"]))
    for v in sorted([x for x in LOCATIONS.values() if x["sitemap_tier"] in ("priority", "metros")], key=lambda z: z["city"]):
        rss_sources.append((f"Cleaning Services in {v['display_title']} ({v['county']})", f"https://www.zoiriscleaningservices.com/{v['slug']}/", f"Professional residential & commercial cleaning in {v['display_title']} (ZIP {v['primary_zip']})."))

    pub_rfc = "Tue, 17 Nov 2026 12:00:00 +0000"
    for r_title, r_link, r_desc in rss_sources:
        rss_items.append(f"""    <item>
      <title>{html.escape(r_title)}</title>
      <link>{r_link}</link>
      <guid isPermaLink="true">{r_link}</guid>
      <pubDate>{pub_rfc}</pubDate>
      <description>{html.escape(r_desc)}</description>
    </item>""")

    feed_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Zoiris Cleaning Services — Alabama Cleaning Guides, Pricing &amp; Local Hubs</title>
    <link>https://www.zoiriscleaningservices.com/</link>
    <description>Official service updates, 2026 cleaning cost guides, checklists, and local coverage across Mobile, Baldwin County, and all 67 Alabama counties.</description>
    <language>en-us</language>
    <lastBuildDate>{pub_rfc}</lastBuildDate>
    <atom:link href="https://www.zoiriscleaningservices.com/feed.xml" rel="self" type="application/rss+xml" />
    <atom:link href="https://pubsubhubbub.appspot.com/" rel="hub" />
{chr(10).join(rss_items)}
  </channel>
</rss>
"""
    write_atomic(os.path.join(root_dir, "feed.xml"), feed_xml)

    # 4. Write sitemap_pillars_guides.xml + update sitemap_index.xml & robots.txt
    authority_urls = pillar_urls + county_urls + guide_urls
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in authority_urls:
        lines.append(f'  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>')
    lines.append('</urlset>\n')
    write_atomic(os.path.join(root_dir, "sitemap_pillars_guides.xml"), "\n".join(lines))
    print(f"  -> Wrote sitemap_pillars_guides.xml ({len(authority_urls)} URLs)")

    child_sitemaps = [
        "https://www.zoiriscleaningservices.com/sitemap_pillars_guides.xml",
        "https://www.zoiriscleaningservices.com/sitemap_priority.xml",
        "https://www.zoiriscleaningservices.com/sitemap_metros.xml",
        "https://www.zoiriscleaningservices.com/sitemap_regions_north.xml",
        "https://www.zoiriscleaningservices.com/sitemap_regions_south.xml",
    ]
    idx_lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for sm in child_sitemaps:
        idx_lines.append(f'  <sitemap><loc>{sm}</loc><lastmod>{TODAY}</lastmod></sitemap>')
    idx_lines.append('</sitemapindex>\n')
    idx_xml = "\n".join(idx_lines)
    write_atomic(os.path.join(root_dir, "sitemap_index.xml"), idx_xml)
    write_atomic(os.path.join(root_dir, "sitemap.xml"), idx_xml)

    # Explicitly welcome Googlebot, Google-Extended (AI Overviews / Gemini), GPTBot, OAI-SearchBot, PerplexityBot, ClaudeBot, Bingbot!
    robots_txt = """User-agent: Googlebot
Allow: /
Disallow: /seo/
Disallow: /dashboard.html
Disallow: /Gallery/Dash.html
Disallow: /404.html

User-agent: Google-Extended
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: *
Allow: /
Disallow: /seo/
Disallow: /dashboard.html
Disallow: /Gallery/Dash.html
Disallow: /404.html

Sitemap: https://www.zoiriscleaningservices.com/sitemap_index.xml
"""
    write_atomic(os.path.join(root_dir, "robots.txt"), robots_txt)
    print("  -> Updated robots.txt welcoming Googlebot, Google-Extended (AI Overviews), OAI-SearchBot, PerplexityBot, ClaudeBot & Bingbot!")

def main():
    shell = load_shell_template()
    pillar_urls = build_service_pillars(shell)
    county_urls = build_county_hubs(shell)
    guide_urls = build_guides_and_blog(shell)
    build_ai_llms_rss_indexnow_and_sitemaps(pillar_urls, county_urls, guide_urls)
    print(f"EXTREME AUTHORITY EXPANSION BUILT: {len(pillar_urls)} Service Pillars + {len(county_urls)} County Hubs + {len(guide_urls)} AI-Overview Guides = {len(pillar_urls)+len(county_urls)+len(guide_urls)} new high-authority pages!")

if __name__ == "__main__":
    main()

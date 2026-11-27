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
    county_to_slug, render_faq_details_html, build_jsonld_schema,
    is_indexable_service_subpage
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
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Downtown Mobile",
            "addressLocality": "Mobile",
            "addressRegion": "AL",
            "postalCode": "36602",
            "addressCountry": "US"
        },
        "geo": {"@type": "GeoCoordinates", "latitude": 30.6954, "longitude": -88.0399},
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
        "publisher": {"@id": "https://www.zoiriscleaningservices.com/#organization"},
        "potentialAction": {
            "@type": "SearchAction",
            "target": {
                "@type": "EntryPoint",
                "urlTemplate": "https://www.zoiriscleaningservices.com/locations/?q={search_term_string}"
            },
            "query-input": "required name=search_term_string"
        }
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
        sec_map = {"services": "All Cleaning Services", "counties": "Alabama Counties", "guides": "Cleaning Checklists & Guides"}
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
                View Scope, Checklist &amp; Cities &rarr;
              </a>
            </div>
          </div>""")

    idx_faqs = [
        {"q": "What types of residential and commercial cleaning services does Zoiris offer across Alabama?", "a": "Zoiris Cleaning Services offers 29 specialized services across all 67 Alabama counties—including recurring house cleaning & maid service, top-to-bottom deep cleaning, move-in/move-out turnovers, Airbnb & vacation rental turnovers, commercial office & medical janitorial, VCT floor stripping & waxing, carpet & upholstery steam cleaning, pure-water window & solar panel washing, gutter clearing, and soft-wash pressure washing."},
        {"q": "Do any of your 29 cleaning services require a long-term contract?", "a": "No. Every residential, commercial, and vacation-rental service is 100% contract-free with zero cancellation or rescheduling penalties."},
        {"q": "Are all Zoiris cleaning technicians W-2 employees and insured?", "a": "Yes. Every crew member is a background-checked, uniformed W-2 employee covered by comprehensive general liability insurance and workers' compensation."},
        {"q": "How do I book any cleaning service in Alabama with Zoiris?", "a": "Submit our online booking form on this page, explore our room-by-room cleaning checklists, or call our team directly at (251) 220-2515 to schedule your service."}
    ]
    idx_body = f"""
    <section class="px-6 py-20 bg-transparent relative z-10">
      <div class="max-w-7xl mx-auto">
        <div id="ai-quick-answer" class="bg-white rounded-3xl p-6 sm:p-8 shadow-2xl border-2 border-blue-500/30 mb-14">
          <span class="inline-block bg-blue-100 text-blue-800 text-xs font-extrabold uppercase px-3 py-1 rounded-full mb-2">Complete 29-Service Master Directory</span>
          <h2 class="text-2xl sm:text-3xl font-extrabold text-gray-900 mb-3">Complete Residential, Commercial &amp; Turnover Cleaning Catalog</h2>
          <p class="text-sm sm:text-base text-gray-700 leading-relaxed">
            <strong>Zoiris Cleaning Services LLC</strong> executes <strong>29 specialized interior and exterior cleaning protocols</strong> across <strong>Mobile, Semmes, Theodore, Baldwin County, Birmingham, Huntsville, Montgomery, and all 503 Alabama communities</strong>. Every service includes commercial HEPA filtration, EPA-registered disinfectants, custom room-by-room checklists, zero locked contracts, and our 100% Re-Clean Satisfaction Guarantee.
          </p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-7">
{chr(10).join(cards)}
        </div>
      </div>
    </section>
{render_faq_details_html(idx_faqs, "Frequently Asked Questions About Our 29 Cleaning Services", "Answers on service combinations, commercial COI documentation, equipment, and statewide booking.")}"""

    idx_canon = "https://www.zoiriscleaningservices.com/services/"
    idx_html = render_shell_page(
        shell,
        "All 29 Residential & Commercial Cleaning Services in Alabama | Zoiris",
        "Explore all 29 house cleaning, deep cleaning, move-out, Airbnb turnover, medical/commercial janitorial, carpet, window & pressure washing services across Alabama. Book at (251) 220-2515!",
        idx_canon,
        "29 Specialized Cleaning Services Across Alabama",
        "<strong>No-Contract</strong> residential housekeeping, commercial janitorial, vacation-rental turnovers, and exterior washing across all 67 Alabama counties — book with us today.",
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
            f'            <a href="{("/" + v["slug"] + "/" + (DET_MAP[v["slug"]] if sk=="detailing" else sk) + "/") if is_indexable_service_subpage(v["slug"], sk, DET_MAP[v["slug"]] if sk=="detailing" else sk) else ("/" + v["slug"] + "/")}" class="bg-white/10 hover:bg-white/20 border border-white/20 rounded-xl px-4 py-2.5 text-white text-xs sm:text-sm font-semibold flex justify-between items-center transition"><span>{html.escape(sv["short_name"] + " in " + v["city"] + ", AL" if is_indexable_service_subpage(v["slug"], sk, DET_MAP[v["slug"]] if sk=="detailing" else sk) else v["city"] + ", AL Cleaning Hub")}</span><span class="text-purple-200 text-xs">{html.escape(v["county_short"])} Co.</span></a>'
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
            <a href="/guides/house-cleaning-cost-guide-alabama/" class="text-xs font-bold text-blue-600 hover:underline">Open Custom Cleaning Plan Builder &rarr;</a>
          </div>
          <h2 class="text-2xl sm:text-3xl font-extrabold text-gray-900 mb-3">{html.escape(sv['name'])}: Complete Scope, Equipment &amp; Execution Matrix</h2>
          <p class="text-sm sm:text-base text-gray-700 leading-relaxed mb-6">
            <strong>{html.escape(sv['name'])}</strong> by Zoiris Cleaning Services is designed for <em>{html.escape(sv['ideal_for'].lower())}</em> across Mobile, Baldwin County, and all 67 Alabama counties. Using <strong>{html.escape(sv['equipment'].lower())}</strong>, our W-2 insured teams deliver contract-free service ({html.escape(sv['cadence'])}) backed by our 100% Re-Clean Satisfaction Guarantee.
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
          <p class="text-sm text-purple-200 mb-6">Select your local Gulf Coast branch for neighborhood-specific scheduling &amp; online booking:</p>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2.5">
{gulf_city_links}
          </div>
        </div>

        <div class="bg-black/35 backdrop-blur-md border border-white/15 rounded-3xl p-6 sm:p-8">
          <h2 class="text-2xl font-extrabold text-white mb-2">{html.escape(sv['short_name'])} in Major Alabama Metros ({len(metro_locs)} Cities)</h2>
          <p class="text-sm text-purple-200 mb-6">Direct statewide dispatch with zero locked contracts and easy online booking:</p>
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

        p_title = f"{sv['name']} in Alabama | Checklist & Local Branches | Zoiris"
        p_desc = f"Professional {sv['short_name'].lower()} across Mobile, Semmes, Theodore, Gulf Shores, Birmingham, Huntsville & all 67 AL counties. See full 6-step checklist & book at (251) 220-2515!"
        p_html = render_shell_page(
            shell, p_title, p_desc, canon,
            f"{sv['name']} Across Alabama",
            f"Vetted W-2 specialists, {html.escape(sv['cadence'].lower())}, zero locked contracts, and our 100% Re-Clean Satisfaction Guarantee.",
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
        {"q": "Which Alabama counties have priority local dispatch?", "a": "Mobile County and Baldwin County feature rapid coastal and metro dispatch across 55 communities, with full scheduled coverage across Jefferson, Madison, Montgomery, Shelby, Tuscaloosa, Lee, Houston, Morgan, and every county statewide."}
    ]
    c_idx_body = f"""
    <section class="px-6 py-20 bg-transparent relative z-10">
      <div class="max-w-7xl mx-auto">
        <div id="ai-quick-answer" class="bg-white rounded-3xl p-6 sm:p-8 shadow-2xl border-2 border-blue-500/30 mb-14">
          <span class="inline-block bg-blue-100 text-blue-800 text-xs font-extrabold uppercase px-3 py-1 rounded-full mb-2">67-County Statewide Coverage Matrix</span>
          <h2 class="text-2xl sm:text-3xl font-extrabold text-gray-900 mb-3">Every County in Alabama Served — Select Your County Below</h2>
          <p class="text-sm sm:text-base text-gray-700 leading-relaxed">
            Browse all <strong>67 Alabama counties</strong> from Autauga to Winston to access local city cleaning branches, USPS ZIP code coverage, county-specific environmental cleaning protocols, and direct booking online or at <strong>(251) 220-2515</strong>.
          </p>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
{chr(10).join(cnt_cards)}
        </div>
      </div>
    </section>
{render_faq_details_html(c_idx_faqs, "Alabama County Coverage FAQs", "How statewide county dispatch, zero-contract scheduling, and commercial janitorial work across Alabama.")}"""

    c_idx_html = render_shell_page(
        shell,
        "All 67 Alabama Counties Served | Local House & Commercial Cleaning | Zoiris",
        "Complete directory of all 67 Alabama counties served by Zoiris Cleaning Services — Mobile County, Baldwin County, Jefferson, Madison, Montgomery, Shelby & statewide. Book at (251) 220-2515!",
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

        def _city_srv_cell(c):
            links = []
            for sk_i, lbl_i in [("house-cleaning", "Maid"), ("deep-cleaning", "Deep Clean"), ("move-out-cleaning", "Move-Out"), ("commercial-cleaning", "Commercial")]:
                u_i = f'/{c["slug"]}/{sk_i}/' if is_indexable_service_subpage(c["slug"], sk_i, sk_i) else f'/services/{sk_i}/'
                links.append(f'<a href="{u_i}" class="text-indigo-600 hover:underline mr-2">{lbl_i}</a>')
            return " • ".join(links)

        city_rows = "\n".join(
            f'                <tr class="hover:bg-blue-50/50"><td class="py-3 px-4 font-bold"><a href="/{c["slug"]}/" class="text-blue-700 hover:underline">{html.escape(c["display_title"])}</a></td><td class="py-3 px-4">{html.escape(", ".join(c["zips"][:3]))}</td><td class="py-3 px-4">{_city_srv_cell(c)}</td></tr>'
            for c in cities
        )

        srv_pills = "\n".join(
            f'            <a href="{("/" + lead_city["slug"] + "/" + (DET_MAP[lead_city["slug"]] if sk=="detailing" else sk) + "/") if is_indexable_service_subpage(lead_city["slug"], sk, DET_MAP[lead_city["slug"]] if sk=="detailing" else sk) else ("/services/" + sk + "/")}" class="bg-white/10 hover:bg-white/20 border border-white/20 rounded-xl px-4 py-3 text-white text-xs sm:text-sm font-semibold flex justify-between items-center transition"><span>{html.escape(sv["short_name"])}</span><i class="fas fa-arrow-right text-blue-300 text-xs"></i></a>'
            for sk, sv in SERVICES.items()
        )

        c_faqs = [
            {"q": f"Which cities and communities in {cname} County, AL do you clean?", "a": f"Zoiris Cleaning Services covers all communities across {cname} County (ZIP codes {zips_str}), including " + ", ".join(c["city"] for c in cities) + "."},
            {"q": f"How do I schedule house cleaning or deep cleaning in {cname} County, AL?", "a": f"Book directly through our online scheduling form or call our team at (251) 220-2515 to reserve recurring maid visits, top-to-bottom deep cleans, or empty-home move-in/move-out turnovers across {cname} County—always with zero locked contracts and zero travel surcharges."},
            {"q": f"How do your {cname} County crews handle local environmental challenges?", "a": f"Homes and facilities in {cname} County ({reg['label']}) experience {reg['climate']}. Our W-2 teams deploy 0.3-micron commercial HEPA vacuums and EPA-registered disinfectants focused on {reg['care_focus']}."},
            {"q": f"Do you provide commercial, medical, and post-construction cleaning in {cname} County?", "a": f"Yes! We provide insured commercial janitorial, OSHA/EPA medical & dental clinic sanitization, VCT floor stripping & waxing, gutter clearing, window cleaning, and post-construction cleanup throughout {cname} County. Call (251) 220-2515 to book."}
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
            <strong>Zoiris Cleaning Services</strong> serves homeowners, landlords, vacation-rental hosts, and commercial facilities across all <strong>{len(cities)} communities in {html.escape(cname)} County, Alabama</strong> (ZIP codes {html.escape(zips_str)}). Addressing {html.escape(reg['climate'])}, our background-checked W-2 crews deliver contract-free cleaning backed by our 100% Re-Clean Satisfaction Guarantee.
          </p>
          <div class="overflow-x-auto rounded-2xl border border-gray-200">
            <table class="w-full text-left border-collapse text-xs sm:text-sm">
              <thead>
                <tr class="bg-slate-900 text-white">
                  <th class="py-3 px-4 font-bold">{html.escape(cname)} County City / Town</th>
                  <th class="py-3 px-4 font-bold">ZIP Codes</th>
                  <th class="py-3 px-4 font-bold">Core Cleaning Programs</th>
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
          <p class="text-sm text-purple-200 mb-6">Contract-free scheduling with zero travel fees anywhere in {html.escape(cname)} County:</p>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2.5">
{srv_pills}
          </div>
        </div>
      </div>
    </section>
{render_faq_details_html(c_faqs, f"Frequently Asked Questions — {cname} County, AL Cleaning", f"Coverage, checklists, and online booking across {cname} County ({zips_str}).")}"""

        c_title = f"Cleaning Services in {cname} County, AL | Maid, Deep & Commercial | Zoiris"
        c_desc = f"Trusted house cleaning, deep cleaning, move-out turnovers & commercial janitorial across all {len(cities)} cities in {cname} County, AL (ZIP {zips_str[:25]}). No contracts! Book at (251) 220-2515!"
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
        "title": "Custom House Cleaning Plan & Room Checklist Guide in Alabama | Zoiris",
        "desc": "Build your custom house cleaning plan in Mobile, Birmingham, Huntsville & Alabama! Compare room-by-room checklists by home layout, bedrooms & service type and book online!",
        "h1": "Custom House Cleaning Plan & Room-by-Room Checklist Builder",
        "sub": "Compare included cleaning checklists by home layout, bedroom count, and service level—plus build your custom cleaning plan online.",
        "answer": "Across Mobile, Baldwin County, Birmingham, Huntsville, Montgomery, and all 67 Alabama counties, Zoiris Cleaning Services tailors every residential cleaning plan to your exact home layout, bathroom count, and surface needs—offering recurring maid maintenance, restorative top-to-bottom deep cleaning, and empty-home move-in/move-out turnovers with zero locked contracts.",
        "headers": ["Home Size / Layout", "Recurring Maid Scope", "Deep Clean Upgrade", "Move-In / Move-Out Scope", "Ideal Property Match"],
        "rows": [
            ["1–2 Bed / 1–2 Bath (< 1,200 sq ft)", "Kitchen, baths, dusting & HEPA floors", "Wet-washed baseboards, blinds & grout", "Inside cabinets, drawers, oven & fridge", "Apartments, Condos & Cottages"],
            ["3 Bed / 2 Bath (1,200 – 2,000 sq ft)", "Full-home sanitization & microfiber care", "Hand-scrubbed trim, vents, fans & tile", "Complete landlord deposit inspection prep", "Standard Single-Family Homes"],
            ["4 Bed / 2.5–3 Bath (2,000 – 3,000 sq ft)", "Multi-bath sanitization & living areas", "Detailed woodwork, doors, sills & hood", "Full-property empty cabinet & closet reset", "Two-Story & Suburban Residences"],
            ["5+ Bed / Luxury Estate (3,200+ sq ft)", "Multi-crew stone, hardwood & suite care", "Top-to-bottom architectural detail scrub", "White-glove closing & relocation readiness", "Custom Estates & Waterfront Homes"]
        ],
        "plan_builder": True,
        "related_srv": ["house-cleaning", "deep-cleaning", "move-out-cleaning", "move-in-cleaning"],
        "faqs": [
            {"q": "How do you customize a cleaning plan for my Alabama home?", "a": "We match our room-by-room checklist to your bedroom and bathroom count, flooring types (hardwood, natural stone, tile, carpet), pets, and preferred recurring or one-time schedule so every surface is thoroughly completed."},
            {"q": "Should I book a Deep Clean for my first visit before starting recurring maid service?", "a": "An initial Top-to-Bottom Deep Clean removes accumulated baseboard dust, bathroom mineral scale, blind dust, and kitchen buildup so ongoing weekly or bi-weekly maintenance visits keep your home spotless."},
            {"q": "Are supplies, HEPA vacuums, and insurance included when I book with Zoiris?", "a": "Yes—100%. Every Zoiris Cleaning Services appointment includes commercial HEPA vacuums, sanitized microfiber pads, EPA-registered child/pet-safe cleaners, W-2 workers' comp, general liability insurance, and zero travel fees."}
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
        "plan_builder": False,
        "related_srv": ["move-out-cleaning", "move-in-cleaning", "carpet-cleaning", "property-management-janitorial"],
        "faqs": [
            {"q": "What is the #1 reason landlords deduct cleaning fees from security deposits?", "a": "Skipped appliance interiors (baked-on oven grease and sticky refrigerator crisper bins), dusty baseboards/blinds, and bathroom shower soap scum account for over 80% of security deposit cleaning deductions."},
            {"q": "Should move-out cleaning happen before or after movers load the truck?", "a": "Always schedule move-out cleaning after 100% of boxes and furniture are removed so crews have unobstructed access to closet floors, baseboards, wall edges, and cabinet shelves."},
            {"q": "Does Zoiris provide an itemized move-out cleaning receipt for my landlord?", "a": "Yes! We provide an itemized completion confirmation documenting appliance interior, cabinet, bathroom, and floor sanitization—backed by our 100% Walkthrough Re-Clean Satisfaction Guarantee."}
        ]
    },
    {
        "slug": "deep-cleaning-vs-regular-cleaning",
        "title": "Deep Cleaning vs. Regular House Cleaning: Full Comparison Chart | Zoiris",
        "desc": "What is the difference between a deep clean and a regular clean? Side-by-side 20-point room-by-room task comparison chart, surface checklists & when your home needs each.",
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
        "plan_builder": False,
        "related_srv": ["deep-cleaning", "house-cleaning", "detailing", "carpet-cleaning"],
        "faqs": [
            {"q": "Do I need a deep clean before starting bi-weekly maid service?", "a": "If your home has not been professionally cleaned within the past 45 days, starting with a one-time Deep Clean resets baseboards, grout, and buildup so ongoing bi-weekly visits stay thorough and consistent."},
            {"q": "How often does an average Alabama home need a deep clean?", "a": "Most households schedule a comprehensive deep clean twice per year—once in late spring after live-oak/pine pollen season and once before autumn/holiday hosting."}
        ]
    },
    {
        "slug": "airbnb-turnover-cleaning-checklist",
        "title": "5-Star Airbnb & Vacation Rental Turnover Cleaning Checklist | Zoiris",
        "desc": "Complete same-day Airbnb & VRBO beach/condo turnover cleaning checklist for Superhosts. Zero-hair bathroom protocol, linen staging, sand removal & inventory table!",
        "h1": "5-Star Airbnb & Vacation Rental Turnover Checklist (Superhost Protocol)",
        "sub": "How top Gulf Shores, Orange Beach, Dauphin Island, and Alabama hosts achieve 5.0-star Cleanliness ratings on back-to-back guest checkouts.",
        "answer": "A 5-star Airbnb turnover requires six synchronized steps between guest checkout and next-guest check-in: immediate damage and left-item photo logging, stripping and laundering/swapping par-stock bed and bath linens, food-free refrigerator and dishwasher reset, LED zero-hair bathroom sterilization, HEPA sand and pet-dander floor extraction, and staged welcome amenities verified by host photos.",
        "headers": ["Turnover Stage", "Superhost Critical Checkpoints", "Guest Review Protection Goal"],
        "rows": [
            ["1. Checkout Arrival Walk", "Check smart lock, thermostat, broken items, smoke odors & under beds", "Immediate claim documentation before cleaning starts"],
            ["2. Linen & Bed Staging", "Inspect mattress protectors, lint-roll pillows, crisp hospital corners", "Hotel-crisp presentation matching hero listing photos"],
            ["3. Bathroom Zero-Hair Audit", "Sanitize tub/toilet/vanity, clear drain hair, polish glass & roll towels", "Eliminates the #1 cause of 3-star Airbnb reviews"],
            ["4. Kitchen & Coffee Reset", "Empty fridge, unload clean dishes, wipe microwave/crumbs, restock pods", "Spotless guest-ready kitchen & starter supplies"],
            ["5. Floors, Patio & Photo Sign-Off", "Agitated HEPA sand extraction, balcony glass wipe & 8 staging photos", "Remote host peace of mind prior to guest check-in"]
        ],
        "plan_builder": False,
        "related_srv": ["airbnb-cleaning", "vacation-rental-cleaning", "airbnb-vacation-rental-management", "laundry-services"],
        "faqs": [
            {"q": "How many sets of sheets and towels should an Airbnb host keep on site?", "a": "Always maintain 3 full par sets per bed and guest (1 on the bed, 1 in wash/turnover rotation, and 1 backup locked in the owner closet) to guarantee seamless same-day guest turnovers."},
            {"q": "Can Zoiris sync directly with my Airbnb, VRBO, or Guesty calendar?", "a": "Yes! We sync directly with host booking calendars and send staging verification photos after every checkout across Gulf Shores, Orange Beach, Fort Morgan, Dauphin Island, Mobile, Fairhope, and statewide."}
        ]
    },
    {
        "slug": "commercial-office-cleaning-checklist-pricing",
        "title": "Commercial Office & Medical Cleaning Scope & Checklist Guide | Zoiris",
        "desc": "Commercial cleaning & office janitorial checklist in Alabama + daily, weekly & monthly scope matrix for offices, clinics, banks & warehouses.",
        "h1": "Commercial Cleaning & Office Janitorial Scope + Checklist Matrix",
        "sub": "Facility manager's guide to commercial janitorial checklists, OSHA/EPA List N clinical disinfection standards, and customizable custodial schedules.",
        "answer": "Commercial office and facility cleaning across Alabama is tailored to your building's square footage, restroom count, foot traffic, floor surfaces (VCT, tile, concrete, carpet), and clinical EPA List N disinfection requirements—with flexible recurring schedules and zero locked multi-year contracts.",
        "headers": ["Facility Type", "Recommended Cadence", "Key Sanitation Focus", "Service Plan Structure"],
        "rows": [
            ["Corporate & Law/CPA Offices", "1x – 5x Weekly", "Workstations, conference glass, breakrooms & restrooms", "Custom Recurring Plan (No Lock-In)"],
            ["Medical, Dental & Urgent Care", "Daily Terminal Clean", "EPA List N dwell-time exam room & waiting room disinfection", "Clinical Sanitization + Logs"],
            ["Retail, Banks & Dealerships", "3x – 7x Weekly", "Entry glass, showroom VCT/tile shine & customer restrooms", "Custom Plan + Periodic Floor Care"],
            ["Industrial & Warehouses", "Weekly / Scheduled", "Concrete auto-scrubbing, shop locker rooms & shipping offices", "Custom Facility Schedule"]
        ],
        "plan_builder": False,
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
        "answer": "Iron-rich Alabama red clay requires dry HEPA vacuuming first followed by a neutral detergent and tannin/iron spotter—never hot bleach, which sets iron oxide permanently. Subtropical bathroom mildew responds best to EPA-registered peroxide or botanical thymol disinfectants with full contact dwell coverage, while cloudy shower glass requires acid-free mineral descalers rather than abrasive pads.",
        "headers": ["Regional Stain / Buildup", "What NOT to Use (Damages Surface)", "Pro Technician Removal Method"],
        "rows": [
            ["Alabama Red Clay (Carpet & Grout)", "Chlorine bleach or rubbing wet mud deeper", "Dry vacuum loose soil -> iron/surfactant pre-treat -> hot-water rinse"],
            ["Gulf Humidity Shower Mildew", "Painting over damp caulk or quick wipe", "Full EPA antimicrobial dwell -> nylon grout scrub -> dry airflow"],
            ["Hard-Water Glass & Chrome Scale", "Steel wool or green scouring pads (scratches!)", "Non-abrasive chelated mineral descaler + #0000 bronze wool / squeegee"],
            ["Yellow Pine & Live-Oak Pollen", "Dry feather dusters (launches spores airborne)", "0.3-micron sealed HEPA vacuum + damp microfiber capture"]
        ],
        "plan_builder": False,
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
        "headers": ["Construction Phase", "Project Milestone", "Core Deliverables"],
        "rows": [
            ["Phase 1: Rough Clean", "After framing, drywall & rough trades", "Debris sweep, ram-board removal, sticker/plastic peel & rough HEPA vac"],
            ["Phase 2: Final Detail Clean", "After paint, cabinets, tile & fixtures", "Walls/ceilings dusted, cabinet/drawer interiors HEPA vacuumed, grout-haze buff & glass razor-safe wash"],
            ["Phase 3: Punch-List Touch-Up", "Prior to final owner walkthrough / CO", "Final footprint/dust removal, stainless/mirror polish & white-glove inspection"]
        ],
        "plan_builder": False,
        "related_srv": ["post-construction-cleanup", "window-cleaning", "floor-stripping-waxing", "pressure-washing"],
        "faqs": [
            {"q": "Why can't regular shop vacs clean post-construction drywall dust?", "a": "Standard shop vacs exhaust ultrafine sub-micron gypsum dust right back into the room air, where it settles back onto freshly cleaned cabinets and floors. Sealed 0.3-micron commercial HEPA extractors trap 99.97% of fine dust permanently."}
        ]
    },
    {
        "slug": "carpet-steam-cleaning-vs-shampooing-guide",
        "title": "Carpet Steam Cleaning (Hot-Water Extraction) vs. Shampooing Guide | Zoiris",
        "desc": "Why carpet manufacturers require hot-water extraction (steam cleaning) over rotary shampooing or bonnet cleaning—moisture recovery, pet odor enzymes & upholstery care.",
        "h1": "Hot-Water Extraction Steam Cleaning vs. Carpet Shampooing & Dry Bonnet",
        "sub": "Compare residue levels, allergen removal, moisture recovery, and Shaw/Mohawk carpet warranty requirements.",
        "answer": "Major carpet mills (including Shaw and Mohawk) recommend hot-water extraction ('steam cleaning') because 200°F pressurized water and high-lift vacuum suction flush both deep-embedded grit and cleaning solution out of the carpet pile. Traditional rotary shampooing leaves sticky soap residue that attracts dirt rapidly, while dry bonnet pads only buff the top 15% of fibers.",
        "headers": ["Carpet Method", "Soil & Allergen Depth", "Soap Residue Risk", "Moisture Recovery"],
        "rows": [
            ["Hot-Water Extraction (Steam)", "100% down to primary backing", "Zero residue (pH-balanced rinse)", "High-suction fast air-mover dry"],
            ["Bio-Enzyme + Steam (Pet Odors)", "Penetrates sub-pad urine crystals", "Zero residue + odor molecule breakdown", "Deep extraction + air circulation"],
            ["Rotary Foam Shampooing", "Top 40% of pile", "High sticky soap re-soiling risk", "Slow heavy moisture retention"],
            ["Dry Bonnet / Encapsulation", "Surface 15%–25% commercial maintenance", "Low (interim commercial use only)", "Low-moisture surface buff"]
        ],
        "plan_builder": False,
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
        "plan_builder": False,
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
        "plan_builder": False,
        "related_srv": ["house-cleaning", "deep-cleaning", "carpet-cleaning", "gutter-cleaning", "window-cleaning"],
        "faqs": [
            {"q": "Is weekly or bi-weekly maid service better for homes with pets or allergies?", "a": "Households with indoor dogs/cats, young children, or seasonal pollen allergies benefit strongly from weekly 0.3-micron HEPA vacuuming and damp microfiber dusting, while couples and smaller households often prefer bi-weekly service."}
        ]
    }
]

PLAN_BUILDER_HTML = """
        <div class="bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 rounded-3xl p-6 sm:p-8 text-white shadow-2xl border border-blue-400/30 mb-14">
          <h2 class="text-2xl sm:text-3xl font-extrabold mb-2"><i class="fas fa-clipboard-list text-blue-400 mr-2"></i>Interactive Custom Cleaning Plan &amp; Checklist Builder</h2>
          <p class="text-sm text-purple-200 mb-6">Select your home layout, cleaning type, and preferred schedule to preview your included checklist and book with us:</p>
          <div class="grid grid-cols-1 sm:grid-cols-4 gap-4 mb-6">
            <div>
              <label class="block text-xs uppercase font-bold text-blue-300 mb-1" for="planBeds">Bedrooms</label>
              <select id="planBeds" onchange="runPlanBuilder()" class="w-full rounded-xl bg-white text-gray-900 font-bold p-3 text-sm">
                <option value="1 Bedroom">1 Bedroom</option>
                <option value="2 Bedrooms">2 Bedrooms</option>
                <option value="3 Bedrooms" selected>3 Bedrooms</option>
                <option value="4 Bedrooms">4 Bedrooms</option>
                <option value="5+ Bedrooms">5+ Bedrooms</option>
              </select>
            </div>
            <div>
              <label class="block text-xs uppercase font-bold text-blue-300 mb-1" for="planBaths">Bathrooms</label>
              <select id="planBaths" onchange="runPlanBuilder()" class="w-full rounded-xl bg-white text-gray-900 font-bold p-3 text-sm">
                <option value="1 Bathroom">1 Bathroom</option>
                <option value="2 Bathrooms" selected>2 Bathrooms</option>
                <option value="3 Bathrooms">3 Bathrooms</option>
                <option value="4+ Bathrooms">4+ Bathrooms</option>
              </select>
            </div>
            <div>
              <label class="block text-xs uppercase font-bold text-blue-300 mb-1" for="planType">Service Type</label>
              <select id="planType" onchange="runPlanBuilder()" class="w-full rounded-xl bg-white text-gray-900 font-bold p-3 text-sm">
                <option value="maid" selected>Recurring Maid Clean</option>
                <option value="deep">Top-to-Bottom Deep Clean</option>
                <option value="move">Empty Move-In / Move-Out</option>
                <option value="airbnb">Airbnb / Vacation Turnover</option>
              </select>
            </div>
            <div>
              <label class="block text-xs uppercase font-bold text-blue-300 mb-1" for="planFreq">Preferred Schedule</label>
              <select id="planFreq" onchange="runPlanBuilder()" class="w-full rounded-xl bg-white text-gray-900 font-bold p-3 text-sm">
                <option value="Weekly Plan">Weekly Plan</option>
                <option value="Bi-Weekly Plan" selected>Bi-Weekly Plan</option>
                <option value="Monthly Plan">Monthly Plan</option>
                <option value="One-Time Visit">One-Time Visit</option>
              </select>
            </div>
          </div>
          <div class="bg-white/10 border border-white/20 rounded-2xl p-5 flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
              <p class="text-xs uppercase font-bold text-blue-300">Customized Cleaning Plan (Zero Locked Contracts)</p>
              <p id="planOutTitle" class="text-xl sm:text-2xl font-extrabold text-white mt-1">3 Bedrooms &bull; 2 Bathrooms &bull; Recurring Maid Clean (Bi-Weekly Plan)</p>
              <p id="planOutScope" class="text-xs sm:text-sm text-purple-200 mt-1">Includes full kitchen &amp; bathroom sanitization, microfiber dusting, 0.3-micron HEPA floor care &amp; all supplies.</p>
            </div>
            <div class="flex flex-wrap gap-3 shrink-0">
              <a href="tel:2512202515" class="bg-white text-blue-800 font-extrabold px-5 py-3 rounded-xl text-sm shadow hover:bg-gray-100 transition">Call (251) 220-2515</a>
              <a href="#quote" class="bg-blue-600 text-white font-extrabold px-5 py-3 rounded-xl text-sm shadow hover:bg-blue-500 transition">Book With Us &rarr;</a>
            </div>
          </div>
          <script>
            function runPlanBuilder() {
              var beds = document.getElementById('planBeds').value;
              var baths = document.getElementById('planBaths').value;
              var typeEl = document.getElementById('planType');
              var typeKey = typeEl.value;
              var typeTxt = typeEl.options[typeEl.selectedIndex].text;
              var freq = document.getElementById('planFreq').value;
              var scopes = {
                maid: 'Includes full kitchen & bathroom sanitization, microfiber dusting, 0.3-micron HEPA floor care & all supplies.',
                deep: 'Includes wet-washed baseboards, window blinds, HVAC vents, shower grout descaling, kitchen degreasing & HEPA floors.',
                move: 'Includes inside all cabinets, drawers, closets, oven & refrigerator interiors, baseboards & landlord walkthrough prep.',
                airbnb: 'Includes fresh par-stock linen staging, zero-hair bathroom reset, sand/allergen HEPA extraction & host staging photos.'
              };
              document.getElementById('planOutTitle').textContent = beds + ' • ' + baths + ' • ' + typeTxt + ' (' + freq + ')';
              document.getElementById('planOutScope').textContent = scopes[typeKey] || scopes.maid;
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
          <h2 class="text-2xl sm:text-3xl font-extrabold text-gray-900 mb-2">Alabama Cleaning Checklists, Custom Plan Builder &amp; Pro Stain Guides</h2>
          <p class="text-sm sm:text-base text-gray-700">
            Published by the field supervisors at <strong>Zoiris Cleaning Services LLC</strong>—explore room-by-room cleaning scope charts, landlord move-out inspection sheets, Superhost Airbnb protocols, and safe PSI/stain chemistry guides.
          </p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
{chr(10).join(cards)}
        </div>
      </div>
    </section>"""

    g_idx_html = render_shell_page(
        shell,
        "Cleaning Checklists, Scope Guides & Stain Charts | Zoiris Cleaning",
        "Custom house cleaning plan builder, landlord move-out checklists, deep vs regular cleaning tables, Airbnb turnover guides & Alabama stain removal charts.",
        g_idx_canon,
        "Cleaning Checklists, Scope Guides & Expert Charts",
        "Printable inspection matrices, custom room-by-room plans, and technician-tested surface care guides.",
        g_idx_body
    )
    write_atomic(os.path.join(g_root, "index.html"), g_idx_html)
    guide_urls.append(g_idx_canon)

    # Build a 100% unique Mobile Bay & Alabama Seasonal Cleaning Journal for /mobile-al/blog/index.html (zero body duplication with /guides/)!
    blog_canon = "https://www.zoiriscleaningservices.com/mobile-al/blog/"
    blog_faqs = [
        {"q": "How do Mobile and Baldwin County homeowners prevent live-oak pollen and humidity buildup indoors?", "a": "During Gulf Coast spring pollen blooms and humid summer months, sealed 0.3-micron commercial HEPA vacuuming paired with damp microfiber trim wiping and HVAC return-grille dusting prevents airborne allergens and bathroom mildew from taking hold."},
        {"q": "What is the best cleaning routine for historic Midtown Mobile and Fairhope hardwood floors?", "a": "Heart-pine and white-oak floors should never be steam-mopped or soaked. Our W-2 teams dry-extract grit with soft-bristle HEPA floor heads and damp-clean using pH-neutral Bona-standard wood cleaners."},
        {"q": "Where can I find printable room-by-room Zoiris checklists for deep cleaning and move-outs?", "a": "Explore our complete interactive Custom Cleaning Plan Builder and all 10 technical room-by-room checklists in our Alabama Cleaning Guides library."}
    ]
    blog_body = f"""
    <section class="px-6 py-20 bg-transparent relative z-10">
      <div class="max-w-6xl mx-auto">
        <div id="ai-quick-answer" class="bg-white rounded-3xl p-6 sm:p-8 shadow-2xl border-2 border-blue-500/30 mb-12">
          <span class="inline-block bg-blue-100 text-blue-800 text-xs font-extrabold uppercase px-3 py-1 rounded-full mb-2">Gulf Coast &amp; Statewide Field Notes</span>
          <h2 class="text-2xl sm:text-3xl font-extrabold text-gray-900 mb-3">Mobile Bay, Eastern Shore &amp; Alabama Seasonal Cleaning Insights</h2>
          <p class="text-sm sm:text-base text-gray-700 leading-relaxed">
            Written by the local W-2 field supervisors at <strong>Zoiris Cleaning Services LLC</strong> in Downtown Mobile, AL—discover regional home-care strategies tailored for Gulf Coast subtropical humidity, historic Spring Hill &amp; Midtown woodwork, Pleasure Island beach-sand extraction, and Piedmont red-clay protection.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <div class="bg-white rounded-2xl p-6 shadow-xl border border-gray-100 flex flex-col justify-between">
            <div>
              <span class="text-xs font-extrabold uppercase tracking-wider text-blue-600">Spring &amp; Summer Care • Mobile &amp; Daphne</span>
              <h3 class="text-lg font-extrabold text-gray-900 mt-1 mb-2">Beating Live-Oak Pollen &amp; Gulf Humidity Indoors</h3>
              <p class="text-sm text-gray-600 leading-relaxed mb-4">Why dry feather dusting spreads yellow pine and oak spores across vents—and how sealed 0.3-micron HEPA filtration plus EPA botanical bath sanitization keeps coastal homes fresh.</p>
            </div>
            <a href="/guides/remove-red-clay-mildew-hard-water-stains/" class="text-blue-700 font-bold text-sm hover:underline">Read Regional Stain &amp; Mildew Protocol &rarr;</a>
          </div>
          <div class="bg-white rounded-2xl p-6 shadow-xl border border-gray-100 flex flex-col justify-between">
            <div>
              <span class="text-xs font-extrabold uppercase tracking-wider text-indigo-600">Coastal Hosts • Gulf Shores &amp; Orange Beach</span>
              <h3 class="text-lg font-extrabold text-gray-900 mt-1 mb-2">Zero-Sand Condo &amp; Beach House Guest Turnovers</h3>
              <p class="text-sm text-gray-600 leading-relaxed mb-4">How Superhosts eliminate ultrafine quartz beach sand from LVP seams, descale salt-mist balcony sliders, and stage crisp par-stock linens between back-to-back bookings.</p>
            </div>
            <a href="/guides/airbnb-turnover-cleaning-checklist/" class="text-indigo-700 font-bold text-sm hover:underline">Open Superhost Turnover Checklist &rarr;</a>
          </div>
          <div class="bg-white rounded-2xl p-6 shadow-xl border border-gray-100 flex flex-col justify-between">
            <div>
              <span class="text-xs font-extrabold uppercase tracking-wider text-purple-600">Relocation &amp; Leasing • Statewide AL</span>
              <h3 class="text-lg font-extrabold text-gray-900 mt-1 mb-2">Passing Your Landlord Walkthrough on the First Try</h3>
              <p class="text-sm text-gray-600 leading-relaxed mb-4">From oven racks and refrigerator crisper bins to hand-wiped baseboards and blind slats—the exact inspection points property managers verify across Alabama.</p>
            </div>
            <a href="/guides/ultimate-move-out-cleaning-checklist/" class="text-purple-700 font-bold text-sm hover:underline">See Move-Out Inspection Checklist &rarr;</a>
          </div>
        </div>

        <div class="bg-black/40 backdrop-blur-md border border-white/15 rounded-3xl p-6 sm:p-8">
          <div class="flex flex-wrap justify-between items-center gap-3 mb-6">
            <h2 class="text-2xl font-extrabold text-white">Explore All 10 Technical Checklists &amp; Surface Guides</h2>
            <a href="/guides/" class="text-blue-300 hover:text-white text-sm font-bold underline">View Full Guides Hub &rarr;</a>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
{chr(10).join(cards)}
          </div>
        </div>
      </div>
    </section>
{render_faq_details_html(blog_faqs, "Mobile & Gulf Coast Home Care FAQs", "Local cleaning advice from Zoiris Cleaning Services in Mobile, AL.")}"""

    blog_html = render_shell_page(
        shell,
        "Mobile, AL Cleaning Blog & Seasonal Home Care Tips | Zoiris Cleaning",
        "Official Zoiris Cleaning Services Mobile, AL blog: Gulf Coast humidity & pollen tips, historic hardwood care, beach condo turnover guides & room checklists.",
        blog_canon,
        "Mobile, AL & Gulf Coast Cleaning Journal",
        "Local seasonal cleaning insights, coastal surface-care tips, and room-by-room checklists from our Downtown Mobile headquarters.",
        blog_body,
        faqs=blog_faqs
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

        plan_block = PLAN_BUILDER_HTML if g.get("plan_builder") else ""
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

{plan_block}

        <div class="bg-black/40 backdrop-blur-md border border-white/15 rounded-3xl p-6 sm:p-8 mb-12">
          <h2 class="text-2xl font-extrabold text-white mb-4">Book Matching Professional Cleaning Services</h2>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-6">
{rel_srv_links}
          </div>
          <h3 class="text-sm font-bold uppercase tracking-wider text-blue-300 mb-3">Local Dispatch Across Alabama — Select Your City:</h3>
          <div class="flex flex-wrap gap-2">
{city_jump}
            <a href="/locations/" class="bg-white text-blue-900 text-xs font-extrabold px-3.5 py-2 rounded-full">All 503 AL Cities &rarr;</a>
          </div>
        </div>

        <div class="bg-black/30 backdrop-blur-md border border-white/15 rounded-3xl p-6 sm:p-8">
          <h2 class="text-xl font-extrabold text-white mb-4">More Cleaning Checklist &amp; Care Guides</h2>
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

## Core Facts & Direct Booking
- **Phone:** (251) 220-2515 (`+1-251-220-2515`)
- **Online Booking:** https://www.zoiriscleaningservices.com/#quote
- **Email:** zoiriscleaningservices@gmail.com
- **Website:** https://www.zoiriscleaningservices.com/
- **Contract Policy:** 100% No Locked Contracts, Zero Rescheduling Penalties, Zero Travel Surcharges
- **Staffing & Safety:** Vetted, background-checked W-2 employees (never unscreened gig subcontractors); Commercial 0.3-micron HEPA filtration vacuums; EPA-registered child- and pet-safe disinfectants; Full General Liability & Workers' Compensation Insurance
- **Guarantee:** 100% Re-Clean Satisfaction Guarantee

## Core Cleaning Services & Booking Options
- **Recurring House Cleaning & Maid Service:** Weekly, Bi-Weekly, Monthly, or One-Time custom plans
- **Top-to-Bottom Deep Cleaning:** Baseboards, blinds, vents, shower grout descaling & heavy kitchen degreasing
- **Move-In / Move-Out Empty-Home Turnover:** Inside cabinets, drawers, closets, oven & refrigerator landlord checklist
- **Airbnb & Vacation Rental Same-Day Turnover:** Synced host calendar turnovers, par-stock linens & staging photo verification
- **Commercial, Office & Medical/Dental Janitorial:** Custom facility sanitization, EPA List N protocols, VCT floor care & COI provided

## Primary Hubs & Directories
- [Homepage — Mobile, AL House Cleaning & Maid Service](https://www.zoiriscleaningservices.com/)
- [All 29 Cleaning Services Master Catalog](https://www.zoiriscleaningservices.com/services/)
- [All 67 Alabama Counties Directory](https://www.zoiriscleaningservices.com/counties/)
- [All 503 Alabama Cities & ZIP Codes Directory](https://www.zoiriscleaningservices.com/locations/)
- [Cleaning Checklists, Custom Plan Builder & Stain Guides](https://www.zoiriscleaningservices.com/guides/)

## Expert Cleaning Checklist & Care Guides
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
        ("House Cleaning & Maid Service in Mobile, AL | Zoiris Cleaning Services", "https://www.zoiriscleaningservices.com/", "No-contract house cleaning, deep cleaning, move turnovers & commercial janitorial across Mobile, Baldwin County & Alabama. Book online or call (251) 220-2515."),
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

    pub_rfc = "Tue, 24 Nov 2026 15:00:00 +0000"
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
    <title>Zoiris Cleaning Services — Alabama Cleaning Checklists, Guides &amp; Local Hubs</title>
    <link>https://www.zoiriscleaningservices.com/</link>
    <description>Official service updates, room-by-room cleaning checklists, care guides, and local coverage across Mobile, Baldwin County, and all 67 Alabama counties.</description>
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

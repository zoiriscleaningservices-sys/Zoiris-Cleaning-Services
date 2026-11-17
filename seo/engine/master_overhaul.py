import os
import sys
import re
import json
import html
import concurrent.futures
import multiprocessing
import xml.etree.ElementTree as ET
from datetime import datetime

engine_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(engine_dir))
sys.path.insert(0, engine_dir)

from geo_service_content import (
    LOCATIONS, SERVICES, get_enriched_profile,
    build_hub_body_html, build_service_body_html,
    build_hub_faqs, build_service_faqs, build_jsonld_schema
)

TODAY = "2026-11-17"

# 1. Discover exact Detailing folder names across all 504 *-al directories
DET_MAP = {}
SPACE_DUP_DETAILING = set()

for loc_slug in LOCATIONS.keys():
    loc_dir = os.path.join(root_dir, loc_slug)
    if not os.path.isdir(loc_dir):
        continue
    dets = sorted([d for d in os.listdir(loc_dir) if os.path.isdir(os.path.join(loc_dir, d)) and d.lower().startswith("detailing")])
    if len(dets) > 1:
        no_space = [d for d in dets if " " not in d]
        canon_det = no_space[0] if no_space else dets[0]
        DET_MAP[loc_slug] = canon_det
        for d in dets:
            if d != canon_det:
                SPACE_DUP_DETAILING.add(f"{loc_slug}/{d}/index.html")
    elif len(dets) == 1:
        DET_MAP[loc_slug] = dets[0]
    else:
        DET_MAP[loc_slug] = f"Detailing-{loc_slug}"

VALID_LOC_SLUGS = set(LOCATIONS.keys())

# Regexes for fast, deterministic transformations
HEAD_TO_STYLE_RE = re.compile(r'<head\b[^>]*>.*?(?=<style\b)', re.I | re.S)
BROKEN_WOFF_RE = re.compile(r'@font-face\s*\{[^}]*\.\.\.fa-(?:solid-900|brands-400)\.woff2[^}]*\}', re.I | re.S)
CLOSE_STYLE_TO_BODY_RE = re.compile(r'</style>\s*(?:</head>\s*)?(?=<body\b)', re.I | re.S)
HERO_H1_P_RE = re.compile(
    r'(<section\b[^>]*id=["\']home["\'][^>]*>.*?<h1\b[^>]*>)(.*?)(</h1>\s*<p\b[^>]*>)(.*?)(</p>)',
    re.I | re.S
)
HERO_SECTION_RE = re.compile(r'(<section\b[^>]*id=["\']home["\'][^>]*>.*?</section>)', re.I | re.S)
QUOTE_SECTION_RE = re.compile(r'(<section\b[^>]*id=["\']quote["\'][^>]*>.*?</section>)', re.I | re.S)
FOOTER_START_RE = re.compile(r'(<footer\b)', re.I)

# Broken link regexes
APOS_DETAILING_RE = re.compile(r"""href=['"](/([a-z0-9-]+-al)/Detailing-[^'"<>]*?)['"](?:\s*[a-zA-Z-]+-AL/['"])?""", re.I)
PLAIN_DETAILING_RE = re.compile(r'href=(["\'])/([a-z0-9-]+-al)/(Detailing-[^/"\'<>]+)/\1', re.I)
FAKE_NEIGHBORHOOD_LINK_RE = re.compile(r'href=(["\'])/(downtown|midtown|west)-([a-z0-9-]+-al)/\1', re.I)
MAID_DOUBLE_AL_RE = re.compile(r'href=(["\'])/maid-service-([a-z0-9-]+-al)-al/\1', re.I)
REGIONAL_UTILITY_LINK_RE = re.compile(r'href=(["\'])/([a-z0-9-]+-al)/(about|blog|contact)/\1', re.I)
DESKTOP_LOC_DROPDOWN_RE = re.compile(
    r'(<div class="absolute left-0 top-full hidden group-hover:flex flex-col w-56 z-50">).*?(</div>)',
    re.I | re.S
)

NEW_DESKTOP_LOC_DROPDOWN_INNER = """
                  <a class="contact-button text-sm py-2 hover:bg-blue-700" href="/mobile-al/">Mobile, AL</a>
                  <a class="contact-button text-sm py-2 hover:bg-blue-700" href="/semmes-al/">Semmes, AL</a>
                  <a class="contact-button text-sm py-2 hover:bg-blue-700" href="/theodore-al/">Theodore, AL</a>
                  <a class="contact-button text-sm py-2 hover:bg-blue-700" href="/saraland-al/">Saraland, AL</a>
                  <a class="contact-button text-sm py-2 hover:bg-blue-700" href="/daphne-al/">Daphne, AL</a>
                  <a class="contact-button text-sm py-2 hover:bg-blue-700" href="/fairhope-al/">Fairhope, AL</a>
                  <a class="contact-button text-sm py-2 hover:bg-blue-700" href="/spanish-fort-al/">Spanish Fort, AL</a>
                  <a class="contact-button text-sm py-2 hover:bg-blue-700" href="/foley-al/">Foley, AL</a>
                  <a class="contact-button text-sm py-2 hover:bg-blue-700" href="/gulf-shores-al/">Gulf Shores, AL</a>
                  <a class="contact-button text-sm py-2 hover:bg-blue-700" href="/orange-beach-al/">Orange Beach, AL</a>
                  <a class="contact-button text-sm py-2 hover:bg-blue-700" href="/birmingham-al/">Birmingham, AL</a>
                  <a class="contact-button text-sm py-2 hover:bg-blue-700" href="/huntsville-al/">Huntsville, AL</a>
                  <a class="contact-button text-sm py-2 hover:bg-blue-700" href="/montgomery-al/">Montgomery, AL</a>
                  <a class="contact-button text-sm py-2 hover:bg-blue-700" href="/counties/">All 67 AL Counties &rarr;</a>
                  <a class="contact-button text-sm py-2 hover:bg-blue-700" href="/services/">All 29 Services &rarr;</a>
                  <a class="contact-button text-sm py-2 hover:bg-blue-700" href="/guides/">Pricing &amp; Checklists &rarr;</a>
                  <a class="contact-button text-sm py-2 bg-blue-700 font-bold" href="/locations/">All 503+ AL Cities &rarr;</a>
                """

def build_clean_head_top(title, desc, canonical_url, robots="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1", og_image="/images/services_action.png", schema_block=""):
    esc_t = html.escape(title)
    esc_d = html.escape(desc)
    full_img = og_image if og_image.startswith("http") else f"https://www.zoiriscleaningservices.com{og_image}"
    canon_tag = f'  <link rel="canonical" href="{canonical_url}" />\n' if canonical_url else ""
    og_url_tag = f'  <meta property="og:url" content="{canonical_url}" />\n' if canonical_url else ""
    return f"""<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <meta name="robots" content="{robots}" />
  <title>{esc_t}</title>
  <meta name="description" content="{esc_d}" />
{canon_tag}  <meta property="og:locale" content="en_US" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{esc_t}" />
  <meta property="og:description" content="{esc_d}" />
{og_url_tag}  <meta property="og:site_name" content="Zoiris Cleaning Services" />
  <meta property="og:image" content="{full_img}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{esc_t}" />
  <meta name="twitter:description" content="{esc_d}" />
  <meta name="twitter:image" content="{full_img}" />
  <link rel="sitemap" type="application/xml" href="https://www.zoiriscleaningservices.com/sitemap_index.xml" />
  <link rel="alternate" type="application/rss+xml" title="Zoiris Cleaning Services — Alabama Cleaning Guides &amp; Coverage" href="https://www.zoiriscleaningservices.com/feed.xml" />
  <link rel="preload" as="image" href="/images/location_hero.webp" type="image/webp" fetchpriority="high" />
  <link rel="apple-touch-icon" sizes="180x180" href="/favicon/apple-touch-icon.png" />
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon/favicon-32x32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon/favicon-16x16.png" />
  <link rel="manifest" href="/favicon/site.webmanifest" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin />
  <link rel="preconnect" href="https://cdnjs.cloudflare.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&amp;display=swap" rel="stylesheet" />
  {schema_block}
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet" />
  <link href="https://cdn.jsdelivr.net/npm/swiper@12/swiper-bundle.min.css" rel="stylesheet" />
  <script defer src="https://cdn.jsdelivr.net/npm/swiper@12/swiper-bundle.min.js"></script>
  """

def fix_detailing_href(match):
    city_slug = match.group(2).lower()
    if city_slug in DET_MAP:
        return f'href="/{city_slug}/{DET_MAP[city_slug]}/"'
    return f'href="/mobile-al/{DET_MAP["mobile-al"]}/"'

def fix_fake_neighborhood(match):
    q, prefix, base_city_al = match.group(1), match.group(2).lower(), match.group(3).lower()
    candidate = f"{prefix}-{base_city_al}"
    if candidate in VALID_LOC_SLUGS:
        return f'href={q}/{candidate}/{q}'
    if base_city_al in VALID_LOC_SLUGS:
        return f'href={q}/{base_city_al}/{q}'
    return f'href={q}/mobile-al/{q}'

def fix_maid_double_al(match):
    q, city_al = match.group(1), match.group(2).lower()
    if city_al in VALID_LOC_SLUGS:
        return f'href={q}/{city_al}/house-cleaning/{q}'
    return f'href={q}/mobile-al/house-cleaning/{q}'

def fix_regional_utility(match):
    q, city_al, util = match.group(1), match.group(2).lower(), match.group(3).lower()
    return f'href={q}/mobile-al/{util}/{q}'

def sanitize_common_html(raw, loc_slug=None):
    # Fix broken apostrophe attributes first (Jacksons Gap & Tillman's Corner)
    raw = raw.replace("href='/jacksons-gap-al/Detailing-Jackson's Gap-AL/'", f'href="/jacksons-gap-al/{DET_MAP.get("jacksons-gap-al", "Detailing-jacksons-gap-al")}/"')
    raw = raw.replace('href="/jacksons-gap-al/Detailing-Jackson\'s Gap-AL/"', f'href="/jacksons-gap-al/{DET_MAP.get("jacksons-gap-al", "Detailing-jacksons-gap-al")}/"')
    raw = raw.replace("href='/tillmans-corner-al/Detailing-Tillman's Corner-AL/'", f'href="/tillmans-corner-al/{DET_MAP.get("tillmans-corner-al", "Detailing-tillmans-corner-al")}/"')
    raw = raw.replace('href="/tillmans-corner-al/Detailing-Tillman\'s Corner-AL/"', f'href="/tillmans-corner-al/{DET_MAP.get("tillmans-corner-al", "Detailing-tillmans-corner-al")}/"')

    # If scaffolded from mobile-al/daphne-al/gulf-shores-al, rewrite source slug nav links for the 3 new directories
    if loc_slug == "downtown-mobile-al":
        for srv_k in SERVICES.keys():
            if srv_k != "detailing":
                raw = raw.replace(f'href="/mobile-al/{srv_k}/"', f'href="/downtown-mobile-al/{srv_k}/"')
        raw = raw.replace('href="/mobile-al/Detailing-Mobile-AL/"', 'href="/downtown-mobile-al/Detailing-downtown-mobile-al/"')
        raw = raw.replace("onclick=\"location.href='/mobile-al/'\"", "onclick=\"location.href='/downtown-mobile-al/'\"")
    elif loc_slug == "eastern-shore-al":
        for srv_k in SERVICES.keys():
            if srv_k != "detailing":
                raw = raw.replace(f'href="/daphne-al/{srv_k}/"', f'href="/eastern-shore-al/{srv_k}/"')
        raw = raw.replace('href="/daphne-al/Detailing-daphne-al/"', 'href="/eastern-shore-al/Detailing-eastern-shore-al/"')
        raw = raw.replace('href="/daphne-al/Detailing-Daphne-AL/"', 'href="/eastern-shore-al/Detailing-eastern-shore-al/"')
        raw = raw.replace("onclick=\"location.href='/daphne-al/'\"", "onclick=\"location.href='/eastern-shore-al/'\"")
    elif loc_slug == "fort-morgan-al":
        for srv_k in SERVICES.keys():
            if srv_k != "detailing":
                raw = raw.replace(f'href="/gulf-shores-al/{srv_k}/"', f'href="/fort-morgan-al/{srv_k}/"')
        raw = raw.replace('href="/gulf-shores-al/Detailing-gulf-shores-al/"', 'href="/fort-morgan-al/Detailing-fort-morgan-al/"')
        raw = raw.replace('href="/gulf-shores-al/Detailing-Gulf Shores-AL/"', 'href="/fort-morgan-al/Detailing-fort-morgan-al/"')
        raw = raw.replace("onclick=\"location.href='/gulf-shores-al/'\"", "onclick=\"location.href='/fort-morgan-al/'\"")

    # Rewrite all Detailing hrefs to exact canonical folder on disk
    raw = PLAIN_DETAILING_RE.sub(fix_detailing_href, raw)
    raw = APOS_DETAILING_RE.sub(fix_detailing_href, raw)

    # Fix corrupt jacksons-gap entity links & sitemap.xml links
    raw = raw.replace("/jackson&#39;s-gap-al/", "/jacksons-gap-al/")
    raw = raw.replace("/jackson&amp;#39;s-gap-al/", "/jacksons-gap-al/")
    raw = raw.replace('href="/sitemap.xml"', 'href="/sitemap_index.xml"')
    raw = raw.replace("href='/sitemap.xml'", 'href="/sitemap_index.xml"')

    # Fix fake neighborhood & maid-service-*-al-al links
    raw = FAKE_NEIGHBORHOOD_LINK_RE.sub(fix_fake_neighborhood, raw)
    raw = MAID_DOUBLE_AL_RE.sub(fix_maid_double_al, raw)

    # Consolidate regional about/blog/contact links to /mobile-al/{about|blog|contact}/
    raw = REGIONAL_UTILITY_LINK_RE.sub(fix_regional_utility, raw)

    # Upgrade Desktop Header Locations Dropdown
    raw = DESKTOP_LOC_DROPDOWN_RE.sub(lambda m: m.group(1) + NEW_DESKTOP_LOC_DROPDOWN_INNER + m.group(2), raw, count=1)

    # Upgrade ZIP Code Finder so all valid Alabama 5-digit ZIP codes (35xxx & 36xxx) pass!
    raw = raw.replace(
        "if (serviceZips.includes(zip)) {",
        "if (/^3[56]\\d{3}$/.test(zip) || serviceZips.includes(zip)) {"
    )

    # Remove broken @font-face ...fa-solid-900.woff2 & ...fa-brands-400.woff2 and render-blocking @import
    raw = BROKEN_WOFF_RE.sub("", raw)
    raw = raw.replace("@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');", "")
    raw = raw.replace("url('/images/location_hero.png')", "url('/images/location_hero.webp')")
    raw = raw.replace('src="/images/services_action.png"', 'src="/images/services_action.webp"')

    # Ensure </head> closes cleanly before <body
    raw = CLOSE_STYLE_TO_BODY_RE.sub("</style>\n</head>\n", raw, count=1)

    # Fix NAP & Social Links
    raw = raw.replace("251-930-8621", "(251) 220-2515")
    raw = raw.replace("12519308621", "12512202515")
    raw = raw.replace("123 Dauphin St, Mobile, AL 36602", "Downtown Mobile, AL 36602")
    raw = raw.replace("123+Dauphin+St,+Mobile,+AL+36602", "Downtown+Mobile,+AL+36602")
    raw = raw.replace("https://instagram.com/zoiriscleaning", "https://www.instagram.com/zoiriscleaningservices/")
    raw = raw.replace("https://www.instagram.com/zoiriscleaning\"", "https://www.instagram.com/zoiriscleaningservices/\"")
    raw = raw.replace('href="https://tiktok.com"', 'href="https://www.tiktok.com/@zoiriscleaningservices"')
    raw = raw.replace('href="https://yelp.com"', 'href="https://www.yelp.com/user_details?userid=7SDy8Urgj43gfYxrR5o2eQ"')
    raw = raw.replace('View All\n          480+ Locations', 'View All 503+ AL Locations')
    raw = raw.replace('View All 480+ Locations', 'View All 503+ AL Locations')
    raw = raw.replace('View All 504+ AL Locations', 'View All 503+ AL Locations')

    # Inject 1-click Crawl Accelerator links to /services/, /counties/, and /guides/ in bottom bar if not present
    if 'href="/counties/"' not in raw and 'href="/locations/"' in raw:
        raw = raw.replace(
            '<a href="/locations/" class="text-blue-500 hover:text-pink-400 font-bold text-xs transition-colors">',
            '<a href="/services/" class="text-blue-400 hover:text-pink-400 font-bold text-xs transition-colors">All 29 Services</a>\n        <a href="/counties/" class="text-blue-400 hover:text-pink-400 font-bold text-xs transition-colors">All 67 AL Counties</a>\n        <a href="/guides/" class="text-blue-400 hover:text-pink-400 font-bold text-xs transition-colors">Pricing &amp; Checklists</a>\n        <a href="/locations/" class="text-blue-500 hover:text-pink-400 font-bold text-xs transition-colors">',
            1
        )

    return raw

def write_atomic(filepath, content):
    tmp = filepath + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(content)
    os.replace(tmp, filepath)

def process_city_file(rel_and_fp):
    rel, fp = rel_and_fp
    parts = rel.split("/")
    loc_slug = parts[0]

    # Case 0: Space-named duplicate Detailing folder -> clean noindex + canonical + instant redirect stub
    if rel in SPACE_DUP_DETAILING:
        canon_det = DET_MAP[loc_slug]
        target_url = f"https://www.zoiriscleaningservices.com/{loc_slug}/{canon_det}/"
        target_rel = f"/{loc_slug}/{canon_det}/"
        stub = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="robots" content="noindex, follow" />
  <title>Redirecting to {html.escape(LOCATIONS[loc_slug]['display_title'])} Interior Detailing | Zoiris</title>
  <link rel="canonical" href="{target_url}" />
  <meta http-equiv="refresh" content="0; url={target_rel}" />
  <script>window.location.replace({json.dumps(target_rel)});</script>
</head>
<body style="background:#0f172a;color:#fff;font-family:sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh;">
  <p>Redirecting to <a href="{target_rel}" style="color:#60a5fa;">{target_url}</a>...</p>
</body>
</html>
"""
        write_atomic(fp, stub)
        return ("dup_stub", rel)

    with open(fp, "r", encoding="utf-8", errors="replace") as f:
        raw = f.read()

    prof = get_enriched_profile(loc_slug)
    city = prof["city"]
    display = prof["display_title"]
    county = prof["county"]
    pzip = prof["primary_zip"]
    det_folder = DET_MAP[loc_slug]

    # Case 1: Location Hub (/<loc_slug>/index.html)
    if len(parts) == 2 and parts[1] == "index.html":
        canon_url = f"https://www.zoiriscleaningservices.com/{loc_slug}/"
        if loc_slug == "mobile-al":
            title = "Cleaning Services in Mobile, AL | Residential, Commercial & Maid Hub | Zoiris"
        else:
            title = f"Cleaning Services in {display} | Home, Deep & Commercial Cleaners | Zoiris"
        desc = f"Top-rated residential & commercial cleaning services in {display} ({county}, ZIP {pzip}). Maid service, deep cleans, move-outs & janitorial — no contracts! Call (251) 220-2515!"
        h1_txt = f"Professional Cleaning Services in {display}"
        sub_txt = f"Flat-rate, <strong>No-Contract</strong> residential housekeeping, deep cleaning, move turnovers, and commercial janitorial across {html.escape(city)} and {html.escape(county)} (ZIP {html.escape(prof['zips_str'])})."

        body_html, faqs = build_hub_body_html(loc_slug, det_folder)
        schema_block = build_jsonld_schema("location_hub", canon_url, loc_slug=loc_slug, faqs=faqs, title=title, desc=desc)
        head_top = build_clean_head_top(title, desc, canon_url, og_image="/images/location_hero.png", schema_block=schema_block)

        raw = HEAD_TO_STYLE_RE.sub(lambda _: head_top, raw, count=1)
        raw = HERO_H1_P_RE.sub(lambda m: f"{m.group(1)}\n          {html.escape(h1_txt)}\n        {m.group(3)}\n          {sub_txt}\n        {m.group(5)}", raw, count=1)

        hm = HERO_SECTION_RE.search(raw)
        qm = QUOTE_SECTION_RE.search(raw)
        fm = FOOTER_START_RE.search(raw)
        if hm and qm and fm:
            raw = raw[:hm.end()] + "\n\n" + body_html + "\n\n    " + qm.group(1) + "\n\n    " + raw[fm.start():]
        elif hm and fm:
            raw = raw[:hm.end()] + "\n\n" + body_html + "\n\n    " + raw[fm.start():]

        raw = sanitize_common_html(raw, loc_slug=loc_slug)
        write_atomic(fp, raw)
        return ("hub", rel)

    # Case 2: Subpages inside /<loc_slug>/<sub_folder>/index.html
    sub_folder = parts[1]

    # Case 2A: Regional /about/, /blog/, /contact/
    if sub_folder in ("about", "blog", "contact"):
        if loc_slug == "mobile-al":
            # Primary brand About / Blog / Contact pages (INDEXABLE!)
            canon_url = f"https://www.zoiriscleaningservices.com/mobile-al/{sub_folder}/"
            if sub_folder == "about":
                title = "About Zoiris Cleaning Services | Licensed & Insured Alabama Cleaners"
                desc = "Meet Zoiris Cleaning Services LLC — headquartered in Mobile, AL and serving all 67 Alabama counties with vetted W-2 cleaners, HEPA filtration & zero locked contracts. Call (251) 220-2515!"
            elif sub_folder == "blog":
                title = "Cleaning Tips, Checklists & Home Care Guides | Zoiris Cleaning Blog"
                desc = "Expert residential & commercial cleaning guides, seasonal deep-cleaning checklists, and Gulf Coast humidity & stain care tips from Zoiris Cleaning Services."
            else:
                title = "Contact Zoiris Cleaning Services | 24/7 Free Cleaning Quotes | (251) 220-2515"
                desc = "Contact Zoiris Cleaning Services 24/7 at (251) 220-2515 or request a fast online flat-rate estimate for house cleaning, deep cleaning, move turnovers & commercial janitorial."
            schema_block = build_jsonld_schema("global_page", canon_url, title=title, desc=desc)
            head_top = build_clean_head_top(title, desc, canon_url, schema_block=schema_block)
            raw = HEAD_TO_STYLE_RE.sub(lambda _: head_top, raw, count=1)
            raw = sanitize_common_html(raw, loc_slug=loc_slug)
            write_atomic(fp, raw)
            return ("brand_utility", rel)
        else:
            # 503 regional utility clones -> NOINDEX + canonical to /mobile-al/{sub_folder}/
            canon_url = f"https://www.zoiriscleaningservices.com/mobile-al/{sub_folder}/"
            title = f"{sub_folder.capitalize()} — {display} | Zoiris Cleaning Services"
            desc = f"Zoiris Cleaning Services {sub_folder} information for {display} ({county}). Call (251) 220-2515 for a free flat-rate quote."
            head_top = build_clean_head_top(title, desc, canon_url, robots="noindex, follow", schema_block="")
            raw = HEAD_TO_STYLE_RE.sub(lambda _: head_top, raw, count=1)
            raw = sanitize_common_html(raw, loc_slug=loc_slug)
            write_atomic(fp, raw)
            return ("noindex_utility", rel)

    # Case 2B: Location Service Page (29 services including canonical Detailing!)
    srv_key = "detailing" if sub_folder.lower().startswith("detailing") else sub_folder
    if srv_key not in SERVICES:
        # Safety fallback if any unexpected subfolder ever existed
        canon_url = f"https://www.zoiriscleaningservices.com/{loc_slug}/"
        head_top = build_clean_head_top(f"Cleaning Services in {display} | Zoiris", f"Cleaning services in {display}.", canon_url, robots="noindex, follow")
        raw = HEAD_TO_STYLE_RE.sub(lambda _: head_top, raw, count=1)
        raw = sanitize_common_html(raw, loc_slug=loc_slug)
        write_atomic(fp, raw)
        return ("other_sub", rel)

    srv = SERVICES[srv_key]
    canon_url = f"https://www.zoiriscleaningservices.com/{loc_slug}/{sub_folder}/"
    fmt_vars = {
        "City": display[:-4] if display.endswith(", AL") else display,
        "DisplayCity": display,
        "County": county,
        "Zip": pzip
    }
    # For Lake View vs Lakeview, ensure title clearly includes county disambiguator!
    city_for_tpl = f"{city} ({prof['county_short']} Co.)" if loc_slug in ("lake-view-al", "lakeview-al") else city
    tpl_vars = {"City": city_for_tpl, "County": county, "Zip": pzip}

    title = srv["title_tpl"].format(**tpl_vars)
    desc = srv["desc_tpl"].format(**tpl_vars)
    h1_txt = srv["h1_tpl"].format(**tpl_vars)
    sub_txt = srv["subtitle_tpl"].format(**tpl_vars)

    body_html, faqs = build_service_body_html(loc_slug, srv_key, sub_folder, DET_MAP)
    schema_block = build_jsonld_schema("location_service", canon_url, loc_slug=loc_slug, srv_key=srv_key, faqs=faqs, title=title, desc=desc)
    head_top = build_clean_head_top(title, desc, canon_url, og_image=srv["image"], schema_block=schema_block)

    raw = HEAD_TO_STYLE_RE.sub(lambda _: head_top, raw, count=1)
    raw = HERO_H1_P_RE.sub(lambda m: f"{m.group(1)}\n          {html.escape(h1_txt)}\n        {m.group(3)}\n          {html.escape(sub_txt)}\n        {m.group(5)}", raw, count=1)

    hm = HERO_SECTION_RE.search(raw)
    qm = QUOTE_SECTION_RE.search(raw)
    fm = FOOTER_START_RE.search(raw)
    if hm and qm and fm:
        raw = raw[:hm.end()] + "\n\n" + body_html + "\n\n    " + qm.group(1) + "\n\n    " + raw[fm.start():]
    elif hm and fm:
        raw = raw[:hm.end()] + "\n\n" + body_html + "\n\n    " + raw[fm.start():]

    raw = sanitize_common_html(raw, loc_slug=loc_slug)
    write_atomic(fp, raw)
    return ("service", rel)

def update_global_and_root_pages():
    print("Updating Homepage, /locations/, /apply/, /Gallery/, 404.html, privacy.html, terms.html, dashboard.html...")

    # 1. Homepage (index.html)
    hp_path = os.path.join(root_dir, "index.html")
    raw_hp = open(hp_path, "r", encoding="utf-8", errors="replace").read()
    hp_title = "House Cleaning & Maid Service in Mobile, AL | Free Flat-Rate Quote | Zoiris"
    hp_desc = "4.9★ Rated House Cleaning & Maid Service in Mobile, AL, Semmes, Theodore & Baldwin County. Flat-rate pricing, no contracts, bonded W-2 cleaners. Call (251) 220-2515 24/7!"
    hp_canon = "https://www.zoiriscleaningservices.com/"
    # Extract existing visible FAQ questions/answers on index.html or inject clean FAQ section matching schema
    hp_prof = get_enriched_profile("mobile-al")
    hp_faqs = build_hub_faqs(hp_prof)
    hp_schema = build_jsonld_schema("location_hub", hp_canon, loc_slug="mobile-al", faqs=hp_faqs, title=hp_title, desc=hp_desc)
    hp_head = build_clean_head_top(hp_title, hp_desc, hp_canon, og_image="/images/services_action.png", schema_block=hp_schema)
    raw_hp = HEAD_TO_STYLE_RE.sub(lambda _: hp_head, raw_hp, count=1)
    # Replace or inject #ai-quick-answer + #faq on homepage right before #quote so visible FAQs & Speakable 100% match JSON-LD!
    from geo_service_content import render_faq_details_html, build_ai_hub_summary_and_table
    hp_ai_sec = f"""    <section id="hp-ai-summary" class="py-12 px-4 sm:px-6 bg-transparent relative z-10">
      <div class="max-w-5xl mx-auto">
{build_ai_hub_summary_and_table(hp_prof)}
      </div>
    </section>"""
    hp_faq_html = hp_ai_sec + "\n\n" + render_faq_details_html(
        hp_faqs,
        "Frequently Asked Questions About House Cleaning & Maid Service in Mobile, AL",
        "Answers on flat-rate pricing, zero locked contracts, HEPA equipment, and coverage across Mobile & Baldwin County."
    )
    raw_hp = re.sub(r'<section\b[^>]*id=["\']hp-ai-summary["\'][^>]*>.*?</section>\s*', "", raw_hp, flags=re.I | re.S)
    old_faq_re = re.compile(r'<section\b[^>]*id=["\']faq["\'][^>]*>.*?</section>', re.I | re.S)
    if old_faq_re.search(raw_hp):
        raw_hp = old_faq_re.sub(lambda _: hp_faq_html, raw_hp, count=1)
    else:
        raw_hp = QUOTE_SECTION_RE.sub(lambda m: hp_faq_html + "\n\n    " + m.group(1), raw_hp, count=1)
    raw_hp = sanitize_common_html(raw_hp)
    write_atomic(hp_path, raw_hp)

    # 2. /locations/index.html — Complete 67-County, 504-City Directory
    loc_idx_path = os.path.join(root_dir, "locations", "index.html")
    raw_loc = open(loc_idx_path, "r", encoding="utf-8", errors="replace").read()
    loc_title = "Alabama Cleaning Service Areas (All 67 Counties & 504 Cities) | Zoiris"
    loc_desc = "Browse all 504 Alabama cities & 67 counties served by Zoiris Cleaning Services — Mobile, Semmes, Theodore, Daphne, Fairhope, Gulf Shores, Birmingham, Huntsville & Montgomery. Call (251) 220-2515!"
    loc_canon = "https://www.zoiriscleaningservices.com/locations/"
    loc_schema = build_jsonld_schema("locations_index", loc_canon, title=loc_title, desc=loc_desc)
    loc_head = build_clean_head_top(loc_title, loc_desc, loc_canon, og_image="/images/service_areas.png", schema_block=loc_schema)
    raw_loc = HEAD_TO_STYLE_RE.sub(lambda _: loc_head, raw_loc, count=1)

    gulf_hubs = [v for v in LOCATIONS.values() if v["sitemap_tier"] == "priority"]
    gulf_hubs.sort(key=lambda x: (0 if x["slug"] in ("mobile-al", "semmes-al", "theodore-al", "daphne-al", "fairhope-al", "gulf-shores-al", "orange-beach-al", "foley-al", "spanish-fort-al", "saraland-al") else 1, x["city"]))
    metro_hubs = sorted([v for v in LOCATIONS.values() if v["sitemap_tier"] == "metros"], key=lambda x: x["city"])
    all_sorted = sorted(LOCATIONS.values(), key=lambda x: x["display_title"])

    gulf_cards = "\n".join(
        f'            <a href="/{v["slug"]}/" class="bg-blue-600/25 hover:bg-blue-600/45 border border-blue-400/40 rounded-xl px-4 py-3 text-left transition flex items-center justify-between"><span class="font-bold text-white text-sm">{html.escape(v["display_title"])}</span><span class="text-xs text-blue-200">{html.escape(v["primary_zip"])}</span></a>'
        for v in gulf_hubs
    )
    metro_cards = "\n".join(
        f'            <a href="/{v["slug"]}/" class="bg-purple-600/20 hover:bg-purple-600/40 border border-purple-400/35 rounded-xl px-4 py-3 text-left transition flex items-center justify-between"><span class="font-bold text-white text-sm">{html.escape(v["display_title"])}</span><span class="text-xs text-purple-200">{html.escape(v["county_short"])} Co.</span></a>'
        for v in metro_hubs
    )
    all_cards = "\n".join(
        f'            <a href="/{v["slug"]}/" data-search="{html.escape((v["display_title"] + " " + v["county"] + " " + " ".join(v["zips"])).lower())}" class="city-card contact-button text-sm sm:text-base block w-full text-center hover:scale-105 transition-transform bg-white/10 backdrop-blur-sm border border-white/20 py-3 px-3"><span class="block font-bold text-white">{html.escape(v["display_title"])}</span><span class="block text-xs text-blue-200 mt-0.5">{html.escape(v["county"])} • {html.escape(v["primary_zip"])}</span></a>'
        for v in all_sorted
    )

    new_dir_section = f"""    <!-- Locations Directory Grid Section -->
    <section class="min-h-screen pt-20 pb-20 flex flex-col items-center justify-start relative z-10 w-full">
      <div class="relative px-4 sm:px-6 lg:px-8 max-w-7xl w-full">
        <div class="text-center max-w-4xl mx-auto mb-12">
          <span class="text-sm font-bold uppercase tracking-wider text-blue-100 bg-white/10 backdrop-blur-md border border-white/20 px-4 py-1.5 rounded-full">
            ✦ Statewide Coverage • All 67 Counties &amp; 504 Communities ✦
          </span>
          <h1 class="text-4xl md:text-5xl font-extrabold text-white leading-tight mt-4 mb-5 text-shadow">
            Alabama Cleaning Service Areas &amp; Local Branches
          </h1>
          <p class="text-lg md:text-xl text-purple-100 font-medium mx-auto mb-8 leading-relaxed">
            From our headquarters in <strong>Downtown Mobile, AL</strong> across <strong>Semmes, Theodore, Baldwin County &amp; the Gulf Coast</strong> to <strong>Birmingham, Huntsville, Montgomery, Tuscaloosa &amp; Auburn</strong> — select your city or search by ZIP code below.
          </p>
          <div class="w-full max-w-2xl mx-auto relative">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <i class="fas fa-search text-gray-300"></i>
            </div>
            <input type="text" id="citySearch" onkeyup="filterCities()" placeholder="Search by city, county, or ZIP code (e.g. Semmes, 36575, Baldwin County)..." class="w-full pl-12 pr-4 py-4 rounded-full bg-white/15 backdrop-blur-md border border-white/30 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400 transition-all shadow-xl text-base sm:text-lg" />
          </div>
        </div>

        <!-- Tier 1 Gulf Coast Priority Grid -->
        <div class="bg-black/40 backdrop-blur-md border border-white/15 rounded-3xl p-6 sm:p-8 mb-12" id="gulfPriorityBlock">
          <h2 class="text-2xl font-extrabold text-white mb-2"><i class="fas fa-star text-yellow-400 mr-2"></i>Mobile &amp; Baldwin County Gulf Coast Hubs ({len(gulf_hubs)} Areas)</h2>
          <p class="text-sm text-purple-200 mb-6">Immediate 24/7 dispatch across Greater Mobile, Eastern Shore, and Pleasure Island beaches:</p>
          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
{gulf_cards}
          </div>
        </div>

        <!-- Tier 2 Major Alabama Metros -->
        <div class="bg-black/35 backdrop-blur-md border border-white/15 rounded-3xl p-6 sm:p-8 mb-12" id="metroPriorityBlock">
          <h2 class="text-2xl font-extrabold text-white mb-2"><i class="fas fa-city text-purple-400 mr-2"></i>Major Alabama Metropolitan Areas ({len(metro_hubs)} Cities)</h2>
          <p class="text-sm text-purple-200 mb-6">Full residential housekeeping, move-out turnovers, and commercial janitorial across Alabama's largest metros:</p>
          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
{metro_cards}
          </div>
        </div>

        <!-- Complete A-Z 504 City Grid -->
        <div>
          <h2 class="text-2xl sm:text-3xl font-extrabold text-white text-center mb-8">Complete A–Z Directory of All {len(all_sorted)} Alabama Service Areas</h2>
          <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 w-full" id="cityGrid">
{all_cards}
          </div>
        </div>
      </div>
    </section>
    <script>
      function filterCities() {{
        const q = (document.getElementById('citySearch').value || '').toLowerCase().trim();
        const cards = document.querySelectorAll('#cityGrid .city-card');
        cards.forEach(card => {{
          const hay = (card.getAttribute('data-search') || card.textContent).toLowerCase();
          card.style.display = (!q || hay.includes(q)) ? '' : 'none';
        }});
      }}
    </script>"""

    loc_sec_re = re.compile(r'<!-- Locations Directory Grid Section -->.*?(?=<footer\b)', re.I | re.S)
    raw_loc = loc_sec_re.sub(lambda _: new_dir_section + "\n\n    ", raw_loc, count=1)
    raw_loc = sanitize_common_html(raw_loc)
    write_atomic(loc_idx_path, raw_loc)

    # 3. Create /apply/index.html (fixes 16,656 broken /apply/ links!)
    apply_dir = os.path.join(root_dir, "apply")
    os.makedirs(apply_dir, exist_ok=True)
    contact_tpl = open(os.path.join(root_dir, "mobile-al", "contact", "index.html"), "r", encoding="utf-8", errors="replace").read()
    apply_title = "Cleaning Jobs & Careers in Mobile, AL & Alabama | Apply at Zoiris"
    apply_desc = "Now hiring dependable W-2 residential & commercial cleaning technicians across Mobile, Semmes, Theodore, Baldwin County & Alabama. Competitive pay, flexible hours & paid training!"
    apply_canon = "https://www.zoiriscleaningservices.com/apply/"
    apply_schema = build_jsonld_schema("global_page", apply_canon, title=apply_title, desc=apply_desc)
    apply_head = build_clean_head_top(apply_title, apply_desc, apply_canon, schema_block=apply_schema)
    apply_html = HEAD_TO_STYLE_RE.sub(lambda _: apply_head, contact_tpl, count=1)
    apply_html = HERO_H1_P_RE.sub(
        lambda m: f"{m.group(1)}\n          Join the Zoiris Cleaning Services Team\n        {m.group(3)}\n          Now hiring dependable, detail-oriented W-2 residential &amp; commercial cleaning professionals across Mobile, Baldwin County, and Alabama.\n        {m.group(5)}",
        apply_html, count=1
    )
    careers_body = """
    <section class="py-16 px-4 sm:px-6 lg:px-8 bg-transparent relative z-10">
      <div class="max-w-5xl mx-auto">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <div class="bg-white rounded-2xl p-6 shadow-xl">
            <h2 class="text-xl font-extrabold text-gray-900 mb-2"><i class="fas fa-dollar-sign text-green-600 mr-2"></i>Competitive W-2 Pay</h2>
            <p class="text-sm text-gray-700">Direct W-2 employment with weekly pay, performance bonuses, tips, and workers' compensation protection.</p>
          </div>
          <div class="bg-white rounded-2xl p-6 shadow-xl">
            <h2 class="text-xl font-extrabold text-gray-900 mb-2"><i class="fas fa-graduation-cap text-blue-600 mr-2"></i>Paid Hands-On Training</h2>
            <p class="text-sm text-gray-700">Full training on commercial HEPA systems, eco-safe disinfectants, fine hardwood/stone care, and team safety.</p>
          </div>
          <div class="bg-white rounded-2xl p-6 shadow-xl">
            <h2 class="text-xl font-extrabold text-gray-900 mb-2"><i class="fas fa-calendar-check text-purple-600 mr-2"></i>Flexible Shifts</h2>
            <p class="text-sm text-gray-700">Daytime residential routes, coastal vacation-rental teams, and evening commercial janitorial schedules available.</p>
          </div>
        </div>
        <div class="bg-black/45 backdrop-blur-md border border-white/20 rounded-3xl p-8 text-center text-white">
          <h2 class="text-2xl sm:text-3xl font-extrabold mb-3">Apply Today in 2 Minutes</h2>
          <p class="text-purple-100 max-w-2xl mx-auto mb-6">Email your name, phone number, city, and availability to <a href="mailto:zoiriscleaningservices@gmail.com?subject=Job%20Application%20-%20Zoiris%20Cleaning%20Services" class="text-blue-300 underline font-bold">zoiriscleaningservices@gmail.com</a> or call our hiring desk at <a href="tel:2512202515" class="text-blue-300 underline font-bold">(251) 220-2515</a>, or submit the contact form below.</p>
          <div class="flex flex-col sm:flex-row justify-center gap-4">
            <a href="mailto:zoiriscleaningservices@gmail.com?subject=Cleaner%20Application%20-%20Zoiris" class="bg-blue-600 hover:bg-blue-500 text-white font-bold px-6 py-3 rounded-full transition">Email Hiring Team</a>
            <a href="tel:2512202515" class="bg-white text-gray-900 font-bold px-6 py-3 rounded-full hover:bg-gray-100 transition">Call (251) 220-2515</a>
          </div>
        </div>
      </div>
    </section>"""
    hm = HERO_SECTION_RE.search(apply_html)
    qm = QUOTE_SECTION_RE.search(apply_html)
    fm = FOOTER_START_RE.search(apply_html)
    if hm and qm and fm:
        apply_html = apply_html[:hm.end()] + "\n\n" + careers_body + "\n\n    " + qm.group(1) + "\n\n    " + apply_html[fm.start():]
    apply_html = sanitize_common_html(apply_html)
    write_atomic(os.path.join(apply_dir, "index.html"), apply_html)

    # 4. /Gallery/index.html (Indexable unique Gallery page!)
    gal_path = os.path.join(root_dir, "Gallery", "index.html")
    if os.path.exists(gal_path):
        raw_gal = open(gal_path, "r", encoding="utf-8", errors="replace").read()
        gal_title = "Before & After Cleaning Results Gallery | Zoiris Cleaning Services"
        gal_desc = "See real before-and-after house cleaning, deep cleaning, carpet extraction, and commercial janitorial photos across Mobile & Baldwin County, AL by Zoiris Cleaning Services."
        gal_canon = "https://www.zoiriscleaningservices.com/Gallery/"
        gal_schema = build_jsonld_schema("global_page", gal_canon, title=gal_title, desc=gal_desc)
        gal_head = build_clean_head_top(gal_title, gal_desc, gal_canon, schema_block=gal_schema)
        if HEAD_TO_STYLE_RE.search(raw_gal):
            raw_gal = HEAD_TO_STYLE_RE.sub(lambda _: gal_head, raw_gal, count=1)
        raw_gal = sanitize_common_html(raw_gal)
        write_atomic(gal_path, raw_gal)

    # 5. privacy.html & terms.html (noindex, follow + unique titles — zero cannibalization!)
    for fname, t_txt, d_txt in [
        ("privacy.html", "Privacy Policy | Zoiris Cleaning Services LLC", "Official customer data and privacy policy for Zoiris Cleaning Services LLC in Mobile, AL and across Alabama."),
        ("terms.html", "Terms of Service & Booking Policies | Zoiris Cleaning Services LLC", "Official service terms, zero-contract scheduling policy, and 24-hour satisfaction guarantee terms for Zoiris Cleaning Services LLC.")
    ]:
        fpath = os.path.join(root_dir, fname)
        if os.path.exists(fpath):
            raw_f = open(fpath, "r", encoding="utf-8", errors="replace").read()
            c_url = f"https://www.zoiriscleaningservices.com/{fname}"
            h_top = build_clean_head_top(t_txt, d_txt, c_url, robots="noindex, follow", schema_block="")
            raw_f = HEAD_TO_STYLE_RE.sub(lambda _: h_top, raw_f, count=1)
            raw_f = sanitize_common_html(raw_f)
            write_atomic(fpath, raw_f)

    # 6. Admin dashboards (dashboard.html & Gallery/Dash.html) -> strict noindex, nofollow
    for admin_rel in ["dashboard.html", os.path.join("Gallery", "Dash.html")]:
        ap = os.path.join(root_dir, admin_rel)
        if os.path.exists(ap):
            raw_a = open(ap, "r", encoding="utf-8", errors="replace").read()
            if 'name="robots"' not in raw_a.lower():
                raw_a = re.sub(r'(<head\b[^>]*>)', r'\1\n  <meta name="robots" content="noindex, nofollow" />', raw_a, count=1, flags=re.I)
            write_atomic(ap, raw_a)

    # 7. 404.html — Clean themed 404 page (noindex, follow, NO canonical, NO schema, + Smart Legacy URL Recovery!)
    p404 = os.path.join(root_dir, "404.html")
    clean_404 = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <meta name="robots" content="noindex, follow" />
  <title>Page Not Found (404) | Zoiris Cleaning Services</title>
  <meta name="description" content="The page you requested could not be found. Explore Zoiris Cleaning Services across Mobile, Semmes, Theodore, Baldwin County & all 504 Alabama locations." />
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon/favicon-32x32.png" />
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet" />
  <script>
    // Smart Legacy Bookmark Recovery for human visitors hitting retired URL patterns
    (function () {
      var p = window.location.pathname || '';
      var parts = p.split('/').filter(Boolean);
      if (!parts.length) return;
      var s = parts[0].toLowerCase();
      // Pattern 1: /maid-service-<city>-al-al/
      var m1 = s.match(/^maid-service-(.+?-al)(?:-al)?$/);
      if (m1) { window.location.replace('/' + m1[1] + '/house-cleaning/'); return; }
      // Pattern 2: /<city-al>/(best|top-rated|affordable)-<service>/
      if (parts.length >= 2 && s.endsWith('-al')) {
        var sub = parts[1].toLowerCase();
        var m2 = sub.match(/^(?:best|top-rated|affordable)-(.+)$/);
        if (m2) { window.location.replace('/' + s + '/' + m2[1] + '/'); return; }
        if (sub === 'nearby-locations' || sub === 'gallery') { window.location.replace('/' + s + '/'); return; }
      }
      // Pattern 3: /<city-without-al>/<service>/
      if (!s.endsWith('-al') && s !== 'locations' && s !== 'apply' && s !== 'gallery' && s !== 'services' && s !== 'counties' && s !== 'guides' && parts.length >= 1 && !s.includes('.')) {
        if (parts.length === 2) { window.location.replace('/' + s + '-al/' + parts[1].toLowerCase() + '/'); return; }
      }
    })();
  </script>
</head>
<body class="min-h-screen bg-gradient-to-br from-indigo-950 via-purple-950 to-slate-950 text-white flex flex-col justify-between font-sans">
  <header class="max-w-6xl mx-auto w-full px-6 py-6 flex justify-between items-center">
    <a href="/" class="flex items-center gap-3">
      <img src="/images/logo.png" alt="Zoiris Cleaning Services" class="h-16 w-auto" />
    </a>
    <a href="tel:2512202515" class="bg-blue-600 hover:bg-blue-500 text-white font-bold px-5 py-2.5 rounded-full text-sm transition shadow-lg">
      <i class="fas fa-phone-alt mr-2"></i>(251) 220-2515
    </a>
  </header>

  <main class="max-w-3xl mx-auto px-6 py-16 text-center">
    <span class="inline-block bg-white/10 border border-white/20 text-blue-300 text-xs font-bold uppercase tracking-wider px-4 py-1.5 rounded-full mb-4">
      404 — Page Moved or Not Found
    </span>
    <h1 class="text-4xl sm:text-5xl font-extrabold mb-4">Let's Get You to the Right Cleaning Page</h1>
    <p class="text-purple-200 text-lg mb-10">
      The link you followed may be outdated, but our teams are available 24/7 across <strong>Mobile, Semmes, Theodore, Baldwin County, and all 504 Alabama communities</strong>.
    </p>
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-10 text-left">
      <a href="/" class="bg-white/10 hover:bg-white/20 border border-white/20 rounded-2xl p-5 transition">
        <h2 class="font-bold text-lg text-white"><i class="fas fa-home text-blue-400 mr-2"></i>Mobile, AL Homepage</h2>
        <p class="text-xs text-gray-300 mt-1">Instant flat-rate quotes, maid service &amp; zero contracts.</p>
      </a>
      <a href="/locations/" class="bg-white/10 hover:bg-white/20 border border-white/20 rounded-2xl p-5 transition">
        <h2 class="font-bold text-lg text-white"><i class="fas fa-map-marked-alt text-green-400 mr-2"></i>All 504 Alabama Locations</h2>
        <p class="text-xs text-gray-300 mt-1">Search your city, county, or ZIP code across Alabama.</p>
      </a>
      <a href="/semmes-al/" class="bg-white/10 hover:bg-white/20 border border-white/20 rounded-2xl p-5 transition">
        <h2 class="font-bold text-lg text-white"><i class="fas fa-broom text-purple-400 mr-2"></i>Semmes &amp; West Mobile</h2>
        <p class="text-xs text-gray-300 mt-1">Local residential &amp; commercial cleaning in Semmes, AL.</p>
      </a>
      <a href="/theodore-al/" class="bg-white/10 hover:bg-white/20 border border-white/20 rounded-2xl p-5 transition">
        <h2 class="font-bold text-lg text-white"><i class="fas fa-sparkles text-pink-400 mr-2"></i>Theodore &amp; Gulf Coast</h2>
        <p class="text-xs text-gray-300 mt-1">House cleaning, move-out &amp; facility janitorial in Theodore, AL.</p>
      </a>
    </div>
    <a href="/mobile-al/contact/" class="inline-flex items-center bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold px-8 py-4 rounded-full shadow-xl transition">
      Request a Free Cleaning Estimate <i class="fas fa-arrow-right ml-2"></i>
    </a>
  </main>

  <footer class="border-t border-white/10 py-6 text-center text-xs text-gray-400">
    &copy; 2026 Zoiris Cleaning Services LLC • Downtown Mobile, AL 36602 • (251) 220-2515
  </footer>
</body>
</html>
"""
    write_atomic(p404, clean_404)

def generate_clean_sitemaps_and_robots():
    print("Generating clean XML sitemaps and robots.txt...")

    def write_urlset(urls, filename):
        lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
        for u in urls:
            lines.append(f'  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>')
        lines.append('</urlset>\n')
        write_atomic(os.path.join(root_dir, filename), "\n".join(lines))
        print(f"  -> Wrote {filename} ({len(urls)} URLs)")

    priority_urls = [
        "https://www.zoiriscleaningservices.com/",
        "https://www.zoiriscleaningservices.com/locations/",
        "https://www.zoiriscleaningservices.com/mobile-al/about/",
        "https://www.zoiriscleaningservices.com/mobile-al/contact/",
        "https://www.zoiriscleaningservices.com/mobile-al/blog/",
        "https://www.zoiriscleaningservices.com/Gallery/",
        "https://www.zoiriscleaningservices.com/apply/",
    ]
    metro_urls = []
    north_urls = []
    south_urls = []

    for loc_slug in sorted(LOCATIONS.keys()):
        loc = LOCATIONS[loc_slug]
        tier = loc["sitemap_tier"]
        bucket = (
            priority_urls if tier == "priority"
            else metro_urls if tier == "metros"
            else north_urls if tier == "north"
            else south_urls
        )
        loc_dir = os.path.join(root_dir, loc_slug)
        if not os.path.isdir(loc_dir):
            continue
        bucket.append(f"https://www.zoiriscleaningservices.com/{loc_slug}/")

        for sk in SERVICES.keys():
            folder = DET_MAP[loc_slug] if sk == "detailing" else sk
            if os.path.isfile(os.path.join(loc_dir, folder, "index.html")):
                bucket.append(f"https://www.zoiriscleaningservices.com/{loc_slug}/{folder}/")

    write_urlset(priority_urls, "sitemap_priority.xml")
    write_urlset(metro_urls, "sitemap_metros.xml")
    write_urlset(north_urls, "sitemap_regions_north.xml")
    write_urlset(south_urls, "sitemap_regions_south.xml")

    child_sitemaps = [
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
    total = len(priority_urls) + len(metro_urls) + len(north_urls) + len(south_urls)
    print(f"  -> Wrote sitemap_index.xml & sitemap.xml covering {total} verified indexable URLs!")

    robots_txt = """User-agent: *
Allow: /
Disallow: /seo/
Disallow: /dashboard.html
Disallow: /Gallery/Dash.html
Disallow: /404.html

Sitemap: https://www.zoiriscleaningservices.com/sitemap_index.xml
"""
    write_atomic(os.path.join(root_dir, "robots.txt"), robots_txt)
    print("  -> Wrote clean robots.txt")

def main():
    update_global_and_root_pages()

    city_tasks = []
    for loc_slug in sorted(LOCATIONS.keys()):
        loc_dir = os.path.join(root_dir, loc_slug)
        if not os.path.isdir(loc_dir):
            continue
        for r, d, files in os.walk(loc_dir):
            for f in files:
                if f.endswith(".html"):
                    fp = os.path.join(r, f)
                    rel = os.path.relpath(fp, root_dir).replace("\\", "/")
                    city_tasks.append((rel, fp))

    print(f"Processing {len(city_tasks)} city & subpage HTML files in parallel...", flush=True)
    counts = {}
    done = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=32) as ex:
        for kind, _ in ex.map(process_city_file, city_tasks):
            counts[kind] = counts.get(kind, 0) + 1
            done += 1
            if done % 2000 == 0:
                print(f"  Processed {done}/{len(city_tasks)} files...", flush=True)

    print("Completed city file overhaul:", counts)
    generate_clean_sitemaps_and_robots()
    print("ALL STATEWIDE SEO & INDEXING OVERHAUL TASKS COMPLETE!")

if __name__ == "__main__":
    main()

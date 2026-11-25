import os
import sys
import re
import csv
import io
import json
import html
import zipfile
from urllib.parse import urlparse

engine_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(engine_dir))
sys.path.insert(0, engine_dir)

from geo_service_content import LOCATIONS, SERVICES, county_to_slug
from master_overhaul import DET_MAP, build_redirect_stub, write_atomic
from extreme_authority_expansion import (
    ALL_67_ALABAMA_COUNTIES, GUIDES_DATA, load_shell_template, render_shell_page
)

SPECIAL_CITY_FALLBACKS = {
    "randolph-al": "/counties/bibb-county-al/",
    "salem-al": "/counties/lee-county-al/",
    "jack-al": "/counties/coffee-county-al/",
    "alys-beach": "/orange-beach-al/",
    "cleaning-services-bradenton-fl": "/",
    "jackson's-gap-al": "/jacksons-gap-al/",
    "jackson&#39;s-gap-al": "/jacksons-gap-al/",
    "jackson&amp;#39;s-gap-al": "/jacksons-gap-al/",
    "jackson's-gap": "/jacksons-gap-al/",
    "jacksons-gap": "/jacksons-gap-al/",
}

def normalize_city_token(tok):
    t = tok.lower().replace("&amp;#39;", "").replace("&#39;", "").replace("'", "")
    return t

def map_legacy_path_to_canonical(p):
    clean = p.strip()
    if clean.endswith("/index.html"):
        stem = clean.lstrip("/")[:-11]
    elif clean.endswith(".html"):
        stem = clean.lstrip("/")[:-5]
    else:
        stem = clean.strip("/")

    parts = [s for s in stem.split("/") if s]
    if not parts:
        return "/"

    if len(parts) == 1:
        sl = parts[0].lower()
        sl_norm = normalize_city_token(sl)
        if sl in ("about",):
            return "/mobile-al/about/"
        if sl in ("contact",):
            return "/mobile-al/contact/"
        if sl in ("blog",):
            return "/guides/"
        if sl == "services":
            return "/services/"
        if sl == "locations":
            return "/locations/"
        if sl in SERVICES:
            return f"/services/{sl}/"
        if sl in SPECIAL_CITY_FALLBACKS:
            return SPECIAL_CITY_FALLBACKS[sl]
        if sl_norm in LOCATIONS:
            return f"/{sl_norm}/"
        if f"{sl_norm}-al" in LOCATIONS:
            return f"/{sl_norm}-al/"
        m_maid = re.match(r"^maid-service-(.+?)(?:-al)?(?:-al)?$", sl_norm)
        if m_maid:
            c_base = m_maid.group(1)
            if not c_base.endswith("-al"):
                c_base += "-al"
            if c_base in LOCATIONS:
                return f"/{c_base}/house-cleaning/"
            return "/mobile-al/house-cleaning/"
        m_pref = re.match(r"^(?:downtown|midtown|west)-(.+)$", sl_norm)
        if m_pref:
            c_base = m_pref.group(1)
            if not c_base.endswith("-al"):
                c_base += "-al"
            if c_base in LOCATIONS:
                return f"/{c_base}/"
        return "/"

    c_raw, sub_raw = normalize_city_token(parts[0]), parts[1].lower()
    city_slug = None
    m_maid = re.match(r"^maid-service-(.+?)(?:-al)?(?:-al)?$", c_raw)
    if m_maid:
        cand = m_maid.group(1)
        if not cand.endswith("-al"):
            cand += "-al"
        city_slug = cand if cand in LOCATIONS else "mobile-al"
    elif c_raw in LOCATIONS:
        city_slug = c_raw
    elif f"{c_raw}-al" in LOCATIONS:
        city_slug = f"{c_raw}-al"
    elif parts[0].lower() in SPECIAL_CITY_FALLBACKS:
        fb = SPECIAL_CITY_FALLBACKS[parts[0].lower()]
        if fb.startswith("/counties/") or fb == "/":
            return fb
        city_slug = fb.strip("/")

    if not city_slug:
        return "/"

    if sub_raw in ("about", "contact"):
        return f"/mobile-al/{sub_raw}/"
    if sub_raw == "blog":
        return "/guides/"
    if sub_raw in ("nearby-locations", "gallery"):
        return f"/{city_slug}/"

    sub_clean = re.sub(r"^(?:best|top-rated|affordable|\d{5})-", "", sub_raw)
    city_no_al = city_slug[:-3]
    if sub_clean.endswith(f"-{city_no_al}"):
        sub_clean = sub_clean[: -(len(city_no_al) + 1)]
    if sub_clean == "move-in-out":
        sub_clean = "move-out-cleaning"

    if sub_clean == "detailing" or sub_clean.startswith("detailing-"):
        return f"/{city_slug}/{DET_MAP[city_slug]}/"
    if sub_clean in SERVICES:
        return f"/{city_slug}/{sub_clean}/"

    return f"/{city_slug}/"

def is_live_canonical_file(fp):
    if not os.path.isfile(fp):
        return False
    head = open(fp, "r", encoding="utf-8", errors="replace").read(2500)
    if 'http-equiv="refresh"' in head.lower():
        return False
    return True

def build_html_site_map(shell):
    print("Building /site-map/index.html (Master HTML Crawl Sitemap)...")
    sm_dir = os.path.join(root_dir, "site-map")
    os.makedirs(sm_dir, exist_ok=True)
    canon = "https://www.zoiriscleaningservices.com/site-map/"

    srv_links = "\n".join(
        f'            <a href="/services/{sk}/" class="text-blue-700 hover:underline font-semibold text-xs sm:text-sm">{html.escape(sv["name"])}</a>'
        for sk, sv in SERVICES.items()
    )
    guide_links = "\n".join(
        f'            <a href="/guides/{g["slug"]}/" class="text-indigo-700 hover:underline font-semibold text-xs sm:text-sm">{html.escape(g["h1"])}</a>'
        for g in GUIDES_DATA
    )
    cnt_links = "\n".join(
        f'            <a href="/counties/{county_to_slug(c)}/" class="text-blue-200 hover:text-white underline text-xs sm:text-sm font-medium">{html.escape(c)} County, AL</a>'
        for c in ALL_67_ALABAMA_COUNTIES
    )
    city_links = "\n".join(
        f'            <a href="/{v["slug"]}/" class="text-purple-100 hover:text-white underline text-xs">{html.escape(v["display_title"])}</a>'
        for v in sorted(LOCATIONS.values(), key=lambda x: x["display_title"])
    )

    body = f"""
    <section class="px-6 py-20 bg-transparent relative z-10">
      <div class="max-w-7xl mx-auto">
        <div id="ai-quick-answer" class="bg-white rounded-3xl p-6 sm:p-8 shadow-2xl border-2 border-blue-500/30 mb-12">
          <h2 class="text-2xl sm:text-3xl font-extrabold text-gray-900 mb-3">Complete Zoiris Cleaning Services HTML Site Directory</h2>
          <p class="text-sm sm:text-base text-gray-700 mb-6">
            Direct 1-click navigation to all <strong>29 Cleaning Service Pillars</strong>, <strong>10 Room-by-Room Checklist &amp; Care Guides</strong>, <strong>67 Alabama County Hubs</strong>, and <strong>503 Alabama City Service Hubs</strong> (supporting 15,209 total local pages).
          </p>
          <div class="flex flex-wrap gap-3 mb-6 text-xs sm:text-sm font-extrabold">
            <a href="/" class="bg-blue-600 text-white px-4 py-2 rounded-xl">Mobile, AL Homepage</a>
            <a href="/services/" class="bg-indigo-600 text-white px-4 py-2 rounded-xl">All 29 Services</a>
            <a href="/counties/" class="bg-purple-600 text-white px-4 py-2 rounded-xl">All 67 AL Counties</a>
            <a href="/guides/" class="bg-slate-800 text-white px-4 py-2 rounded-xl">Cleaning Checklists &amp; Guides</a>
            <a href="/locations/" class="bg-blue-800 text-white px-4 py-2 rounded-xl">Searchable Locations</a>
            <a href="/Gallery/" class="bg-gray-700 text-white px-4 py-2 rounded-xl">Results Gallery</a>
            <a href="/mobile-al/about/" class="bg-gray-700 text-white px-4 py-2 rounded-xl">About Us</a>
            <a href="/mobile-al/contact/" class="bg-gray-700 text-white px-4 py-2 rounded-xl">Book &amp; Contact</a>
            <a href="/apply/" class="bg-gray-700 text-white px-4 py-2 rounded-xl">Careers</a>
          </div>
          <h3 class="text-xl font-extrabold text-gray-900 mb-3">29 Residential, Commercial &amp; Turnover Cleaning Services</h3>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2 mb-8">
{srv_links}
          </div>
          <h3 class="text-xl font-extrabold text-gray-900 mb-3">Custom Cleaning Checklists, Scope Matrices &amp; Stain Guides</h3>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
{guide_links}
          </div>
        </div>

        <div class="bg-black/45 backdrop-blur-md border border-white/15 rounded-3xl p-6 sm:p-8 mb-10">
          <h2 class="text-2xl font-extrabold text-white mb-4">All 67 Alabama County Hubs</h2>
          <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-2.5">
{cnt_links}
          </div>
        </div>

        <div class="bg-black/35 backdrop-blur-md border border-white/15 rounded-3xl p-6 sm:p-8">
          <h2 class="text-2xl font-extrabold text-white mb-4">All 503 Alabama Cities &amp; Neighborhood Hubs (A–Z)</h2>
          <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2">
{city_links}
          </div>
        </div>
      </div>
    </section>"""

    sm_html = render_shell_page(
        shell,
        "Complete HTML Site Map — All 503 AL Cities, 67 Counties & 29 Services | Zoiris",
        "Complete HTML directory of Zoiris Cleaning Services across Mobile, Semmes, Theodore, Baldwin County, all 67 Alabama counties, 503 cities, 29 services & checklist guides.",
        canon,
        "Complete Alabama Cleaning Services HTML Site Map",
        "Fast 1-click directory to every city, county, cleaning service, and room-by-room checklist guide across Alabama.",
        body
    )
    write_atomic(os.path.join(sm_dir, "index.html"), sm_html)
    print("  -> Wrote /site-map/index.html")

def recover_all_historical_peak_urls(dl_dir):
    print("Recovering 100% of missing Historical Peak URLs + non-'-al' Gulf Coast/Metro slugs...")
    legacy_paths = set()

    # 1. Load every URL from 16-month & Peak-Window GSC exports if present
    for fn in ("zoiriscleaningservices.com-Performance-on-Search-2026-11-23.zip", "zoiriscleaningservices.com-Performance-on-Search-2026-11-23_1.zip"):
        zp = os.path.join(dl_dir, fn)
        if os.path.isfile(zp):
            with zipfile.ZipFile(zp, "r") as z:
                for row in list(csv.reader(io.StringIO(z.read("Pages.csv").decode("utf-8", "replace"))))[1:]:
                    p = urlparse(row[0]).path
                    if p and p != "/":
                        legacy_paths.add(p)

    # 2. Also ensure all 90 Priority & Metro non-'-al' city hub slugs + /about/, /contact/, /blog/ exist!
    for v in LOCATIONS.values():
        if v["sitemap_tier"] in ("priority", "metros"):
            no_al = v["slug"][:-3]
            legacy_paths.add(f"/{no_al}/")
    for util_slug in ("/about/", "/contact/", "/blog/"):
        legacy_paths.add(util_slug)

    created = 0
    for p in sorted(legacy_paths):
        # Skip if illegal Windows characters (e.g. quotes or &)
        if any(ch in p for ch in ('"', "<", ">", "|", "?", "*")):
            continue
        tgt_rel = map_legacy_path_to_canonical(p)
        tgt_url = "https://www.zoiriscleaningservices.com" + tgt_rel

        if p.endswith(".html"):
            out_fp = os.path.join(root_dir, p.lstrip("/").replace("/", os.sep))
        else:
            # Write <dir>/index.html (serves both /foo/ and /foo via 301->200 on GitHub Pages!)
            dir_rel = p.strip("/").replace("/", os.sep)
            if not dir_rel:
                continue
            out_fp = os.path.join(root_dir, dir_rel, "index.html")

        # NEVER overwrite a live canonical page!
        if is_live_canonical_file(out_fp):
            continue

        # Windows case-collision check: if parent has same name in different case (e.g. Detailing-Hurtsboro-AL vs Detailing-hurtsboro-al), skip!
        rel_out = os.path.relpath(out_fp, root_dir).replace("\\", "/")
        segs = rel_out.split("/")
        cur = root_dir
        case_collision = False
        for seg in segs[:-1]:
            if os.path.isdir(cur):
                existing = os.listdir(cur)
                low_map = {e.lower(): e for e in existing}
                if seg.lower() in low_map and low_map[seg.lower()] != seg:
                    case_collision = True
                    break
            cur = os.path.join(cur, seg)
        if case_collision:
            continue

        os.makedirs(os.path.dirname(out_fp), exist_ok=True)
        write_atomic(out_fp, build_redirect_stub(tgt_url, tgt_rel, f"Zoiris Cleaning Services ({tgt_rel})"))
        created += 1

    print(f"  -> Wrote {created} HTTP-200 Canonical Consolidation Redirect Stubs for Historical Peak URLs!")

def upgrade_rss_feed_with_peak_winners(dl_dir):
    print("Upgrading /feed.xml with Top Historical Peak Canonical Pages + All Pillars, Counties & Guides...")
    pub_rfc = "Wed, 25 Nov 2026 16:00:00 +0000"
    seen = set()
    rss_sources = []

    def add_item(title, url, desc):
        if url not in seen:
            seen.add(url)
            rss_sources.append((title, url, desc))

    add_item("#1 House Cleaning & Cleaning Services in Mobile, AL | Book Zoiris", "https://www.zoiriscleaningservices.com/", "Top-rated residential maid service, deep cleaning, move turnovers & commercial janitorial across Mobile, Semmes, Theodore, Baldwin County & Alabama. Book online or call (251) 220-2515.")
    add_item("Complete HTML Site Map — Zoiris Cleaning Services", "https://www.zoiriscleaningservices.com/site-map/", "Direct 1-click directory of all 503 Alabama cities, 67 counties, 29 cleaning services & room-by-room checklist guides.")
    add_item("All 29 Residential & Commercial Cleaning Services in Alabama", "https://www.zoiriscleaningservices.com/services/", "Complete catalog of 29 cleaning services across all 67 Alabama counties.")
    add_item("All 67 Alabama Counties Cleaning Coverage Directory", "https://www.zoiriscleaningservices.com/counties/", "County-by-county cleaning service directory across Alabama.")
    add_item("All 503 Alabama Cities & Service Areas", "https://www.zoiriscleaningservices.com/locations/", "Searchable A-Z directory of all 503 Alabama cities and USPS ZIP codes.")
    add_item("House Cleaning & Maid Service in Silverhill (Silver Hill), AL | Book Zoiris", "https://www.zoiriscleaningservices.com/silverhill-al/", "Top-rated house cleaning & maid service in Silverhill (Silver Hill), AL (36576) with zero locked contracts.")

    for g in GUIDES_DATA:
        add_item(g["title"], f"https://www.zoiriscleaningservices.com/guides/{g['slug']}/", g["answer"])
    for sk, sv in SERVICES.items():
        add_item(f"{sv['name']} in Alabama", f"https://www.zoiriscleaningservices.com/services/{sk}/", sv["short_description"])
    for c in ALL_67_ALABAMA_COUNTIES:
        cslug = county_to_slug(c)
        add_item(f"Cleaning Services in {c} County, AL", f"https://www.zoiriscleaningservices.com/counties/{cslug}/", f"House cleaning, deep cleaning & commercial janitorial across {c} County, Alabama.")

    # Add top historical impression canonical URLs from 16m Pages.csv!
    z16 = os.path.join(dl_dir, "zoiriscleaningservices.com-Performance-on-Search-2026-11-23.zip")
    if os.path.isfile(z16):
        with zipfile.ZipFile(z16, "r") as z:
            rows = list(csv.reader(io.StringIO(z.read("Pages.csv").decode("utf-8", "replace"))))[1:]
            rows.sort(key=lambda r: (-int(r[1]), -int(r[2])))
            for row in rows[:220]:
                p = urlparse(row[0]).path
                canon_rel = "/" if (not p or p == "/") else map_legacy_path_to_canonical(p)
                full_u = "https://www.zoiriscleaningservices.com" + canon_rel
                label = canon_rel.strip("/").replace("/", " — ").replace("-", " ").title() or "Mobile AL Homepage"
                add_item(f"Zoiris Cleaning Services — {label}", full_u, f"Top-rated residential & commercial cleaning services ({canon_rel}) — book online or call (251) 220-2515.")

    rss_items = [
        f"""    <item>
      <title>{html.escape(t)}</title>
      <link>{u}</link>
      <guid isPermaLink="true">{u}</guid>
      <pubDate>{pub_rfc}</pubDate>
      <description>{html.escape(d)}</description>
    </item>"""
        for t, u, d in rss_sources[:350]
    ]

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
    print(f"  -> Wrote /feed.xml with {len(rss_items)} priority crawl items!")

def main():
    dl_dir = r"C:\Users\lucia\.gemini\antigravity\brain\4ebb2c79-469b-4104-9189-04731681ef54\browser_sandbox\downloads"
    shell = load_shell_template()
    build_html_site_map(shell)
    recover_all_historical_peak_urls(dl_dir)
    upgrade_rss_feed_with_peak_winners(dl_dir)
    print("PEAK URL RECOVERY & CRAWL ACCELERATION COMPLETE!")

if __name__ == "__main__":
    main()

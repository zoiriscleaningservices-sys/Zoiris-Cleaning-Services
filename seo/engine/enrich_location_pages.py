import os
import re
import json
import sys

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from localized_faq_generator import (
    get_city_profile,
    generate_location_faqs,
    get_localized_about_html,
    get_localized_city_services_html,
    get_localized_faq_html
)
from schema_generator import generate_schema
from page_classifier import classify_page

with open(os.path.join(root_dir, 'seo', 'locations.json'), 'r', encoding='utf-8') as f:
    LOCATIONS = json.load(f)

# Hero Trust Badges snippet
def get_trust_badges_html():
    return """
        <!-- 🌟 TRUST SIGNALS & KEY VALUE HIGHLIGHTS -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 max-w-3xl mx-auto pt-2 text-left">
          <div class="bg-black/40 backdrop-blur-md border border-white/10 rounded-xl p-3 flex items-center gap-3">
            <div class="w-9 h-9 rounded-lg bg-green-500/20 text-green-400 flex items-center justify-center text-lg shrink-0">
              <i class="fas fa-shield-alt"></i>
            </div>
            <div>
              <p class="text-xs text-gray-400 uppercase font-semibold">Fully Insured</p>
              <p class="text-xs sm:text-sm font-bold text-white">Licensed &amp; Bonded</p>
            </div>
          </div>

          <div class="bg-black/40 backdrop-blur-md border border-white/10 rounded-xl p-3 flex items-center gap-3">
            <div class="w-9 h-9 rounded-lg bg-blue-500/20 text-blue-400 flex items-center justify-center text-lg shrink-0">
              <i class="fas fa-file-contract"></i>
            </div>
            <div>
              <p class="text-xs text-gray-400 uppercase font-semibold">Zero Lock-In</p>
              <p class="text-xs sm:text-sm font-bold text-white">No Contracts Ever</p>
            </div>
          </div>

          <div class="bg-black/40 backdrop-blur-md border border-white/10 rounded-xl p-3 flex items-center gap-3">
            <div class="w-9 h-9 rounded-lg bg-purple-500/20 text-purple-400 flex items-center justify-center text-lg shrink-0">
              <i class="fas fa-calendar-check"></i>
            </div>
            <div>
              <p class="text-xs text-gray-400 uppercase font-semibold">Flexibility</p>
              <p class="text-xs sm:text-sm font-bold text-white">No Reschedule Fees</p>
            </div>
          </div>

          <div class="bg-black/40 backdrop-blur-md border border-white/10 rounded-xl p-3 flex items-center gap-3">
            <div class="w-9 h-9 rounded-lg bg-yellow-500/20 text-yellow-400 flex items-center justify-center text-lg shrink-0">
              <i class="fas fa-star"></i>
            </div>
            <div>
              <p class="text-xs text-gray-400 uppercase font-semibold">Top Rated</p>
              <p class="text-xs sm:text-sm font-bold text-white">4.9★ (240+ Reviews)</p>
            </div>
          </div>
        </div>
"""

# Cleaning Standards Checklist snippet
def get_cleaning_standards_html(city, county):
    return f"""
    <!-- 🧼 SECTION: ZOIRIS STANDARD OF CLEANING (ROOM-BY-ROOM CHECKLIST) -->
    <section class="py-20 px-4 sm:px-6 lg:px-8 bg-transparent relative z-10" id="cleaning-standards">
      <div class="max-w-7xl mx-auto">
        
        <div class="text-center max-w-3xl mx-auto mb-16">
          <span class="text-sm font-bold uppercase tracking-wider text-blue-100 bg-white/10 backdrop-blur-md border border-white/20 px-4 py-1.5 rounded-full">
            ✦ Detailed Room-by-Room Protocol in {city}, AL ✦
          </span>
          <h2 class="text-3xl md:text-4xl font-extrabold text-white mt-4 tracking-tight">
            Our Standard of Cleaning: Little Things Make The Difference
          </h2>
          <div class="mt-3 h-1 w-24 bg-gradient-to-r from-blue-400 to-indigo-400 mx-auto rounded"></div>
          <p class="mt-4 text-purple-100 text-base md:text-lg leading-relaxed">
            Every home cleaned by <strong>Zoiris Cleaning Services in {city}</strong> follows a meticulous, systematic checklist. From high-efficiency HEPA vacuuming to delicate surface polishing, we treat your home with unparalleled respect and precision.
          </p>
        </div>

        <!-- Room Checklists Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
          
          <!-- Bathrooms -->
          <div class="bg-white rounded-2xl p-6 sm:p-8 shadow-2xl border border-white/10 hover:shadow-2xl transition-all duration-300">
            <div class="flex items-center gap-4 mb-6">
              <div class="w-12 h-12 rounded-xl bg-blue-100 text-blue-600 flex items-center justify-center text-2xl">
                <i class="fas fa-bath"></i>
              </div>
              <div>
                <h3 class="text-xl font-bold text-gray-900">Bathrooms</h3>
                <p class="text-xs text-blue-600 font-semibold uppercase tracking-wide">Sanitized &amp; Sparkling</p>
              </div>
            </div>
            <ul class="space-y-3 text-sm text-gray-700">
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Tub &amp; Shower Scrub:</strong> Tiles, glass doors, walls &amp; fixtures descaled and shined.</span></li>
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Toilet Disinfection:</strong> Basin, seat, lid, outer hinges, base &amp; handle sanitized.</span></li>
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Vanity &amp; Mirrors:</strong> Countertops disinfected, chrome fixtures polished, streak-free glass.</span></li>
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Accessories &amp; Trash:</strong> Toiletries &amp; towel bars wiped down, trash emptied &amp; relined.</span></li>
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Flooring:</strong> Hand-washed tile or sanitized steam mopping.</span></li>
            </ul>
          </div>

          <!-- Kitchen & Dining -->
          <div class="bg-white rounded-2xl p-6 sm:p-8 shadow-2xl border border-white/10 hover:shadow-2xl transition-all duration-300">
            <div class="flex items-center gap-4 mb-6">
              <div class="w-12 h-12 rounded-xl bg-purple-100 text-purple-600 flex items-center justify-center text-2xl">
                <i class="fas fa-utensils"></i>
              </div>
              <div>
                <h3 class="text-xl font-bold text-gray-900">Kitchen &amp; Dining</h3>
                <p class="text-xs text-purple-600 font-semibold uppercase tracking-wide">Degreased &amp; Polished</p>
              </div>
            </div>
            <ul class="space-y-3 text-sm text-gray-700">
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Stovetop &amp; Range:</strong> Burners scrubbed, grease removed, control knobs wiped.</span></li>
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Microwave Detail:</strong> Fully cleaned and deodorized inside and outside.</span></li>
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Countertops &amp; Backsplash:</strong> Disinfected &amp; granite/quartz polished.</span></li>
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Appliance Exteriors:</strong> Refrigerator, dishwasher &amp; oven exterior stainless polish.</span></li>
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Sinks &amp; Chrome:</strong> Scrubbed, disinfected, and chrome fixtures polished.</span></li>
            </ul>
          </div>

          <!-- Living Rooms & Bedrooms -->
          <div class="bg-white rounded-2xl p-6 sm:p-8 shadow-2xl border border-white/10 hover:shadow-2xl transition-all duration-300">
            <div class="flex items-center gap-4 mb-6">
              <div class="w-12 h-12 rounded-xl bg-pink-100 text-pink-600 flex items-center justify-center text-2xl">
                <i class="fas fa-bed"></i>
              </div>
              <div>
                <h3 class="text-xl font-bold text-gray-900">Living &amp; Bedrooms</h3>
                <p class="text-xs text-pink-600 font-semibold uppercase tracking-wide">Fresh, Tidy &amp; Allergen-Free</p>
              </div>
            </div>
            <ul class="space-y-3 text-sm text-gray-700">
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Beds &amp; Linens:</strong> Beds made neatly; sheets washed &amp; changed upon request.</span></li>
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Upholstery &amp; Pet Hair:</strong> Excess pet hair vacuumed from furniture and couches.</span></li>
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Furniture Care:</strong> Wood, glass &amp; leather furniture dry or damp wiped.</span></li>
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>High-Touch Sanitation:</strong> Light switches, remotes &amp; door knobs sanitized.</span></li>
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Cobweb Removal:</strong> Corners, ceiling trims &amp; wall moldings cleared.</span></li>
            </ul>
          </div>

        </div>

      </div>
    </section>
"""

schema_pattern = re.compile(
    r'<script\s+type=["\']application/ld\+json["\']>.*?</script>',
    re.DOTALL | re.IGNORECASE
)

def enrich_location_file(filepath):
    try:
        rel = os.path.relpath(filepath, root_dir).replace('\\', '/')
        parts = rel.split('/')
        if len(parts) != 2 or not parts[0].endswith('-al') or parts[1] != 'index.html':
            return False
            
        loc_slug = parts[0]
        loc_data = LOCATIONS.get(loc_slug, {})
        city = loc_data.get('city', loc_slug[:-3].replace('-', ' ').title())
        county = loc_data.get('county', 'Alabama')
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        original_content = content
        
        # 1. Inject / Update Trust Badges in Hero if not present
        if '<!-- 🌟 TRUST SIGNALS' not in content:
            if '<!-- Scroll Down Arrow -->' in content:
                content = content.replace('<!-- Scroll Down Arrow -->', f'{get_trust_badges_html()}\n        <!-- Scroll Down Arrow -->', 1)
                
        # 2. Build complete bespoke middle block (About, Tailored Services Grid, Unique FAQs)
        new_about_html = get_localized_about_html(city, loc_slug, county)
        new_services_html = get_localized_city_services_html(city, loc_slug, county)
        new_faq_html = get_localized_faq_html(city, loc_slug, county)
        
        bespoke_hub_html = f"{new_about_html}\n\n{new_services_html}\n\n{new_faq_html}"
        
        # 3. Clean hero-to-quote-to-bottom replacement
        hero_match = re.search(r'(<section[^>]*id=["\']home["\'].*?</section>)', content, re.DOTALL | re.IGNORECASE)
        quote_match = re.search(r'(<section[^>]*id=["\']quote["\'].*?</section>)', content, re.DOTALL | re.IGNORECASE)
        loc_match = re.search(r'(<!-- =+ LOCATION SECTION =+ -->|<section[^>]*id=["\']location["\'])', content, re.DOTALL | re.IGNORECASE)
        if not loc_match:
            loc_match = re.search(r'(<footer\b)', content, re.DOTALL | re.IGNORECASE)
            
        if hero_match and quote_match and loc_match:
            top_part = content[:hero_match.end()]
            quote_block = quote_match.group(1)
            bottom_part = content[loc_match.start():]
            content = top_part + "\n\n" + bespoke_hub_html + "\n\n    " + quote_block + "\n\n    " + bottom_part
        elif hero_match and quote_match:
            hero_end = hero_match.end()
            quote_start = quote_match.start()
            content = content[:hero_end] + "\n\n" + bespoke_hub_html + "\n\n    " + content[quote_start:]
        elif '<footer' in content:
            content = content.replace('<footer', f'{bespoke_hub_html}\n    <footer', 1)
            
        # 4. Replace Schema JSON-LD with Updated 8-Question Localized Schema
        info = classify_page(filepath)
        new_schema = generate_schema(info)
        content = schema_pattern.sub('', content)
        if '<!-- Tailwind CSS Play CDN' in content:
            content = content.replace('<!-- Tailwind CSS Play CDN', f'{new_schema}\n  <!-- Tailwind CSS Play CDN', 1)
        elif '</head>' in content:
            content = content.replace('</head>', f'{new_schema}\n</head>', 1)
            
        # 5. Fix styling classes (remove lightGray, fix font-awesome icons)
        content = content.replace('class="py-16 bg-lightGray"', 'class="py-16 bg-transparent relative z-10"')
        content = content.replace('class="py-20 bg-lightGray"', 'class="py-20 bg-transparent relative z-10"')
        content = content.replace('fa-shield-check', 'fa-shield-alt')
        content = content.replace('fa-vacuum', 'fa-tools')
        content = content.replace('fa-sparkles', 'fa-magic')
        content = content.replace('fa-clock-rotate-left', 'fa-history')
        
        if content != original_content:
            tmp = filepath + '.tmp'
            with open(tmp, 'w', encoding='utf-8') as f:
                f.write(content)
            os.replace(tmp, filepath)
            return True
            
        return False
    except Exception as e:
        print(f"Error enriching {filepath}: {e}")
        return False

if __name__ == '__main__':
    import concurrent.futures
    import multiprocessing
    
    print("Starting hyper-localized location page enrichment across Alabama...")
    loc_files = []
    for slug in LOCATIONS.keys():
        fp = os.path.join(root_dir, slug, 'index.html')
        if os.path.exists(fp):
            loc_files.append(fp)
            
    print(f"Enriching {len(loc_files)} city hub pages with unique localized FAQs, About copy, Standards checklists, and Schemas...")
    
    count = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count() * 4) as executor:
        for r in executor.map(enrich_location_file, loc_files):
            if r:
                count += 1
                
    print(f"Successfully enriched {count}/{len(loc_files)} location hub pages with unique dedicated SEO architecture!")

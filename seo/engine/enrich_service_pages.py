import os
import re
import json
import sys

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bespoke_content_generator import (
    get_bespoke_location_service_html,
    generate_bespoke_service_faqs,
    get_service_meta
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

schema_pattern = re.compile(
    r'<script\s+type=["\']application/ld\+json["\']>.*?</script>',
    re.DOTALL | re.IGNORECASE
)

def enrich_service_file(filepath):
    try:
        rel = os.path.relpath(filepath, root_dir).replace('\\', '/')
        parts = rel.split('/')
        if len(parts) < 3 or not parts[0].endswith('-al') or parts[-1] != 'index.html':
            return False
            
        loc_slug = parts[0]
        service_slug = parts[1]
        
        # Skip informational subpages (about, contact, blog)
        if service_slug in ['about', 'contact', 'blog', 'terms', 'privacy']:
            return False
            
        loc_data = LOCATIONS.get(loc_slug, {})
        city = loc_data.get('city', loc_slug[:-3].replace('-', ' ').title())
        county = loc_data.get('county', 'Alabama')
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        original_content = content
        
        # 1. Inject Trust Badges in Hero if not present
        if '<!-- 🌟 TRUST SIGNALS' not in content:
            if '<!-- Scroll Down Arrow -->' in content:
                content = content.replace('<!-- Scroll Down Arrow -->', f'{get_trust_badges_html()}\n        <!-- Scroll Down Arrow -->', 1)
                
        # 2. Robust Hero to Quote to Footer reconstruction to remove all orphaned swipers, old faqs, and old abouts
        bespoke_html = get_bespoke_location_service_html(city, loc_slug, county, service_slug)
        
        hero_match = re.search(r'(<section[^>]*id=["\']home["\'].*?</section>)', content, re.DOTALL | re.IGNORECASE)
        quote_match = re.search(r'(<section[^>]*id=["\']quote["\'].*?</section>)', content, re.DOTALL | re.IGNORECASE)
        footer_match = re.search(r'(<footer\b.*)', content, re.DOTALL | re.IGNORECASE)
        
        if hero_match and quote_match and footer_match:
            top_part = content[:hero_match.end()]
            quote_block = quote_match.group(1)
            bottom_part = footer_match.group(1)
            content = top_part + "\n\n" + bespoke_html + "\n\n    " + quote_block + "\n\n    " + bottom_part
        elif hero_match and quote_match:
            hero_end = hero_match.end()
            quote_start = quote_match.start()
            content = content[:hero_end] + "\n\n" + bespoke_html + "\n\n    " + content[quote_start:]
        elif '<footer' in content:
            content = content.replace('<footer', f'{bespoke_html}\n    <footer', 1)
            
        # 3. Update Schema JSON-LD with bespoke service info and unique FAQs
        info = classify_page(filepath)
        new_schema = generate_schema(info)
        content = schema_pattern.sub('', content)
        if '<!-- Tailwind CSS Play CDN' in content:
            content = content.replace('<!-- Tailwind CSS Play CDN', f'{new_schema}\n  <!-- Tailwind CSS Play CDN', 1)
        elif '</head>' in content:
            content = content.replace('</head>', f'{new_schema}\n</head>', 1)
            
        # 4. Clean up styling classes and icons
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
        print(f"Error enriching service page {filepath}: {e}")
        return False

if __name__ == '__main__':
    import concurrent.futures
    import multiprocessing
    import argparse
    
    parser = argparse.ArgumentParser(description="Enrich location-service pages with bespoke unique content.")
    parser.add_argument("--priority-only", action="store_true", help="Enrich priority Tier A location-service pages.")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of pages processed.")
    args = parser.parse_args()
    
    print("Discovering location-service pages...")
    service_files = []
    
    priority_slugs = {
        'mobile-al', 'daphne-al', 'fairhope-al', 'spanish-fort-al', 'foley-al',
        'gulf-shores-al', 'orange-beach-al', 'saraland-al', 'semmes-al', 'theodore-al',
        'birmingham-al', 'huntsville-al', 'montgomery-al', 'tuscaloosa-al', 'auburn-al'
    }
    
    for r, d, f in os.walk(root_dir):
        if '.git' in d: d.remove('.git')
        if 'seo' in d: d.remove('seo')
        for file in f:
            if file == 'index.html':
                fp = os.path.join(r, file)
                rel = os.path.relpath(fp, root_dir).replace('\\', '/')
                parts = rel.split('/')
                if len(parts) == 3 and parts[0].endswith('-al') and parts[1] not in ['about', 'contact', 'blog', 'terms', 'privacy']:
                    if not args.priority_only or parts[0] in priority_slugs:
                        service_files.append(fp)
                        
    if args.limit:
        service_files = service_files[:args.limit]
        
    print(f"Enriching {len(service_files)} location-service pages with bespoke local content and unique FAQs...")
    
    count = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count() * 4) as executor:
        for r in executor.map(enrich_service_file, service_files):
            if r:
                count += 1
                
    print(f"Successfully enriched {count}/{len(service_files)} location-service pages!")

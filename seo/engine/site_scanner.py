import os
import re
import json
import csv
from page_classifier import classify_page

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

title_re = re.compile(r'<title>(.*?)</title>', re.IGNORECASE | re.DOTALL)
desc_re = re.compile(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', re.IGNORECASE | re.DOTALL)
canonical_re = re.compile(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', re.IGNORECASE)
h1_re = re.compile(r'<h1[^>]*>(.*?)</h1>', re.IGNORECASE | re.DOTALL)
schema_re = re.compile(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', re.IGNORECASE | re.DOTALL)

STALE_PATTERNS = [
    re.compile(r'@themaidscorp', re.IGNORECASE),
    re.compile(r'imgur\.com', re.IGNORECASE),
    re.compile(r'Match made with Zoiris', re.IGNORECASE),
    re.compile(r'Find affordable .* options in .* Search local cleaners by rates', re.IGNORECASE),
    re.compile(r'We have top-rated local cleaners in .* Explore .* services and compare', re.IGNORECASE)
]

def scan_file(filepath):
    try:
        classification = classify_page(filepath)
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        t_match = title_re.search(content)
        title = t_match.group(1).strip() if t_match else ""
        
        d_match = desc_re.search(content)
        desc = d_match.group(1).strip() if d_match else ""
        
        c_match = canonical_re.search(content)
        canonical = c_match.group(1).strip() if c_match else ""
        
        h1_match = h1_re.search(content)
        h1 = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip() if h1_match else ""
        
        has_schema = bool(schema_re.search(content))
        
        stale_hits = []
        for pat in STALE_PATTERNS:
            if pat.search(content):
                stale_hits.append(pat.pattern)
                
        has_form = "form" in content.lower()
        has_phone = "251-220-2515" in content or "(251) 220-2515" in content or "2512202515" in content
        
        return {
            "rel_path": classification["rel_path"],
            "page_type": classification["page_type"],
            "location_slug": classification["location_slug"],
            "city_name": classification["city_name"],
            "service_name": classification["service_name"],
            "tier": classification["tier"],
            "title": title,
            "title_length": len(title),
            "description": desc,
            "desc_length": len(desc),
            "canonical": canonical,
            "h1": h1,
            "has_schema": has_schema,
            "stale_flags": len(stale_hits),
            "has_form": has_form,
            "has_phone": has_phone,
            "size_bytes": len(content)
        }
    except Exception as e:
        return {
            "rel_path": filepath,
            "error": str(e)
        }

if __name__ == '__main__':
    import concurrent.futures
    import multiprocessing
    
    print("Starting full site crawl and audit...")
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        if '.git' in dirs:
            dirs.remove('.git')
        if 'seo' in dirs:
            dirs.remove('seo')
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
                
    print(f"Discovered {len(html_files)} HTML files. Running audit...")
    
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count() * 4) as executor:
        for r in executor.map(scan_file, html_files):
            results.append(r)
            
    reports_dir = os.path.join(root_dir, 'seo', 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    json_path = os.path.join(reports_dir, 'site-audit.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
        
    csv_path = os.path.join(reports_dir, 'site-audit.csv')
    if results:
        keys = results[0].keys()
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(results)
            
    total = len(results)
    stale_count = sum(1 for r in results if r.get('stale_flags', 0) > 0)
    missing_schema = sum(1 for r in results if not r.get('has_schema', False))
    print(f"Audit Complete! Scanned {total} pages.")
    print(f"Pages with stale competitor/placeholder text: {stale_count}")
    print(f"Pages missing JSON-LD schema: {missing_schema}")
    print(f"Reports saved to {csv_path} and {json_path}")

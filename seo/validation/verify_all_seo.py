import os
import re
import json
import sys

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

schema_re = re.compile(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', re.IGNORECASE | re.DOTALL)
title_re = re.compile(r'<title>(.*?)</title>', re.IGNORECASE | re.DOTALL)
desc_re = re.compile(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', re.IGNORECASE | re.DOTALL)
canonical_re = re.compile(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', re.IGNORECASE)

# Verification checks on a representative sample of pages
SAMPLE_PAGES = [
    "index.html",
    "mobile-al/index.html",
    "mobile-al/about/index.html",
    "mobile-al/house-cleaning/index.html",
    "mobile-al/deep-cleaning/index.html",
    "mobile-al/commercial-cleaning/index.html",
    "daphne-al/index.html",
    "daphne-al/deep-cleaning/index.html",
    "fairhope-al/index.html",
    "fairhope-al/move-out-cleaning/index.html",
    "gulf-shores-al/index.html",
    "gulf-shores-al/vacation-rental-cleaning/index.html",
    "foley-al/index.html",
    "foley-al/carpet-cleaning/index.html",
    "saraland-al/index.html",
    "spanish-fort-al/index.html",
    "birmingham-al/index.html",
    "birmingham-al/commercial-cleaning/index.html",
    "huntsville-al/index.html",
    "montgomery-al/index.html"
]

def verify_all():
    print("=" * 60)
    print("RUNNING ZOIRIS MASTER SEO & INTEGRITY VERIFICATION SUITE")
    print("=" * 60)
    
    passed_count = 0
    total_checks = 0
    errors = []
    
    for page_rel in SAMPLE_PAGES:
        filepath = os.path.join(root_dir, page_rel)
        if not os.path.exists(filepath):
            print(f"⚠️ Warning: Sample file {page_rel} not found.")
            continue
            
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        total_checks += 1
        page_errors = []
        
        # 1. Check Title
        t_m = title_re.search(content)
        if not t_m or not t_m.group(1).strip():
            page_errors.append("Missing title tag")
        elif "Zoiris" not in t_m.group(1):
            page_errors.append(f"Title missing brand name: '{t_m.group(1)}'")
            
        # 2. Check Description
        d_m = desc_re.search(content)
        if not d_m or not d_m.group(1).strip():
            page_errors.append("Missing meta description")
        elif "251-220-2515" not in d_m.group(1) and "(251) 220-2515" not in d_m.group(1):
            page_errors.append("Meta description missing phone number")
            
        # 3. Check Canonical
        c_m = canonical_re.search(content)
        if not c_m or not c_m.group(1).strip().startswith("https://www.zoiriscleaningservices.com"):
            page_errors.append("Invalid or missing canonical link")
            
        # 4. Check Stale Assets
        if "@themaidscorp" in content:
            page_errors.append("Contains stale @themaidscorp handle")
        if "imgur.com/yjACVrG.png" in content:
            page_errors.append("Contains stale imgur image link")
            
        # 5. Check Schema
        s_matches = schema_re.findall(content)
        if not s_matches:
            page_errors.append("Missing Schema.org JSON-LD block")
        else:
            for raw_json in s_matches:
                try:
                    data = json.loads(raw_json)
                    if "@graph" not in data and "@type" not in data:
                        page_errors.append("Schema JSON-LD missing @graph or @type")
                except Exception as e:
                    page_errors.append(f"Invalid Schema JSON-LD syntax: {e}")
                    
        # 6. Check Form & Interactive elements
        if "id=\"quote\"" in content and "toggleMobileMenu" not in content and "mobile-menu" not in content:
            page_errors.append("Missing mobile navigation scripts/markup")
            
        if page_errors:
            print(f"[FAIL]: {page_rel}")
            for err in page_errors:
                print(f"   - {err}")
                errors.append(f"{page_rel}: {err}")
        else:
            print(f"[PASS]: {page_rel}")
            passed_count += 1
            
    print("=" * 60)
    print(f"Verification Results: {passed_count}/{total_checks} sample pages passed.")
    if errors:
        print(f"Total error issues found: {len(errors)}")
        sys.exit(1)
    else:
        print("ALL SAMPLE VERIFICATION TESTS PASSED PERFECTLY!")
        sys.exit(0)

if __name__ == '__main__':
    verify_all()

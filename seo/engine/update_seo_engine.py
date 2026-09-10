import os
import re
import sys
import json
import csv
import shutil
import argparse
from datetime import datetime
import concurrent.futures
import multiprocessing

from page_classifier import classify_page
from title_generator import generate_title
from meta_generator import generate_meta_description
from schema_generator import generate_schema
from content_engine import generate_hero_content

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

head_pattern = re.compile(
    r'<title>.*?(?=<!-- / Yoast SEO plugin\. -->|<!-- Favicons -->|<!-- Local Business Schema -->)',
    re.DOTALL | re.IGNORECASE
)

# Schema removal / replacement pattern
old_schema_pattern = re.compile(
    r'<script\s+type=["\']application/ld\+json["\']>.*?</script>',
    re.DOTALL | re.IGNORECASE
)

# Hero section pattern (H1 and subtitle)
hero_pattern = re.compile(
    r'(<h1 class="text-3xl[^>]*>).*?(</h1>\s*<p class="text-base[^>]*>).*?(</p>)',
    re.DOTALL | re.IGNORECASE
)

def build_head_block(info):
    title = generate_title(info)
    desc = generate_meta_description(info)
    city = info.get("city_name", "Mobile")
    service = info.get("service_name", "House Cleaning")
    canonical_url = f"https://www.zoiriscleaningservices.com{info.get('canonical_path', '/')}"
    
    if service.lower() in ["house cleaning", "maid service"]:
        keywords = f"House Cleaning {city} AL, Maid Service {city} AL, Cleaning Services {city} AL, Residential Cleaning {city}"
    else:
        keywords = f"{service} {city} AL, House Cleaning {city} AL, Cleaning Services {city} AL"
        
    return f"""<title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta name="keywords" content="{keywords}" />
  <link rel="canonical" href="{canonical_url}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:type" content="website" />
  <meta property="og:image" content="https://www.zoiriscleaningservices.com/images/services_action.png" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:type" content="image/png" />
  <meta property="og:url" content="{canonical_url}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:site_name" content="Zoiris Cleaning Services" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{desc}" />
  <meta name="twitter:image" content="https://www.zoiriscleaningservices.com/images/services_action.png" />
  <link rel="sitemap" type="application/xml" href="https://www.zoiriscleaningservices.com/sitemap_index.xml" />
  """

def process_single_file(filepath, dry_run=False, backup_dir=None):
    try:
        info = classify_page(filepath)
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        original_content = content
        
        # 1. Update Head metadata (Title, Meta description, OG, Twitter, Canonical)
        new_head = build_head_block(info)
        content, n_head = head_pattern.subn(new_head, content, count=1)
        
        # 2. Update / Inject Schema
        schema_jsonld = generate_schema(info)
        
        # Remove any previous JSON-LD in the file
        content = old_schema_pattern.sub('', content)
        
        # Inject fresh schema right before Tailwind CDN or </head>
        if '<!-- Tailwind CSS Play CDN' in content:
            content = content.replace('<!-- Tailwind CSS Play CDN', f'{schema_jsonld}\n  <!-- Tailwind CSS Play CDN', 1)
        elif '</head>' in content:
            content = content.replace('</head>', f'{schema_jsonld}\n</head>', 1)
            
        # 3. Update Hero H1 and Subtitle
        h1_text, subtitle_text = generate_hero_content(info)
        new_h1_markup = f"\n          {h1_text}\n        "
        new_p_markup = f"\n          {subtitle_text}\n        "
        content, n_hero = hero_pattern.subn(r'\1' + new_h1_markup + r'\2' + new_p_markup + r'\3', content, count=1)
        
        # 4. Clean up any remaining @themaidscorp or imgur
        content = content.replace('@themaidscorp', 'Zoiris Cleaning Services')
        content = content.replace('https://imgur.com/yjACVrG.png', 'https://www.zoiriscleaningservices.com/images/services_action.png')
        
        modified = (content != original_content)
        
        record = {
            "rel_path": info["rel_path"],
            "page_type": info["page_type"],
            "city_name": info["city_name"],
            "service_name": info["service_name"],
            "tier": info["tier"],
            "title": generate_title(info),
            "canonical": f"https://www.zoiriscleaningservices.com{info.get('canonical_path', '/')}",
            "modified": modified,
            "status": "success"
        }
        
        if modified and not dry_run:
            # Backup if backup_dir provided
            if backup_dir:
                rel = os.path.relpath(filepath, root_dir)
                b_path = os.path.join(backup_dir, rel)
                os.makedirs(os.path.dirname(b_path), exist_ok=True)
                with open(b_path, 'w', encoding='utf-8') as bf:
                    bf.write(original_content)
                    
            # Atomic write
            tmp_path = filepath + '.tmp'
            with open(tmp_path, 'w', encoding='utf-8') as tf:
                tf.write(content)
                
            os.replace(tmp_path, filepath)
            
        return record
    except Exception as e:
        return {
            "rel_path": filepath,
            "error": str(e),
            "status": "failed"
        }

def run_engine(dry_run=False, location_filter=None, service_filter=None, priority_only=False, sample_limit=None):
    print("Collecting files for SEO engine...")
    html_files = []
    
    for root, dirs, files in os.walk(root_dir):
        if '.git' in dirs:
            dirs.remove('.git')
        if 'seo' in dirs:
            dirs.remove('seo')
        for file in files:
            if file.endswith('.html'):
                fp = os.path.join(root, file)
                rel = os.path.relpath(fp, root_dir).replace('\\', '/')
                
                # Filters
                if location_filter and not rel.startswith(location_filter):
                    continue
                if service_filter and f"/{service_filter}/" not in rel:
                    continue
                if priority_only:
                    info = classify_page(fp)
                    if info.get("tier") != "A":
                        continue
                        
                html_files.append(fp)
                
    if sample_limit and sample_limit > 0:
        html_files = html_files[:sample_limit]
        
    print(f"Targeting {len(html_files)} HTML files. (Dry Run: {dry_run})")
    
    backup_dir = None
    if not dry_run:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join(root_dir, 'seo', 'backups', ts)
        os.makedirs(backup_dir, exist_ok=True)
        print(f"Backups will be stored in {backup_dir}")
        
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count() * 4) as executor:
        futures = {executor.submit(process_single_file, fp, dry_run, backup_dir): fp for fp in html_files}
        count = 0
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            results.append(res)
            count += 1
            if count % 250 == 0:
                print(f"Processed {count}/{len(html_files)} files...", flush=True)
                
    reports_dir = os.path.join(root_dir, 'seo', 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    report_file = os.path.join(reports_dir, 'dry-run.csv' if dry_run else 'seo-change-report.csv')
    if results:
        keys = results[0].keys()
        with open(report_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(results)
            
    success_count = sum(1 for r in results if r.get('status') == 'success')
    modified_count = sum(1 for r in results if r.get('modified') is True)
    print("=" * 60)
    print(f"Engine Run Completed!")
    print(f"Total files evaluated: {len(results)}")
    print(f"Successfully processed: {success_count}")
    print(f"Files modified: {modified_count}")
    print(f"Report written to: {report_file}")
    print("=" * 60)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Zoiris SEO Domination Engine")
    parser.add_argument('--dry-run', action='store_true', help="Run without writing files")
    parser.add_argument('--location', type=str, help="Filter by location slug (e.g. mobile-al)")
    parser.add_argument('--service', type=str, help="Filter by service slug (e.g. deep-cleaning)")
    parser.add_argument('--priority-only', action='store_true', help="Process only Tier A locations")
    parser.add_argument('--sample', type=int, help="Limit to N sample files")
    
    args = parser.parse_args()
    run_engine(
        dry_run=args.dry_run,
        location_filter=args.location,
        service_filter=args.service,
        priority_only=args.priority_only,
        sample_limit=args.sample
    )

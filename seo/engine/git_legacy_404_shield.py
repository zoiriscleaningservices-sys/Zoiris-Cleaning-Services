import os
import sys
import re
import shutil
import subprocess

engine_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(engine_dir))
sys.path.insert(0, engine_dir)

from geo_service_content import LOCATIONS, SERVICES
from master_overhaul import DET_MAP, build_redirect_stub, generate_clean_sitemaps_and_robots
import extreme_authority_expansion
import peak_url_recovery_and_crawl_booster
from peak_url_recovery_and_crawl_booster import map_legacy_path_to_canonical

SAFE_WILDCARDS = [
    "!/*-al/affordable-*/",
    "!/*-al/best-*/",
    "!/*-al/top-rated-*/",
    "!/*-al/[0-9][0-9][0-9][0-9][0-9]-*/",
    "!/*-al/detailing/",
    "!/*-al/nearby-locations/",
    "!/*-al/gallery/",
]

WILDCARD_RES = [
    re.compile(r"^[^/]+-al/(?:affordable|best|top-rated)-[^/]+/index\.html$"),
    re.compile(r"^[^/]+-al/\d{5}-[^/]+/index\.html$"),
    re.compile(r"^[^/]+-al/(?:detailing|nearby-locations|gallery)/index\.html$"),
]

def matches_safe_wildcard(p):
    return any(rx.match(p) for rx in WILDCARD_RES)

def ensure_root_favicons():
    fav_src = os.path.join(root_dir, "favicon", "favicon.ico")
    fav_dst = os.path.join(root_dir, "favicon.ico")
    if os.path.isfile(fav_src):
        shutil.copy2(fav_src, fav_dst)
        print("  -> Copied root /favicon.ico")

    app_src = os.path.join(root_dir, "favicon", "apple-touch-icon.png")
    app_dst = os.path.join(root_dir, "apple-touch-icon.png")
    if os.path.isfile(app_src):
        shutil.copy2(app_src, app_dst)
        print("  -> Copied root /apple-touch-icon.png")

def collect_all_historical_and_pattern_paths():
    candidates = set()

    # 1. Every .html path & sitemap <loc> ever committed in Git history
    commits = subprocess.check_output(["git", "-C", root_dir, "rev-list", "--all"], text=True).splitlines()
    xml_shas = set()
    for c in commits:
        for line in subprocess.check_output(["git", "-C", root_dir, "ls-tree", "-r", c], text=True).splitlines():
            parts = line.split("\t", 1)
            if len(parts) != 2:
                continue
            meta, path = parts
            if path.startswith("seo/") or path in ("dashboard.html", "Gallery/Dash.html", "404.html"):
                continue
            if path.endswith(".html"):
                candidates.add(path)
            elif path.endswith(".xml") and "sitemap" in path.lower():
                xml_shas.add(meta.split()[2])

    loc_re = re.compile(r"<loc>\s*https?://[^/]+(/[^<\s]*)\s*</loc>", re.I)
    for sha in xml_shas:
        xml_txt = subprocess.check_output(["git", "-C", root_dir, "cat-file", "-p", sha], text=True, errors="replace")
        for m in loc_re.finditer(xml_txt):
            u = m.group(1).strip()
            if not u or u == "/" or u.endswith(".xml"):
                continue
            clean = u.lstrip("/")
            if clean.endswith(".html"):
                candidates.add(clean)
            else:
                candidates.add(clean.rstrip("/") + "/index.html")

    # 2. Deterministic legacy link patterns across all 503 Alabama cities
    for c_slug, loc in LOCATIONS.items():
        no_al = c_slug[:-3]
        city_name = loc["city"]
        candidates.add(f"downtown-{c_slug}/index.html")
        candidates.add(f"downtown-{no_al}/index.html")
        candidates.add(f"midtown-{c_slug}/index.html")
        candidates.add(f"midtown-{no_al}/index.html")
        candidates.add(f"west-{c_slug}/index.html")
        candidates.add(f"west-{no_al}/index.html")
        candidates.add(f"maid-service-{c_slug}-al/index.html")
        candidates.add(f"maid-service-{c_slug}/index.html")
        candidates.add(f"maid-service-{no_al}/index.html")
        candidates.add(f"{no_al}/index.html")
        candidates.add(f"{c_slug}/detailing/index.html")
        candidates.add(f"{c_slug}/nearby-locations/index.html")
        candidates.add(f"{c_slug}/gallery/index.html")
        candidates.add(f"{c_slug}/Detailing-{city_name}-AL/index.html")
        candidates.add(f"{c_slug}/Detailing-{no_al.title()}-AL/index.html")
        candidates.add(f"{c_slug}/Detailing-{c_slug}/index.html")
        candidates.add(f"{c_slug}/detailing-{c_slug}/index.html")

    # 3. Jackson's Gap apostrophe variants
    for jprefix in ("jackson's-gap-al", "jackson&#39;s-gap-al"):
        candidates.add(f"{jprefix}/index.html")
        for sub in list(SERVICES.keys()) + ["about", "blog", "contact"]:
            if sub == "detailing":
                candidates.add(f"{jprefix}/Detailing-Jackson's Gap-AL/index.html")
                candidates.add(f"{jprefix}/Detailing-Jackson&#39;s Gap-AL/index.html")
                candidates.add(f"{jprefix}/detailing/index.html")
            else:
                candidates.add(f"{jprefix}/{sub}/index.html")

    return sorted(candidates)

import tempfile

def hash_blobs_batch(tgt_rels):
    """Hash all unique redirect stubs in ONE single git hash-object -w --stdin-paths call!"""
    blob_map = {}
    if not tgt_rels:
        return blob_map
    with tempfile.TemporaryDirectory() as td:
        paths = []
        ordered = sorted(tgt_rels)
        for i, tgt_rel in enumerate(ordered):
            tgt_url = "https://www.zoiriscleaningservices.com" + tgt_rel
            stub_html = build_redirect_stub(tgt_url, tgt_rel, f"Zoiris Cleaning Services ({tgt_rel})")
            fp = os.path.join(td, f"stub_{i}.html")
            with open(fp, "w", encoding="utf-8", newline="\n") as f:
                f.write(stub_html)
            paths.append(fp)
        out = subprocess.check_output(
            ["git", "-C", root_dir, "-c", "core.autocrlf=false", "hash-object", "-w", "--stdin-paths"],
            input=("\n".join(paths) + "\n").encode("utf-8")
        ).decode("utf-8").splitlines()
        for tgt_rel, sha in zip(ordered, out):
            blob_map[tgt_rel] = sha.strip()
    return blob_map

def main():
    os.chdir(root_dir)
    subprocess.check_call(["git", "config", "core.sparseCheckout", "false"])

    if "--skip-rebuild" not in sys.argv:
        print("1. Ensuring root favicons + refreshing sitemaps, pillars/guides/blog, and feed.xml...")
        ensure_root_favicons()
        generate_clean_sitemaps_and_robots()
        extreme_authority_expansion.main()
        peak_url_recovery_and_crawl_booster.main()

    print("2. Staging all on-disk files cleanly before injecting legacy 404 shield...")
    subprocess.check_call(["git", "add", "-A"])

    staged_lines = subprocess.check_output(["git", "ls-files", "--stage"], text=True, encoding="utf-8").splitlines()
    staged_exact = {}
    staged_lower = {}
    for line in staged_lines:
        meta, path = line.split("\t", 1)
        sha = meta.split()[1]
        staged_exact[path] = sha
        # Prefer real on-disk file for lower lookup
        if os.path.exists(os.path.join(root_dir, path.replace("/", os.sep))):
            staged_lower[path.lower()] = (path, sha)
        elif path.lower() not in staged_lower:
            staged_lower[path.lower()] = (path, sha)

    print(f"  -> Staged exact entries: {len(staged_exact)}")

    print("3. Collecting 100% of historical & legacy URL candidates across all 60 commits...")
    candidates = collect_all_historical_and_pattern_paths()
    print(f"  -> Total candidate legacy HTML paths inspected: {len(candidates)}")

    case_alias_entries = []
    pending_redirects = []
    needed_targets = set()
    explicit_sparse_excludes = set()

    for p in candidates:
        # Skip illegal git/URL control chars
        if any(ch in p for ch in ('"', "<", ">", "|", "?", "*")):
            continue
        if p in staged_exact:
            continue

        low = p.lower()
        if low in staged_lower:
            orig_path, orig_sha = staged_lower[low]
            # Only mirror SHA when the underlying file exists on Windows disk (case-variant alias!)
            if os.path.exists(os.path.join(root_dir, orig_path.replace("/", os.sep))):
                case_alias_entries.append(f"100644 blob {orig_sha}\t{p}")
                continue

        # Otherwise, queue canonical 0-second HTTP-200 redirect stub!
        tgt_rel = map_legacy_path_to_canonical("/" + p)
        needed_targets.add(tgt_rel)
        pending_redirects.append((p, tgt_rel))

        if not matches_safe_wildcard(p):
            parent = p.rsplit("/", 1)[0] if "/" in p else p
            disk_target = os.path.join(root_dir, parent.replace("/", os.sep))
            if not os.path.exists(disk_target):
                if "/" in p:
                    explicit_sparse_excludes.add(f"!/{parent}/")
                else:
                    explicit_sparse_excludes.add(f"!/{p}")

    print(f"  -> Hashing {len(needed_targets)} unique canonical redirect blobs in 1 batch...")
    blob_cache = hash_blobs_batch(needed_targets)
    redirect_entries = [f"100644 blob {blob_cache[tgt_rel]}\t{p}" for p, tgt_rel in pending_redirects]

    print(f"  -> Linux Case-Variant Aliases (e.g. Detailing-Hurtsboro-AL): {len(case_alias_entries)}")
    print(f"  -> Missing Legacy Redirect Stubs (deduped into {len(blob_cache)} blobs): {len(redirect_entries)}")
    print(f"  -> Explicit non-wildcard sparse exclusions: {len(explicit_sparse_excludes)}")

    print("4. Injecting all case-aliases & redirect stubs into Git index (binary LF mode)...")
    all_index_lines = ("\n".join(case_alias_entries + redirect_entries) + "\n").encode("utf-8")
    subprocess.run(
        ["git", "update-index", "--index-info"],
        input=all_index_lines,
        check=True
    )

    print("5. Writing .git/info/sparse-checkout rules...")
    sc_path = os.path.join(root_dir, ".git", "info", "sparse-checkout")
    sc_lines = ["/*"] + SAFE_WILDCARDS + sorted(explicit_sparse_excludes)
    with open(sc_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(sc_lines) + "\n")

    print("LEGACY 404 SHIELD STAGED IN GIT INDEX — COMMITTING & REAPPLYING SPARSE-CHECKOUT NEXT!")

if __name__ == "__main__":
    main()

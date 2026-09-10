import os
import re
import json
import math
from collections import Counter

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Regex to strip header, footer, scripts, styles, and shared chrome
NAV_RE = re.compile(r'<header.*?</header>', re.IGNORECASE | re.DOTALL)
FOOTER_RE = re.compile(r'<footer.*?</footer>', re.IGNORECASE | re.DOTALL)
QUOTE_RE = re.compile(r'<section[^>]*id=["\']quote["\'].*?</section>', re.IGNORECASE | re.DOTALL)
LOCATION_DIR_RE = re.compile(r'<section[^>]*id=["\']location["\'].*?</section>', re.IGNORECASE | re.DOTALL)
SCRIPT_RE = re.compile(r'<script.*?</script>', re.IGNORECASE | re.DOTALL)
STYLE_RE = re.compile(r'<style.*?</style>', re.IGNORECASE | re.DOTALL)
SVG_RE = re.compile(r'<svg.*?</svg>', re.IGNORECASE | re.DOTALL)
TAG_RE = re.compile(r'<[^>]+>')
PHONE_RE = re.compile(r'251[-.\s]?220[-.\s]?2515|\(251\)\s*220-2515', re.IGNORECASE)
BOILERPLATE_RE = re.compile(r'Zoiris Cleaning Services LLC|zoiriscleaningservices@gmail\.com|Licensed, bonded & insured', re.IGNORECASE)

STOP_WORDS = {
    'the', 'and', 'to', 'of', 'a', 'in', 'is', 'that', 'for', 'it', 'as', 'was', 'with', 'be',
    'by', 'on', 'not', 'he', 'i', 'this', 'have', 'from', 'at', 'which', 'or', 'an', 'they',
    'you', 'were', 'their', 'we', 'our', 'your', 'are', 'all', 'any', 'can', 'will', 'do', 'so'
}

def extract_core_body_text(html_content):
    """Extracts unique primary body content by removing shared chrome and markup."""
    text = NAV_RE.sub(' ', html_content)
    text = FOOTER_RE.sub(' ', text)
    text = QUOTE_RE.sub(' ', text)
    text = LOCATION_DIR_RE.sub(' ', text)
    text = SCRIPT_RE.sub(' ', text)
    text = STYLE_RE.sub(' ', text)
    text = SVG_RE.sub(' ', text)
    text = PHONE_RE.sub(' ', text)
    text = BOILERPLATE_RE.sub(' ', text)
    text = TAG_RE.sub(' ', text)
    
    # Normalize words
    words = re.findall(r'[a-zA-Z]{3,}', text.lower())
    filtered_words = [w for w in words if w not in STOP_WORDS]
    return filtered_words

def compute_tf_idf_cosine_similarity(words1, words2):
    """Calculates cosine similarity between two word frequency distributions."""
    if not words1 or not words2:
        return 0.0
        
    vec1 = Counter(words1)
    vec2 = Counter(words2)
    
    intersection = set(vec1.keys()) & set(vec2.keys())
    dot_product = sum(vec1[x] * vec2[x] for x in intersection)
    
    sum1 = sum(v ** 2 for v in vec1.values())
    sum2 = sum(v ** 2 for v in vec2.values())
    
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    if not denominator:
        return 0.0
    return float(dot_product) / denominator

def compute_jaccard_ngram_similarity(words1, words2, n=3):
    """Calculates Jaccard similarity of word n-grams."""
    if len(words1) < n or len(words2) < n:
        return 0.0
        
    ngrams1 = set(tuple(words1[i:i+n]) for i in range(len(words1) - n + 1))
    ngrams2 = set(tuple(words2[i:i+n]) for i in range(len(words2) - n + 1))
    
    intersection = len(ngrams1 & ngrams2)
    union = len(ngrams1 | ngrams2)
    
    return intersection / union if union else 0.0

def audit_page_pair(file1_path, file2_path):
    """Audits similarity between two files and returns metrics."""
    with open(file1_path, 'r', encoding='utf-8', errors='ignore') as f1:
        c1 = f1.read()
    with open(file2_path, 'r', encoding='utf-8', errors='ignore') as f2:
        c2 = f2.read()
        
    w1 = extract_core_body_text(c1)
    w2 = extract_core_body_text(c2)
    
    cosine_sim = compute_tf_idf_cosine_similarity(w1, w2)
    jaccard_3gram = compute_jaccard_ngram_similarity(w1, w2, n=3)
    
    return {
        "file1": os.path.relpath(file1_path, root_dir).replace('\\', '/'),
        "file2": os.path.relpath(file2_path, root_dir).replace('\\', '/'),
        "words_count1": len(w1),
        "words_count2": len(w2),
        "cosine_similarity": round(cosine_sim, 4),
        "jaccard_3gram": round(jaccard_3gram, 4),
        "is_substantially_different": (cosine_sim < 0.50 and jaccard_3gram < 0.20)
    }

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Audit content similarity across location and service pages.")
    parser.add_argument("--sample", action="store_true", help="Run similarity audit on key representative sample pairs.")
    args = parser.parse_args()
    
    print("=" * 70)
    print("ZOIRIS CONTENT UNIQUENESS & SIMILARITY AUDITOR")
    print("=" * 70)
    
    sample_pairs = [
        ("daphne-al/deep-cleaning/index.html", "gulf-shores-al/deep-cleaning/index.html"),
        ("daphne-al/deep-cleaning/index.html", "fairhope-al/deep-cleaning/index.html"),
        ("mobile-al/deep-cleaning/index.html", "gulf-shores-al/deep-cleaning/index.html"),
        ("daphne-al/index.html", "gulf-shores-al/index.html"),
        ("daphne-al/index.html", "fairhope-al/index.html"),
        ("mobile-al/index.html", "birmingham-al/index.html"),
        ("huntsville-al/index.html", "gulf-shores-al/index.html")
    ]
    
    results = []
    for p1, p2 in sample_pairs:
        fp1 = os.path.join(root_dir, p1)
        fp2 = os.path.join(root_dir, p2)
        if os.path.exists(fp1) and os.path.exists(fp2):
            res = audit_page_pair(fp1, fp2)
            results.append(res)
            print(f"\nComparing:")
            print(f"  Page 1: {res['file1']} ({res['words_count1']} body words)")
            print(f"  Page 2: {res['file2']} ({res['words_count2']} body words)")
            print(f"  Cosine Similarity: {res['cosine_similarity'] * 100:.1f}%")
            print(f"  3-Gram Overlap:    {res['jaccard_3gram'] * 100:.1f}%")
            status = "[PASS] Substantially Unique" if res['is_substantially_different'] else "[FLAGGED] High Overlap"
            print(f"  Status: {status}")
            
    print("\n" + "=" * 70)
    passed = sum(1 for r in results if r['is_substantially_different'])
    print(f"Audit Summary: {passed}/{len(results)} sample pairs meet strict Meaningful Uniqueness criteria.")
    print("=" * 70)

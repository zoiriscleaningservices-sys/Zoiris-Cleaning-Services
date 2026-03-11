import os
import re
import random
import argparse

# --- SPINTAX ENGINE ---
def spin(text):
    """Parses standard spintax {option1|option2|option3} recursively."""
    while True:
        match = re.search(r'\{([^{}]*)\}', text)
        if not match:
            break
        options = match.group(1).split('|')
        choice = random.choice(options)
        text = text[:match.start()] + choice + text[match.end():]
    return text

# --- SEO TEMPLATES ---

TITLE_TEMPLATES = [
    "{#1|Top} <service> in <city> | Zoiris Cleaning Services",
    "Zoiris Cleaning Services: {#1|Best} <service> <city>",
    "<service> <city> | Zoiris Cleaning Services"
]

DESC_TEMPLATES = [
    "Looking for the {best|top|most reliable|#1} <service> in <city>? Zoiris Cleaning Services {delivers|provides|guarantees} {flawless|spotless|perfect|immaculate} results every time. {We specialize in residential and commercial cleaning|Our expert team handles all your cleaning needs|Get a 100% satisfaction guarantee with every clean}. {Book your appointment today|Call us now for a free quote|Experience the best cleaning in town} and {see the difference|let us make your space shine|enjoy a spotless environment}! {Top rated cleaners|Trusted by locals|Affordable & reliable}.",
    
    "Zoiris Cleaning Services is your {trusted|#1|go-to|premier} choice for premium <service> in <city>. {Whether you need a deep clean or regular maintenance|From homes to massive office spaces|No job is too big or small}, {our professional team has you covered|we deliver extreme cleanliness|we guarantee your absolute satisfaction}. {Don't settle for less than the best|Experience elite cleaning standards|Join hundreds of happy customers} in <city>. {Call Zoiris Cleaning Services today for a spotless transformation|Book now for guaranteed perfection|Get your free estimate immediately}!",
    
    "{Get|Experience|Discover} the absolute {best|highest-rated|most thorough|ultimate} <service> <city> has to offer with Zoiris Cleaning Services. {We use eco-friendly products|Our meticulous staff leaves nothing untouched|We guarantee 100% pristine results}. {Perfect for busy professionals|Ideal for homes and businesses|Trusted by property managers everywhere}. {Why choose anyone else?|We are clearly the superior choice|Stop stressing over messes}. {Contact Zoiris Cleaning Services today|Schedule your extreme clean now|Let us handle the dirty work}!"
]

H1_TEMPLATES = [
    "The {Best|#1|Top-Rated|Most Trusted} <service> in <city>",
    "{Premium|Expert|Elite|Professional} <service> Services in <city>",
    "Zoiris Cleaning Services: <city>'s {#1|Best|Elite} <service>",
    "{Ultimate|Flawless|Spotless} <service> in <city>"
]

P_TEMPLATES = [
    "<strong>Zoiris Cleaning Services</strong> guarantees the absolute {best|highest quality|most meticulous} <em><service> <city></em> has to offer. <strong>Trusted across <city> & surrounding areas</strong>. {From deep cleans to move-in/out and eco-friendly solutions|Whether it's a massive commercial space or an intimate residential home|We pride ourselves on attention to detail}, we ensure your space is spotless with a 100% satisfaction guarantee. <span class=\"font-semibold text-blue-400\">Book the #1 <service> in <city> today</span>.",
    
    "When it comes to <em><service> in <city></em>, <strong>Zoiris Cleaning Services</strong> is the {undisputed|proven|absolute} leader. <strong>We set the standard for extreme cleanliness in <city></strong>. {Our professional teams use top-tier equipment|We combine efficiency with meticulous care|Every corner is scrubbed to perfection}, leaving your environment pristine. <span class=\"font-semibold text-blue-400\">Experience the superior difference by booking Zoiris Cleaning Services today</span>.",
    
    "Choose <strong>Zoiris Cleaning Services</strong> for {elite|unmatched|unparalleled} <em><service> <city></em>. <strong>We dominate the competition with our meticulous attention to detail</strong>. {Stop settling for average cleaners|Your home or business deserves the absolute best|We treat every property like a palace}. <span class=\"font-semibold text-blue-400\">Trust the true experts in <city> and get a free quote instantly!</span>"
]


def format_location(folder_name):
    # e.g. "mobile-al" -> "Mobile, AL"
    if not folder_name.endswith("-al") and not folder_name.endswith("-tx"):
        # Just capitalize it if it doesn't match the state format perfectly
        return folder_name.replace('-', ' ').title()
    
    parts = folder_name.split('-')
    state = parts[-1].upper()
    city = " ".join(parts[:-1]).title()
    return f"{city}, {state}"

def format_service(folder_name):
    if folder_name == "index.html" or folder_name.endswith("-al") or folder_name.endswith("-tx"):
        return "Cleaning Services"
    
    # e.g. "deep-cleaning" -> "Deep Cleaning"
    return folder_name.replace('-', ' ').title()


def generate_seo(city, service):
    # Title: Try to keep under 65 chars
    # We will spin multiple times and pick the best length one if possible, or just truncate smartly if needed.
    # Actually, spinning is random, let's just generate a few and pick one <= 65 that is longest, or just the first if all > 65
    
    candidates = []
    for _ in range(10):
        t = spin(random.choice(TITLE_TEMPLATES)).replace('<city>', city).replace('<service>', service)
        candidates.append(t)
    
    valid_titles = [t for t in candidates if len(t) <= 65]
    if valid_titles:
        title = sorted(valid_titles, key=len, reverse=True)[0]
    else:
        # If all are over 65, force truncation safely
        # E.g. Top Cleaning Services Mobile... | Zoiris Cleaning Services
        t = candidates[0]
        if " | Zoiris Cleaning Services" in t:
            prefix = t.replace(" | Zoiris Cleaning Services", "")
            max_prefix_len = 65 - len(" | Zoiris Cleaning Services") - 3
            title = prefix[:max_prefix_len] + "... | Zoiris Cleaning Services"
        elif "Zoiris Cleaning Services: " in t:
            suffix = t.replace("Zoiris Cleaning Services: ", "")
            max_suffix_len = 65 - len("Zoiris Cleaning Services: ") - 3
            title = "Zoiris Cleaning Services: " + suffix[:max_suffix_len] + "..."
        else:
            title = t[:62] + "..."

    # Description: max 320 chars, try to make it meaty.
    desc_candidates = []
    for _ in range(10):
        d = spin(random.choice(DESC_TEMPLATES)).replace('<city>', city).replace('<service>', service)
        desc_candidates.append(d)
    
    valid_descs = [d for d in desc_candidates if len(d) <= 320]
    if valid_descs:
        desc = sorted(valid_descs, key=len, reverse=True)[0]
    else:
        desc = desc_candidates[0][:317] + "..."

    h1 = spin(random.choice(H1_TEMPLATES)).replace('<city>', city).replace('<service>', service)
    p_text = spin(random.choice(P_TEMPLATES)).replace('<city>', city).replace('<service>', service)
    
    return title, desc, h1, p_text


def process_file(filepath, city_name, service_name):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False
        
    title, desc, h1, p_text = generate_seo(city_name, service_name)
    
    original_content = content
    
    # 1. Replace <title>
    content = re.sub(r'(<title>)(.*?)(</title>)', rf'\1{title}\3', content, flags=re.IGNORECASE | re.DOTALL)
    
    # 2. Replace <meta name="description" ...>
    # Note: Description might span multiple lines.
    content = re.sub(
        r'(<meta\s+name=["\']description["\']\s+content=["\'])(.*?)(["\']\s*/?>)', 
        rf'\g<1>{desc}\g<3>', 
        content, 
        flags=re.IGNORECASE | re.DOTALL
    )
    
    # 3. Replace OG Title
    content = re.sub(
        r'(<meta\s+property=["\']og:title["\']\s+content=["\'])(.*?)(["\']\s*/?>)', 
        rf'\g<1>{title}\g<3>', 
        content, 
        flags=re.IGNORECASE | re.DOTALL
    )
    
    # 4. Replace OG Description
    content = re.sub(
        r'(<meta\s+property=["\']og:description["\']\s+content=["\'])(.*?)(["\']\s*/?>)', 
        rf'\g<1>{desc}\g<3>', 
        content, 
        flags=re.IGNORECASE | re.DOTALL
    )
    
    # 5. Replace H1 text (preserving attributes)
    # <h1 class="...">Old Text</h1> -> <h1 class="...">New Text</h1>
    content = re.sub(
        r'(<h1[^>]*>)(.*?)(</h1>)',
        rf'\g<1>\n          {h1}\n        \g<3>',
        content,
        flags=re.IGNORECASE | re.DOTALL
    )
    
    # 6. Replace the Hero <p> tag text
    # The hero p tag is typically right after the h1. 
    # It has classes like "text-base md:text-lg text-white font-medium max-w-md mx-auto mb-6 leading-relaxed"
    # We will look for <p class="text-base md:text-lg text-white font-medium max-w-md mx-auto mb-6 leading-relaxed">...</p>
    content = re.sub(
        r'(<p\s+class=["\']text-base md:text-lg text-white font-medium max-w-md mx-auto mb-6 leading-relaxed["\'][^>]*>)(.*?)(</p>)',
        rf'\g<1>\n          {p_text}\n        \g<3>',
        content,
        flags=re.IGNORECASE | re.DOTALL
    )
    
    if content != original_content:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error writing {filepath}: {e}")
            return False
    return False

def main():
    parser = argparse.ArgumentParser(description="Extreme SEO Overhaul Script")
    parser.add_argument("--test", action="store_true", help="Run only on a small test subset (mobile-al)")
    parser.add_argument("--dir", type=str, default=".", help="Base directory to start replacing")
    args = parser.parse_args()
    
    base_dir = args.dir
    files_processed = 0
    files_updated = 0
    
    for root, dirs, files in os.walk(base_dir):
        rel_path = os.path.relpath(root, base_dir)
        if rel_path == '.': 
            continue
            
        parts = rel_path.split(os.sep)
        city_slug = parts[0]
        
        # Only process known city folders (optimization)
        if not (city_slug.endswith('-al') or city_slug.endswith('-tx')):
            continue
            
        if args.test and city_slug != 'mobile-al':
            continue
            
        # Determine City Name
        city_name = format_location(city_slug)
        
        # Determine Service Name
        if len(parts) == 1:
            service_name = "Cleaning Services" # Main city page
        else:
            service_slug = parts[1]
            # Ignore non-service folders like "blog", "contact", "about", "images"
            if service_slug in ["blog", "contact", "about", "images"]:
                continue
            service_name = format_service(service_slug)
            
        for file in files:
            if not file.endswith('.html'):
                continue
                
            filepath = os.path.join(root, file)
            # print(f"Processing: {filepath} | City: {city_name} | Service: {service_name}")
            
            if process_file(filepath, city_name, service_name):
                files_updated += 1
            files_processed += 1
            
            # If testing, stop early so we don't flood the logs
            if args.test and files_processed >= 10:
                print(f"Test mode finished. Processed {files_processed} files, updated {files_updated}.")
                return
                
    print(f"Global Run Finished! Processed {files_processed} files, updated {files_updated}.")


if __name__ == "__main__":
    main()

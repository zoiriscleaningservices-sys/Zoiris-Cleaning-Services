"""
Statewide Spintax SEO Engine v2 - Multithreaded
Generates unique competitor-comparison blocks for every Alabama city.
"""
import os
import glob
import random
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

BASE_DIR = r"c:\Users\lucia\Downloads\Zoiris-Cleaning-Services"
SKIP_DIRS = {"mobile-al", "albertville-al", "assets", "node_modules"}

TARGET_PATTERNS = [
    "    </section>\n\n    <section class=\"py-16 bg-lightGray\" id=\"services\">",
    "    </section>\n    <section class=\"py-16 bg-lightGray\" id=\"services\">",
]

SKIP_MARKER = "zcs-spintax-injected"

# ─────────────────────── SPINTAX DATA ────────────────────────

COMPETITOR_MAP = {
    "birmingham-al":        ["MaidPro", "The Cleaning Authority", "Merry Maids", "Lemon & Love"],
    "huntsville-al":        ["Bear Brothers Cleaning", "Rosie Cleans", "Two Maids of Huntsville"],
    "montgomery-al":        ["The Tidy Toad Cleaning", "The Maids", "Merry Maids", "Two Maids"],
    "tuscaloosa-al":        ["Alabama Extra Mile", "Bear Brothers", "Two Maids of Tuscaloosa"],
    "mobile-al":            ["Merry Maids", "Molly Maid", "Homeaglow"],
    "auburn-al":            ["Two Maids", "The Maids", "Molly Maid"],
    "dothan-al":            ["Merry Maids", "Molly Maid", "CottageCare"],
    "decatur-al":           ["MaidPro", "Two Maids", "Molly Maid"],
    "hoover-al":            ["The Cleaning Authority", "MaidPro", "Merry Maids"],
    "madison-al":           ["Two Maids", "MaidPro", "Pure + Natural"],
    "gadsden-al":           ["Merry Maids", "The Maids", "Molly Maid"],
    "vestavia-hills-al":    ["The Cleaning Authority", "MaidPro", "Merry Maids"],
    "prattville-al":        ["Molly Maid", "The Maids", "Merry Maids"],
    "phenix-city-al":       ["Merry Maids", "Two Maids", "The Maids"],
    "anniston-al":          ["Merry Maids", "Molly Maid", "CottageCare"],
    "albertville-al":       ["Norma's House Cleaning", "Merry Maids", "Molly Maid"],
    "DEFAULT": [
        "Merry Maids", "Molly Maid", "The Maids", "MaidPro",
        "The Cleaning Authority", "Two Maids", "CottageCare",
        "Homeaglow Cleaners", "Angi Certified Cleaners",
        "Local Franchise Maid Service"
    ]
}

HEADLINE_TEMPLATES = [
    "Looking for a Superior Alternative to {competitor} in {city}, AL?",
    "Tired of {competitor}? Discover {city}'s Best Local Cleaners",
    "Why {city} Residents Choose Zoiris Over {competitor}",
    "The #1 {city} Alternative to {competitor} — Zoiris Cleaning Services",
    "Searching for Reliable Cleaners Over {competitor} in {city}?",
    "Moving on from {competitor}? Meet {city}'s Trusted Cleaning Team",
    "How Zoiris Outperforms {competitor} for {city}, AL Homeowners",
    "{city}'s Top-Rated Cleaning Service vs. {competitor}",
]

INTROS = [
    "Homeowners across {city} who have tried large national services like <strong>{competitor}</strong> often tell us the same thing: cleaning felt rushed, impersonal, and inconsistent. <strong>Zoiris Cleaning Services</strong> was built to solve exactly that — delivering a meticulous, personalized, and genuinely local clean every single time.",
    "When comparing your options for professional cleaning in {city}, AL, it's easy to default to a recognizable brand like <strong>{competitor}</strong>. But local residents who switch to <strong>Zoiris Cleaning Services</strong> consistently report the difference is remarkable — more thorough, more flexible, and far more personal.",
    "Many {city} residents searching for alternatives to <strong>{competitor}</strong> end up choosing <strong>Zoiris Cleaning Services</strong> — and once they do, they never look back. From our eco-friendly products to our bonded, background-checked professionals, we set a new standard for cleaning in {city} and surrounding communities.",
    "If you've been relying on <strong>{competitor}</strong> for your {city} home but feel like something's missing, you're not alone. <strong>Zoiris Cleaning Services</strong> has become the go-to alternative for discerning homeowners who demand consistency, attention to detail, and true local expertise.",
]

FEATURES = [
    {
        "icon": "fa-medal",
        "titles": ["Unmatched Thoroughness", "Deep-Clean Precision", "Elite Cleaning Standards"],
        "descs": [
            "We clean areas that rushed franchise teams consistently skip — from ceiling fan blades to baseboards, every inch of your {city} home is addressed.",
            "Our {city} team follows a rigorous checklist that consistently outperforms standard franchise routines used by companies like {competitor}.",
            "No job is 'good enough' for us. We stay until every surface in your {city} property meets our own high standards — not just a corporate quota.",
        ]
    },
    {
        "icon": "fa-user-friends",
        "titles": ["Your Dedicated Local Team", "Consistent, Familiar Cleaners", "A Team You Can Trust"],
        "descs": [
            "Unlike {competitor}, we assign you a consistent team for repeat visits, so your {city} home is always in familiar, caring hands.",
            "No stranger at your door every visit. Your Zoiris team in {city} gets to know your home inside and out for a cleaner that's perfectly tailored to you.",
            "We believe trust is everything. That's why every Zoiris cleaner serving {city} is fully bonded, insured, and personally vetted by our management team.",
        ]
    },
    {
        "icon": "fa-leaf",
        "titles": ["100% Eco-Friendly Products", "Safe for Kids, Pets & Planet", "Green Cleaning Experts"],
        "descs": [
            "We use only plant-based, non-toxic cleaning solutions — protecting your {city} family, pets, and indoor air quality without sacrificing cleaning power.",
            "Where {competitor} may rely on industrial chemicals, we've committed to natural, cruelty-free solutions that are tough on grime and gentle on your {city} home.",
            "Every product we bring into your {city} property is meticulously sourced to be eco-conscious, fragrance-safe, and highly effective.",
        ]
    },
    {
        "icon": "fa-star",
        "titles": ["5-Star Rated by {city} Locals", "Award-Winning Service", "Loved by {city} Homeowners"],
        "descs": [
            "Don't take our word for it — our {city} clients consistently rate us 5 stars for reliability, attention to detail, and outstanding communication.",
            "We've earned the trust of hundreds of families across {city} by delivering an exceptional cleaning experience that outshines competitors like {competitor}.",
            "Our {city} reviews speak for themselves. Homeowners switching from {competitor} regularly note that Zoiris exceeds their expectations on the very first visit.",
        ]
    },
]

CTAS = [
    "Join hundreds of happy {city} homeowners — book your first clean today.",
    "Ready to experience the Zoiris difference in {city}? Get your free quote.",
    "Don't settle for {competitor}'s standards. Upgrade to Zoiris in {city} today.",
    "The {city} home you deserve is one Zoiris clean away. Schedule now.",
]

BTN_TEXTS = [
    "Book My Free Estimate",
    "Get My {city} Quote Now",
    "Schedule My First Clean",
    "Claim a Special Offer",
]

COLOR_PALETTES = [
    {"bg": "bg-gradient-to-br from-blue-50 via-white to-indigo-50", "border": "border-blue-100", "badge": "bg-blue-600 text-white", "accent_bar": "bg-blue-600", "icon_ring": "ring-blue-100 text-blue-600 bg-blue-50", "check": "text-blue-600", "btn": "from-blue-600 to-indigo-700", "btn_solid": "bg-blue-600 hover:bg-blue-700"},
    {"bg": "bg-gradient-to-br from-teal-50 via-white to-emerald-50", "border": "border-teal-100", "badge": "bg-teal-600 text-white", "accent_bar": "bg-teal-500", "icon_ring": "ring-teal-100 text-teal-600 bg-teal-50", "check": "text-teal-600", "btn": "from-teal-500 to-emerald-600", "btn_solid": "bg-teal-600 hover:bg-teal-700"},
    {"bg": "bg-gradient-to-br from-indigo-50 via-white to-purple-50", "border": "border-indigo-100", "badge": "bg-indigo-700 text-white", "accent_bar": "bg-indigo-600", "icon_ring": "ring-indigo-100 text-indigo-600 bg-indigo-50", "check": "text-indigo-600", "btn": "from-indigo-600 to-purple-700", "btn_solid": "bg-indigo-700 hover:bg-indigo-800"},
    {"bg": "bg-white", "border": "border-gray-200", "badge": "bg-gray-900 text-white", "accent_bar": "bg-gray-900", "icon_ring": "ring-gray-100 text-gray-800 bg-gray-50", "check": "text-gray-700", "btn": "from-gray-800 to-black", "btn_solid": "bg-gray-900 hover:bg-black"},
    {"bg": "bg-gradient-to-br from-rose-50 via-white to-orange-50", "border": "border-rose-100", "badge": "bg-rose-600 text-white", "accent_bar": "bg-rose-500", "icon_ring": "ring-rose-100 text-rose-600 bg-rose-50", "check": "text-rose-500", "btn": "from-rose-500 to-orange-500", "btn_solid": "bg-rose-600 hover:bg-rose-700"},
]

# ─────────────────────── TEMPLATE BUILDERS ────────────────────

def _pick(lst, **kw):
    """Pick random item and format with kwargs."""
    return random.choice(lst).format(**kw)

def build_grid_block(city, competitor, c):
    headline = _pick(HEADLINE_TEMPLATES, city=city, competitor=competitor)
    intro    = _pick(INTROS, city=city, competitor=competitor)
    cta      = _pick(CTAS, city=city, competitor=competitor)
    btn      = _pick(BTN_TEXTS, city=city, competitor=competitor)
    
    feats_html = ""
    sampled = random.sample(FEATURES, 4)
    for f in sampled:
        t = _pick(f["titles"], city=city, competitor=competitor)
        d = _pick(f["descs"], city=city, competitor=competitor)
        feats_html += f"""
            <div class="flex items-start gap-5">
              <div class="flex-shrink-0 w-14 h-14 rounded-2xl {c['icon_ring']} ring-2 flex items-center justify-center shadow-sm">
                <i class="fas {f['icon']} text-xl"></i>
              </div>
              <div>
                <h3 class="text-lg font-bold text-gray-900 mb-1">{t}</h3>
                <p class="text-gray-600 leading-relaxed text-sm">{d}</p>
              </div>
            </div>"""

    return f"""    </section>

    <!-- {SKIP_MARKER} | {city} vs {competitor} -->
    <section class="{c['bg']} py-20" id="zoiris-vs-{competitor.lower().replace(' ','').replace('&','')[:30]}">
      <div class="max-w-6xl mx-auto px-4">
        <div class="bg-white rounded-3xl shadow-xl border {c['border']} overflow-hidden">
          <div class="p-10 md:p-14">
            <div class="text-center mb-12">
              <span class="inline-block {c['badge']} text-xs font-extrabold uppercase tracking-widest py-1.5 px-4 rounded-full mb-5">#1 Rated in {city}, AL</span>
              <h2 class="text-4xl md:text-5xl font-black text-gray-900 leading-tight mb-5">
                {headline}
              </h2>
              <div class="h-1.5 w-24 {c['accent_bar']} rounded-full mx-auto mb-7"></div>
              <p class="text-gray-600 text-lg leading-relaxed max-w-3xl mx-auto">{intro}</p>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">{feats_html}
            </div>
            <div class="text-center">
              <p class="text-gray-700 font-medium mb-6">{cta}</p>
              <a href="#quote" class="inline-flex items-center gap-2 bg-gradient-to-r {c['btn']} text-white font-bold py-4 px-10 rounded-full shadow-lg hover:shadow-2xl transition-all transform hover:-translate-y-1">
                <i class="fas fa-calendar-check"></i>
                <span>{btn}</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="py-16 bg-lightGray" id="services">"""


def build_split_block(city, competitor, c):
    headline = _pick(HEADLINE_TEMPLATES, city=city, competitor=competitor)
    intro    = _pick(INTROS, city=city, competitor=competitor)
    cta      = _pick(CTAS, city=city, competitor=competitor)
    btn      = _pick(BTN_TEXTS, city=city, competitor=competitor)

    checklist_html = ""
    for f in random.sample(FEATURES, 4):
        t = _pick(f["titles"], city=city, competitor=competitor)
        d = _pick(f["descs"], city=city, competitor=competitor)
        checklist_html += f"""
                <li class="flex items-start gap-4">
                  <i class="fas fa-check-circle {c['check']} text-2xl mt-0.5 flex-shrink-0"></i>
                  <div>
                    <span class="font-bold text-gray-900">{t}</span>
                    <p class="text-sm text-gray-500 mt-0.5">{d}</p>
                  </div>
                </li>"""

    return f"""    </section>

    <!-- {SKIP_MARKER} | {city} vs {competitor} -->
    <section class="py-20 bg-white" id="zoiris-vs-{competitor.lower().replace(' ','').replace('&','')[:30]}">
      <div class="max-w-7xl mx-auto px-4 lg:flex items-center gap-16">
        <div class="lg:w-1/2 mb-12 lg:mb-0">
          <span class="inline-block {c['badge']} text-xs font-extrabold uppercase tracking-widest py-1.5 px-4 rounded-full mb-5">{city}'s Local Favorite</span>
          <h2 class="text-4xl md:text-5xl font-black text-gray-900 leading-tight mb-5">{headline}</h2>
          <div class="h-1.5 w-16 {c['accent_bar']} rounded mb-6"></div>
          <p class="text-gray-600 text-lg leading-relaxed mb-8">{intro}</p>
          <a href="#quote" class="inline-flex items-center gap-2 {c['btn_solid']} text-white font-bold py-4 px-8 rounded-xl shadow-lg transition transform hover:-translate-y-1">
            <span>{btn}</span>
            <i class="fas fa-arrow-right text-sm"></i>
          </a>
        </div>
        <div class="lg:w-1/2">
          <div class="bg-gray-50 border {c['border']} rounded-3xl p-8 shadow-inner">
            <h3 class="text-xl font-bold text-gray-900 mb-6 pb-4 border-b {c['border']}">
              Zoiris vs. {competitor} — The {city} Difference
            </h3>
            <ul class="space-y-6">{checklist_html}
            </ul>
            <div class="mt-8 pt-6 border-t {c['border']} text-center">
              <p class="text-sm text-gray-600 italic">{cta}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="py-16 bg-lightGray" id="services">"""


def build_card_block(city, competitor, c):
    headline = _pick(HEADLINE_TEMPLATES, city=city, competitor=competitor)
    intro    = _pick(INTROS, city=city, competitor=competitor)
    cta      = _pick(CTAS, city=city, competitor=competitor)
    btn      = _pick(BTN_TEXTS, city=city, competitor=competitor)

    cards_html = ""
    for f in random.sample(FEATURES, 3):
        t = _pick(f["titles"], city=city, competitor=competitor)
        d = _pick(f["descs"], city=city, competitor=competitor)
        cards_html += f"""
          <div class="bg-white rounded-2xl p-7 border {c['border']} shadow-md hover:shadow-xl transition-all transform hover:-translate-y-1 text-center">
            <div class="w-16 h-16 rounded-full {c['icon_ring']} ring-2 flex items-center justify-center mx-auto mb-5">
              <i class="fas {f['icon']} text-2xl"></i>
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-3">{t}</h3>
            <p class="text-gray-500 text-sm leading-relaxed">{d}</p>
          </div>"""

    return f"""    </section>

    <!-- {SKIP_MARKER} | {city} vs {competitor} -->
    <section class="{c['bg']} py-20" id="zoiris-vs-{competitor.lower().replace(' ','').replace('&','')[:30]}">
      <div class="max-w-6xl mx-auto px-4">
        <div class="text-center mb-14">
          <span class="inline-block {c['badge']} text-xs font-extrabold uppercase tracking-widest py-1.5 px-4 rounded-full mb-5">Serving {city}, AL</span>
          <h2 class="text-4xl md:text-5xl font-black text-gray-900 leading-tight mb-5">{headline}</h2>
          <div class="h-1.5 w-24 {c['accent_bar']} rounded-full mx-auto mb-7"></div>
          <p class="text-gray-600 text-lg max-w-3xl mx-auto leading-relaxed">{intro}</p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-14">{cards_html}
        </div>
        <div class="bg-gray-900 text-white rounded-3xl p-10 flex flex-col md:flex-row items-center justify-between gap-8 shadow-2xl">
          <div>
            <h3 class="text-2xl font-bold mb-2">{cta}</h3>
            <p class="text-gray-400">Stop settling for less than the best in {city}. Zoiris delivers perfection.</p>
          </div>
          <a href="#quote" class="flex-shrink-0 inline-flex items-center gap-2 bg-gradient-to-r {c['btn']} font-bold py-4 px-8 rounded-full text-white shadow-lg hover:shadow-2xl transition transform hover:scale-105">
            <span>{btn}</span>
            <i class="fas fa-chevron-right"></i>
          </a>
        </div>
      </div>
    </section>

    <section class="py-16 bg-lightGray" id="services">"""


TEMPLATE_FNS = [build_grid_block, build_split_block, build_card_block]

# ─────────────────────── CITY SEED ────────────────────────

def get_city_seed(folder_name):
    """Hash folder name to get a deterministic but unique seed."""
    return int(hashlib.md5(folder_name.encode()).hexdigest(), 16) % (2**32)

# ─────────────────────── PROCESSING ────────────────────────

counter_lock = threading.Lock()
processed_files = [0]
processed_cities = [0]

def process_city(city_folder_path, folder_name):
    city = folder_name.replace("-al", "").replace("-", " ").title()

    # Seed random for this city so all its pages get the same layout/competitor
    rng = random.Random(get_city_seed(folder_name))

    # Pick competitor, layout, and color for this city
    competitor_pool = COMPETITOR_MAP.get(folder_name, COMPETITOR_MAP["DEFAULT"])
    competitor  = rng.choice(competitor_pool)
    layout_fn   = rng.choice(TEMPLATE_FNS)
    palette     = rng.choice(COLOR_PALETTES)

    # Build the block ONCE for the city
    seo_block = layout_fn(city, competitor, palette)

    html_files = glob.glob(os.path.join(city_folder_path, "**", "*.html"), recursive=True)
    injected = 0

    for fp in html_files:
        try:
            with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception:
            continue

        if SKIP_MARKER in content:
            continue

        original = content
        for pat in TARGET_PATTERNS:
            if pat in content:
                content = content.replace(pat, seo_block, 1)
                break

        if content != original:
            try:
                with open(fp, 'w', encoding='utf-8') as f:
                    f.write(content)
                injected += 1
            except Exception:
                pass

    with counter_lock:
        processed_files[0] += injected
        processed_cities[0] += 1
        c = processed_cities[0]
        if c % 25 == 0:
            print(f"  [OK] {c} cities done -- {processed_files[0]} pages injected so far")

    return folder_name, injected


def main():
    print("=" * 60)
    print("  ZOIRIS STATEWIDE SPINTAX SEO ENGINE v2 - Multithreaded")
    print("=" * 60)

    city_dirs = []
    for item in os.listdir(BASE_DIR):
        full = os.path.join(BASE_DIR, item)
        if os.path.isdir(full) and item.endswith("-al") and item not in SKIP_DIRS:
            city_dirs.append((full, item))

    print(f"Found {len(city_dirs)} city directories to process.\n")

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(process_city, full, name): name for full, name in city_dirs}
        for future in as_completed(futures):
            city_name, count = future.result()

    print("\n" + "=" * 60)
    print("  [DONE] SPINTAX INJECTION COMPLETE")
    print(f"  Cities Processed : {processed_cities[0]}")
    print(f"  Pages Injected   : {processed_files[0]}")
    print("=" * 60)


if __name__ == "__main__":
    main()

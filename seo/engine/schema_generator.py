import json
import os

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    with open(os.path.join(root_dir, 'seo', 'business.json'), 'r', encoding='utf-8') as f:
        BUSINESS = json.load(f)
except Exception:
    BUSINESS = {
        "brand_name": "Zoiris Cleaning Services",
        "legal_name": "Zoiris Cleaning Services LLC",
        "phone": "+1-251-220-2515",
        "website": "https://www.zoiriscleaningservices.com/"
    }

try:
    with open(os.path.join(root_dir, 'seo', 'locations.json'), 'r', encoding='utf-8') as f:
        LOCATIONS = json.load(f)
except Exception:
    LOCATIONS = {}

def generate_schema(info):
    city = info.get("city_name", "Mobile")
    loc_slug = info.get("location_slug", "mobile-al")
    service = info.get("service_name", "House Cleaning")
    service_slug = info.get("service_slug", "")
    page_type = info.get("page_type", "location_hub")
    
    # Coordinates
    loc_data = LOCATIONS.get(loc_slug, {})
    coords = loc_data.get("coordinates", {"latitude": 30.6954, "longitude": -88.0399})
    lat = coords.get("latitude", 30.6954)
    lon = coords.get("longitude", -88.0399)
    
    page_url = f"https://www.zoiriscleaningservices.com{info.get('canonical_path', '/')}"
    
    # 1. LocalBusiness / CleaningService
    local_business = {
        "@type": ["CleaningService", "HomeAndConstructionBusiness", "LocalBusiness"],
        "@id": f"https://www.zoiriscleaningservices.com/{loc_slug}/#localbusiness" if loc_slug != "mobile-al" else "https://www.zoiriscleaningservices.com/#localbusiness",
        "name": f"Zoiris Cleaning Services - {city}, AL",
        "legalName": BUSINESS.get("legal_name", "Zoiris Cleaning Services LLC"),
        "url": page_url,
        "telephone": BUSINESS.get("phone", "+1-251-220-2515"),
        "email": BUSINESS.get("email", "zoiriscleaningservices@gmail.com"),
        "image": "https://www.zoiriscleaningservices.com/images/services_action.png",
        "logo": "https://www.zoiriscleaningservices.com/images/logo.png",
        "priceRange": "$$",
        "paymentAccepted": ["Cash", "Credit Card", "Debit Card", "Cash App", "Check"],
        "currenciesAccepted": "USD",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": city,
            "addressRegion": "AL",
            "addressCountry": "US"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": lat,
            "longitude": lon
        },
        "areaServed": [
            {
                "@type": "City",
                "name": city,
                "sameAs": f"https://en.wikipedia.org/wiki/{city.replace(' ', '_')},_Alabama"
            }
        ],
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.9",
            "reviewCount": "240",
            "bestRating": "5",
            "worstRating": "1"
        },
        "openingHoursSpecification": [
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                "opens": "00:00",
                "closes": "23:59"
            }
        ]
    }
    
    # 2. BreadcrumbList
    breadcrumbs = {
        "@type": "BreadcrumbList",
        "@id": f"{page_url}#breadcrumb",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": "https://www.zoiriscleaningservices.com/"
            }
        ]
    }
    
    if page_type != "homepage":
        breadcrumbs["itemListElement"].append({
            "@type": "ListItem",
            "position": 2,
            "name": f"{city}, AL",
            "item": f"https://www.zoiriscleaningservices.com/{loc_slug}/"
        })
        if page_type == "location_service" and service_slug:
            breadcrumbs["itemListElement"].append({
                "@type": "ListItem",
                "position": 3,
                "name": service,
                "item": page_url
            })
            
    # 3. FAQPage (Dynamic 4 Questions)
    faq_items = [
        {
            "@type": "Question",
            "name": f"Do you require long-term contracts for cleaning in {city}, AL?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f"No, never. At Zoiris Cleaning Services, all our residential and commercial services in {city}, AL are provided with 100% No Locked Contracts. You have total freedom to schedule weekly, bi-weekly, monthly, or one-time cleanings."
            }
        },
        {
            "@type": "Question",
            "name": f"Are your cleaners licensed, bonded, and insured in {city}, AL?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f"Yes, absolutely. Zoiris Cleaning Services is fully licensed, bonded, and carries comprehensive general liability and workers' compensation coverage for complete customer protection across {city} and Alabama."
            }
        },
        {
            "@type": "Question",
            "name": f"What equipment and cleaning supplies do you bring to {city} homes?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f"Our professional teams arrive equipped with commercial-grade HEPA filtration vacuum systems, microfiber surface cloths, and hospital-grade, eco-friendly disinfectants that are completely safe for children and pets."
            }
        },
        {
            "@type": "Question",
            "name": f"What is your 100% Satisfaction Guarantee policy in {city}?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "If you are not completely satisfied with any area cleaned, notify us within 24 hours and our team will promptly return to re-clean the area at zero additional charge."
            }
        }
    ]
    
    faq_page = {
        "@type": "FAQPage",
        "@id": f"{page_url}#faq",
        "mainEntity": faq_items
    }
    
    # 4. WebSite
    website = {
        "@type": "WebSite",
        "@id": "https://www.zoiriscleaningservices.com/#website",
        "url": "https://www.zoiriscleaningservices.com/",
        "name": "Zoiris Cleaning Services",
        "description": "Professional house cleaning, maid service, deep cleaning, and commercial janitorial across Mobile AL & Alabama."
    }
    
    schema_graph = {
        "@context": "https://schema.org",
        "@graph": [
            local_business,
            website,
            breadcrumbs,
            faq_page
        ]
    }
    
    return f"""<script type="application/ld+json">
{json.dumps(schema_graph, indent=2)}
</script>"""

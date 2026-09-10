import json
import os
import sys

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from localized_faq_generator import generate_location_faqs

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
    county = loc_data.get("county", "Alabama")
    
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
            
    # 3. FAQPage (8 Dynamic & Unique Questions per Location)
    faqs_data = generate_location_faqs(city, loc_slug, county)
    faq_items = []
    for item in faqs_data:
        faq_items.append({
            "@type": "Question",
            "name": item["q"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": item["a"]
            }
        })
        
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

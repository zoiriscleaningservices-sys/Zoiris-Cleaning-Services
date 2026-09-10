def generate_hero_content(info):
    page_type = info.get("page_type")
    city = info.get("city_name", "Mobile")
    service = info.get("service_name", "House Cleaning")
    service_lower = service.lower()
    tier = info.get("tier", "B")
    
    if page_type == "homepage":
        h1 = "House Cleaning & Maid Services in Mobile, AL"
        subtitle = "Affordable, <strong>No-Contract</strong> residential and commercial cleaning tailored to your lifestyle. Weekly, bi-weekly, monthly, deep cleaning, and move-in/out services across Mobile & Baldwin County."
        return h1, subtitle
        
    if page_type == "location_hub":
        if tier == "A":
            h1 = f"House Cleaning & Maid Services in {city}, AL"
            subtitle = f"Affordable, <strong>No-Contract</strong> house cleaning and maid services in {city}, AL. Fully licensed, bonded, insured, and background-checked cleaners with a 100% satisfaction guarantee."
        else:
            h1 = f"House Cleaning Services in {city}, AL"
            subtitle = f"Trusted residential and commercial cleaning services in {city}, AL. No locked contracts, commercial HEPA vacuuming, and free instant estimates."
        return h1, subtitle
        
    if page_type == "location_service":
        h1 = f"{service} in {city}, AL"
        if "deep" in service_lower:
            subtitle = f"Intensive, top-to-bottom detail deep cleaning in {city}, AL. Hand-scrubbed baseboards, sanitized kitchens & bathrooms, and zero locked contracts."
        elif "move" in service_lower:
            subtitle = f"Immaculate {service_lower} in {city}, AL for homeowners, renters, and property managers. 100% inspection and deposit-ready sanitization."
        elif "commercial" in service_lower or "janitorial" in service_lower or "office" in service_lower:
            subtitle = f"Professional commercial cleaning and janitorial services in {city}, AL. Custom recurring schedules, bonded crews, and high-standard facility care."
        elif "airbnb" in service_lower or "vacation" in service_lower:
            subtitle = f"5-Star turnover cleaning for vacation rentals and Airbnb properties in {city}, AL. Fast checkout-to-checkin turnarounds and guest staging."
        elif "post-construction" in service_lower:
            subtitle = f"Comprehensive post-construction cleaning in {city}, AL. Multi-phase drywall dust removal, window cleaning, and detail finishing for builders."
        elif "carpet" in service_lower:
            subtitle = f"Commercial hot-water extraction carpet cleaning in {city}, AL. Deep stain removal, pet odor elimination, and fast drying times."
        elif "pressure" in service_lower:
            subtitle = f"High-grade pressure washing and soft-washing in {city}, AL. Clean driveways, siding, patios, and commercial walkways."
        else:
            subtitle = f"Professional, reliable {service_lower} in {city}, AL by Zoiris Cleaning Services. Licensed, insured, and 100% satisfaction guaranteed."
        return h1, subtitle
        
    if page_type == "location_about":
        h1 = f"About Zoiris Cleaning Services in {city}, AL"
        subtitle = f"Dedicated to spotless results and reliable housekeeping across {city}, AL with zero locked contracts and 100% background-checked cleaners."
        return h1, subtitle
        
    if page_type == "location_contact":
        h1 = f"Contact Zoiris Cleaning Services in {city}, AL"
        subtitle = f"Get in touch with our {city} cleaning team today for a fast, free estimate on residential or commercial cleaning."
        return h1, subtitle
        
    h1 = f"{service} in {city}, AL"
    subtitle = f"Professional cleaning services in {city}, AL by Zoiris Cleaning Services. No contracts, fully insured, 100% satisfaction guaranteed."
    return h1, subtitle

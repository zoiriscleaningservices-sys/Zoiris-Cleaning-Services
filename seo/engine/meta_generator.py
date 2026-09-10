def generate_meta_description(info):
    page_type = info.get("page_type")
    city = info.get("city_name", "Mobile")
    service = info.get("service_name", "House Cleaning")
    service_lower = service.lower()
    
    if page_type == "homepage":
        return "Looking for trusted house cleaning and maid services in Mobile, AL? Zoiris Cleaning Services offers affordable no-contract recurring cleaning, deep cleaning, move-in/out, and commercial janitorial. Licensed, bonded & insured. Call 251-220-2515 for a free estimate!"
        
    if page_type == "location_hub":
        return f"Professional house cleaning & maid services in {city}, AL. Zoiris Cleaning Services provides reliable no-contract recurring cleans, deep cleaning, and move turnovers. Licensed, bonded & insured. Call (251) 220-2515!"
        
    if page_type == "location_service":
        if "deep" in service_lower:
            return f"Top-rated deep cleaning services in {city}, AL. Detailed top-to-bottom scrub of baseboards, kitchens, baths & appliances. No contracts, 100% guaranteed. Call (251) 220-2515 for a free quote!"
        elif "move" in service_lower:
            return f"Expert {service_lower} in {city}, AL. Move-in & move-out turnover cleaning for tenants, homeowners & landlords. Full deposit-ready sanitization. Call (251) 220-2515 for an instant estimate!"
        elif "commercial" in service_lower or "janitorial" in service_lower or "office" in service_lower:
            return f"Trusted commercial cleaning & janitorial services in {city}, AL. Customized office maintenance, sanitization & after-hours facility care. Fully bonded & insured. Call (251) 220-2515!"
        elif "airbnb" in service_lower or "vacation" in service_lower:
            return f"5-Star {service_lower} in {city}, AL. Fast turnarounds, fresh linen service & guest staging for short-term rental hosts. Zero contracts. Call (251) 220-2515!"
        elif "post-construction" in service_lower:
            return f"Professional post-construction cleanup in {city}, AL. Drywall dust extraction, sticker removal & detail polishing for contractors & builders. Call (251) 220-2515!"
        elif "carpet" in service_lower:
            return f"Commercial & residential carpet cleaning in {city}, AL. Hot water steam extraction for deep stain & pet odor removal. Fast drying times. Call (251) 220-2515!"
        elif "pressure" in service_lower:
            return f"Top-rated pressure washing & soft-wash services in {city}, AL. Driveways, siding, patios & commercial exterior washing. Free estimates at (251) 220-2515!"
        else:
            return f"Affordable, professional {service_lower} in {city}, AL by Zoiris Cleaning Services. Licensed, bonded & insured crews with zero locked contracts. Call (251) 220-2515 for a free estimate!"
            
    if page_type == "location_about":
        return f"Learn why homeowners and businesses in {city}, AL trust Zoiris Cleaning Services. Vetted in-house cleaners, commercial HEPA equipment & 100% satisfaction guarantee. Call (251) 220-2515!"
        
    if page_type == "location_contact":
        return f"Contact Zoiris Cleaning Services in {city}, AL. Call (251) 220-2515 or request an online estimate for residential, commercial, or deep cleaning services."
        
    return f"Professional {service_lower} in {city}, AL by Zoiris Cleaning Services. 100% satisfaction guaranteed with zero locked-in contracts. Call (251) 220-2515!"

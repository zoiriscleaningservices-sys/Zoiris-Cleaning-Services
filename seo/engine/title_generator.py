def generate_title(info):
    page_type = info.get("page_type")
    city = info.get("city_name", "Mobile")
    service = info.get("service_name", "House Cleaning")
    tier = info.get("tier", "B")
    
    if page_type == "homepage":
        return "House Cleaning & Maid Services in Mobile, AL | Top-Rated Cleaners - Zoiris"
        
    if page_type == "location_hub":
        if tier == "A":
            return f"House Cleaning & Maid Services in {city}, AL | Zoiris Cleaning"
        else:
            return f"House Cleaning Services in {city}, AL | Zoiris Cleaning Services"
            
    if page_type == "location_service":
        if service.lower() in ["house cleaning", "maid service"]:
            return f"Maid & House Cleaning Services in {city}, AL | Zoiris"
        elif service.lower() == "deep cleaning":
            return f"Deep Cleaning Services in {city}, AL | Zoiris Cleaners"
        elif service.lower() in ["move in cleaning", "move out cleaning"]:
            return f"{service} in {city}, AL | Move Cleaners - Zoiris"
        elif service.lower() in ["commercial cleaning", "office janitorial services", "janitorial cleaning services"]:
            return f"{service} in {city}, AL | Commercial Cleaners - Zoiris"
        elif service.lower() in ["vacation rental cleaning", "airbnb cleaning"]:
            return f"{service} in {city}, AL | Turnover Cleaners - Zoiris"
        else:
            return f"{service} in {city}, AL | Zoiris Cleaning Services"
            
    if page_type == "location_about":
        return f"About Zoiris Cleaning Services in {city}, AL | Trusted Local Cleaners"
    if page_type == "location_contact":
        return f"Contact Zoiris Cleaning Services in {city}, AL | Get a Free Estimate"
    if page_type == "location_blog":
        return f"Cleaning Tips & Expert Advice in {city}, AL | Zoiris Blog"
    if page_type == "locations_index":
        return "Alabama Service Areas & Coverage Map | Zoiris Cleaning Services"
        
    return f"{service} Services in {city}, AL | Zoiris Cleaning Services"

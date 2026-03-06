import os
import re
import random

services_data = [
    ("house-cleaning", "House Cleaning", "fa-house-chimney", "Flexible residential cleaning for apartments, condos, and houses."),
    ("deep-cleaning", "Deep Cleaning", "fa-broom", "A top-to-bottom detailed clean to eliminate hidden grime."),
    ("move-in-cleaning", "Move-In Cleaning", "fa-key", "Fresh, sanitized, and move-in ready from day one."),
    ("move-out-cleaning", "Move-Out Cleaning", "fa-truck", "Leave your old space spotless and ready for inspection."),
    ("carpet-cleaning", "Carpet Cleaning", "fa-rug", "Deep carpet cleaning that removes dirt, stains, and allergens."),
    ("window-cleaning", "Window Cleaning", "fa-border-all", "Streak-free, crystal-clear window cleaning for any property."),
    ("pressure-washing", "Pressure Washing", "fa-water", "Restore driveways, decks, and exteriors with powerful washing."),
    ("luxury-estate-cleaning", "Luxury Estate Cleaning", "fa-gem", "Premium, meticulous cleaning for high-end homes and estates."),
    ("laundry-services", "Laundry Services", "fa-shirt", "Professional laundry and folding services to save you time."),
    ("Detailing-Mobile-AL", "Detailing", "fa-sparkles", "Detailed, immaculate cleaning focusing on the little things."),
    ("commercial-cleaning", "Commercial Cleaning", "fa-building", "Professional cleaning for offices and businesses of all sizes."),
    ("office-janitorial-services", "Office Janitorial Services", "fa-briefcase", "Reliable janitorial cleaning to keep your office professional."),
    ("janitorial-cleaning-services", "Janitorial Cleaning Services", "fa-clipboard-check", "Comprehensive janitorial services tailored to your facility."),
    ("medical-dental-facility-cleaning", "Medical Facility Cleaning", "fa-hospital", "Sanitation and sterilization services for medical environments."),
    ("industrial-warehouse-cleaning", "Industrial & Warehouse Cleaning", "fa-warehouse", "Heavy-duty cleaning designed for warehouses and factories."),
    ("floor-stripping-waxing", "Floor Stripping & Waxing", "fa-tablets", "Revitalize your hard floors with professional stripping and waxing."),
    ("gym-fitness-center-cleaning", "Gym & Fitness Center Cleaning", "fa-dumbbell", "Hygienic, deep cleaning for fitness centers and athletic clubs."),
    ("school-daycare-cleaning", "School & Daycare Cleaning", "fa-school", "Safe, thorough cleaning for educational facilities and daycares."),
    ("church-worship-center-cleaning", "Church & Worship Cleaning", "fa-church", "Respectful, detailed cleaning for places of worship."),
    ("solar-panel-cleaning", "Solar Panel Cleaning", "fa-solar-panel", "Maximize energy efficiency with safe solar panel cleaning."),
    ("vacation-rental-cleaning", "Vacation Rental Cleaning", "fa-umbrella-beach", "Keep your rental property spotless and guest-ready every time."),
    ("airbnb-cleaning", "Airbnb Cleaning", "fa-airbnb", "Quick turnaround cleaning for Airbnb hosts to keep 5-star ratings."),
    ("airbnb-vacation-rental-management", "Airbnb & Rental Management", "fa-house-user", "Complete cleaning and management solutions for your rentals."),
    ("post-construction-cleanup", "Post-Construction Cleanup", "fa-hammer", "Remove dust, debris, and construction mess for a polished look."),
    ("property-management-janitorial", "Property Management Janitorial", "fa-building-user", "Reliable cleaning services for property management companies."),
    ("property-maintenance", "Property Maintenance", "fa-tools", "Keep your property in pristine shape entirely year-round."),
    ("home-watch-services", "Home Watch Services", "fa-eye", "Trustworthy property checks while you are away from home."),
    ("luxury-estate-management", "Luxury Estate Management", "fa-crown", "Comprehensive upkeep and cleaning management for luxury estates."),
    ("gutter-cleaning", "Gutter Cleaning", "fa-cloud-rain", "Professional gutter cleaning to protect your property's exterior.")
]

random.shuffle(services_data)

slides_html = "\n"
for slug, name, icon, desc in services_data:
    # map to image file name based on what's in images/services/
    img_name_map = {
        "House Cleaning": "house_cleaning.jpg",
        "Deep Cleaning": "deep_cleaning.jpg",
        "Move-In Cleaning": "move_in_cleaning.jpg",
        "Move-Out Cleaning": "move_out_cleaning.jpg",
        "Carpet Cleaning": "carpet_cleaning.jpg",
        "Window Cleaning": "window_cleaning.jpg",
        "Pressure Washing": "pressure_washing.jpg",
        "Luxury Estate Cleaning": "luxury_estate_cleaning.jpg",
        "Laundry Services": "laundry_services.jpg",
        "Detailing": "detailing.jpg",
        "Commercial Cleaning": "commercial_cleaning.jpg",
        "Office Janitorial Services": "office_janitorial_services.jpg",
        "Janitorial Cleaning Services": "janitorial_cleaning_services.jpg",
        "Medical Facility Cleaning": "medical_facility_cleaning.jpg",
        "Industrial & Warehouse Cleaning": "industrial_warehouse_cleaning.jpg",
        "Floor Stripping & Waxing": "floor_stripping_waxing.jpg",
        "Gym & Fitness Center Cleaning": "gym_fitness_center_cleaning.jpg",
        "School & Daycare Cleaning": "school_daycare_cleaning.jpg",
        "Church & Worship Cleaning": "church_worship_cleaning.jpg",
        "Solar Panel Cleaning": "solar_panel_cleaning.jpg",
        "Vacation Rental Cleaning": "vacation_rental_cleaning.jpg",
        "Airbnb Cleaning": "airbnb_cleaning.jpg",
        "Airbnb & Rental Management": "airbnb_rental_management.jpg",
        "Post-Construction Cleanup": "post_construction_cleanup.jpg",
        "Property Management Janitorial": "property_management_janitorial.jpg",
        "Property Maintenance": "property_maintenance.jpg",
        "Home Watch Services": "home_watch_services.jpg",
        "Luxury Estate Management": "luxury_estate_management.jpg",
        "Gutter Cleaning": "gutter_cleaning.jpg"
    }

    photo_filename = img_name_map[name]
    photo_path = f"/images/services/{photo_filename}"

    slide = f"""        <!-- {name} -->
        <div class="swiper-slide">
          <div class="contact-button text-lg">
            <img alt="{name}" class="h-48 w-full object-cover" src="{photo_path}" />
            <div class="p-6">
              <div class="flex items-center justify-center mb-4">
                <i class="fa-solid {icon} text-xl"></i>
              </div>
              <h3 class="font-bold text-xl mb-2 text-center">{name}</h3>
              <p class="text-sm text-center mb-4">{desc}</p>
              <div class="text-center">
                <a class="contact-button text-lg" href="/mobile-al/{slug}/">Learn More About {name} <i class="fa-solid fa-arrow-right"></i></a>
              </div>
            </div>
          </div>
        </div>\n"""
    slides_html += slide

try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    new_html = re.sub(
        r'(<div class="swiper-wrapper">).*?(</div>\s*<!-- Navigation Arrows -->)',
        r'\g<1>' + slides_html + r'      \g<2>',
        html_content,
        flags=re.DOTALL
    )

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_html)

    print("Success: Updated index.html with 29 randomized service cards!")
except Exception as e:
    print(f"Error: {e}")

import os
import sys
import time
import json
import cloudscraper
import urllib.parse
from bs4 import BeautifulSoup

try:
    from PIL import Image
except ImportError:
    os.system(f"{sys.executable} -m pip install Pillow")
    from PIL import Image

def download_image(url, save_path, scraper):
    if not os.path.exists(save_path):
        try:
            response = scraper.get(url, stream=True)
            if response.status_code == 200:
                with open(save_path, 'wb') as out_file:
                    for chunk in response.iter_content(chunk_size=8192):
                        out_file.write(chunk)
                
                # Verify it's not a tiny error page
                if os.path.getsize(save_path) < 5000:
                    os.remove(save_path)
                    print(f"Failed to download {url}: file too small")
                    return False
                
                print(f"Downloaded {save_path}")
                return True
            else:
                print(f"Failed to download {url}: Status {response.status_code}")
                return False
        except Exception as e:
            print(f"Download exception: {e}")
            return False
    return True

def add_watermark(input_path, output_path, watermark_path):
    try:
        base_image = Image.open(input_path).convert("RGBA")
        watermark = Image.open(watermark_path).convert("RGBA")
        
        # Calculate watermark size (15% of the image width)
        wm_width = int(base_image.width * 0.15)
        wm_ratio = wm_width / watermark.width
        wm_height = int(watermark.height * wm_ratio)
        watermark = watermark.resize((wm_width, wm_height), Image.Resampling.LANCZOS)
        
        alpha = watermark.split()[3]
        alpha = alpha.point(lambda p: p * 0.7)
        watermark.putalpha(alpha)

        # Position watermark at bottom-right
        position = (base_image.width - wm_width - 20, base_image.height - wm_height - 20)

        transparent = Image.new('RGBA', base_image.size, (0,0,0,0))
        transparent.paste(base_image, (0,0))
        transparent.paste(watermark, position, mask=watermark)
        
        final = transparent.convert("RGB")
        final.save(output_path, "JPEG", quality=95)
        print(f"Watermark added to {output_path}")
        return True
    except Exception as e:
        print(f"Error watermarking {input_path}: {e}")
        return False

if __name__ == "__main__":
    logo_path = r"C:\Users\lucia\.gemini\antigravity\brain\034a902f-78cb-433e-a3a1-b0d0ee9cc460\media__1772799578712.png"
    output_dir = "images/services"
    os.makedirs(output_dir, exist_ok=True)
    
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True})
    
    categories = {
        # Residential & Property
        "House Cleaning": "house cleaning maid",
        "Deep Cleaning": "deep clean bathroom kitchen",
        "Move-In Cleaning": "empty bright house interior",
        "Move-Out Cleaning": "cleaning empty room",
        "Carpet Cleaning": "vacuuming carpet",
        "Window Cleaning": "washing windows squeegee",
        "Pressure Washing": "pressure washing driveway",
        "Luxury Estate Cleaning": "luxury mansion cleaning",
        "Laundry Services": "folding clean laundry",
        "Detailing": "car interior cleaning detailing",
        # Commercial & Industrial
        "Commercial Cleaning": "commercial cleaning floor",
        "Office Janitorial Services": "office janitor cleaning desk",
        "Janitorial Cleaning Services": "janitor mopping floor",
        "Medical Facility Cleaning": "hospital clinic cleaning sterile",
        "Industrial & Warehouse Cleaning": "warehouse cleaning sweeping",
        "Floor Stripping & Waxing": "polishing floor machine",
        "Gym & Fitness Center Cleaning": "gym cleaning disinfecting equipment",
        "School & Daycare Cleaning": "classroom cleaning school",
        "Church & Worship Cleaning": "empty church interior clean",
        "Solar Panel Cleaning": "solar panel washing",
        # Property Management
        "Vacation Rental Cleaning": "luxury vacation rental interior",
        "Airbnb Cleaning": "airbnb bedroom cleaning",
        "Airbnb & Rental Management": "luxury rental property management",
        "Post-Construction Cleanup": "post construction cleaning",
        "Property Management Janitorial": "apartment building cleaning",
        "Property Maintenance": "property maintenance repair",
        "Home Watch Services": "home security empty house",
        "Luxury Estate Management": "luxury estate exterior",
        "Gutter Cleaning": "gutter cleaning roof"
    }

    print(f"Starting gathering for {len(categories)} categories...")

    for category, query in categories.items():
        # Sanitize name for filename
        safe_name = category.lower().replace('& ', '').replace(' ', '_').replace('-', '_')
        final_path = os.path.join(output_dir, f"{safe_name}.jpg")
        
        if os.path.exists(final_path):
            print(f"Skipping {category}, already exists.")
            continue
            
        search_url = f"https://www.pexels.com/search/{urllib.parse.quote(query)}/?orientation=landscape"
        print(f"Searching for [{category}]: {query}")
        
        html = scraper.get(search_url).text
        soup = BeautifulSoup(html, 'html.parser')
        images = soup.find_all('img')
        
        # Find first valid high res image
        success = False
        for img in images:
            src = img.get('src') or img.get('data-src') or ""
            if "images.pexels.com/photos/" in src and "auto=compress" in src:
                high_res = src.split('?')[0] + "?auto=compress&cs=tinysrgb&w=1600&h=900&fit=crop"
                temp_path = f"{output_dir}/temp_{safe_name}.jpg"
                
                if download_image(high_res, temp_path, scraper):
                    success = add_watermark(temp_path, final_path, logo_path)
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                
                if success:
                    break # Move to next category
        
        if not success:
            print(f"Could not find or process image for {category}.")
        time.sleep(2) # Prevent rate limiting

    print("Finished generating all specific service images.")

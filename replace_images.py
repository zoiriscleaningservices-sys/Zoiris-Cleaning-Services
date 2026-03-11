import os
import re

def main():
    directory = '.'
    files_modified = 0
    files_scanned = 0

    # Dictionary of specific URLs to find and replace with their local equivalents
    url_mapping = {
        "https://i.ibb.co/gbzKPdnc/Chat-GPT-Image-Aug-31-2025-12-19-42-AM-Picsart-Background-Remover.png": "/images/logo.png",
        "https://i.ibb.co/F4gsMz1c/7e6c60fb-e7da-4ac4-9db4-251daab42a76.png": "/images/location_hero.png",
        "https://i.ibb.co/Z6C6FkKH/Chat-GPT-Image-Sep-1-2025-10-20-56-PM.png": "/images/services_action.png",
        "https://i.ibb.co/Xx556fXM/Office-Cleaning-Crew.jpg": "/images/services/commercial_cleaning.jpg",
        "https://i.ibb.co/mfTgZTC/Seasonal-Deep-Cleaning-Tips.png": "/images/services/deep_cleaning.jpg",
        "https://i.ibb.co/xVwj2hV/Home-Cleaning-Service-in-Action.png": "/images/services/house_cleaning.jpg",
        "https://i.ibb.co/pBhLCp0m/Cleaning-Movers-MH-1.jpg": "/images/services/move_in_cleaning.jpg",
        "https://i.ibb.co/fzSDxHXB/64119f3c30e4db48a06316e0-Move-out-cleaning-min.jpg": "/images/services/move_out_cleaning.jpg",
        "https://i.ibb.co/MDq72Z6T/Vacation-Rental-Cleaning-Contract-1-scaled-e1636734588512.jpg": "/images/services/vacation_rental_cleaning.jpg",
        "https://i.ibb.co/cXbxNC7y/airbnb-pixabay-e1584981299557-1.webp": "/images/services/airbnb_cleaning.jpg",
        "https://i.ibb.co/kgbB5kPD/Captura-de-Tela-2020-07-06-a-s-15-13-39-1-e1599762634567.png": "/images/services/post_construction_cleanup.jpg",
        "https://i.ibb.co/4nn05G5j/carpetcleaning-UT-768x406.jpg": "/images/services/carpet_cleaning.jpg",
        "https://i.ibb.co/5gDXrjxs/Hotsy-Pressure-Washer-PSI-vs-GPM.jpg": "/images/services/pressure_washing.jpg"
    }

    print("Scanning repository to replace broken image URLs...")

    # Set up compiled regex to match any of the keys quickly
    # Escape the URLs for regex use
    escaped_keys = [re.escape(k) for k in url_mapping.keys()]
    pattern = re.compile("|".join(escaped_keys))
    
    # We will use this function for the substitution
    def replacement_func(match):
        return url_mapping[match.group(0)]

    for root, dirs, files in os.walk(directory):
        # Skip git and gemini
        if '.git' in root or '.gemini' in root:
            continue
            
        for file in files:
            if file.endswith('.html'):
                files_scanned += 1
                filepath = os.path.join(root, file)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Only perform sub if we find at least 'ibb.co' as a quick heuristic
                    if 'ibb.co' in content:
                        new_content = pattern.sub(replacement_func, content)

                        if content != new_content:
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            files_modified += 1
                            if files_modified % 1000 == 0:
                                print(f"Modified {files_modified} files so far...")
                        
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")

    print(f"\nDone! Scanned {files_scanned} files. Replaced image URLs in {files_modified} files.")

if __name__ == "__main__":
    main()

import os

# Define the replacements based on the implementation plan
replacements = {
    # Old logo -> New Logo
    "https://i.ibb.co/gbzKPdnc/Chat-GPT-Image-Aug-31-2025-12-19-42-AM-Picsart-Background-Remover.png": "/images/logo.png",
    
    # Old Hero -> New Hero
    "https://i.ibb.co/F4gsMz1c/7e6c60fb-e7da-4ac4-9db4-251daab42a76.png": "/images/location_hero.png",
    
    # Old About Action -> New Services Action
    "https://i.ibb.co/b3jZbdv3/living-room-cleaning.png": "/images/services_action.png",
    
    # Old Favicons -> New Local Favicons
    "https://imgur.com/yjACVrG.png": "/favicon/apple-touch-icon.png",
    "https://www.zoiriscleaningservices.com/favicon/": "/favicon/"
}

# The files in the root directory that need patching
loose_files = ["404.html", "dashboard.html"]

for file in loose_files:
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            
        modified = False
        for old, new in replacements.items():
            if old in content:
                content = content.replace(old, new)
                modified = True
                
        if modified:
            with open(file, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Patched old image URLs in {file}")
        else:
            print(f"No old URLs found in {file}")
            
print("Root file patching complete.")

import re

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

matches = re.findall(r'https://[^"\'\s]+ibb\.co[^"\'\s]+', text)
print(matches)

# Automatically replace them too just in case
for match in matches:
    if "7e6c60fb-e7da-4ac4" in match: # hero
        text = text.replace(match, "/images/location_hero.png")
    else:
        text = text.replace(match, "/images/logo.png")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(text)

print("Replacement complete.")

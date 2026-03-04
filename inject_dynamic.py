import re

with open("components/PageTemplate.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the component signature
content = content.replace("export default function Home() {", "export default function PageTemplate({ city = 'Mobile', state = 'AL', service = 'Cleaning Service' }: { city?: string, state?: string, service?: string }) {")

# Replace "Mobile, AL" in text nodes
content = re.sub(r'Mobile, AL(?!")', r'{city}, {state}', content)

# Replace "Mobile, AL" in attribute strings (e.g. content="...Mobile, AL...")
# We will convert the attribute to a template literal.
def attr_replacer(match):
    attr = match.group(1)
    val = match.group(2)
    new_val = val.replace("Mobile, AL", "${city}, ${state}")
    new_val = new_val.replace("Mobile", "${city}")
    return f"{attr}={{`{new_val}`}}"

content = re.sub(r'([a-zA-Z0-9_]+)="([^"]*Mobile, AL[^"]*)"', attr_replacer, content)

# Replace remaining text "Mobile" with {city} in text nodes
content = re.sub(r'(?<!")\bMobile\b(?!")', r'{city}', content)
# Replace "#1 Cleaning Services" or "Cleaning Services" in text nodes with {service}
# Actually this might be tricky, let's keep it simple and just let them use the default template for now.

with open("components/PageTemplate.tsx", "w", encoding="utf-8") as f:
    f.write(content)

print("Template dynamic variables injected.")

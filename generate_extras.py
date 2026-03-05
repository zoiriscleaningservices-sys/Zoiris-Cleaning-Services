import os

# Base directory for the new folders
BASE_DIR = r"c:\Users\lucia\OneDrive\Desktop\New folder (2)"

# The template index file
TEMPLATE_FILE = os.path.join(BASE_DIR, "index.html")

# Extra pages list as tuples of (folder_name, page_name)
extra_pages = [
    ("mobile-al/about", "About Us"),
    ("mobile-al/blog", "Cleaning Blog"),
    ("mobile-al/contact", "Contact Us")
]

with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
    template_content = f.read()

for folder_path, page_name in extra_pages:
    # Prepare exact replacements
    content = template_content
    
    # 1. Title tag
    content = content.replace(
        "<title>#1 Cleaning Service in Mobile, AL | Zoiris Cleaning Services</title>",
        f"<title>{page_name} | Zoiris Cleaning Services in Mobile, AL</title>"
    )
    
    # 2. Meta description
    content = content.replace(
        'content="Cleaning Services in Mobile, AL. Zoiris Cleaning Services offer the best house cleaning and maid services in the Mobile area. Call (251) 930 8621 for a free quote today!" />',
        f'content="{page_name} for Zoiris Cleaning Services in Mobile, AL. We offer the best residential and commercial cleaning in the Mobile area. Call (251) 930 8621 for a free quote today!" />'
    )
    
    # 3. OG Title
    content = content.replace(
        '<meta property="og:title" content="House Cleaning Services in Mobile, AL. Free Estimate | Zoiris Cleaning Services" />',
        f'<meta property="og:title" content="{page_name} | Zoiris Cleaning Services" />'
    )
    
    # 4. Schema Description
    content = content.replace(
        '"description": "Zoiris Cleaning Service is the leading residential, commercial, and Airbnb cleaning company in Mobile, Alabama. Offering deep cleaning, move-in/out, post-construction cleaning, office cleaning, and eco-friendly cleaning solutions.",',
        f'"description": "{page_name} page for Zoiris Cleaning Service, the leading residential, commercial, and Airbnb cleaning company in Mobile, Alabama.",'
    )
    
    # 5. H1 tag
    content = content.replace(
        '#1 Cleaning Services in Mobile, AL',
        f'{page_name}'
    )
    
    # 6. Hero subtext
    if page_name == "About Us":
        hero_subtext = "Learn more about <em>Zoiris Cleaning Service</em>, your trusted provider for residential & commercial cleaning across Mobile, Baldwin County, and nearby cities."
    elif page_name == "Cleaning Blog":
        hero_subtext = "Read the latest tips, tricks, and news from <em>Zoiris Cleaning Service</em> on how to maintain a spotless home or business."
    elif page_name == "Contact Us":
        hero_subtext = "Get in touch with <em>Zoiris Cleaning Service</em> today. We are ready to help with your residential & commercial cleaning needs across Mobile and Baldwin County."
        
    content = content.replace(
        '<strong>Zoiris Cleaning Service</strong> provides trusted\n          <em>residential & commercial cleaning</em> across\n          <strong>Mobile, Baldwin County, and nearby cities</strong>.\n          From deep cleans to move-in/out and eco-friendly solutions, we make your home or business spotless.',
        hero_subtext
    )
    
    content = re.sub(r'onclick="location\.href=[\'"]/[\'"]"', 'onclick="location.href=\'/mobile-al/\'"', content)
    content = content.replace('href="/" class="contact-button text-lg">Home</a>', 'href="/mobile-al/" class="contact-button text-lg">Home</a>')
    content = re.sub(r'href="/index\.html"(\s*)><i([^>]*fa-home[^>]*)></i>(\s*)Home</a>', r'href="/mobile-al/"\1><i\2></i>\3Home</a>', content)
    content = re.sub(r'href="/"(\s*)class="block px-4 py-4 text-xl font-medium text-white hover:text-blue-400', r'href="/mobile-al/"\1class="block px-4 py-4 text-xl font-medium text-white hover:text-blue-400', content)

    # Make the directory
    out_dir = os.path.join(BASE_DIR, folder_path)
    os.makedirs(out_dir, exist_ok=True)
    
    # Write the new index file
    out_file = os.path.join(out_dir, "index.html")
    with open(out_file, "w", encoding="utf-8") as out:
        out.write(content)
        
    print(f"Generated {out_file}")

print("Successfully generated About, Blog, and Contact pages.")

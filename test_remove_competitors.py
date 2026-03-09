import os
import re

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to capture the entire competitor injection section.
    # It starts with the HTML comment: <!-- UNIQUE SEO SPINTAX COMPETITOR INJECTION: ... -->
    # Then captures the <section> ... </section> that follows it.
    
    # We'll use re.sub with re.DOTALL to match across newlines
    pattern = re.compile(
        r'[\t ]*<!-- UNIQUE SEO SPINTAX COMPETITOR INJECTION:.*?-->\s*'
        r'<section\s+class="[^"]*"\s+id="alternative-to-[^"]*">.*?</section>\s*',
        re.IGNORECASE | re.DOTALL
    )
    
    new_content = pattern.sub('', content)
    
    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

if __name__ == "__main__":
    test_file = r"c:\Users\lucia\Downloads\Zoiris-Cleaning-Services\birmingham-al\home-watch-services\index.html"
    if clean_file(test_file):
        print("Competitor section successfully removed from test file.")
    else:
        print("No competitor section found or regex failed.")

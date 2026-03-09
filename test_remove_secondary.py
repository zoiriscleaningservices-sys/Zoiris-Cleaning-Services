import os
import re

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex targeting the secondary competitor section
    pattern = re.compile(
        r'[\t ]*<!-- zcs-spintax-injected \| .*? vs .*? -->\s*'
        r'<section\s+class="[^"]*"\s+id="zoiris-vs-[^"]*">.*?</section>\s*',
        re.IGNORECASE | re.DOTALL
    )
    
    new_content = pattern.sub('', content)
    
    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

if __name__ == "__main__":
    test_file = r"c:\Users\lucia\Downloads\Zoiris-Cleaning-Services\birmingham-al\gym-fitness-center-cleaning\index.html"
    if clean_file(test_file):
        print("Secondary competitor section successfully removed from test file.")
    else:
        print("No secondary competitor section found or regex failed.")

import os
import re

def main():
    directory = '.'
    files_modified = 0
    files_scanned = 0

    # Match the spintax comment and the subsequent section block
    pattern = re.compile(
        r'[\t ]*<!-- UNIQUE SEO SPINTAX COMPETITOR INJECTION:.*?-->\s*'
        r'<section\s+class="[^"]*"\s+id="alternative-to-[^"]*">.*?</section>\s*',
        re.IGNORECASE | re.DOTALL
    )

    print("Scanning repository for competitor sections...")

    # Traverse all directories
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

                    new_content = pattern.sub('', content)

                    if content != new_content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        files_modified += 1
                        
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")

    print(f"\nDone! Scanned {files_scanned} files. Removed competitor sections from {files_modified} files.")

if __name__ == "__main__":
    main()

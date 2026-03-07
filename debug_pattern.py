import re

with open(r'c:\Users\lucia\Downloads\Zoiris-Cleaning-Services\abbeville-al\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Find the services section
idx = content.find('id="services"')
if idx == -1:
    print("NO services section found!")
else:
    snippet = content[max(0,idx-300):idx+50]
    print("FOUND services section. Context before:")
    print(repr(snippet))
    print()
    print("---RAW---")
    print(snippet)

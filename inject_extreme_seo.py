import os
import re

BASE_DIR = "."

def inject_extreme_schema():
    print("Initiating Phase 4: Extreme Schema Injection across 97,000+ files...")
    count = 0
    modified = 0
    
    for root, dirs, files in os.walk(BASE_DIR):
        # Exclude hidden folders, node_modules, temp builds
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'venv', '__pycache__', 'locations_backup']]
        
        for file in files:
            if file == "index.html":
                count += 1
                filepath = os.path.join(root, file)
                
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Check if we already injected the extreme schema
                if "Zoiris Service Schema Injection (Phase 4)" in content:
                    continue
                
                # Extract the specific city
                city_match = re.search(r'<title>.*?in (.*?), AL', content)
                city_name = city_match.group(1) if city_match else "Alabama"
                
                # Extract the specific service
                service_match = re.search(r'<title>(.*?) in .*?, AL', content)
                service_name = service_match.group(1).replace("#1", "").replace("Top", "").strip() if service_match else "Cleaning Service"
                
                if "About" in service_name or "Blog" in service_name or "Contact" in service_name or "Service Areas" in service_name:
                    service_name = "Cleaning Service"
                
                # --- INJECTION 1: The 5-Star AggregateRating Hack ---
                review_count = str(120 + (len(service_name) * 7) % 300)
                
                content = re.sub(
                    r'"aggregateRating": \{[^}]+\}', 
                    f'''"aggregateRating": {{\n    "@type": "AggregateRating",\n    "ratingValue": "4.9",\n    "reviewCount": "{review_count}",\n    "bestRating": "5",\n    "worstRating": "1"\n  }}''', 
                    content
                )

                # --- INJECTION 2: Dedicated Service Schema ---
                service_schema = f'''
  <!-- Zoiris Service Schema Injection (Phase 4) -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Service",
    "name": "{service_name}",
    "provider": {{
      "@type": "LocalBusiness",
      "name": "Zoiris Cleaning Services"
    }},
    "areaServed": {{
      "@type": "City",
      "name": "{city_name}"
    }},
    "description": "Zoiris provides the highest-rated {service_name.lower()} in {city_name}, Alabama. Satisfaction guaranteed.",
    "serviceType": "{service_name}"
  }}
  </script>
'''             
                content = content.replace('<!-- FAQ Schema (Boosts Google Featured Snippets) -->', f'{service_schema}\n  <!-- FAQ Schema (Boosts Google Featured Snippets) -->')
                
                
                # --- INJECTION 3: The Automated Authority Web (Footer Interlinking) ---
                footer_interlink = f'''
    <!-- Phase 4 Authority Web Interlinking -->
    <section class="bg-gray-900 py-12 border-t border-gray-800 z-50 relative mt-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-8">
          <h3 class="text-2xl font-bold text-white mb-2">Nearby Featured Service Areas</h3>
          <p class="text-gray-400 text-sm max-w-2xl mx-auto">We provide top-rated {service_name.lower()} not just in {city_name}, but across the entire Gulf Coast and State of Alabama.</p>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3 text-center">
            <a href="/daphne-al/" class="text-gray-500 hover:text-blue-400 text-xs transition-colors">Daphne, AL</a>
            <a href="/birmingham-al/" class="text-gray-500 hover:text-blue-400 text-xs transition-colors">Birmingham, AL</a>
            <a href="/spanish-fort-al/" class="text-gray-500 hover:text-blue-400 text-xs transition-colors">Spanish Fort, AL</a>
            <a href="/huntsville-al/" class="text-gray-500 hover:text-blue-400 text-xs transition-colors">Huntsville, AL</a>
            <a href="/foley-al/" class="text-gray-500 hover:text-blue-400 text-xs transition-colors">Foley, AL</a>
            <a href="/montgomery-al/" class="text-gray-500 hover:text-blue-400 text-xs transition-colors">Montgomery, AL</a>
            <a href="/locations/" class="text-blue-500 hover:text-pink-400 font-bold text-xs transition-colors">View All 480+ Locations</a>
        </div>
      </div>
    </section>
'''             
                content = content.replace('</body>', f'{footer_interlink}\n</body>')

                with open(filepath, "w", encoding="utf-8") as out:
                    out.write(content)
                    modified += 1
                
                if modified % 5000 == 0:
                    print(f"Phase 4 executing... ({modified}/{count} files modified so far)")
                    
    print(f"Phase 4 EXECUTION COMPLETE. Modified {modified} of {count} total files across Alabama.")

if __name__ == "__main__":
    inject_extreme_schema()

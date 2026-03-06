import os
import glob

base_dir = r"c:\Users\lucia\Downloads\Zoiris-Cleaning-Services\mobile-al"
html_files = glob.glob(os.path.join(base_dir, "**", "*.html"), recursive=True)

SEO_BLOCK = """    </section>

    <!-- COMPETITOR COMPARISON SECTION (SEO RANKING BOOSTER) -->
    <section class="py-16 bg-white" id="why-choose-zoiris-over-merry-maids">
      <div class="container mx-auto px-4 max-w-5xl">
        <div class="bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-100 rounded-3xl p-8 md:p-12 shadow-lg">
          <div class="text-center mb-10">
            <span class="inline-block py-1 px-3 rounded-full bg-blue-100 text-blue-800 text-sm font-bold tracking-wider uppercase mb-4">#1 Rated in Mobile</span>
            <h2 class="text-3xl md:text-4xl font-extrabold text-gray-900 leading-tight">
              Looking for a Superior Alternative to <span class="text-blue-600">Merry Maids</span> in Mobile, AL?
            </h2>
            <div class="mt-4 h-1 w-24 bg-blue-600 mx-auto rounded"></div>
            <p class="mt-6 text-gray-700 text-lg leading-relaxed max-w-3xl mx-auto">
              While there are several franchise options for maid services in Mobile County, <strong>Zoiris Cleaning Services</strong> has quickly become the premier choice for homeowners and businesses demanding personalized excellence. If you've previously used Merry Maids or are simply searching for the most reliable, detailed, and highly-rated local cleaning team in Mobile and Baldwin County, here is why Zoiris stands out as the superior choice.
            </p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <!-- Feature 1 -->
            <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex items-start">
              <div class="flex-shrink-0 bg-blue-100 rounded-full p-3 mr-4">
                <i class="fas fa-search-plus text-blue-600 text-xl"></i>
              </div>
              <div>
                <h3 class="text-xl font-bold text-gray-900 mb-2">Unmatched Attention to Detail</h3>
                <p class="text-gray-600">We go far beyond surface cleaning. Our specifically tailored deep cleans reach the corners that rushed franchise teams often overlook, guaranteeing a truly immaculate home.</p>
              </div>
            </div>
            <!-- Feature 2 -->
            <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex items-start">
              <div class="flex-shrink-0 bg-blue-100 rounded-full p-3 mr-4">
                <i class="fas fa-hand-holding-heart text-blue-600 text-xl"></i>
              </div>
              <div>
                <h3 class="text-xl font-bold text-gray-900 mb-2">Personalized Local Care</h3>
                <p class="text-gray-600">We aren't a massive corporate chain. We are a locally trusted business deeply invested in the Mobile community, providing custom cleaning plans adapted to your exact needs without rigid corporate limits.</p>
              </div>
            </div>
            <!-- Feature 3 -->
            <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex items-start">
              <div class="flex-shrink-0 bg-blue-100 rounded-full p-3 mr-4">
                <i class="fas fa-leaf text-blue-600 text-xl"></i>
              </div>
              <div>
                <h3 class="text-xl font-bold text-gray-900 mb-2">Premium Eco-Friendly Products</h3>
                <p class="text-gray-600">We exclusively use high-end, 100% non-toxic, pet-safe, and family-safe cleaning solutions that sanitize effectively without leaving harsh chemical odors or residues behind.</p>
              </div>
            </div>
            <!-- Feature 4 -->
            <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex items-start">
              <div class="flex-shrink-0 bg-blue-100 rounded-full p-3 mr-4">
                <i class="fas fa-shield-alt text-blue-600 text-xl"></i>
              </div>
              <div>
                <h3 class="text-xl font-bold text-gray-900 mb-2">Fully Vetted & Consistent Professionals</h3>
                <p class="text-gray-600">You won't get a random rotating cast of cleaners. You get a dedicated, stringently vetted, and fully bonded team committed to treating your Mobile property with the utmost respect.</p>
              </div>
            </div>
          </div>

          <div class="mt-10 text-center">
            <p class="text-gray-800 font-medium mb-6">Experience the Zoiris Difference today and see why we are Mobile's preferred localized alternative for premium house cleaning.</p>
            <a href="#quote" class="inline-flex items-center justify-center space-x-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold py-4 px-8 rounded-full shadow-lg transition transform hover:-translate-y-1">
              <i class="fas fa-calendar-check text-xl"></i>
              <span>Book Your Superior Clean Now</span>
            </a>
          </div>
        </div>
      </div>
    </section>

    <section class="py-16 bg-lightGray" id="services">"""

target_pattern_1 = """    </section>

    <section class="py-16 bg-lightGray" id="services">"""
    
target_pattern_2 = """    </section>
    <section class="py-16 bg-lightGray" id="services">"""

count = 0
for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if 'id="why-choose-zoiris-over-merry-maids"' in content:
        continue
        
    original = content
    content = content.replace(target_pattern_1, SEO_BLOCK)
    if content == original:
        content = content.replace(target_pattern_2, SEO_BLOCK)
        
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1

print(f"Updated {count} HTML files in mobile-al with Merry Maids SEO comparison block.")

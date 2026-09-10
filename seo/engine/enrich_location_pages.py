import os
import re
import json

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with open(os.path.join(root_dir, 'seo', 'locations.json'), 'r', encoding='utf-8') as f:
    LOCATIONS = json.load(f)

# Hero Trust Badges snippet
def get_trust_badges_html():
    return """
        <!-- 🌟 TRUST SIGNALS & KEY VALUE HIGHLIGHTS -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 max-w-3xl mx-auto pt-2 text-left">
          <div class="bg-black/40 backdrop-blur-md border border-white/10 rounded-xl p-3 flex items-center gap-3">
            <div class="w-9 h-9 rounded-lg bg-green-500/20 text-green-400 flex items-center justify-center text-lg shrink-0">
              <i class="fas fa-shield-alt"></i>
            </div>
            <div>
              <p class="text-xs text-gray-400 uppercase font-semibold">Fully Insured</p>
              <p class="text-xs sm:text-sm font-bold text-white">Licensed &amp; Bonded</p>
            </div>
          </div>

          <div class="bg-black/40 backdrop-blur-md border border-white/10 rounded-xl p-3 flex items-center gap-3">
            <div class="w-9 h-9 rounded-lg bg-blue-500/20 text-blue-400 flex items-center justify-center text-lg shrink-0">
              <i class="fas fa-file-contract"></i>
            </div>
            <div>
              <p class="text-xs text-gray-400 uppercase font-semibold">Zero Lock-In</p>
              <p class="text-xs sm:text-sm font-bold text-white">No Contracts Ever</p>
            </div>
          </div>

          <div class="bg-black/40 backdrop-blur-md border border-white/10 rounded-xl p-3 flex items-center gap-3">
            <div class="w-9 h-9 rounded-lg bg-purple-500/20 text-purple-400 flex items-center justify-center text-lg shrink-0">
              <i class="fas fa-calendar-check"></i>
            </div>
            <div>
              <p class="text-xs text-gray-400 uppercase font-semibold">Flexibility</p>
              <p class="text-xs sm:text-sm font-bold text-white">No Reschedule Fees</p>
            </div>
          </div>

          <div class="bg-black/40 backdrop-blur-md border border-white/10 rounded-xl p-3 flex items-center gap-3">
            <div class="w-9 h-9 rounded-lg bg-yellow-500/20 text-yellow-400 flex items-center justify-center text-lg shrink-0">
              <i class="fas fa-star"></i>
            </div>
            <div>
              <p class="text-xs text-gray-400 uppercase font-semibold">Top Rated</p>
              <p class="text-xs sm:text-sm font-bold text-white">4.9★ (240+ Reviews)</p>
            </div>
          </div>
        </div>
"""

# Cleaning Standards Checklist snippet
def get_cleaning_standards_html(city, county):
    return f"""
    <!-- 🧼 SECTION: ZOIRIS STANDARD OF CLEANING (ROOM-BY-ROOM CHECKLIST) -->
    <section class="py-20 px-4 sm:px-6 lg:px-8 bg-transparent relative z-10" id="cleaning-standards">
      <div class="max-w-7xl mx-auto">
        
        <div class="text-center max-w-3xl mx-auto mb-16">
          <span class="text-sm font-bold uppercase tracking-wider text-blue-100 bg-white/10 backdrop-blur-md border border-white/20 px-4 py-1.5 rounded-full">
            ✦ Detailed Room-by-Room Protocol in {city}, AL ✦
          </span>
          <h2 class="text-3xl md:text-4xl font-extrabold text-white mt-4 tracking-tight">
            Our Standard of Cleaning: Little Things Make The Difference
          </h2>
          <div class="mt-3 h-1 w-24 bg-gradient-to-r from-blue-400 to-indigo-400 mx-auto rounded"></div>
          <p class="mt-4 text-purple-100 text-base md:text-lg leading-relaxed">
            Every home cleaned by <strong>Zoiris Cleaning Services in {city}</strong> follows a meticulous, systematic checklist. From high-efficiency HEPA vacuuming to delicate surface polishing, we treat your home with unparalleled respect and precision.
          </p>
        </div>

        <!-- Room Checklists Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
          
          <!-- Bathrooms -->
          <div class="bg-white rounded-2xl p-6 sm:p-8 shadow-2xl border border-white/10 hover:shadow-2xl transition-all duration-300">
            <div class="flex items-center gap-4 mb-6">
              <div class="w-12 h-12 rounded-xl bg-blue-100 text-blue-600 flex items-center justify-center text-2xl">
                <i class="fas fa-bath"></i>
              </div>
              <div>
                <h3 class="text-xl font-bold text-gray-900">Bathrooms</h3>
                <p class="text-xs text-blue-600 font-semibold uppercase tracking-wide">Sanitized &amp; Sparkling</p>
              </div>
            </div>
            <ul class="space-y-3 text-sm text-gray-700">
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Tub &amp; Shower Scrub:</strong> Tiles, glass doors, walls &amp; fixtures descaled and shined.</span></li>
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Toilet Disinfection:</strong> Basin, seat, lid, outer hinges, base &amp; handle sanitized.</span></li>
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Vanity &amp; Mirrors:</strong> Countertops disinfected, chrome fixtures polished, streak-free glass.</span></li>
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Accessories &amp; Trash:</strong> Toiletries &amp; towel bars wiped down, trash emptied &amp; relined.</span></li>
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Flooring:</strong> Hand-washed tile or sanitized steam mopping.</span></li>
            </ul>
          </div>

          <!-- Kitchen & Dining -->
          <div class="bg-white rounded-2xl p-6 sm:p-8 shadow-2xl border border-white/10 hover:shadow-2xl transition-all duration-300">
            <div class="flex items-center gap-4 mb-6">
              <div class="w-12 h-12 rounded-xl bg-purple-100 text-purple-600 flex items-center justify-center text-2xl">
                <i class="fas fa-utensils"></i>
              </div>
              <div>
                <h3 class="text-xl font-bold text-gray-900">Kitchen &amp; Dining</h3>
                <p class="text-xs text-purple-600 font-semibold uppercase tracking-wide">Degreased &amp; Polished</p>
              </div>
            </div>
            <ul class="space-y-3 text-sm text-gray-700">
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Stovetop &amp; Range:</strong> Burners scrubbed, grease removed, control knobs wiped.</span></li>
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Microwave Detail:</strong> Fully cleaned and deodorized inside and outside.</span></li>
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Countertops &amp; Backsplash:</strong> Disinfected &amp; granite/quartz polished.</span></li>
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Appliance Exteriors:</strong> Refrigerator, dishwasher &amp; oven exterior stainless polish.</span></li>
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Sinks &amp; Chrome:</strong> Scrubbed, disinfected, and chrome fixtures polished.</span></li>
            </ul>
          </div>

          <!-- Living Rooms & Bedrooms -->
          <div class="bg-white rounded-2xl p-6 sm:p-8 shadow-2xl border border-white/10 hover:shadow-2xl transition-all duration-300">
            <div class="flex items-center gap-4 mb-6">
              <div class="w-12 h-12 rounded-xl bg-pink-100 text-pink-600 flex items-center justify-center text-2xl">
                <i class="fas fa-bed"></i>
              </div>
              <div>
                <h3 class="text-xl font-bold text-gray-900">Living &amp; Bedrooms</h3>
                <p class="text-xs text-pink-600 font-semibold uppercase tracking-wide">Fresh, Tidy &amp; Allergen-Free</p>
              </div>
            </div>
            <ul class="space-y-3 text-sm text-gray-700">
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Beds &amp; Linens:</strong> Beds made neatly; sheets washed &amp; changed upon request.</span></li>
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Upholstery &amp; Pet Hair:</strong> Excess pet hair vacuumed from furniture and couches.</span></li>
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Furniture Care:</strong> Wood, glass &amp; leather furniture dry or damp wiped.</span></li>
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>High-Touch Sanitation:</strong> Light switches, remotes &amp; door knobs sanitized.</span></li>
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Cobweb Removal:</strong> Corners, ceiling trims &amp; wall moldings cleared.</span></li>
            </ul>
          </div>

          <!-- Detailed Dusting Standards -->
          <div class="bg-white rounded-2xl p-6 sm:p-8 shadow-2xl border border-white/10 hover:shadow-2xl transition-all duration-300">
            <div class="flex items-center gap-4 mb-6">
              <div class="w-12 h-12 rounded-xl bg-amber-100 text-amber-600 flex items-center justify-center text-2xl">
                <i class="fas fa-feather"></i>
              </div>
              <div>
                <h3 class="text-xl font-bold text-gray-900">Dusting Standards</h3>
                <p class="text-xs text-amber-600 font-semibold uppercase tracking-wide">Regular &amp; Rotational Care</p>
              </div>
            </div>
            <ul class="space-y-3 text-sm text-gray-700">
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Ceiling Fans &amp; Fixtures:</strong> Blades, globes &amp; chandelier dust removal.</span></li>
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Blinds &amp; Window Coverings:</strong> Slats dusted and window sills wiped clean.</span></li>
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Baseboards &amp; Chair Rails:</strong> Trim detailed regularly or on deep rotation.</span></li>
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Air Vents &amp; Intake Grills:</strong> Filter covers and intake slats dusted.</span></li>
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Decor &amp; Picture Frames:</strong> Wall art, knick-knacks &amp; tabletop accents.</span></li>
            </ul>
          </div>

          <!-- Floor & Carpet Care -->
          <div class="bg-white rounded-2xl p-6 sm:p-8 shadow-2xl border border-white/10 hover:shadow-2xl transition-all duration-300">
            <div class="flex items-center gap-4 mb-6">
              <div class="w-12 h-12 rounded-xl bg-teal-100 text-teal-600 flex items-center justify-center text-2xl">
                <i class="fas fa-broom"></i>
              </div>
              <div>
                <h3 class="text-xl font-bold text-gray-900">Floors &amp; Surfaces</h3>
                <p class="text-xs text-teal-600 font-semibold uppercase tracking-wide">HEPA Vacuum &amp; Microfiber Mop</p>
              </div>
            </div>
            <ul class="space-y-3 text-sm text-gray-700">
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>HEPA Filtration Vacuums:</strong> Commercial Miele &amp; Kirby grade vacuuming.</span></li>
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Rugs &amp; Carpeting:</strong> Bath &amp; kitchen rugs shaken, edges &amp; carpets vacuumed.</span></li>
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Hardwood Floor Care:</strong> Damp mopped with dedicated cloth mops &amp; Bona cleaners.</span></li>
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Tile &amp; Grout:</strong> Steam mopping and residue-free tile cleaning.</span></li>
              <li class="flex items-start"><i class="fas fa-check-circle text-green-500 mt-1 mr-3 shrink-0"></i><span><strong>Under Furniture:</strong> Accessible spaces under beds and sofas vacuumed.</span></li>
            </ul>
          </div>

          <!-- Deep Clean & Custom Add-ons -->
          <div class="bg-white rounded-2xl p-6 sm:p-8 shadow-2xl border border-white/10 hover:shadow-2xl transition-all duration-300">
            <div class="flex items-center gap-4 mb-6">
              <div class="w-12 h-12 rounded-xl bg-indigo-100 text-indigo-600 flex items-center justify-center text-2xl">
                <i class="fas fa-magic"></i>
              </div>
              <div>
                <h3 class="text-xl font-bold text-gray-900">Custom Add-Ons</h3>
                <p class="text-xs text-indigo-600 font-semibold uppercase tracking-wide">Deep Clean &amp; Move Turnovers</p>
              </div>
            </div>
            <ul class="space-y-3 text-sm text-gray-700">
              <li class="flex items-start"><i class="fas fa-plus-circle text-indigo-500 mt-1 mr-3 shrink-0"></i><span><strong>Inside Oven Detailing:</strong> Deep degrease of racks, glass &amp; interior walls.</span></li>
              <li class="flex items-start"><i class="fas fa-plus-circle text-indigo-500 mt-1 mr-3 shrink-0"></i><span><strong>Inside Refrigerator / Freezer:</strong> Shelves and bins washed and sanitized.</span></li>
              <li class="flex items-start"><i class="fas fa-plus-circle text-indigo-500 mt-1 mr-3 shrink-0"></i><span><strong>Cabinet &amp; Drawer Interiors:</strong> Vacuumed &amp; wiped for move-in/out.</span></li>
              <li class="flex items-start"><i class="fas fa-plus-circle text-indigo-500 mt-1 mr-3 shrink-0"></i><span><strong>Hand-Washed Baseboards:</strong> Deep scrub of grime and scuff marks.</span></li>
              <li class="flex items-start"><i class="fas fa-plus-circle text-indigo-500 mt-1 mr-3 shrink-0"></i><span><strong>Post-Construction Detail:</strong> Drywall dust and residue extraction.</span></li>
            </ul>
          </div>

        </div>

        <!-- 📊 SERVICE COMPARISON MATRIX -->
        <div class="bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 rounded-3xl p-6 sm:p-10 text-white shadow-2xl border border-indigo-500/30">
          <div class="text-center max-w-2xl mx-auto mb-10">
            <h3 class="text-2xl sm:text-3xl font-extrabold tracking-tight">
              Choose the Service That Fits Your {city} Home
            </h3>
            <p class="text-gray-300 text-sm sm:text-base mt-2">
              All services feature <strong>No Contracts</strong>, background-checked staff, and our 100% Satisfaction Guarantee.
            </p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
            
            <!-- Recurring Maintenance -->
            <div class="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/15 flex flex-col justify-between hover:bg-white/15 transition-all">
              <div>
                <span class="inline-block bg-blue-500/30 text-blue-300 text-xs font-bold uppercase tracking-wider px-3 py-1 rounded-full mb-3">
                  Most Popular
                </span>
                <h4 class="text-xl font-bold text-white mb-2">Recurring Maid Service</h4>
                <p class="text-xs text-gray-300 mb-4 leading-relaxed">Weekly, bi-weekly, or monthly custom routine keeping your {city} home immaculate all year.</p>
                <ul class="text-xs space-y-2 text-gray-200 mb-6">
                  <li class="flex items-center"><i class="fas fa-check text-green-400 mr-2"></i> All bathrooms &amp; kitchen sanitized</li>
                  <li class="flex items-center"><i class="fas fa-check text-green-400 mr-2"></i> Whole-home HEPA vacuuming</li>
                  <li class="flex items-center"><i class="fas fa-check text-green-400 mr-2"></i> Hardwood &amp; tile mopping</li>
                  <li class="flex items-center"><i class="fas fa-check text-green-400 mr-2"></i> Dusting furniture &amp; decor</li>
                  <li class="flex items-center"><i class="fas fa-check text-green-400 mr-2"></i> <strong>Zero locked contracts</strong></li>
                </ul>
              </div>
              <a href="#quote" class="w-full text-center bg-blue-600 hover:bg-blue-500 text-white font-bold py-2.5 rounded-xl transition text-sm shadow-md">
                Get Instant Quote
              </a>
            </div>

            <!-- Deep Cleaning -->
            <div class="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/15 flex flex-col justify-between hover:bg-white/15 transition-all">
              <div>
                <span class="inline-block bg-purple-500/30 text-purple-300 text-xs font-bold uppercase tracking-wider px-3 py-1 rounded-full mb-3">
                  Deep Detail
                </span>
                <h4 class="text-xl font-bold text-white mb-2">Deep Cleaning</h4>
                <p class="text-xs text-gray-300 mb-4 leading-relaxed">Top-to-bottom intensive scrub perfect for spring resets or first-time service.</p>
                <ul class="text-xs space-y-2 text-gray-200 mb-6">
                  <li class="flex items-center"><i class="fas fa-check text-green-400 mr-2"></i> All Standard clean features</li>
                  <li class="flex items-center"><i class="fas fa-check text-green-400 mr-2"></i> Baseboards &amp; doors hand-scrubbed</li>
                  <li class="flex items-center"><i class="fas fa-check text-green-400 mr-2"></i> Blinds &amp; ceiling fan blades cleaned</li>
                  <li class="flex items-center"><i class="fas fa-check text-green-400 mr-2"></i> Inside microwave &amp; stovetop degreased</li>
                  <li class="flex items-center"><i class="fas fa-check text-green-400 mr-2"></i> Heavy scale &amp; soap scum removal</li>
                </ul>
              </div>
              <a href="#quote" class="w-full text-center bg-purple-600 hover:bg-purple-500 text-white font-bold py-2.5 rounded-xl transition text-sm shadow-md">
                Get Deep Clean Quote
              </a>
            </div>

            <!-- Move-In / Move-Out -->
            <div class="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/15 flex flex-col justify-between hover:bg-white/15 transition-all">
              <div>
                <span class="inline-block bg-pink-500/30 text-pink-300 text-xs font-bold uppercase tracking-wider px-3 py-1 rounded-full mb-3">
                  Turnkey Ready
                </span>
                <h4 class="text-xl font-bold text-white mb-2">Move In / Out Clean</h4>
                <p class="text-xs text-gray-300 mb-4 leading-relaxed">Immaculate turnaround for empty homes, renters, realtors &amp; new buyers.</p>
                <ul class="text-xs space-y-2 text-gray-200 mb-6">
                  <li class="flex items-center"><i class="fas fa-check text-green-400 mr-2"></i> Complete interior cabinet wipeout</li>
                  <li class="flex items-center"><i class="fas fa-check text-green-400 mr-2"></i> Inside oven &amp; refrigerator clean</li>
                  <li class="flex items-center"><i class="fas fa-check text-green-400 mr-2"></i> Closets, shelving &amp; baseboards</li>
                  <li class="flex items-center"><i class="fas fa-check text-green-400 mr-2"></i> Deposit-return guarantee standard</li>
                </ul>
              </div>
              <a href="#quote" class="w-full text-center bg-pink-600 hover:bg-pink-500 text-white font-bold py-2.5 rounded-xl transition text-sm shadow-md">
                Get Move Clean Quote
              </a>
            </div>

            <!-- Commercial Janitorial -->
            <div class="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/15 flex flex-col justify-between hover:bg-white/15 transition-all">
              <div>
                <span class="inline-block bg-emerald-500/30 text-emerald-300 text-xs font-bold uppercase tracking-wider px-3 py-1 rounded-full mb-3">
                  B2B Facility
                </span>
                <h4 class="text-xl font-bold text-white mb-2">Commercial Cleaning</h4>
                <p class="text-xs text-gray-300 mb-4 leading-relaxed">Offices, medical clinics, retail centers &amp; short-term rentals in {city}.</p>
                <ul class="text-xs space-y-2 text-gray-200 mb-6">
                  <li class="flex items-center"><i class="fas fa-check text-green-400 mr-2"></i> Restroom disinfection &amp; restocking</li>
                  <li class="flex items-center"><i class="fas fa-check text-green-400 mr-2"></i> Trash removal &amp; recycling sorting</li>
                  <li class="flex items-center"><i class="fas fa-check text-green-400 mr-2"></i> High-traffic floor care &amp; vacuuming</li>
                  <li class="flex items-center"><i class="fas fa-check text-green-400 mr-2"></i> Breakroom &amp; kitchen sanitization</li>
                  <li class="flex items-center"><i class="fas fa-check text-green-400 mr-2"></i> Customized commercial scheduling</li>
                </ul>
              </div>
              <a href="#quote" class="w-full text-center bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-2.5 rounded-xl transition text-sm shadow-md">
                Get Commercial Quote
              </a>
            </div>

          </div>
        </div>

      </div>
    </section>
"""

# FAQ Section snippet
def get_faq_section_html(city):
    return f"""
    <!-- ❓ SECTION: FREQUENTLY ASKED QUESTIONS (ACCORDION & RICH SEO) -->
    <section class="py-20 px-4 sm:px-6 lg:px-8 bg-transparent relative z-10" id="faq">
      <div class="max-w-5xl mx-auto">
        
        <div class="text-center max-w-3xl mx-auto mb-14">
          <span class="text-sm font-bold uppercase tracking-wider text-blue-100 bg-white/10 backdrop-blur-md border border-white/20 px-4 py-1.5 rounded-full">
            ✦ Got Questions? We Have Answers ✦
          </span>
          <h2 class="text-3xl md:text-4xl font-extrabold text-white mt-4 tracking-tight">
            Frequently Asked Questions About {city} AL Cleaning Services
          </h2>
          <div class="mt-3 h-1 w-24 bg-gradient-to-r from-blue-400 to-indigo-400 mx-auto rounded"></div>
          <p class="mt-4 text-purple-100 text-base md:text-lg leading-relaxed">
            Everything you need to know about our cleaning standards, flexible scheduling, pricing, and safety protections in {city} and surrounding Alabama areas.
          </p>
        </div>

        <!-- Accordion Items -->
        <div class="space-y-4">

          <!-- FAQ 1 -->
          <div class="bg-white rounded-2xl border border-white/20 shadow-xl overflow-hidden transition-all duration-200">
            <button class="w-full px-6 py-5 text-left font-bold text-lg text-gray-900 flex justify-between items-center hover:bg-slate-50 transition" onclick="toggleFaq(this)">
              <span class="flex items-center gap-3">
                <i class="fas fa-file-signature text-blue-600"></i>
                Do you require long-term contracts for recurring house cleaning in {city}?
              </span>
              <i class="fas fa-chevron-down text-gray-400 transition-transform duration-300"></i>
            </button>
            <div class="faq-answer px-6 pb-6 pt-2 text-gray-700 text-sm sm:text-base leading-relaxed hidden border-t border-gray-100">
              <p>
                <strong>No, never!</strong> At Zoiris Cleaning Services, all our residential and commercial services in {city} are provided with <strong>100% No Locked Contracts</strong>. You can enjoy weekly, bi-weekly, monthly, or on-demand cleanings with total freedom to pause, change frequency, or cancel at any time. We earn your business on every single visit through unmatched quality.
              </p>
            </div>
          </div>

          <!-- FAQ 2 -->
          <div class="bg-white rounded-2xl border border-white/20 shadow-xl overflow-hidden transition-all duration-200">
            <button class="w-full px-6 py-5 text-left font-bold text-lg text-gray-900 flex justify-between items-center hover:bg-slate-50 transition" onclick="toggleFaq(this)">
              <span class="flex items-center gap-3">
                <i class="fas fa-calendar-alt text-blue-600"></i>
                Are there fees if I need to reschedule or postpone my cleaning in {city}?
              </span>
              <i class="fas fa-chevron-down text-gray-400 transition-transform duration-300"></i>
            </button>
            <div class="faq-answer px-6 pb-6 pt-2 text-gray-700 text-sm sm:text-base leading-relaxed hidden border-t border-gray-100">
              <p>
                <strong>No. There are zero rescheduling fees!</strong> We understand that life happens—sickness, unexpected travel, or visiting family can change your schedule. Simply notify us in advance, and our team will gladly work with you to move your cleaning appointment to the next convenient available day with no penalty.
              </p>
            </div>
          </div>

          <!-- FAQ 3 -->
          <div class="bg-white rounded-2xl border border-white/20 shadow-xl overflow-hidden transition-all duration-200">
            <button class="w-full px-6 py-5 text-left font-bold text-lg text-gray-900 flex justify-between items-center hover:bg-slate-50 transition" onclick="toggleFaq(this)">
              <span class="flex items-center gap-3">
                <i class="fas fa-shield-alt text-blue-600"></i>
                Are your cleaners licensed, bonded, insured, and background-checked?
              </span>
              <i class="fas fa-chevron-down text-gray-400 transition-transform duration-300"></i>
            </button>
            <div class="faq-answer px-6 pb-6 pt-2 text-gray-700 text-sm sm:text-base leading-relaxed hidden border-t border-gray-100">
              <p>
                <strong>Yes, absolutely.</strong> Zoiris Cleaning Services is fully licensed, bonded, and insured with both general liability and workers' compensation insurance for your total peace of mind. Furthermore, <strong>100% of our staff are in-house vetted employees</strong> (never random gig subcontractors) who undergo rigorous criminal background screenings, drug testing, and thorough hands-on training.
              </p>
            </div>
          </div>

          <!-- FAQ 4 -->
          <div class="bg-white rounded-2xl border border-white/20 shadow-xl overflow-hidden transition-all duration-200">
            <button class="w-full px-6 py-5 text-left font-bold text-lg text-gray-900 flex justify-between items-center hover:bg-slate-50 transition" onclick="toggleFaq(this)">
              <span class="flex items-center gap-3">
                <i class="fas fa-calculator text-blue-600"></i>
                How are your cleaning prices calculated in {city}, AL?
              </span>
              <i class="fas fa-chevron-down text-gray-400 transition-transform duration-300"></i>
            </button>
            <div class="faq-answer px-6 pb-6 pt-2 text-gray-700 text-sm sm:text-base leading-relaxed hidden border-t border-gray-100">
              <p>
                We do not use rigid generic square-footage formulas because every home is unique. We evaluate your home’s bedrooms, bathrooms, flooring types, pet shedding, and personal priorities to formulate a transparent, customized flat-rate price. We provide free, fast estimates with zero hidden fees.
              </p>
            </div>
          </div>

          <!-- FAQ 5 -->
          <div class="bg-white rounded-2xl border border-white/20 shadow-xl overflow-hidden transition-all duration-200">
            <button class="w-full px-6 py-5 text-left font-bold text-lg text-gray-900 flex justify-between items-center hover:bg-slate-50 transition" onclick="toggleFaq(this)">
              <span class="flex items-center gap-3">
                <i class="fas fa-spray-can text-blue-600"></i>
                What equipment and cleaning products do you bring?
              </span>
              <i class="fas fa-chevron-down text-gray-400 transition-transform duration-300"></i>
            </button>
            <div class="faq-answer px-6 pb-6 pt-2 text-gray-700 text-sm sm:text-base leading-relaxed hidden border-t border-gray-100">
              <p>
                We supply all necessary professional equipment! Our teams arrive with commercial HEPA filtration vacuum systems (Miele &amp; Kirby standards for deep cleanings), extension dusters, microfiber cloth mop systems, and hospital-grade, eco-friendly disinfectants that are safe for children and pets. If you have specific specialty floor or stone cleaners you prefer (like Bona or Bruce), our staff will gladly utilize them.
              </p>
            </div>
          </div>

          <!-- FAQ 6 -->
          <div class="bg-white rounded-2xl border border-white/20 shadow-xl overflow-hidden transition-all duration-200">
            <button class="w-full px-6 py-5 text-left font-bold text-lg text-gray-900 flex justify-between items-center hover:bg-slate-50 transition" onclick="toggleFaq(this)">
              <span class="flex items-center gap-3">
                <i class="fas fa-layer-group text-blue-600"></i>
                What is the difference between a standard clean and a deep clean?
              </span>
              <i class="fas fa-chevron-down text-gray-400 transition-transform duration-300"></i>
            </button>
            <div class="faq-answer px-6 pb-6 pt-2 text-gray-700 text-sm sm:text-base leading-relaxed hidden border-t border-gray-100">
              <p>
                A <strong>Standard Maintenance Clean</strong> is designed for routine upkeep (bathrooms sanitized, kitchen surfaces degreased, beds made, whole-home HEPA vacuuming and mopping). A <strong>Deep Clean</strong> is an intensive restorative clean that includes detailed hand-scrubbing of baseboards, door frames, blinds, ceiling fan blades, air intake vents, microwave interior, and removal of deep scale/soap scum buildup.
              </p>
            </div>
          </div>

          <!-- FAQ 7 -->
          <div class="bg-white rounded-2xl border border-white/20 shadow-xl overflow-hidden transition-all duration-200">
            <button class="w-full px-6 py-5 text-left font-bold text-lg text-gray-900 flex justify-between items-center hover:bg-slate-50 transition" onclick="toggleFaq(this)">
              <span class="flex items-center gap-3">
                <i class="fas fa-map-marked-alt text-blue-600"></i>
                What service areas do you cover around {city}?
              </span>
              <i class="fas fa-chevron-down text-gray-400 transition-transform duration-300"></i>
            </button>
            <div class="faq-answer px-6 pb-6 pt-2 text-gray-700 text-sm sm:text-base leading-relaxed hidden border-t border-gray-100">
              <p>
                We service all neighborhoods in <strong>{city}</strong> and across Mobile &amp; Baldwin County including Downtown Mobile, Midtown, West Mobile, Spring Hill, Cottage Hill, Saraland, Semmes, Theodore, Daphne, Fairhope, Spanish Fort, Foley, Gulf Shores, and Orange Beach.
              </p>
            </div>
          </div>

          <!-- FAQ 8 -->
          <div class="bg-white rounded-2xl border border-white/20 shadow-xl overflow-hidden transition-all duration-200">
            <button class="w-full px-6 py-5 text-left font-bold text-lg text-gray-900 flex justify-between items-center hover:bg-slate-50 transition" onclick="toggleFaq(this)">
              <span class="flex items-center gap-3">
                <i class="fas fa-award text-blue-600"></i>
                What is your 100% Satisfaction Guarantee policy?
              </span>
              <i class="fas fa-chevron-down text-gray-400 transition-transform duration-300"></i>
            </button>
            <div class="faq-answer px-6 pb-6 pt-2 text-gray-700 text-sm sm:text-base leading-relaxed hidden border-t border-gray-100">
              <p>
                Your complete satisfaction is our primary priority. If any area does not meet your expectations, let us know within 24 hours. We will promptly send a team back to re-clean the specific area at zero charge to ensure you are 100% thrilled with our work!
              </p>
            </div>
          </div>

        </div>

        <!-- FAQ CTA -->
        <div class="mt-12 text-center bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl p-6 sm:p-8 text-white shadow-xl">
          <h3 class="text-xl sm:text-2xl font-bold mb-2">Have a specific question about your home or office in {city}?</h3>
          <p class="text-blue-100 text-sm sm:text-base mb-6 max-w-xl mx-auto">
            Our friendly local team is available 24/7 to help structure the perfect cleaning plan for your space.
          </p>
          <div class="flex flex-col sm:flex-row justify-center gap-4">
            <a href="tel:2512202515" class="bg-white text-blue-700 font-bold px-6 py-3 rounded-full hover:bg-gray-100 transition shadow-md">
              <i class="fas fa-phone-alt mr-2"></i> Call (251) 220-2515
            </a>
            <a href="#quote" class="bg-black/30 hover:bg-black/50 text-white font-bold px-6 py-3 rounded-full border border-white/30 transition">
              <i class="fas fa-file-invoice mr-2"></i> Request A Free Estimate
            </a>
          </div>
        </div>

      </div>
    </section>

    <script>
      function toggleFaq(button) {{
        const answer = button.nextElementSibling;
        const icon = button.querySelector('.fa-chevron-down');
        const isOpen = !answer.classList.contains('hidden');

        document.querySelectorAll('.faq-answer').forEach(el => {{
          el.classList.add('hidden');
        }});
        document.querySelectorAll('#faq .fa-chevron-down').forEach(el => {{
          el.classList.remove('rotate-180');
        }});

        if (!isOpen) {{
          answer.classList.remove('hidden');
          icon.classList.add('rotate-180');
        }}
      }}
    </script>
"""

def enrich_location_file(filepath):
    try:
        rel = os.path.relpath(filepath, root_dir).replace('\\', '/')
        parts = rel.split('/')
        if not parts[0].endswith('-al') or len(parts) > 2 or parts[-1] != 'index.html':
            return False
            
        loc_slug = parts[0]
        loc_data = LOCATIONS.get(loc_slug, {})
        city = loc_data.get('city', loc_slug[:-3].replace('-', ' ').title())
        county = loc_data.get('county', 'Alabama')
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        original_content = content
        
        # 1. Inject Trust Badges if not present in hero
        if '<!-- 🌟 TRUST SIGNALS' not in content:
            # Inject right before the scroll down arrow in hero
            if '<!-- Scroll Down Arrow -->' in content:
                content = content.replace('<!-- Scroll Down Arrow -->', f'{get_trust_badges_html()}\n        <!-- Scroll Down Arrow -->', 1)
                
        # 2. Inject Cleaning Standards section if not present
        if 'id="cleaning-standards"' not in content:
            # Place right before #quote section
            if '<section id="quote"' in content:
                content = content.replace('<section id="quote"', f'{get_cleaning_standards_html(city, county)}\n    <section id="quote"', 1)
                
        # 3. Inject FAQ section if not present
        if 'id="faq"' not in content:
            # Place right after services-preview or before blog / location
            if '<section class="py-20 bg-lightGray" id="blog">' in content:
                content = content.replace('<section class="py-20 bg-lightGray" id="blog">', f'{get_faq_section_html(city)}\n    <section class="py-20 bg-lightGray" id="blog">', 1)
            elif '<section class="py-20 bg-transparent relative z-10" id="blog">' in content:
                content = content.replace('<section class="py-20 bg-transparent relative z-10" id="blog">', f'{get_faq_section_html(city)}\n    <section class="py-20 bg-transparent relative z-10" id="blog">', 1)
            elif 'id="blog"' in content:
                content = re.sub(r'(<section[^>]*id=["\']blog["\'])', f'{get_faq_section_html(city)}\n    \\1', content, count=1)
            elif '<footer' in content:
                content = content.replace('<footer', f'{get_faq_section_html(city)}\n    <footer', 1)
                
        if content != original_content:
            tmp = filepath + '.tmp'
            with open(tmp, 'w', encoding='utf-8') as f:
                f.write(content)
            os.replace(tmp, filepath)
            return True
            
        return False
    except Exception as e:
        print(f"Error enriching {filepath}: {e}")
        return False

if __name__ == '__main__':
    import concurrent.futures
    import multiprocessing
    
    print("Starting location page enrichment...")
    loc_files = []
    for slug in LOCATIONS.keys():
        fp = os.path.join(root_dir, slug, 'index.html')
        if os.path.exists(fp):
            loc_files.append(fp)
            
    print(f"Enriching {len(loc_files)} city hub pages with high-ranking SEO sections...")
    
    count = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count() * 4) as executor:
        for r in executor.map(enrich_location_file, loc_files):
            if r:
                count += 1
                
    print(f"Successfully enriched {count}/{len(loc_files)} location hub pages with full SEO components!")

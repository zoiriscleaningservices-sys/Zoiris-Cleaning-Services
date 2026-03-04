
export default function PageTemplate({ city = '{city}', state = 'AL', service = 'Cleaning Service' }: { city?: string, state?: string, service?: string }) {
  return (
    <>

  
  <div className="floating-bubbles">
    <div className="bubble" ></div>
    <div className="bubble" ></div>
    <div className="bubble" ></div>
    <div className="bubble" ></div>
    <div className="bubble" ></div>
  </div>
  
  <main id="main-content">

    
    <header className="relative z-[999] w-full">
      
      <nav className="hidden md:block bg-transparent z-[999] relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-20">
            <div className="flex items-center">
              <div className="flex-shrink-0 cursor-pointer" >
                <img
                  src="https://i.ibb.co/gbzKPdnc/Chat-GPT-Image-Aug-31-2025-12-19-42-AM-Picsart-Background-Remover.png"
                  alt="Zoiris Cleaning service" className="h-28 w-auto transform hover:scale-105 transition duration-300" />
              </div>
            </div>

            <div className="flex items-center space-x-8 ml-auto">
              <a href="/" className="contact-button text-lg">Home</a>
              <a href="/mobile-al/about/" className="contact-button text-lg">About</a>

              
              <div className="relative group inline-block">
                <button type="button" className="contact-button text-lg flex items-center">
                  Services <i className="fas fa-chevron-down text-sm ml-2"></i>
                </button>
                <div
                  className="absolute -left-32 top-full hidden group-hover:grid grid-cols-3 gap-4 w-[900px] z-[999] pt-2">
                  <div
                    className="flex flex-col space-y-2 bg-white/95 p-4 rounded-xl shadow-2xl backdrop-blur-md border border-gray-200">
                    <h4 className="text-xl font-bold text-gray-900 border-b-2 border-indigo-500 pb-2 mb-2 text-center">
                      Residential & Property</h4>
                    <a className="contact-button text-sm hover:scale-105 transition-transform text-center py-2"
                      href="/mobile-al/house-cleaning/">House Cleaning</a>
                    <a className="contact-button text-sm hover:scale-105 transition-transform text-center py-2"
                      href="/mobile-al/deep-cleaning/">Deep Cleaning</a>
                    <a className="contact-button text-sm hover:scale-105 transition-transform text-center py-2"
                      href="/mobile-al/move-in-cleaning/">Move-In Cleaning</a>
                    <a className="contact-button text-sm hover:scale-105 transition-transform text-center py-2"
                      href="/mobile-al/move-out-cleaning/">Move-Out Cleaning</a>
                    <a className="contact-button text-sm hover:scale-105 transition-transform text-center py-2"
                      href="/mobile-al/carpet-cleaning/">Carpet Cleaning</a>
                    <a className="contact-button text-sm hover:scale-105 transition-transform text-center py-2"
                      href="/mobile-al/window-cleaning/">Window Cleaning</a>
                    <a className="contact-button text-sm hover:scale-105 transition-transform text-center py-2"
                      href="/mobile-al/pressure-washing/">Pressure Washing</a>
                    <a className="contact-button text-sm hover:scale-105 transition-transform text-center py-2"
                      href="/mobile-al/luxury-estate-cleaning/">Luxury Estate Cleaning</a>
                    <a className="contact-button text-sm hover:scale-105 transition-transform text-center py-2"
                      href="/mobile-al/laundry-services/">Laundry Services</a>
                    <a className="contact-button text-sm hover:scale-105 transition-transform text-center py-2"
                      href="/mobile-al/Detailing-{city}-AL/">Detailing</a>
                  </div>

                  <div
                    className="flex flex-col space-y-2 bg-white/95 p-4 rounded-xl shadow-2xl backdrop-blur-md border border-gray-200">
                    <h4 className="text-xl font-bold text-gray-900 border-b-2 border-purple-500 pb-2 mb-2 text-center">
                      Commercial & Industrial</h4>
                    <a className="contact-button text-sm hover:scale-105 transition-transform text-center py-2"
                      href="/mobile-al/commercial-cleaning/">Commercial Cleaning</a>
                    <a className="contact-button text-sm hover:scale-105 transition-transform text-center py-2"
                      href="/mobile-al/office-janitorial-services/">Office Janitorial Services</a>
                    <a className="contact-button text-sm hover:scale-105 transition-transform text-center py-2"
                      href="/mobile-al/janitorial-cleaning-services/">Janitorial Cleaning Services</a>
                    <a className="contact-button text-sm hover:scale-105 transition-transform text-center py-2"
                      href="/mobile-al/medical-dental-facility-cleaning/">Medical Facility Cleaning</a>
                    <a className="contact-button text-sm hover:scale-105 transition-transform text-center py-2"
                      href="/mobile-al/industrial-warehouse-cleaning/">Industrial & Warehouse Cleaning</a>
                    <a className="contact-button text-sm hover:scale-105 transition-transform text-center py-2"
                      href="/mobile-al/floor-stripping-waxing/">Floor Stripping & Waxing</a>
                    <a className="contact-button text-sm hover:scale-105 transition-transform text-center py-2"
                      href="/mobile-al/gym-fitness-center-cleaning/">Gym & Fitness Center Cleaning</a>
                    <a className="contact-button text-sm hover:scale-105 transition-transform text-center py-2"
                      href="/mobile-al/school-daycare-cleaning/">School & Daycare Cleaning</a>
                    <a className="contact-button text-sm hover:scale-105 transition-transform text-center py-2"
                      href="/mobile-al/church-worship-center-cleaning/">Church & Worship Cleaning</a>
                    <a className="contact-button text-sm hover:scale-105 transition-transform text-center py-2"
                      href="/mobile-al/solar-panel-cleaning/">Solar Panel Cleaning</a>
                  </div>

                  <div
                    className="flex flex-col space-y-2 bg-white/95 p-4 rounded-xl shadow-2xl backdrop-blur-md border border-gray-200">
                    <h4 className="text-xl font-bold text-gray-900 border-b-2 border-pink-500 pb-2 mb-2 text-center">
                      Property Management</h4>
                    <a className="contact-button text-sm hover:scale-105 transition-transform text-center py-2"
                      href="/mobile-al/vacation-rental-cleaning/">Vacation Rental Cleaning</a>
                    <a className="contact-button text-sm hover:scale-105 transition-transform text-center py-2"
                      href="/mobile-al/airbnb-cleaning/">Airbnb Cleaning</a>
                    <a className="contact-button text-sm hover:scale-105 transition-transform text-center py-2"
                      href="/mobile-al/airbnb-vacation-rental-management/">Airbnb & Rental Management</a>
                    <a className="contact-button text-sm hover:scale-105 transition-transform text-center py-2"
                      href="/mobile-al/post-construction-cleanup/">Post-Construction Cleanup</a>
                    <a className="contact-button text-sm hover:scale-105 transition-transform text-center py-2"
                      href="/mobile-al/property-management-janitorial/">Property Management Janitorial</a>
                    <a className="contact-button text-sm hover:scale-105 transition-transform text-center py-2"
                      href="/mobile-al/property-maintenance/">Property Maintenance</a>
                    <a className="contact-button text-sm hover:scale-105 transition-transform text-center py-2"
                      href="/mobile-al/home-watch-services/">Home Watch Services</a>
                    <a className="contact-button text-sm hover:scale-105 transition-transform text-center py-2"
                      href="/mobile-al/luxury-estate-management/">Luxury Estate Management</a>
                    <a className="contact-button text-sm hover:scale-105 transition-transform text-center py-2"
                      href="/mobile-al/gutter-cleaning/">Gutter Cleaning</a>
                  </div>
                </div>
              </div>

              
              <div className="relative group inline-block ml-6">
                <button type="button" className="contact-button text-lg flex items-center">
                  Locations <i className="fas fa-chevron-down text-sm ml-2"></i>
                </button>
                <div className="absolute left-0 top-full hidden group-hover:flex flex-col w-56 z-50">
                    <a className="contact-button text-lg hover:bg-blue-700" href="/daphne-al/">Daphne</a>
                    <a className="contact-button text-lg hover:bg-blue-700" href="/fairhope-al/">Fairhope</a>
                    <a className="contact-button text-lg hover:bg-blue-700" href="/foley-al/">Foley</a>
                    <a className="contact-button text-lg hover:bg-blue-700" href="/gulf-shores-al/">Gulf Shores</a>
                    <a className="contact-button text-lg hover:bg-blue-700" href="/skyline-al/">Skyline</a>
                    <a className="contact-button text-lg hover:bg-blue-700" href="/stevenson-al/">Stevenson</a>
                    <a className="contact-button text-lg hover:bg-blue-700" href="/cherokee-al/">Cherokee</a>
                    <a className="contact-button text-lg hover:bg-blue-700" href="/altoona-al/">Altoona</a>
                    <a className="contact-button text-lg hover:bg-blue-700" href="/ohatchee-al/">Ohatchee</a>
                    <a className="contact-button text-lg hover:bg-blue-700" href="/elba-al/">Elba</a>
                    <a className="contact-button text-lg hover:bg-blue-700" href="/saraland-al/">Saraland</a>
                    <a className="contact-button text-lg hover:bg-blue-700" href="/gardendale-al/">Gardendale</a>
                    <a className="contact-button text-lg hover:bg-blue-700" href="/columbia-al/">Columbia</a>
                    <a className="contact-button text-lg hover:bg-blue-700" href="/pollard-al/">Pollard</a>
                    <a className="contact-button text-lg hover:bg-blue-700" href="/fort-payne-al/">Fort Payne</a>
                  </div>
              </div>

              <a href="/mobile-al/blog/" className="contact-button text-lg">Blog</a>
              <a href="/mobile-al/contact/" className="contact-button text-lg">Contact</a>
              <a href="#quote"
                className="contact-button text-lg bg-blue-600 text-white hover:bg-blue-700 px-4 py-2 rounded-full shadow-lg shadow-blue-500/30">Get
                a Quote</a>
            </div>
          </div>
        </div>
      </nav>

      
      <nav className="md:hidden w-full relative z-[999] bg-transparent">
        <div className="px-4 py-2 flex justify-between items-center bg-gradient-to-b from-black/50 to-transparent">
          
          <div className="flex items-center">
            <div className="flex-shrink-0 cursor-pointer" >
              <img src="https://i.ibb.co/gbzKPdnc/Chat-GPT-Image-Aug-31-2025-12-19-42-AM-Picsart-Background-Remover.png"
                alt="Zoiris Cleaning" className="h-24 w-auto drop-shadow-md" />
            </div>
          </div>

          
          <div className="flex items-center space-x-4 pr-2">
            <a href="tel:2519308621" className="text-white hover:text-pink-400 transition-colors duration-300 shadow-md">
              <i className="fas fa-phone-alt animate-pulse text-2xl"></i>
            </a>
            <button id="mobile-menu-toggle" 
              className="text-white hover:text-pink-400 focus:outline-none transition duration-300 drop-shadow-lg"
              aria-label="Open mobile menu" aria-expanded="false">
              <i className="fas fa-bars text-3xl"></i>
            </button>
          </div>
        </div>
      </nav>

      
      <div id="mobile-menu"
        className="hidden md:hidden fixed inset-0 bg-gradient-to-br from-gray-900 to-black w-full h-[100dvh] overflow-y-auto z-[99999] transition-opacity duration-300 opacity-0 flex flex-col">

        
        <div className="px-4 py-3 flex justify-between items-center border-b border-white/10 shrink-0">
          <div className="flex-shrink-0 cursor-pointer" >
            <img src="https://i.ibb.co/gbzKPdnc/Chat-GPT-Image-Aug-31-2025-12-19-42-AM-Picsart-Background-Remover.png"
              alt="Zoiris Cleaning" className="h-20 w-auto drop-shadow-md" />
          </div>
          <button 
            className="text-white hover:text-pink-400 transition-colors duration-300 p-2 mr-2">
            <i className="fas fa-times text-4xl drop-shadow-lg"></i>
          </button>
        </div>

        <div className="px-4 py-6 space-y-3 flex-grow pb-24">
          <a href="/"
            className="block px-4 py-4 text-xl font-medium text-white hover:text-blue-400 hover:bg-white/10 rounded-2xl transition duration-300 flex items-center group cursor-pointer">
            <div
              className="w-12 h-12 rounded-full bg-white/5 flex items-center justify-center group-hover:bg-blue-500/20 transition-colors">
              <i className="fas fa-home text-blue-400 group-hover:text-pink-400 text-xl transition-colors duration-300"></i>
            </div>
            <span className="ml-5 tracking-wide">Home</span>
          </a>

          <a href="/mobile-al/about/"
            className="block px-4 py-4 text-xl font-medium text-white hover:text-blue-400 hover:bg-white/10 rounded-2xl transition duration-300 flex items-center group cursor-pointer">
            <div
              className="w-12 h-12 rounded-full bg-white/5 flex items-center justify-center group-hover:bg-blue-500/20 transition-colors">
              <i
                className="fas fa-info-circle text-blue-400 group-hover:text-pink-400 text-xl transition-colors duration-300"></i>
            </div>
            <span className="ml-5 tracking-wide">About Us</span>
          </a>

          
          <div className="relative bg-white/5 rounded-2xl overflow-hidden">
            <button 
              className="w-full flex justify-between items-center px-4 py-4 text-xl font-medium text-white hover:text-blue-400 hover:bg-white/10 transition duration-300 group cursor-pointer">
              <div className="flex items-center">
                <div
                  className="w-12 h-12 rounded-full bg-white/5 flex items-center justify-center group-hover:bg-blue-500/20 transition-colors">
                  <i
                    className="fas fa-broom text-blue-400 group-hover:text-pink-400 text-xl transition-colors duration-300"></i>
                </div>
                <span className="ml-5 tracking-wide">Services</span>
              </div>
              <div className="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center">
                <i className="fas fa-chevron-down text-lg transition-transform duration-300 transform"></i>
              </div>
            </button>
            <div id="mobile-services-dropdown"
              className="hidden pl-8 pr-4 py-4 space-y-3 mt-1 bg-black/50 backdrop-blur-md rounded-b-2xl border-t border-white/5">
              <div className="flex flex-col">
                
                <div className="mb-2">
                  <h4 className="text-blue-400 font-bold text-sm uppercase tracking-wider mb-2 flex items-center">
                    <i className="fas fa-home mr-2 text-pink-400"></i> Residential
                  </h4>
                  <div className="space-y-2 pl-6 border-l-2 border-blue-500/20">
                    <a className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                      href="/mobile-al/house-cleaning/">House Cleaning</a>
                    <a className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                      href="/mobile-al/deep-cleaning/">Deep Cleaning</a>
                    <a className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                      href="/mobile-al/move-in-cleaning/">Move-In Cleaning</a>
                    <a className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                      href="/mobile-al/move-out-cleaning/">Move-Out Cleaning</a>
                    <a className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                      href="/mobile-al/carpet-cleaning/">Carpet Cleaning</a>
                    <a className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                      href="/mobile-al/window-cleaning/">Window Cleaning</a>
                    <a className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                      href="/mobile-al/pressure-washing/">Pressure Washing</a>
                    <a className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                      href="/mobile-al/luxury-estate-cleaning/">Luxury Estate Cleaning</a>
                    <a className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                      href="/mobile-al/laundry-services/">Laundry Services</a>
                    <a className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                      href="/mobile-al/Detailing-{city}-AL/">Detailing</a>
                  </div>
                </div>

                
                <div className="mb-2">
                  <h4 className="text-purple-400 font-bold text-sm uppercase tracking-wider mb-2 flex items-center">
                    <i className="fas fa-building mr-2 text-pink-400"></i> Commercial
                  </h4>
                  <div className="space-y-2 pl-6 border-l-2 border-purple-500/20">
                    <a className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                      href="/mobile-al/commercial-cleaning/">Commercial Cleaning</a>
                    <a className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                      href="/mobile-al/office-janitorial-services/">Office Janitorial</a>
                    <a className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                      href="/mobile-al/janitorial-cleaning-services/">Janitorial Cleaning</a>
                    <a className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                      href="/mobile-al/medical-dental-facility-cleaning/">Medical Facility</a>
                    <a className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                      href="/mobile-al/industrial-warehouse-cleaning/">Industrial & Warehouse</a>
                    <a className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                      href="/mobile-al/floor-stripping-waxing/">Floor Stripping & Waxing</a>
                    <a className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                      href="/mobile-al/gym-fitness-center-cleaning/">Gym & Fitness Cleaning</a>
                    <a className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                      href="/mobile-al/school-daycare-cleaning/">School & Daycare Cleaning</a>
                    <a className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                      href="/mobile-al/church-worship-center-cleaning/">Church Cleaning</a>
                    <a className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                      href="/mobile-al/solar-panel-cleaning/">Solar Panel Cleaning</a>
                  </div>
                </div>

                
                <div className="mb-2">
                  <h4 className="text-pink-400 font-bold text-sm uppercase tracking-wider mb-2 flex items-center">
                    <i className="fas fa-key mr-2 text-purple-400"></i> Property Mgmt
                  </h4>
                  <div className="space-y-2 pl-6 border-l-2 border-pink-500/20">
                    <a className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                      href="/mobile-al/vacation-rental-cleaning/">Vacation Rental Cleaning</a>
                    <a className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                      href="/mobile-al/airbnb-cleaning/">Airbnb Cleaning</a>
                    <a className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                      href="/mobile-al/airbnb-vacation-rental-management/">Airbnb Management</a>
                    <a className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                      href="/mobile-al/post-construction-cleanup/">Post-Construction Cleanup</a>
                    <a className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                      href="/mobile-al/property-management-janitorial/">Property Management Janitorial</a>
                    <a className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                      href="/mobile-al/property-maintenance/">Property Maintenance</a>
                    <a className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                      href="/mobile-al/home-watch-services/">Home Watch Services</a>
                    <a className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                      href="/mobile-al/luxury-estate-management/">Luxury Estate Management</a>
                    <a className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                      href="/mobile-al/gutter-cleaning/">Gutter Cleaning</a>
                  </div>
                </div>
              </div>
            </div>
          </div>

          
          <div className="relative bg-white/5 rounded-2xl overflow-hidden">
            <button 
              className="w-full flex justify-between items-center px-4 py-4 text-xl font-medium text-white hover:text-blue-400 hover:bg-white/10 transition duration-300 group cursor-pointer">
              <div className="flex items-center">
                <div
                  className="w-12 h-12 rounded-full bg-white/5 flex items-center justify-center group-hover:bg-blue-500/20 transition-colors">
                  <i
                    className="fas fa-map-marker-alt text-blue-400 group-hover:text-pink-400 text-xl transition-colors duration-300"></i>
                </div>
                <span className="ml-5 tracking-wide">Locations</span>
              </div>
              <div className="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center">
                <i className="fas fa-chevron-down text-lg transition-transform duration-300 transform"></i>
              </div>
            </button>
            <div id="mobile-locations-dropdown"
              className="hidden pl-16 pr-4 py-4 space-y-3 mt-1 bg-black/50 backdrop-blur-md rounded-b-2xl border-t border-white/5">
              <a className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                href="/spanish-fort-al/">Spanish Fort</a><a
                className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                href="/saraland-al/">Saraland</a><a
                className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                href="/daphne-al/">Daphne</a><a
                className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                href="/eight-mile-al/">Eight Mile</a><a
                className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                href="/satsuma-al/">Satsuma</a><a
                className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                href="/montrose-al/">Montrose</a><a
                className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                href="/theodore-al/">Theodore</a><a
                className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                href="/semmes-al/">Semmes</a><a
                className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                href="/creola-al/">Creola</a><a
                className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                href="/stapleton-al/">Stapleton</a><a
                className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                href="/fairhope-al/">Fairhope</a><a
                className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                href="/point-clear-al/">Point Clear</a><a
                className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                href="/loxley-al/">Loxley</a><a
                className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                href="/saint-elmo-al/">Saint Elmo</a><a
                className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                href="/irvington-al/">Irvington</a><a
                className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                href="/wilmer-al/">Wilmer</a><a
                className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                href="/bay-minette-al/">Bay Minette</a><a
                className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                href="/coden-al/">Coden</a><a
                className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                href="/chunchula-al/">Chunchula</a><a
                className="block py-2 text-gray-300 hover:text-white hover:translate-x-2 transition duration-300 text-sm"
                href="/silverhill-al/">Silverhill</a>
            </div>
          </div>

          <a href="/mobile-al/blog/"
            className="block px-4 py-4 text-xl font-medium text-white hover:text-blue-400 hover:bg-white/10 rounded-2xl transition duration-300 flex items-center group cursor-pointer">
            <div
              className="w-12 h-12 rounded-full bg-white/5 flex items-center justify-center group-hover:bg-blue-500/20 transition-colors">
              <i className="fas fa-blog text-blue-400 group-hover:text-pink-400 text-xl transition-colors duration-300"></i>
            </div>
            <span className="ml-5 tracking-wide">Blog</span>
          </a>

          <a href="/mobile-al/contact/"
            className="block px-4 py-4 text-xl font-medium text-white hover:text-blue-400 hover:bg-white/10 rounded-2xl transition duration-300 flex items-center group cursor-pointer">
            <div
              className="w-12 h-12 rounded-full bg-white/5 flex items-center justify-center group-hover:bg-blue-500/20 transition-colors">
              <i
                className="fas fa-envelope text-blue-400 group-hover:text-pink-400 text-xl transition-colors duration-300"></i>
            </div>
            <span className="ml-5 tracking-wide">Contact</span>
          </a>

          <div className="pt-6 mt-4">
            <a href="#quote"
              className="w-full flex items-center justify-center space-x-3 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white font-bold py-5 px-6 rounded-2xl shadow-[0_10px_25px_rgba(59,130,246,0.5)] transition duration-300 transform hover:-translate-y-1 cursor-pointer">
              <i className="fas fa-file-invoice-dollar text-2xl group-hover:animate-bounce"></i>
              <span className="text-xl">Get a Free Quote</span>
            </a>
          </div>

          
          <div className="h-10"></div>
        </div>
      </div>

      
    </header>

    
    <div className="contact-button text-lg">
      <div className="max-w-6xl mx-auto px-4 py-2 flex flex-col md:flex-row justify-between items-center">

        
        <div className="flex flex-col md:flex-row md:space-x-6 text-center md:text-left">
          <a href="tel:2519308621" className="flex items-center justify-center space-x-2 hover:underline">
            <i className="fas fa-phone-alt fa-beat"></i>
            <span>(251) 930-8621</span>
          </a>
          <a href="mailto:zoiriscleaningservices@gmail.com"
            className="flex items-center justify-center space-x-2 mt-1 md:mt-0 hover:underline break-all text-sm md:text-base">
            <i className="fas fa-envelope fa-beat"></i>
            <span>zoiriscleaningservices@gmail.com</span>
          </a>
        </div>

        
        <div className="flex space-x-2 mt-2 md:mt-0">
          <a href="#"
            className="w-8 h-8 flex items-center justify-center bg-white text-blue-500 rounded-full hover:bg-gray-200 transition">
            <i className="fab fa-facebook-f fa-beat"></i>
            <span className="sr-only">Follow us on Facebook</span>
          </a>
          <a href="https://www.instagram.com/zoiriscleaning"
            className="w-8 h-8 flex items-center justify-center bg-white text-blue-500 rounded-full hover:bg-gray-200 transition">
            <i className="fab fa-instagram fa-beat"></i>
            <span className="sr-only">Follow us on Instagram</span>
          </a>
          <a href="https://x.com/zoiriscleaning"
            className="w-8 h-8 flex items-center justify-center bg-white text-blue-500 rounded-full hover:bg-gray-200 transition">
            <i className="fab fa-twitter fa-beat"></i>
            <span className="sr-only">Follow us on X (Twitter)</span>
          </a>
          <a href="https://www.linkedin.com/in/zoiriscleaning-services-b5b0b2381/"
            className="w-8 h-8 flex items-center justify-center bg-white text-blue-500 rounded-full hover:bg-gray-200 transition">
            <i className="fab fa-linkedin-in fa-beat"></i>
            <span className="sr-only">Connect with us on LinkedIn</span>
          </a>
          <a href="https://www.yelp.com/user_details?userid=7SDy8Urgj43gfYxrR5o2eQ"
            className="w-8 h-8 flex items-center justify-center bg-white text-blue-500 rounded-full hover:bg-gray-200 transition">
            <i className="fab fa-yelp fa-beat"></i>
            <span className="sr-only">Read our reviews on Yelp</span>
          </a>
          <a href="https://www.youtube.com/channel/UCTewa53AZduD2H9J04RogCw"
            className="w-8 h-8 flex items-center justify-center bg-white text-blue-500 rounded-full hover:bg-gray-200 transition">
            <i className="fab fa-youtube fa-beat"></i>
            <span className="sr-only">Subscribe to our YouTube channel</span>
          </a>
          <a href="https://www.pinterest.com/zoiriolysh/_profile/"
            className="w-8 h-8 flex items-center justify-center bg-white text-blue-500 rounded-full hover:bg-gray-200 transition">
            <i className="fab fa-pinterest-p fa-beat"></i>
            <span className="sr-only">Follow us on Pinterest</span>
          </a>
        </div>
      </div>
    </div>


    










    


    
    <div className="container mx-auto px-6 py-4 flex justify-between items-center">
      

      
      <div className="flex items-center">
        <button
          className="bg-gray-900 text-white px-4 py-2 rounded-lg font-semibold hover:bg-gray-700 contact-button text-lg transition"
          >
          <i className="fa-solid fa-location-dot fa-fade"></i>
          Service Area Finder
        </button>
      </div>
    </div>

    
    <div className="fixed inset-0 bg-black bg-opacity-50 hidden flex items-center justify-center z-50" id="finderModal">
      <div className="contact-button text-lg rounded-2xl shadow-xl w-full max-w-lg p-8 text-center relative"
        >
        
        <button className="absolute top-3 right-3 text-gray-900 hover:text-black text-4xl font-bold transition"
          >
          ×
        </button>
        <h2 className="text-3xl font-extrabold text-black mb-4">
          Service Availability in {city}, {state}
        </h2>
        <p className="text-black mb-6 leading-relaxed">
          Enter your details below to check if <strong>ZOIRIS Cleaning</strong> serves your area.
        </p>
        
        <form className="space-y-3" id="finderForm">
          <div className="flex space-x-2">
            <input
              className="flex-1 border p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-black placeholder-gray-400"
              name="name" placeholder="Enter Name" required type="text" />
          </div>
          <div className="flex space-x-2">
            <input
              className="flex-1 border p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-black placeholder-gray-400"
              name="phone" placeholder="Enter Phone" required type="tel" />
          </div>
          <div className="flex space-x-2">
            <input
              className="flex-1 border p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-black placeholder-gray-400"
              id="zipInput" maxLength={5} name="zipcode" placeholder="Enter ZIP Code" required type="text" />
          </div>
          <button
            className="bg-neutral-950 text-white px-6 rounded-lg font-semibold hover:bg-neutral-900 contact-button text-lg"
            type="submit">
            Check
          </button>
        </form>
        
        <div className="hidden" id="confirmationSection">
          <p className="mt-6 text-lg font-semibold" id="result"></p>
          <div className="mt-6" id="mapContainer">
            <iframe allowFullScreen height="300" id="map" loading="lazy"
              ></iframe>
          </div>

        </div>
      </div>
    </div>
    
    
    <section className="hero-image min-h-screen pt-24 pb-12 flex items-center justify-center relative" id="home">
      
      <div className="absolute inset-0 bg-black bg-opacity-30"></div>
      <div className="relative text-center px-4 sm:px-6 lg:px-8 max-w-3xl">
        <h1 className="text-3xl md:text-4xl font-extrabold text-white leading-tight mb-4 animate-fadeIn">
          #1 Cleaning Services in {city}, {state}
        </h1>

        <p className="text-base md:text-lg text-white font-medium max-w-md mx-auto mb-6 leading-relaxed">
          <strong>Zoiris Cleaning Service</strong> provides trusted
          <em>residential & commercial cleaning</em> across
          <strong>{city}, Baldwin County, and nearby cities</strong>.
          From deep cleans to move-in/out and eco-friendly solutions, we make your home or business spotless.
          <span className="font-semibold text-blue-400">Book online 24/7</span>.
        </p>

        <div className="flex flex-col sm:flex-row justify-center gap-4">
          <a href="tel:2519308621" className="contact-button text-lg">
            <i className="fas fa-phone mr-2 fa-beat"></i>Call Now
          </a>

          <a href="mailto:zoiriscleaningservices@gmail.com" className="contact-button text-lg">
            <i className="fas fa-envelope mr-2 fa-beat"></i>Email Us
          </a>
          <a href="#quote" className="contact-button text-lg">
            <i className="fa-solid fa-circle-check fa-beat"></i>
            Get a Free Quote
          </a>

          

        </div>
        
        <div className="flex justify-center mt-6">
          <button 
            className="animate-bounce text-black hover:text-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2 focus:ring-offset-transparent"
            aria-label="Scroll down to get a quote">

            
            <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10" fill="none" viewBox="0 0 24 24"
              stroke="currentColor" strokeWidth="2" aria-hidden="true">
              <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
            </svg>

            
            <span className="sr-only">Scroll to quote section</span>
          </button>
        </div>

        



        
        <div >
          <div
            >

            
            <div >
              <span
                >Free
                &amp; No Commitment</span>
            </div>

            
            <h3 >
              Let Us Call <span
                >You</span>
            </h3>
            <p >Drop your info
              below and we'll reach out within minutes!</p>

            

            <form id="heroCallForm" autoComplete="off">

              
              <div >
                <div className="hf-wrap">
                  <span className="hf-ico"><i className="fas fa-user"></i></span>
                  <input className="hf-input" type="text" name="first_name" placeholder="First Name" required />
                </div>
                <div className="hf-wrap">
                  <span className="hf-ico"><i className="fas fa-user"></i></span>
                  <input className="hf-input" type="text" name="last_name" placeholder="Last Name" required />
                </div>
              </div>

              
              <div >
                <div className="hf-wrap">
                  <span className="hf-ico"><i className="fas fa-phone-alt"></i></span>
                  <input className="hf-input" type="tel" name="phone" placeholder="Phone Number" required pattern="[0-9+()\-\s]{7,20}" title="Please enter a valid phone number (digits only)" />
                </div>
                <div className="hf-wrap">
                  <span className="hf-ico"><i className="fas fa-envelope"></i></span>
                  <input className="hf-input" type="email" name="email" placeholder="Email Address" required />
                </div>
              </div>

              
              <div >
                <div className="hf-wrap">
                  <span className="hf-ico"><i className="fas fa-map"></i></span>
                  <input className="hf-input" type="text" name="state" placeholder="State" />
                </div>
                <div className="hf-wrap">
                  <span className="hf-ico"><i className="fas fa-city"></i></span>
                  <input className="hf-input" type="text" name="city" placeholder="City" />
                </div>
              </div>

              
              <div >
                <label >
                  <input type="checkbox" name="consent_nonmarketing"
                     />
                  <span >By checking this box, I
                    consent to receive <strong >non-marketing text messages</strong> from <strong
                      >Zoiris Cleaning Services</strong> regarding <strong
                      >appointment updates, scheduling confirmations, service notifications, and
                      account-related information</strong>. Message frequency may vary. Message and data rates may
                    apply. Text <strong >HELP</strong> for assistance or <strong
                      >STOP</strong> to opt out at any time.</span>
                </label>
                <label >
                  <input type="checkbox" name="consent_marketing"
                     />
                  <span >By checking this box, I
                    consent to receive <strong >marketing and promotional text messages</strong>,
                    including special offers, discounts, service updates, and promotional notifications from <strong
                      >Zoiris Cleaning Services</strong> at the phone number provided. Message
                    frequency may vary. Message and data rates may apply. Text <strong >HELP</strong>
                    for assistance or reply <strong >STOP</strong> to opt out at any time.</span>
                </label>
              </div>


              
              <button type="submit" className="hf-btn" id="heroCallBtn">
                <i className="fas fa-phone-alt" ></i> Call Me &mdash; I'm Ready!
              </button>

            </form>

            
            <div id="heroCallSuccess"
              >
              <div >🎉</div>
              <p >Thank You — We'll Be Right With
                You!</p>
              <p >Your request
                has been received. A member of our team will call you within <strong >15
                  minutes</strong> during business hours.</p>
              <p >Zoiris Cleaning Services &bull; (251)
                930-8621</p>
            </div>
            
            <div id="heroCallError"
              >
              <i className="fas fa-exclamation-circle" ></i> Something went wrong. Call <a
                href="tel:2519308621" >(251) 930-8621</a>.
            </div>

            

          </div>
        </div>
        

      </div>
    </section>

    
    <section className="px-6 py-12" id="about">
      <div className="max-w-4xl mx-auto text-center mb-12">
        <h2 className="text-3xl md:text-4xl font-extrabold text-gray-900 sm:text-4xl">
          About Zoiris Cleaning Service – {city} &amp; Baldwin County Experts
        </h2>
        <div className="mt-4 h-1 w-20 bg-blue-600 mx-auto rounded"></div>
        <p className="mt-4 text-gray-800 text-base md:text-lg leading-relaxed">
          <strong>Zoiris Cleaning Service</strong> is the trusted choice for
          <em>residential, commercial, and Airbnb cleaning in {city}, {state} and Baldwin County</em>.
          We specialize in <strong>house cleaning, apartment cleaning, office cleaning, deep cleaning, move-in/out
            services, post-construction cleaning, and eco-friendly solutions</strong> to ensure your home or business is
          spotless, hygienic, and welcoming.
        </p>
        <div className="flex flex-col md:flex-row items-center">
          
          <div className="md:w-1/2 mb-8 md:mb-0 md:pr-6">
            <img alt="Professional eco-friendly cleaning in {city} Alabama by Zoiris team"
              className="rounded-xl shadow-xl w-full h-auto"
              src="https://i.ibb.co/Z6C6FkKH/Chat-GPT-Image-Sep-1-2025-10-20-56-PM.png" />
          </div>
          
          <div className="md:w-1/2">
            <h3 className="text-2xl md:text-3xl font-bold text-gray-900 mb-4">Our Story</h3>
            <p className="text-gray-800 text-base md:text-lg mb-4 leading-relaxed">
              From a small family-run service to one of {city} and Baldwin County’s most trusted cleaning
              companies, our
              mission is simple: provide <strong>affordable, reliable, and high-quality cleaning</strong> that makes
              life easier for homes and businesses.
            </p>
            <h3 className="text-2xl md:text-3xl font-bold text-gray-900 mb-4">Why Choose Us</h3>
            <p className="text-gray-800 text-base md:text-lg mb-4 leading-relaxed">
              Our team uses <strong>eco-friendly, non-toxic products</strong> and <strong>advanced cleaning
                techniques</strong> to ensure a spotless finish every time. Whether it’s recurring residential
              service,
              move-in/move-out, or office cleaning, we guarantee consistent, professional results.
            </p>
            <h3 className="text-2xl md:text-3xl font-bold text-gray-900 mb-4">Our Core Values</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-8">
              <div className="flex items-start">
                <div className="flex-shrink-0 bg-blue-100 rounded-full p-3">
                  <i className="fas fa-hand-holding-heart text-blue-600 text-lg"></i>
                </div>
                <div className="ml-3">
                  <h4 className="text-base font-semibold text-gray-900">Honesty</h4>
                  <p className="mt-1 text-gray-800 text-sm">Clear communication and dependable results.</p>
                </div>
              </div>
              <div className="flex items-start">
                <div className="flex-shrink-0 bg-blue-100 rounded-full p-3">
                  <i className="fas fa-clock text-blue-600 text-lg"></i>
                </div>
                <div className="ml-3">
                  <h4 className="text-base font-semibold text-gray-900">Punctuality</h4>
                  <p className="mt-1 text-gray-800 text-sm">We respect your schedule and arrive on time.</p>
                </div>
              </div>
              <div className="flex items-start">
                <div className="flex-shrink-0 bg-blue-100 rounded-full p-3">
                  <i className="fas fa-leaf text-blue-600 text-lg"></i>
                </div>
                <div className="ml-3">
                  <h4 className="text-base font-semibold text-gray-900">Eco-Friendly</h4>
                  <p className="mt-1 text-gray-800 text-sm">Safe, non-toxic products for your home and the environment.</p>
                </div>
              </div>
              <div className="flex items-start">
                <div className="flex-shrink-0 bg-blue-100 rounded-full p-3">
                  <i className="fas fa-medal text-blue-600 text-lg"></i>
                </div>
                <div className="ml-3">
                  <h4 className="text-base font-semibold text-gray-900">Quality</h4>
                  <p className="mt-1 text-gray-800 text-sm">Attention to detail with consistent, top-tier results.</p>
                </div>
              </div>
            </div>
            <p className="text-gray-800 text-base md:text-lg leading-relaxed">
              At Zoiris, we value your time and your space. We deliver cleaning services that are safe, dependable, and
              personalized. With <strong>5-star reviews and loyal customers</strong>, we are a leading cleaning service
              in {city} and Baldwin County.
            </p>
          </div>
        </div>
      </div>
    </section>

    <section className="py-16 bg-lightGray" id="services">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl md:text-4xl font-bold text-center text-gray-900 mb-6">
          Professional Cleaning Services for Homes &amp; Businesses
        </h2>
        <p className="text-center text-gray-800 max-w-3xl mx-auto mb-12">
          Zoiris Cleaning Service delivers trusted <strong>residential and commercial cleaning</strong>
          solutions designed to keep your space spotless, sanitized, and stress-free.
          Our expert cleaners specialize in <strong>deep cleaning, move-in and move-out cleaning,
            vacation rental turnovers, and post-construction cleanup</strong>. Whether you need a one-time
          detail clean or recurring services, we make every home and business shine with unmatched quality.
        </p>
      </div>
    </section>
    
    <div className="swiper mySwiper">
      <div className="swiper-wrapper">
        
        <div className="swiper-slide">
          <div className="contact-button text-lg">
            <img alt="Commercial Cleaning" className="h-48 w-full object-cover"
              src="https://i.ibb.co/Xx556fXM/Office-Cleaning-Crew.jpg" />
            <div className="p-6">
              <div className="flex items-center justify-center mb-4">
                <i className="fa-solid fa-building text-xl"></i>
              </div>
              <h3 className="font-bold text-xl mb-2 text-center">Commercial Cleaning</h3>
              <p className="text-sm text-center mb-4">Professional cleaning for offices and businesses of all sizes.</p>
              <div className="text-center">
                <a className="contact-button text-lg" href="/mobile-al/commercial-cleaning/">Learn More About Commercial
                  Cleaning <i className="fa-solid fa-arrow-right"></i></a>
              </div>
            </div>
          </div>
        </div>
        
        <div className="swiper-slide">
          <div className="contact-button text-lg">
            <img alt="Deep Cleaning" className="h-48 w-full object-cover"
              src="https://i.ibb.co/mfTgZTC/Seasonal-Deep-Cleaning-Tips.png" />
            <div className="p-6">
              <div className="flex items-center justify-center mb-4">
                <i className="fa-solid fa-broom text-xl"></i>
              </div>
              <h3 className="font-bold text-xl mb-2 text-center">Deep Cleaning</h3>
              <p className="text-sm text-center mb-4">A top-to-bottom detailed clean to eliminate hidden grime.</p>
              <div className="text-center">
                <a className="contact-button text-lg" href="/mobile-al/deep-cleaning/">Learn More About Deep Cleaning <i
                    className="fa-solid fa-arrow-right"></i></a>
              </div>
            </div>
          </div>
        </div>
        
        <div className="swiper-slide">
          <div className="contact-button text-lg">
            <img alt="Home Cleaning" className="h-48 w-full object-cover"
              src="https://i.ibb.co/xVwj2hV/Home-Cleaning-Service-in-Action.png" />
            <div className="p-6">
              <div className="flex items-center justify-center mb-4">
                <i className="fa-solid fa-house-chimney text-xl"></i>
              </div>
              <h3 className="font-bold text-xl mb-2 text-center">Home Cleaning</h3>
              <p className="text-sm text-center mb-4">Flexible residential cleaning for apartments, condos, and houses.</p>
              <div className="text-center">
                <a className="contact-button text-lg" href="/mobile-al/house-cleaning/">Learn More About Home Cleaning <i
                    className="fa-solid fa-arrow-right"></i></a>
              </div>
            </div>
          </div>
        </div>
        
        <div className="swiper-slide">
          <div className="contact-button text-lg">
            <img alt="Move-In Cleaning" className="h-48 w-full object-cover"
              src="https://i.ibb.co/pBhLCp0m/Cleaning-Movers-MH-1.jpg" />
            <div className="p-6">
              <div className="flex items-center justify-center mb-4">
                <i className="fa-solid fa-key text-xl"></i>
              </div>
              <h3 className="font-bold text-xl mb-2 text-center">Move-In Cleaning</h3>
              <p className="text-sm text-center mb-4">Fresh, sanitized, and move-in ready from day one.</p>
              <div className="text-center">
                <a className="contact-button text-lg" href="/mobile-al/move-in-cleaning/">Learn More About Move-In Cleaning
                  <i className="fa-solid fa-arrow-right"></i></a>
              </div>
            </div>
          </div>
        </div>
        
        <div className="swiper-slide">
          <div className="contact-button text-lg">
            <img alt="Move-Out Cleaning" className="h-48 w-full object-cover"
              src="https://i.ibb.co/fzSDxHXB/64119f3c30e4db48a06316e0-Move-out-cleaning-min.jpg" />
            <div className="p-6">
              <div className="flex items-center justify-center mb-4">
                <i className="fa-solid fa-truck text-xl"></i>
              </div>
              <h3 className="font-bold text-xl mb-2 text-center">Move-Out Cleaning</h3>
              <p className="text-sm text-center mb-4">Leave your old space spotless and ready for inspection.</p>
              <div className="text-center">
                <a className="contact-button text-lg" href="/mobile-al/move-out-cleaning/">Learn More About Move-Out
                  Cleaning
                  <i className="fa-solid fa-arrow-right"></i></a>
              </div>
            </div>
          </div>
        </div>
        
        <div className="swiper-slide">
          <div className="contact-button text-lg">
            <img alt="Vacation Rental Cleaning" className="h-48 w-full object-cover"
              src="https://i.ibb.co/MDq72Z6T/Vacation-Rental-Cleaning-Contract-1-scaled-e1636734588512.jpg" />
            <div className="p-6">
              <div className="flex items-center justify-center mb-4">
                <i className="fa-solid fa-umbrella-beach text-xl"></i>
              </div>
              <h3 className="font-bold text-xl mb-2 text-center">Vacation Rental Cleaning</h3>
              <p className="text-sm text-center mb-4">Keep your rental property spotless and guest-ready every time.</p>
              <div className="text-center">
                <a className="contact-button text-lg" href="/mobile-al/vacation-rental-cleaning/">Learn More About Vacation
                  Rental
                  Cleaning <i className="fa-solid fa-arrow-right"></i></a>
              </div>
            </div>
          </div>
        </div>
        
        <div className="swiper-slide">
          <div className="contact-button text-lg">
            <img alt="Airbnb Cleaning" className="h-48 w-full object-cover"
              src="https://i.ibb.co/cXbxNC7y/airbnb-pixabay-e1584981299557-1.webp" />
            <div className="p-6">
              <div className="flex items-center justify-center mb-4">
                <i className="fa-brands fa-airbnb text-xl"></i>
              </div>
              <h3 className="font-bold text-xl mb-2 text-center">Airbnb Cleaning</h3>
              <p className="text-sm text-center mb-4">Quick turnaround cleaning for Airbnb hosts to keep 5-star ratings.</p>
              <div className="text-center">
                <a className="contact-button text-lg" href="/mobile-al/airbnb-cleaning/">Learn More About Airbnb Cleaning <i
                    className="fa-solid fa-arrow-right"></i></a>
              </div>
            </div>
          </div>
        </div>
        
        <div className="swiper-slide">
          <div className="contact-button text-lg">
            <img alt="Post-Construction Cleaning" className="h-48 w-full object-cover"
              src="https://i.ibb.co/kgbB5kPD/Captura-de-Tela-2020-07-06-a-s-15-13-39-1-e1599762634567.png" />
            <div className="p-6">
              <div className="flex items-center justify-center mb-4">
                <i className="fa-solid fa-hammer text-xl"></i>
              </div>
              <h3 className="font-bold text-xl mb-2 text-center">Post-Construction Cleaning</h3>
              <p className="text-sm text-center mb-4">Remove dust, debris, and construction mess for a polished look.</p>
              <div className="text-center">
                <a className="contact-button text-lg" href="/mobile-al/post-construction-cleanup/">Learn More About
                  Post-Construction
                  Cleaning <i className="fa-solid fa-arrow-right"></i></a>
              </div>
            </div>
          </div>
        </div>
        
        <div className="swiper-slide">
          <div className="contact-button text-lg">
            <img alt="Carpet Cleaning" className="h-48 w-full object-cover"
              src="https://i.ibb.co/4nn05G5j/carpetcleaning-UT-768x406.jpg" />
            <div className="p-6">
              <div className="flex items-center justify-center mb-4">
                <i className="fa-solid fa-rug text-xl"></i>
              </div>
              <h3 className="font-bold text-xl mb-2 text-center">Carpet Cleaning</h3>
              <p className="text-sm text-center mb-4">Deep carpet cleaning that removes dirt, stains, and allergens.</p>
              <div className="text-center">
                <a className="contact-button text-lg" href="/mobile-al/carpet-cleaning/">Learn More About Carpet Cleaning <i
                    className="fa-solid fa-arrow-right"></i></a>
              </div>
            </div>
          </div>
        </div>
        
        <div className="swiper-slide">
          <div className="contact-button text-lg">
            <img alt="Pressure Washing" className="h-48 w-full object-cover"
              src="https://i.ibb.co/5gDXrjxs/Hotsy-Pressure-Washer-PSI-vs-GPM.jpg" />
            <div className="p-6">
              <div className="flex items-center justify-center mb-4">
                <i className="fa-solid fa-water text-xl"></i>
              </div>
              <h3 className="font-bold text-xl mb-2 text-center">Pressure Washing</h3>
              <p className="text-sm text-center mb-4">Restore driveways, decks, and exteriors with powerful washing.</p>
              <div className="text-center">
                <a className="contact-button text-lg" href="/mobile-al/pressure-washing/">Learn More About Pressure Washing
                  <i className="fa-solid fa-arrow-right"></i></a>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div className="swiper-button-next text-blue-600"></div>
      <div className="swiper-button-prev text-blue-600"></div>
      
      <div className="swiper-pagination"></div>
    </div>
    
    
    
    
    <section id="quote" className="relative py-20 overflow-hidden scroll-mt-28"
      >

      
      <div
        >
      </div>

      
      <div
        >
      </div>
      <div
        >
      </div>

      

      <div className="container mx-auto px-4 max-w-6xl relative z-10">

        
        <div className="text-center mb-14">
          <p
            >
            ✦ Contact Us ✦</p>
          <h2 >
            Get Your <span className="zcs-badge">Free Quote</span> Today
          </h2>
          <p >Tell us about your
            space and we'll reach out within minutes.</p>
          <div
            >
          </div>
        </div>

        <div className="grid lg:grid-cols-5 gap-10 items-start">

          
          <div className="lg:col-span-3">
            <div
              >
              <form id="contactForm" autoComplete="off" >

                
                <div >
                  <div className="zcs-field">
                    <input className="zcs-input" type="text" name="first_name" placeholder="First Name" required />
                    <span className="zcs-label">First Name</span>
                    <span className="zcs-icon"><i className="fas fa-user"></i></span>
                  </div>
                  <div className="zcs-field">
                    <input className="zcs-input" type="text" name="last_name" placeholder="Last Name" required />
                    <span className="zcs-label">Last Name</span>
                    <span className="zcs-icon"><i className="fas fa-user-tag"></i></span>
                  </div>
                </div>

                
                <div >
                  <div className="zcs-field">
                    <input className="zcs-input" type="tel" name="phone" placeholder="Phone" required pattern="[0-9+()\-\s]{7,20}" title="Please enter a valid phone number (digits only)" />
                    <span className="zcs-label">Phone Number</span>
                    <span className="zcs-icon"><i className="fas fa-phone-alt"></i></span>
                  </div>
                  <div className="zcs-field">
                    <input className="zcs-input" type="email" name="email" placeholder="Email" required />
                    <span className="zcs-label">Email Address</span>
                    <span className="zcs-icon"><i className="fas fa-envelope"></i></span>
                  </div>
                </div>

                
                <div className="zcs-field">
                  <input className="zcs-input" type="text" name="address" placeholder="Address" />
                  <span className="zcs-label">Street Address</span>
                  <span className="zcs-icon"><i className="fas fa-map-marker-alt"></i></span>
                </div>

                
                <div >
                  <div className="zcs-field">
                    <input className="zcs-input" type="text" name="state" placeholder="State" />
                    <span className="zcs-label">State</span>
                    <span className="zcs-icon"><i className="fas fa-map"></i></span>
                  </div>
                  <div className="zcs-field">
                    <input className="zcs-input" type="text" name="city" placeholder="City" />
                    <span className="zcs-label">City</span>
                    <span className="zcs-icon"><i className="fas fa-city"></i></span>
                  </div>
                </div>

                
                <div className="zcs-field">
                  <span className="zcs-icon"><i className="fas fa-broom"></i></span>
                  <select className="zcs-input" id="zcs_service" name="service_type" required
                    >
                    <option value="" disabled></option>
                    <option value="Residential Cleaning">🏠 Residential Cleaning</option>
                    <option value="Commercial Cleaning">🏢 Commercial Cleaning</option>
                    <option value="Deep Cleaning">🧹 Deep Cleaning</option>
                    <option value="Move In / Out">📦 Move In / Out Cleaning</option>
                    <option value="Airbnb Cleaning">🛎️ Airbnb Cleaning</option>
                    <option value="Post-Construction">🏗️ Post-Construction Cleanup</option>
                    <option value="Office Cleaning">💼 Office Cleaning</option>
                    <option value="Other">✨ Other</option>
                  </select>
                  <span className="zcs-label" id="zcs_service_lbl">Type of Service Needed</span>
                </div>

                
                <div className="zcs-field">
                  <textarea className="zcs-input" name="message" rows={3} placeholder="Message"></textarea>
                  <span className="zcs-label" >Message or Special Requests</span>
                  <span className="zcs-icon" ><i className="fas fa-comment-alt"></i></span>
                </div>

                
                <div
                  >
                  <label >
                    <input type="checkbox" name="consent_nonmarketing"
                       />
                    <span >I consent to receive
                      <strong >non-marketing messages</strong> from <strong
                        >Zoiris Cleaning Services</strong> (appointment updates, scheduling, service
                      notifications). Text <strong >STOP</strong> to opt out.</span>
                  </label>
                  <label >
                    <input type="checkbox" name="consent_marketing"
                       />
                    <span >I consent to receive
                      <strong >marketing &amp; promotional messages</strong> including offers &amp;
                      discounts. Reply <strong >STOP</strong> anytime.</span>
                  </label>
                </div>

                
                <button type="submit" className="zcs-btn" id="zcsSubmitBtn">
                  <i className="fas fa-paper-plane" ></i> Send &amp; Get My Free Quote
                </button>

              </form>

              
              <div id="formSuccess"
                >
                <div >✅</div>
                <p >Thank You for Reaching Out!
                </p>
                <p >We have
                  received your request and one of our professional cleaning specialists will contact you within <strong
                    >15 minutes</strong> during business hours.</p>
                <p >Zoiris Cleaning Services &bull; (251)
                  930-8621 &bull; {city}, {state}</p>
              </div>
              <div id="formError"
                >
                <i className="fas fa-exclamation-circle" ></i> Something went wrong. Call us at
                (251) 930-8621.
              </div>

            </div>
          </div>

          
          <div className="lg:col-span-2" >

            
            <div className="zcs-glass">
              <p
                >
                Direct Contact</p>
              <h3 >Reach Us Anytime</h3>
              <div >

                <a href="tel:2519308621" >
                  <div className="zcs-info-pill"
                    >
                    <i className="fas fa-phone-alt" ></i>
                  </div>
                  <div>
                    <p
                      >
                      Phone</p>
                    <p >(251) 930-8621</p>
                  </div>
                </a>

                <a href="mailto:zoiriscleaningservices@gmail.com"
                  >
                  <div className="zcs-info-pill"
                    >
                    <i className="fas fa-envelope" ></i>
                  </div>
                  <div >
                    <p
                      >
                      Email</p>
                    <p >
                      zoiriscleaningservices@gmail.com</p>
                  </div>
                </a>

                <div >
                  <div className="zcs-info-pill"
                    >
                    <i className="fas fa-clock" ></i>
                  </div>
                  <div>
                    <p
                      >
                      Hours</p>
                    <p >24/7 Emergency Service</p>
                  </div>
                </div>

              </div>
            </div>

            
            <div
              >
              <div
                >
              </div>
              <div
                >
              </div>
              <div >
                <div >
                  <div
                    >
                    <i className="fab fa-whatsapp" ></i>
                  </div>
                  <h3 >Quick WhatsApp</h3>
                </div>
                <p >Get an
                  instant response — we typically reply in under 2 minutes!</p>
                <a href="https://wa.me/12519308621" target="_blank"
                  
                  
                  >
                  <i className="fab fa-whatsapp" ></i> Chat Now on WhatsApp
                </a>
              </div>
            </div>

            
            <div className="zcs-glass" >
              <div >⚡</div>
              <p >Lightning Fast Response</p>
              <p >We call back within <strong
                  >15 minutes</strong> during business hours.</p>
            </div>

          </div>
        </div>
      </div>

      

    </section>
    
    

    
    <section className="py-16 bg-gray-5" id="services-preview">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-7xl mx-auto">
          
          <a className="contact-button text-lg" href="/mobile-al/commercial-cleaning/">
            <div className="flex items-center gap-3">
              <div className="contact-button text-lg">
                <i className="fa-solid fa-building text-xl"></i>
              </div>
              <h3 className="contact-button text-lg">Commercial Cleaning</h3>
            </div>
          </a>
          
          <a className="contact-button text-lg" href="/mobile-al/deep-cleaning/">
            <div className="flex items-center gap-3">
              <div className="contact-button text-lg">
                <i className="fa-solid fa-soap text-xl"></i>
              </div>
              <h3 className="contact-button text-lg">Deep Cleaning</h3>
            </div>
          </a>
          
          <a className="contact-button text-lg" href="/mobile-al/house-cleaning/">
            <div className="flex items-center gap-3">
              <div className="contact-button text-lg">
                <i className="fa-solid fa-broom text-xl"></i>
              </div>
              <h3 className="contact-button text-lg">House Cleaning</h3>
            </div>
          </a>
          
          <a className="contact-button text-lg" href="/mobile-al/move-in-cleaning/">
            <div className="flex items-center gap-3">
              <div className="contact-button text-lg">
                <i className="fa-solid fa-box-open text-xl"></i>
              </div>
              <h3 className="contact-button text-lg">Move-In Cleaning</h3>
            </div>
          </a>
          
          <a className="contact-button text-lg" href="/mobile-al/move-out-cleaning/">
            <div className="flex items-center gap-3">
              <div className="contact-button text-lg">
                <i className="fa-solid fa-truck-moving text-xl"></i>
              </div>
              <h3 className="contact-button text-lg">Move-Out Cleaning</h3>
            </div>
          </a>
          
          <a className="contact-button text-lg" href="/mobile-al/vacation-rental-cleaning/">
            <div className="flex items-center gap-3">
              <div className="contact-button text-lg">
                <i className="fa-solid fa-umbrella-beach text-xl"></i>
              </div>
              <h3 className="contact-button text-lg">Vacation Rental Cleaning</h3>
            </div>
          </a>
          
          <a className="contact-button text-lg" href="/mobile-al/airbnb-cleaning/">
            <div className="flex items-center gap-3">
              <div className="contact-button text-lg">
                <i className="fa-brands fa-airbnb text-xl"></i>
              </div>
              <h3 className="contact-button text-lg">Airbnb Cleaning</h3>
            </div>
          </a>
          
          <a className="contact-button text-lg" href="/mobile-al/post-construction-cleanup/">
            <div className="flex items-center gap-3">
              <div className="contact-button text-lg">
                <i className="fa-solid fa-hard-hat text-xl"></i>
              </div>
              <h3 className="contact-button text-lg">Post-Construction Cleanup</h3>
            </div>
          </a>
          
          <a className="contact-button text-lg" href="/mobile-al/carpet-cleaning/">
            <div className="flex items-center gap-3">
              <div className="contact-button text-lg">
                <i className="fa-solid fa-rug text-xl"></i>
              </div>
              <h3 className="contact-button text-lg">Carpet Cleaning</h3>
            </div>
          </a>
          
          <a className="contact-button text-lg" href="/mobile-al/pressure-washing/">
            <div className="flex items-center gap-3">
              <div className="contact-button text-lg">
                <i className="fa-solid fa-water text-xl"></i>
              </div>
              <h3 className="contact-button text-lg">Pressure Washing</h3>
            </div>
          </a>
        </div>
      </div>
    </section>
    
    <section className="py-20" id="blog">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
            Expert Cleaning Tips, Hacks &amp; Professional Insights
          </h2>
          <div className="mt-4 h-1 w-24 bg-blue-600 mx-auto rounded"></div>
          <p className="mt-6 max-w-3xl mx-auto text-gray-800 text-lg leading-relaxed">
            Stay informed with practical cleaning advice, proven hacks, and
            <strong>professional insights from Zoiris Cleaning Service</strong>.
            Our articles cover everything from eco-friendly cleaning methods and home
            organization to <strong>commercial office cleaning strategies</strong> that
            keep businesses in <strong>{city}, {state} &amp; Baldwin County</strong> spotless,
            safe, and welcoming. Whether you’re a homeowner or a business owner,
            these resources will help you maintain a healthier and cleaner environment
            year-round.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          
          <div
            className="bg-white rounded-lg overflow-hidden shadow-md hover:shadow-xl hover:transform hover:-translate-y-1 transition duration-300">
            <img alt="Spring cleaning" className="w-full h-48 object-cover"
              src="https://images.unsplash.com/photo-1595476108010-b4d1f102b1b1?ixlib=rb-4.0.3&amp;ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&amp;auto=format&amp;fit=crop&amp;w=2070&amp;q=80" />
            <div className="p-6">
              <div className="flex items-center text-sm text-gray-500 mb-2">
                <span>March 15, 2023</span>
                <span className="mx-2">”¢</span>
                <span>5 min read</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">10 Spring Cleaning Tips for a Fresher Home</h3>
              <p className="text-gray-600 mb-4">
                Discover our top tips to make your spring cleaning more efficient and effective this year.
              </p>
              <a className="contact-button text-lg" href="/mobile-al/blog/">
                Read More: 10 Spring Cleaning Tips for a Fresher Home
                <i className="fas fa-arrow-right ml-2"></i>
              </a>
            </div>
          </div>
          
          <div className="bg-white rounded-lg overflow-hidden shadow-md">
            <img alt="Eco-friendly cleaning" className="w-full h-48 object-cover"
              src="https://images.unsplash.com/photo-1600880292203-757bb62b4baf?ixlib=rb-4.0.3&amp;ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&amp;auto=format&amp;fit=crop&amp;w=2070&amp;q=80" />
            <div className="p-6">
              <div className="flex items-center text-sm text-gray-500 mb-2">
                <span>February 28, 2023</span>
                <span className="mx-2">”¢</span>
                <span>4 min read</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">The Benefits of Eco-Friendly Cleaning Products</h3>
              <p className="text-gray-600 mb-4">
                Learn why switching to green cleaning products is better for your health and the environment.
              </p>
              <a className="contact-button text-lg" href="/mobile-al/blog/">
                Read More: The Benefits of Eco-Friendly Cleaning Products
                <i className="fas fa-arrow-right ml-2"></i>
              </a>
            </div>
          </div>
          
          <div className="bg-white rounded-lg overflow-hidden shadow-md">
            <img alt="Home organization" className="w-full h-48 object-cover"
              src="https://images.unsplash.com/photo-1600607688969-a5bfcd646154?ixlib=rb-4.0.3&amp;ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&amp;auto=format&amp;fit=crop&amp;w=2070&amp;q=80" />
            <div className="p-6">
              <div className="flex items-center text-sm text-gray-500 mb-2">
                <span>January 10, 2023</span>
                <span className="mx-2">”¢</span>
                <span>6 min read</span>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">Organizing Your Home: Where to Start</h3>
              <p className="text-gray-600 mb-4">
                Feeling overwhelmed by clutter? Follow our step-by-step guide to organize your home effectively.
              </p>
              <a className="contact-button text-lg" href="/mobile-al/blog/">
                Read More: Organizing Your Home: Where to Start
                <i className="fas fa-arrow-right ml-2"></i>
              </a>
            </div>
          </div>
        </div>
        <div className="mt-12 text-center">
          <a className="contact-button text-lg" href="/mobile-al/blog/">
            View All Articles
          </a>
        </div>
      </div>
    </section>
    
    <section className="py-20 bg-gray-5" id="location">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-extrabold text-black sm:text-4xl">
            Our Location &amp; Service Area
          </h2>
          <div className="mt-4 h-1 w-20 bg-blue-500 mx-auto"></div>
          <p className="mt-6 max-w-3xl mx-auto text-black text-lg leading-relaxed">
            <strong>Zoiris Cleaning Service</strong> is proudly headquartered in the heart of <em>Downtown {city},
              Alabama</em>.
            We serve both commercial and residential clients throughout {city} and Baldwin County, including busy office
            districts,
            retail spaces, schools, and medical facilities. Our central location allows us to respond quickly and
            efficiently to clients across the area,
            ensuring top-quality cleaning services whenever you need them —
            <span className="font-semibold text-black">day or night, 24/7</span>.
            Explore our coverage area below and click on any location to view it directly in Google Maps.
          </p>
        </div>
      </div>
    </section>
    <div className="grid lg:grid-cols-2 gap-12 items-start">
      
      <div>
        <h3 className="text-xl font-bold text-gray-900 mb-4">Service Areas We Cover</h3>
        <p className="text-gray-800 mb-6 leading-relaxed">
          At <strong>Zoiris Cleaning Service</strong>, we are proud to serve a wide range of communities across
          <em>{city}, {state} and Baldwin County</em>. Our dedicated team provides trusted, high-quality cleaning solutions
          for
          offices, businesses, and homes in every corner of the region. Whether you’re located in the busy heart
          of
          <strong>Downtown {city}</strong>, the growing neighborhoods of <strong>West {city}</strong>, or the vibrant
          towns
          along the <strong>Eastern Shore</strong>, our team is ready to keep your space spotless, healthy, and
          welcoming.
          We combine flexible scheduling, eco-friendly cleaning products, and years of hands-on experience to deliver
          results
          you can count on — no matter the size or type of property. Explore our full service area below and click
          on a
          location to view it directly on Google Maps.
        </p>
      </div>
      <ul className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 text-gray-700 text-sm md:text-base">
        <li><a className="contact-button w-full text-center hover:bg-blue-600" href="/downtown-mobile-al/"><i
              className="fas fa-map-marker-alt mr-1"></i> Downtown {city}</a></li>
        <li><a className="contact-button w-full text-center hover:bg-blue-600" href="/midtown-mobile-al/"><i
              className="fas fa-map-marker-alt mr-1"></i> Midtown {city}</a></li>
        <li><a className="contact-button w-full text-center hover:bg-blue-600" href="/west-mobile-al/"><i
              className="fas fa-map-marker-alt mr-1"></i> West {city}</a></li>
        <li><a className="contact-button w-full text-center hover:bg-blue-600" href="/saraland-al/"><i
              className="fas fa-map-marker-alt mr-1"></i> Saraland</a></li>
        <li><a className="contact-button w-full text-center hover:bg-blue-600" href="/semmes-al/"><i
              className="fas fa-map-marker-alt mr-1"></i> Semmes</a></li>
        <li><a className="contact-button w-full text-center hover:bg-blue-600" href="/theodore-al/"><i
              className="fas fa-map-marker-alt mr-1"></i> Theodore</a></li>
        <li><a className="contact-button w-full text-center hover:bg-blue-600" href="/satsuma-al/"><i
              className="fas fa-map-marker-alt mr-1"></i> Satsuma</a></li>
        <li><a className="contact-button w-full text-center hover:bg-blue-600" href="/grand-bay-al/"><i
              className="fas fa-map-marker-alt mr-1"></i> Grand Bay</a></li>
        <li><a className="contact-button w-full text-center hover:bg-blue-600" href="/daphne-al/"><i
              className="fas fa-map-marker-alt mr-1"></i> Daphne</a></li>
        <li><a className="contact-button w-full text-center hover:bg-blue-600" href="/fairhope-al/"><i
              className="fas fa-map-marker-alt mr-1"></i> Fairhope</a></li>
        <li><a className="contact-button w-full text-center hover:bg-blue-600" href="/spanish-fort-al/"><i
              className="fas fa-map-marker-alt mr-1"></i> Spanish Fort</a></li>
        <li><a className="contact-button w-full text-center hover:bg-blue-600" href="/eastern-shore-al/"><i
              className="fas fa-map-marker-alt mr-1"></i> Eastern Shore</a></li>
        <li><a className="contact-button w-full text-center hover:bg-blue-600" href="/gulf-shores-al/"><i
              className="fas fa-map-marker-alt mr-1"></i> Gulf Shores</a></li>
        <li><a className="contact-button w-full text-center hover:bg-blue-600" href="/orange-beach-al/"><i
              className="fas fa-map-marker-alt mr-1"></i> Orange Beach</a></li>
        <li><a className="contact-button w-full text-center hover:bg-blue-600" href="/foley-al/"><i
              className="fas fa-map-marker-alt mr-1"></i> Foley</a></li>
        <li><a className="contact-button w-full text-center hover:bg-blue-600" href="/fort-morgan-al/"><i
              className="fas fa-map-marker-alt mr-1"></i> Fort Morgan</a></li>
        <li><a className="contact-button w-full text-center hover:bg-blue-600" href="/robertsdale-al/"><i
              className="fas fa-map-marker-alt mr-1"></i> Robertsdale</a></li>
        <li><a className="contact-button w-full text-center hover:bg-blue-600" href="/bay-minette-al/"><i
              className="fas fa-map-marker-alt mr-1"></i> Bay Minette</a></li>
        <li><a className="contact-button w-full text-center hover:bg-blue-600" href="/loxley-al/"><i
              className="fas fa-map-marker-alt mr-1"></i> Loxley</a></li>
        <li><a className="contact-button w-full text-center hover:bg-blue-600" href="/elberta-al/"><i
              className="fas fa-map-marker-alt mr-1"></i> Elberta</a></li>
        <li><a className="contact-button w-full text-center hover:bg-blue-600" href="/summerdale-al/"><i
              className="fas fa-map-marker-alt mr-1"></i> Summerdale</a></li>
        <li><a className="contact-button w-full text-center hover:bg-blue-600" href="/dauphin-island-al/"><i
              className="fas fa-map-marker-alt mr-1"></i> Dauphin Island</a></li>
        <li><a className="contact-button w-full text-center hover:bg-blue-600" href="/maid-service-mobile-al-al/"><i
              className="fas fa-map-marker-alt mr-1"></i> {city} (All)</a></li>
      </ul>
    </div>
    
    <div>
      <div className="aspect-w-16 aspect-h-9 mb-6">
        
        <iframe allowFullScreen className="rounded-xl shadow-lg" height="350" loading="lazy"
          referrerPolicy="no-referrer-when-downgrade"
          src="https://www.google.com/maps/embed?pb=!4v1711234567890!6m8!1m7!1sCAoSLEFGMVFpcE1FdFZ2aEJzYUVuTFlQbU8wYzZtR2Vzclh2VE1MZnptZVVCN3Vt!2m2!1d30.694356!2d-88.043054!3f90!4f0!5f0.7820865974627469"
           title={`Zoiris Cleaning Service location map in ${city}, ${state}`}>
        </iframe>
        <div className="space-y-3 text-lg">
          
          <p className="flex items-center">
            <i className="fas fa-map-marker-alt text-blue-600 mr-2 fa-beat-fade"></i>
            <a className="text-black font-semibold contact-button text-lg"
              href="https://www.google.com/maps/dir/?api=1&amp;destination=123+Dauphin+St,+{city},+AL+36602"
              target="_blank">
              123 Dauphin St, {city}, {state} 36602
            </a>
          </p>
          
          <p className="flex items-center">
            <i className="fas fa-phone text-blue-600 mr-2 fa-beat-fade"></i>
            <a className="text-black font-bold contact-button text-lg" href="tel:+12519308621">
              (251) 930-8621
            </a>
          </p>
          
          <p className="flex items-center">
            <i className="fas fa-clock text-blue-600 mr-2 fa-beat-fade"></i>
            <a className="text-black font-semibold contact-button text-lg" href="tel:+12519308621">
              Available 24/7
            </a>
          </p>
        </div>
      </div>
    </div>


    
    <footer className="bg-gradient-to-b from-gray-900 to-black text-gray-200 py-16 relative overflow-hidden font-sans">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 lg:grid-cols-3 gap-12">
        
        <div className="space-y-6 relative z-10">
          <a className="flex items-center space-x-3 group" href="/">
            <img alt="Zoiris Cleaning Logo"
              className="h-28 w-auto transition-all duration-300 group-hover:scale-105 group-hover:shadow-[0_0_20px_rgba(37,99,235,0.3)] rounded-full"
              src="https://i.ibb.co/gbzKPdnc/Chat-GPT-Image-Aug-31-2025-12-19-42-AM-Picsart-Background-Remover.png" />
          </a>
          <p className="text-gray-400 text-sm leading-relaxed text-justify">
            Zoiris Cleaning is your trusted partner for professional cleaning services in {city}, {state}, and surrounding
            areas like Daphne, Fairhope, Midtown {city}, Downtown {city}, West {city}, Eastern Shore, and Spanish Fort.
            We specialize in residential and commercial cleaning, deep cleans, move-in/move-out services, carpet and
            window cleaning, Airbnb and vacation rentals, post-construction cleanup, and pressure washing.
          </p>
          
          <div className="space-y-3 pt-4">
            <p className="flex items-center text-gray-300 group">
              <i className="fas fa-map-marker-alt w-6 text-blue-500 group-hover:text-blue-400 transition-colors"></i>
              <span>{city}, {state}</span>
            </p>
            <p className="flex items-center text-gray-300 group">
              <i className="fas fa-phone-alt w-6 text-blue-500 group-hover:text-blue-400 transition-colors"></i>
              <a className="hover:text-white transition-colors" href="tel:+12519308621">(251) 930-8621</a>
            </p>
            <p className="flex items-center text-gray-300 group">
              <i className="fas fa-envelope w-6 text-blue-500 group-hover:text-blue-400 transition-colors"></i>
              <a className="hover:text-white transition-colors"
                href="mailto:zoiriscleaningservices@gmail.com">zoiriscleaningservices@gmail.com</a>
            </p>
            <p className="flex items-center text-gray-300 group">
              <i className="fas fa-sitemap w-6 text-blue-500 group-hover:text-blue-400 transition-colors"></i>
              <a className="hover:text-white transition-colors" href="/sitemap.xml">Sitemap</a>
            </p>
          </div>
        </div>
        
        <div className="relative z-10">
          <h3 className="text-white font-bold text-xl mb-6 tracking-wide border-b border-gray-800 pb-2 inline-block">Our
            Services</h3>
          <ul className="space-y-3 text-gray-400">
            <li><a className="hover:text-blue-400 transition-all duration-200 flex items-center group"
                href="/mobile-al/house-cleaning/"><i
                  className="fas fa-broom w-6 text-blue-600 group-hover:text-blue-400"></i> Residential Cleaning</a></li>
            <li><a className="hover:text-blue-400 transition-all duration-200 flex items-center group"
                href="/mobile-al/deep-cleaning/"><i
                  className="fas fa-sparkles w-6 text-purple-500 group-hover:text-purple-400"></i> Deep Cleaning</a></li>
            <li><a className="hover:text-blue-400 transition-all duration-200 flex items-center group"
                href="/mobile-al/commercial-cleaning/"><i
                  className="fas fa-building w-6 text-gray-500 group-hover:text-gray-400"></i> Commercial Cleaning</a></li>
            <li><a className="hover:text-blue-400 transition-all duration-200 flex items-center group"
                href="/mobile-al/airbnb-cleaning/"><i
                  className="fas fa-home w-6 text-pink-500 group-hover:text-pink-400"></i> Airbnb Cleaning</a></li>
            <li><a className="hover:text-blue-400 transition-all duration-200 flex items-center group"
                href="/mobile-al/carpet-cleaning/"><i
                  className="fas fa-layer-group w-6 text-orange-500 group-hover:text-orange-400"></i> Carpet Cleaning</a>
            </li>
            <li><a className="hover:text-blue-400 transition-all duration-200 flex items-center group"
                href="/mobile-al/window-cleaning/"><i
                  className="fas fa-window-maximize w-6 text-cyan-500 group-hover:text-cyan-400"></i> Window Cleaning</a>
            </li>
            <li><a className="hover:text-blue-400 transition-all duration-200 flex items-center group"
                href="/mobile-al/move-in-cleaning/"><i
                  className="fas fa-box-open w-6 text-yellow-500 group-hover:text-yellow-400"></i> Move-In Cleaning</a></li>
            <li><a className="hover:text-blue-400 transition-all duration-200 flex items-center group"
                href="/mobile-al/move-out-cleaning/"><i
                  className="fas fa-door-open w-6 text-red-500 group-hover:text-red-400"></i> Move-Out Cleaning</a></li>
            <li><a className="hover:text-blue-400 transition-all duration-200 flex items-center group"
                href="/mobile-al/post-construction-cleanup/"><i
                  className="fas fa-hard-hat w-6 text-yellow-600 group-hover:text-yellow-500"></i> Post-Construction</a>
            </li>
            <li><a className="hover:text-blue-400 transition-all duration-200 flex items-center group"
                href="/mobile-al/vacation-rental-cleaning/"><i
                  className="fas fa-umbrella-beach w-6 text-teal-500 group-hover:text-teal-400"></i> Vacation Rental</a>
            </li>
            <li><a className="hover:text-blue-400 transition-all duration-200 flex items-center group"
                href="/mobile-al/pressure-washing/"><i
                  className="fas fa-water w-6 text-blue-400 group-hover:text-blue-300"></i> Pressure Washing</a></li>
          </ul>
        </div>
        
        <div className="relative z-10">
          <h3 className="text-white font-bold text-xl mb-6 tracking-wide border-b border-gray-800 pb-2 inline-block">Service
            Areas</h3>
          
          <div className="bg-gray-900/50 rounded-lg p-4 mb-6 border border-gray-800">
            <ul className="grid grid-cols-2 gap-2 text-gray-400 text-sm">
              <li><a className="hover:text-blue-400 transition-colors flex items-center" href="/spanish-fort-al/"><i
                    className="fas fa-map-pin text-xs mr-2 text-red-500"></i> Spanish Fort</a></li>
              <li><a className="hover:text-blue-400 transition-colors flex items-center" href="/saraland-al/"><i
                    className="fas fa-map-pin text-xs mr-2 text-red-500"></i> Saraland</a></li>
              <li><a className="hover:text-blue-400 transition-colors flex items-center" href="/daphne-al/"><i
                    className="fas fa-map-pin text-xs mr-2 text-red-500"></i> Daphne</a></li>
              <li><a className="hover:text-blue-400 transition-colors flex items-center" href="/eight-mile-al/"><i
                    className="fas fa-map-pin text-xs mr-2 text-red-500"></i> Eight Mile</a></li>
              <li><a className="hover:text-blue-400 transition-colors flex items-center" href="/satsuma-al/"><i
                    className="fas fa-map-pin text-xs mr-2 text-red-500"></i> Satsuma</a></li>
              <li><a className="hover:text-blue-400 transition-colors flex items-center" href="/montrose-al/"><i
                    className="fas fa-map-pin text-xs mr-2 text-red-500"></i> Montrose</a></li>
              <li><a className="hover:text-blue-400 transition-colors flex items-center" href="/theodore-al/"><i
                    className="fas fa-map-pin text-xs mr-2 text-red-500"></i> Theodore</a></li>
              <li><a className="hover:text-blue-400 transition-colors flex items-center" href="/semmes-al/"><i
                    className="fas fa-map-pin text-xs mr-2 text-red-500"></i> Semmes</a></li>
              <li><a className="hover:text-blue-400 transition-colors flex items-center" href="/creola-al/"><i
                    className="fas fa-map-pin text-xs mr-2 text-red-500"></i> Creola</a></li>
              <li><a className="hover:text-blue-400 transition-colors flex items-center" href="/stapleton-al/"><i
                    className="fas fa-map-pin text-xs mr-2 text-red-500"></i> Stapleton</a></li>
              <li><a className="hover:text-blue-400 transition-colors flex items-center" href="/fairhope-al/"><i
                    className="fas fa-map-pin text-xs mr-2 text-red-500"></i> Fairhope</a></li>
              <li><a className="hover:text-blue-400 transition-colors flex items-center" href="/point-clear-al/"><i
                    className="fas fa-map-pin text-xs mr-2 text-red-500"></i> Point Clear</a></li>
              <li><a className="hover:text-blue-400 transition-colors flex items-center" href="/loxley-al/"><i
                    className="fas fa-map-pin text-xs mr-2 text-red-500"></i> Loxley</a></li>
              <li><a className="hover:text-blue-400 transition-colors flex items-center" href="/saint-elmo-al/"><i
                    className="fas fa-map-pin text-xs mr-2 text-red-500"></i> Saint Elmo</a></li>
              <li><a className="hover:text-blue-400 transition-colors flex items-center" href="/irvington-al/"><i
                    className="fas fa-map-pin text-xs mr-2 text-red-500"></i> Irvington</a></li>
              <li><a className="hover:text-blue-400 transition-colors flex items-center" href="/wilmer-al/"><i
                    className="fas fa-map-pin text-xs mr-2 text-red-500"></i> Wilmer</a></li>
              <li><a className="hover:text-blue-400 transition-colors flex items-center" href="/bay-minette-al/"><i
                    className="fas fa-map-pin text-xs mr-2 text-red-500"></i> Bay Minette</a></li>
              <li><a className="hover:text-blue-400 transition-colors flex items-center" href="/coden-al/"><i
                    className="fas fa-map-pin text-xs mr-2 text-red-500"></i> Coden</a></li>
              <li><a className="hover:text-blue-400 transition-colors flex items-center" href="/chunchula-al/"><i
                    className="fas fa-map-pin text-xs mr-2 text-red-500"></i> Chunchula</a></li>
              <li><a className="hover:text-blue-400 transition-colors flex items-center" href="/silverhill-al/"><i
                    className="fas fa-map-pin text-xs mr-2 text-red-500"></i> Silverhill</a></li>
              <li><a className="hover:text-blue-400 transition-colors flex items-center" href="/axis-al/"><i
                    className="fas fa-map-pin text-xs mr-2 text-red-500"></i> Axis</a></li>
              <li><a className="hover:text-blue-400 transition-colors flex items-center" href="/bucks-al/"><i
                    className="fas fa-map-pin text-xs mr-2 text-red-500"></i> Bucks</a></li>
            </ul>
          </div>
          <h3 className="text-white font-bold text-lg mb-4 tracking-wide">Quick Links</h3>
          <ul className="flex flex-wrap gap-4 text-gray-400 text-sm">
            <li><a className="hover:text-white transition-colors flex items-center" href="/index.html"><i
                  className="fas fa-home mr-2 text-blue-500"></i> Home</a></li>
            <li><a className="hover:text-white transition-colors flex items-center" href="/mobile-al/about/"><i
                  className="fas fa-info-circle mr-2 text-blue-500"></i> About</a></li>
            <li><a className="hover:text-white transition-colors flex items-center" href="/mobile-al/blog/"><i
                  className="fas fa-blog mr-2 text-blue-500"></i> Blog</a></li>
            <li><a className="hover:text-white transition-colors flex items-center" href="/mobile-al/contact/"><i
                  className="fas fa-envelope mr-2 text-blue-500"></i> Contact</a></li>
            <li><a className="hover:text-white transition-colors flex items-center" href="/apply/"><i
                  className="fas fa-user-plus mr-2 text-blue-500"></i> Apply</a></li>
          </ul>
          <p className="mt-8 text-gray-500 text-xs text-center lg:text-left">© <span id="year"></span> Zoiris Cleaning.
            All Rights Reserved.</p>
        </div>
      </div>
      
      <div className="mt-12 border-t border-gray-800 pt-8 relative z-10 bg-black/20">
        <div className="flex flex-wrap justify-center gap-6 text-2xl">
          <a className="text-gray-500 hover:scale-110 transition-transform duration-200 hover:text-blue-500"
            href="https://facebook.com" target="_blank"><i className="fab fa-facebook"></i></a>
          <a className="text-gray-500 hover:scale-110 transition-transform duration-200 hover:text-pink-500"
            href="https://instagram.com/zoiriscleaning" target="_blank"><i className="fab fa-instagram"></i></a>
          <a className="text-gray-500 hover:scale-110 transition-transform duration-200 hover:text-sky-400"
            href="https://x.com/zoiriscleaning" target="_blank"><i className="fab fa-x-twitter"></i></a>
          <a className="text-gray-500 hover:scale-110 transition-transform duration-200 hover:text-blue-400"
            href="https://linkedin.com" target="_blank"><i className="fab fa-linkedin"></i></a>
          <a className="text-gray-500 hover:scale-110 transition-transform duration-200 hover:text-red-500"
            href="https://youtube.com" target="_blank"><i className="fab fa-youtube"></i></a>
          <a className="text-gray-500 hover:scale-110 transition-transform duration-200 hover:text-gray-200"
            href="https://tiktok.com" target="_blank"><i className="fab fa-tiktok"></i></a>
          <a className="text-gray-500 hover:scale-110 transition-transform duration-200 hover:text-red-600"
            href="https://pinterest.com" target="_blank"><i className="fab fa-pinterest"></i></a>
          <a className="text-gray-500 hover:scale-110 transition-transform duration-200 hover:text-yellow-400"
            href="https://snapchat.com" target="_blank"><i className="fab fa-snapchat"></i></a>
          <a className="text-gray-500 hover:scale-110 transition-transform duration-200 hover:text-orange-500"
            href="https://reddit.com" target="_blank"><i className="fab fa-reddit"></i></a>
          <a className="text-gray-500 hover:scale-110 transition-transform duration-200 hover:text-indigo-400"
            href="https://tumblr.com" target="_blank"><i className="fab fa-tumblr"></i></a>
          <a className="text-gray-500 hover:scale-110 transition-transform duration-200 hover:text-indigo-500"
            href="https://discord.com" target="_blank"><i className="fab fa-discord"></i></a>
          <a className="text-gray-500 hover:scale-110 transition-transform duration-200 hover:text-green-500"
            href="https://wa.me/12519308621" target="_blank"><i className="fab fa-whatsapp"></i></a>
          <a className="text-gray-500 hover:scale-110 transition-transform duration-200 hover:text-sky-500"
            href="https://telegram.org" target="_blank"><i className="fab fa-telegram"></i></a>
          <a className="text-gray-500 hover:scale-110 transition-transform duration-200 hover:text-red-400"
            href="https://yelp.com" target="_blank"><i className="fab fa-yelp"></i></a>
          <a className="text-gray-500 hover:scale-110 transition-transform duration-200 hover:text-gray-400"
            href="https://github.com" target="_blank"><i className="fab fa-github"></i></a>
        </div>
      </div>
      
      <div className="absolute inset-0 bg-gradient-to-r from-blue-900/10 to-green-900/10 opacity-50 pointer-events-none">
      </div>
      
      
    </footer>
    
    

    
    
    

    
  </main>


  



    
    <section className="bg-gray-900 py-12 border-t border-gray-800 z-50 relative mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-8">
          <h3 className="text-2xl font-bold text-white mb-2">Nearby Featured Service Areas</h3>
          <p className="text-gray-400 text-sm max-w-2xl mx-auto">We provide top-rated cleaning service not just in {city}, but across the entire Gulf Coast and State of Alabama.</p>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3 text-center">
            <a href="/daphne-al/" className="text-gray-500 hover:text-blue-400 text-xs transition-colors">Daphne, AL</a>
            <a href="/birmingham-al/" className="text-gray-500 hover:text-blue-400 text-xs transition-colors">Birmingham, AL</a>
            <a href="/spanish-fort-al/" className="text-gray-500 hover:text-blue-400 text-xs transition-colors">Spanish Fort, AL</a>
            <a href="/huntsville-al/" className="text-gray-500 hover:text-blue-400 text-xs transition-colors">Huntsville, AL</a>
            <a href="/foley-al/" className="text-gray-500 hover:text-blue-400 text-xs transition-colors">Foley, AL</a>
            <a href="/montgomery-al/" className="text-gray-500 hover:text-blue-400 text-xs transition-colors">Montgomery, AL</a>
            <a href="/locations/" className="text-blue-500 hover:text-pink-400 font-bold text-xs transition-colors">View All 480+ Locations</a>
        </div>
      </div>
    </section>


    </>
  );
}

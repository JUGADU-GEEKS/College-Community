document.addEventListener('DOMContentLoaded', () => {
    // Set current year in footer
    document.getElementById('current-year').textContent = new Date().getFullYear();
    
    // Mobile Menu Toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (menuToggle && mobileMenu) {
      menuToggle.addEventListener('click', () => {
        mobileMenu.classList.toggle('active');
        
        // Toggle the icon between bars and X
        const icon = menuToggle.querySelector('i');
        if (icon.classList.contains('fa-bars')) {
          icon.classList.remove('fa-bars');
          icon.classList.add('fa-times');
        } else {
          icon.classList.remove('fa-times');
          icon.classList.add('fa-bars');
        }
      });
    }
    
    // Search form focus effect
    const searchInput = document.getElementById('search-input');
    const searchContainer = document.querySelector('.search-container');
    
    if (searchInput && searchContainer) {
      searchInput.addEventListener('focus', () => {
        searchContainer.classList.add('focused');
      });
      
      searchInput.addEventListener('blur', () => {
        searchContainer.classList.remove('focused');
      });
      
      // Handle search form submission
      const searchForm = document.getElementById('search-form');
      if (searchForm) {
        searchForm.addEventListener('submit', (e) => {
          e.preventDefault();
          console.log('Searching for:', searchInput.value);
          // In a real application, this would trigger a search API call
          alert(`Searching for: ${searchInput.value}`);
        });
      }
    }
    
    // Hero Slider
    const heroSlider = document.querySelector('.hero-slider');
    const heroCaption = document.querySelector('.hero-caption');
    const slideIndicatorsContainer = document.querySelector('.slide-indicators');
    
    // Hero slider data
    const heroSlides = [
      {
        url: "https://images.unsplash.com/photo-1588072432836-e10032774350?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
        caption: "Find lab equipment for your next experiment"
      },
      {
        url: "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
        caption: "Quality drafting tools at student-friendly prices"
      },
      {
        url: "https://images.unsplash.com/photo-1606761568499-6d2451b23c66?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
        caption: "Buy and sell graphic design tools within your campus"
      },
      {
        url: "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
        caption: "Lab coats and safety gear at discounted rates"
      }
    ];
    
    let activeSlide = 0;
    let slideInterval;
    
    // Initialize the hero slider
    function initHeroSlider() {
      if (!heroSlider || !slideIndicatorsContainer) return;
      
      // Create slides
      heroSlides.forEach((slide, index) => {
        const slideElement = document.createElement('div');
        slideElement.className = `hero-slide ${index === 0 ? 'active' : ''}`;
        slideElement.style.backgroundImage = `url(${slide.url})`;
        heroSlider.appendChild(slideElement);
        
        // Create slide indicators
        const indicator = document.createElement('button');
        indicator.className = `slide-indicator ${index === 0 ? 'active' : ''}`;
        indicator.ariaLabel = `Go to slide ${index + 1}`;
        indicator.addEventListener('click', () => {
          goToSlide(index);
        });
        slideIndicatorsContainer.appendChild(indicator);
      });
      
      // Set the initial caption
      if (heroCaption) {
        heroCaption.textContent = heroSlides[0].caption;
      }
      
      // Start the automatic slideshow
      startSlideshow();
    }
    
    // Go to a specific slide
    function goToSlide(index) {
      if (!heroSlider) return;
      
      // Reset the slideshow timer
      if (slideInterval) {
        clearInterval(slideInterval);
        startSlideshow();
      }
      
      // Update active slide
      const slides = heroSlider.querySelectorAll('.hero-slide');
      const indicators = slideIndicatorsContainer.querySelectorAll('.slide-indicator');
      
      slides.forEach((slide, i) => {
        if (i === index) {
          slide.classList.add('active');
        } else {
          slide.classList.remove('active');
        }
      });
      
      indicators.forEach((indicator, i) => {
        if (i === index) {
          indicator.classList.add('active');
        } else {
          indicator.classList.remove('active');
        }
      });
      
      // Update caption
      if (heroCaption) {
        heroCaption.textContent = heroSlides[index].caption;
      }
      
      activeSlide = index;
    }
    
    // Move to the next slide
    function nextSlide() {
      const newIndex = (activeSlide + 1) % heroSlides.length;
      goToSlide(newIndex);
    }
    
    // Start the automatic slideshow
    function startSlideshow() {
      slideInterval = setInterval(nextSlide, 5000); // Change slides every 5 seconds
    }
    
    // Initialize hero slider
    initHeroSlider();
    
    // Categories data
    const categories = [
      { name: "Lab Equipment", icon: "🔬", count: 145 },
      { name: "Drafting Tools", icon: "📏", count: 87 },
      { name: "Design Supplies", icon: "🎨", count: 112 },
      { name: "Textbooks", icon: "📚", count: 201 },
      { name: "Lab Coats", icon: "🥼", count: 63 },
      { name: "Calculators", icon: "🧮", count: 79 }
    ];
    
    // Featured items data
    const featuredItems = [
      {
        title: "Engineering Drafting Set",
        price: "$45",
        seller: "Alex M.",
        college: "MIT",
        condition: "Like New",
        image: "https://images.unsplash.com/photo-1519389950473-47ba0277781c?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
      },
      {
        title: "Chemistry Lab Kit",
        price: "$120",
        seller: "Sofia L.",
        college: "Stanford",
        condition: "Good",
        image: "https://images.unsplash.com/photo-1582719471384-894fbb16e074?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
      },
      {
        title: "Professional Graphics Tablet",
        price: "$85",
        seller: "Marcus J.",
        college: "RISD",
        condition: "Excellent",
        image: "https://images.unsplash.com/photo-1595078475328-1ab05d0a6a0e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
      },
      {
        title: "Lab Safety Glasses (Pack of 2)",
        price: "$15",
        seller: "Priya K.",
        college: "CalTech",
        condition: "New",
        image: "https://images.unsplash.com/photo-1555696958-c5049b866f6f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
      }
    ];
    
    // Testimonials data
    const testimonials = [
      {
        name: "Jessica T.",
        role: "Engineering Student, UCLA",
        text: "I saved over $200 on drafting tools by buying them from a senior student. The quality was excellent, and it was so easy to arrange the pickup on campus."
      },
      {
        name: "Michael R.",
        role: "Chemistry Major, NYU",
        text: "When I graduated, I sold all my lab equipment on College Bazaar. Made back almost half of what I originally paid, and helped out freshmen who needed the supplies."
      },
      {
        name: "Aisha K.",
        role: "Graphic Design Student, RISD",
        text: "Found a practically new graphics tablet for half the retail price. The seller was in my dorm building, so I didn't even have to go far to pick it up. Love this platform!"
      }
    ];
    
    // Initialize categories
    function initCategories() {
      const categoryGrid = document.querySelector('.category-grid');
      if (!categoryGrid) return;
      
      categories.forEach((category, index) => {
        const categoryEl = document.createElement('div');
        categoryEl.className = 'category-card staggered-item';
        categoryEl.innerHTML = `
          <div class="category-icon">${category.icon}</div>
          <h3 class="category-name">${category.name}</h3>
          <p class="category-count">${category.count} items</p>
        `;
        // Set a delay based on the index
        categoryEl.style.transitionDelay = `${index * 0.1}s`;
        categoryGrid.appendChild(categoryEl);
      });
    }
    
    // Initialize featured items
    function initFeaturedItems() {
      const itemsGrid = document.querySelector('.items-grid');
      if (!itemsGrid) return;
      
      featuredItems.forEach((item, index) => {
        const itemEl = document.createElement('div');
        itemEl.className = 'item-card staggered-item';
        itemEl.innerHTML = `
          <div class="item-image-container">
            <img src="${item.image}" alt="${item.title}" class="item-image">
            <div class="item-price">${item.price}</div>
          </div>
          <div class="item-content">
            <h3 class="item-title">${item.title}</h3>
            <div class="item-seller">
              <span>${item.seller}</span>
              <span>•</span>
              <span>${item.college}</span>
            </div>
            <div class="item-footer">
              <span class="item-condition">${item.condition}</span>
              <a href="#" class="item-link">View Details</a>
            </div>
          </div>
        `;
        // Set a delay based on the index
        itemEl.style.transitionDelay = `${index * 0.1}s`;
        itemsGrid.appendChild(itemEl);
      });
    }
    
    // Initialize testimonials
    function initTestimonials() {
      const testimonialsGrid = document.querySelector('.testimonials-grid');
      if (!testimonialsGrid) return;
      
      testimonials.forEach((testimonial, index) => {
        const testimonialEl = document.createElement('div');
        testimonialEl.className = 'testimonial-card staggered-item';
        testimonialEl.innerHTML = `
          <div class="testimonial-header">
            <div class="testimonial-avatar"></div>
            <div class="testimonial-info">
              <h4>${testimonial.name}</h4>
              <p>${testimonial.role}</p>
            </div>
          </div>
          <p class="testimonial-text">"${testimonial.text}"</p>
        `;
        // Set a delay based on the index
        testimonialEl.style.transitionDelay = `${index * 0.1}s`;
        testimonialsGrid.appendChild(testimonialEl);
      });
    }
    
    // Initialize all dynamic content
    initCategories();
    initFeaturedItems();
    initTestimonials();
    
    // Add scroll animation to all sections
    const animateOnScroll = () => {
      const sections = document.querySelectorAll('section');
      const staggeredItems = document.querySelectorAll('.staggered-item');
      
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.1 });
      
      sections.forEach(section => {
        observer.observe(section);
      });
      
      staggeredItems.forEach(item => {
        observer.observe(item);
      });
    };
    
    // Run the scroll animation
    animateOnScroll();
    
    // Make the header sticky and add shadow on scroll
    const header = document.querySelector('.header');
    
    if (header) {
      window.addEventListener('scroll', () => {
        if (window.scrollY > 10) {
          header.style.boxShadow = 'var(--shadow)';
        } else {
          header.style.boxShadow = 'var(--shadow-sm)';
        }
      });
    }
  });
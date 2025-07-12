document.addEventListener('DOMContentLoaded', () => {
  // Set current year in footer
  document.getElementById('current-year').textContent = new Date().getFullYear();

  // Mobile Menu Toggle
  const menuToggle = document.querySelector('.menu-toggle');
  const mobileMenu = document.querySelector('.mobile-menu');
  const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');
  const navLinks = document.querySelectorAll('.nav-link');

  if (menuToggle && mobileMenu) {
    menuToggle.addEventListener('click', () => {
      mobileMenu.classList.toggle('active');

      // Toggle the icon between bars and X
      const icon = menuToggle.querySelector('i');
      if (mobileMenu.classList.contains('active')) {
        icon.classList.remove('fa-bars');
        icon.classList.add('fa-times');
      } else {
        icon.classList.remove('fa-times');
        icon.classList.add('fa-bars');
      }
    });
  }

  // Close mobile menu when clicking on a link
  mobileNavLinks.forEach(link => {
    link.addEventListener('click', () => {
      if (mobileMenu.classList.contains('active')) {
        mobileMenu.classList.remove('active');
        const icon = menuToggle.querySelector('i');
        icon.classList.remove('fa-times');
        icon.classList.add('fa-bars');
      }
    });
  });

  // Close mobile menu when clicking outside
  document.addEventListener('click', (event) => {
    if (mobileMenu && mobileMenu.classList.contains('active')) {
      if (!mobileMenu.contains(event.target) && !menuToggle.contains(event.target)) {
        mobileMenu.classList.remove('active');
        const icon = menuToggle.querySelector('i');
        icon.classList.remove('fa-times');
        icon.classList.add('fa-bars');
      }
    }
  });

  // Handle active states for navigation links
  function setActiveLink() {
    const currentPath = window.location.pathname;
    
    // Remove active class from all links
    navLinks.forEach(link => link.classList.remove('active'));
    mobileNavLinks.forEach(link => link.classList.remove('active'));
    
    // Add active class to current page link
    navLinks.forEach(link => {
      if (link.getAttribute('href') === currentPath) {
        link.classList.add('active');
      }
    });
    
    mobileNavLinks.forEach(link => {
      if (link.getAttribute('href') === currentPath) {
        link.classList.add('active');
      }
    });
  }

  // Set active link on page load
  setActiveLink();

  // Smooth scrolling for About and Contact links
  const smoothScrollLinks = document.querySelectorAll('a[href^="#"]');
  smoothScrollLinks.forEach(link => {
    link.addEventListener('click', function (e) {
      e.preventDefault();

      const targetId = this.getAttribute('href');
      if (targetId === '#') return;

      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        targetElement.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });

  // Check for URL hash on page load for About and Contact sections
  if (window.location.hash) {
    const targetElement = document.querySelector(window.location.hash);
    if (targetElement) {
      setTimeout(() => {
        targetElement.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }, 100);
    }
  }

  // Handle scroll-to from the server side (e.g., /about, /contact routes)
  const scrollTo = document.querySelector('body').getAttribute('data-scroll-to');
  if (scrollTo) {
    const targetElement = document.getElementById(scrollTo);
    if (targetElement) {
      setTimeout(() => {
        targetElement.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }, 100);
    }
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

  const counts = window.productCounts;

  const categories = [
    { name: "Drafting Tools", img: "/static/images/drafter.webp", count: counts.drafter, link:"drafter" },
    { name: "Safety Aprons", img: "/static/images/apron.jpeg", count: counts.apron, link:"apron" },
    { name: "Textbooks", img: "/static/images/books.jpeg", count: counts.books, link:"akash books" },
    { name: "Lab Coats", img: "/static/images/labcoat.jpg", count: counts.labcoat, link:"labcoats" },
    { name: "Calculators", img: "/static/images/calculator.jpg", count: counts.calculator, link:"calculator" },
    { name: "Sheet Holders", img: "/static/images/sheet_holder.avif", count: counts.sheet, link:"sheet" }
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
          <div class="category-icon" style="width:80px;height:80px;border-radius:50%;overflow:hidden;border:3px solid #f7d08a;display:flex;align-items:center;justify-content:center;margin:0 auto 1rem auto;background:#181818;">
            <img src="${category.img}" alt="${category.name}" style="width:100%;height:100%;object-fit:cover;display:block;" />
          </div>
          <h3 class="category-name">${category.name}</h3>
          <p class="category-count">${category.count} items</p>
        `;
      // Set a delay based on the index
      categoryEl.style.transitionDelay = `${index * 0.1}s`;
      categoryEl.addEventListener('click', ()=>[
        window.location.href = `/browse?filter=${encodeURIComponent(category.link)}`
      ])
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
            <div class="testimonial-avatar" style="display: flex; align-items: center; justify-content: center; background: #23272f; border-radius: 50%; width: 48px; height: 48px;">
              <i class='fas fa-user' style="color: #f7d08a; font-size: 1.7rem;"></i>
            </div>
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
  let lastScrollTop = 0;

  window.addEventListener('scroll', () => {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    if (scrollTop > lastScrollTop && scrollTop > 100) {
      // Scrolling down
      header.style.transform = 'translateY(-100%)';
    } else {
      // Scrolling up
      header.style.transform = 'translateY(0)';
    }
    
    lastScrollTop = scrollTop;
  });
});
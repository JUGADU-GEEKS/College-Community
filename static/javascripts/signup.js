
// Apply random positions to particles
document.addEventListener('DOMContentLoaded', function() {
    // Initialize animations
    const elements = document.querySelectorAll('.animate-in');
    elements.forEach((el, index) => {
      setTimeout(() => {
        el.classList.add('active');
      }, 100 * index);
    });
  
    // Set random positions for particles
    const particles = document.querySelectorAll('.particle');
    particles.forEach(particle => {
      particle.style.setProperty('--random', Math.random());
      particle.style.left = `${Math.random() * 100}%`;
    });
  });


  
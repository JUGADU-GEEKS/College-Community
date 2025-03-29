document.addEventListener('DOMContentLoaded', function() {
    // Set up the loading animation
    const loader = document.querySelector('.loader');
    
    setTimeout(() => {
        if (loader) {
            loader.style.opacity = 0;
            loader.style.transition = 'opacity 0.3s';
        }
    }, 2000);
    
    // Set up the particle background
    const canvas = document.getElementById('particleCanvas');
    const ctx = canvas.getContext('2d');
    
    // Make canvas full screen
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    // Particle settings
    const particles = [];
    const particleCount = Math.min(50, Math.floor(window.innerWidth / 20));
    
    // Create particles
    function initParticles() {
        particles.length = 0;
        
        for (let i = 0; i < particleCount; i++) {
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                size: Math.random() * 3 + 1,
                speedX: (Math.random() - 0.5) * 0.5,
                speedY: (Math.random() - 0.5) * 0.5,
                opacity: Math.random() * 0.5 + 0.1
            });
        }
    }
    
    // Draw particles and connections
    function drawParticles() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        particles.forEach((particle, i) => {
            // Update position
            particle.x += particle.speedX;
            particle.y += particle.speedY;
            
            // Wrap around edges
            if (particle.x > canvas.width) particle.x = 0;
            else if (particle.x < 0) particle.x = canvas.width;
            
            if (particle.y > canvas.height) particle.y = 0;
            else if (particle.y < 0) particle.y = canvas.height;
            
            // Draw particle
            ctx.beginPath();
            ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(59, 130, 246, ${particle.opacity})`;
            ctx.fill();
            
            // Connect particles within range
            connectParticles(particle, i);
        });
        
        requestAnimationFrame(drawParticles);
    }
    
    // Draw connections between particles
    function connectParticles(particle, index) {
        for (let i = index + 1; i < particles.length; i++) {
            const dx = particle.x - particles[i].x;
            const dy = particle.y - particles[i].y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance < 100) {
                ctx.beginPath();
                ctx.strokeStyle = `rgba(59, 130, 246, ${0.2 * (1 - distance / 100)})`;
                ctx.lineWidth = 0.5;
                ctx.moveTo(particle.x, particle.y);
                ctx.lineTo(particles[i].x, particles[i].y);
                ctx.stroke();
            }
        }
    }
    
    // Handle window resize
    window.addEventListener('resize', function() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        initParticles();
    });
    
    // Initialize and start animation
    initParticles();
    drawParticles();
});

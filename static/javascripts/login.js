// JavaScript would go here
document.addEventListener('DOMContentLoaded', function () {
    // Toggle password visibility
    const togglePassword = document.getElementById('toggle-password');
    const passwordInput = document.getElementById('password');

    togglePassword.addEventListener('click', function () {
      const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
      passwordInput.setAttribute('type', type);
      togglePassword.textContent = type === 'password' ? '👁️' : '👁️‍🗨️';
    });

    // Forgot password dialog
    const forgotPasswordLink = document.getElementById('forgot-password-link');
    const forgotPasswordDialog = document.getElementById('forgot-password-dialog');
    const dialogClose = document.getElementById('dialog-close');

    forgotPasswordLink.addEventListener('click', function (e) {
      e.preventDefault();
      forgotPasswordDialog.classList.add('open');
    });

    dialogClose.addEventListener('click', function () {
      forgotPasswordDialog.classList.remove('open');
    });

    // Login form submission
    const loginForm = document.getElementById('login-form');

    // Reset form submission
    const resetForm = document.getElementById('reset-form');

    

    // Initialize background canvas
    initBackgroundCanvas();

    // Initialize floating lanterns
    initFloatingLanterns();
  });

  function initBackgroundCanvas() {
    const canvas = document.getElementById('background-canvas');
    const ctx = canvas.getContext('2d');

    // Set canvas dimensions
    function resizeCanvas() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }

    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    // Star properties
    const stars = [];
    const starCount = Math.floor(canvas.width * canvas.height / 10000);

    // Create stars
    for (let i = 0; i < starCount; i++) {
      stars.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        radius: Math.random() * 1.5 + 0.5,
        alpha: Math.random(),
        speed: Math.random() * 0.05
      });
    }

    // Cloud properties
    const clouds = [];
    const cloudCount = 5;

    // Create clouds
    for (let i = 0; i < cloudCount; i++) {
      clouds.push({
        x: Math.random() * canvas.width,
        y: Math.random() * (canvas.height / 2),
        width: Math.random() * 200 + 200,
        height: Math.random() * 100 + 50,
        speed: Math.random() * 0.2 + 0.1,
        opacity: Math.random() * 0.2 + 0.1
      });
    }

    // Animation frame
    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Draw gradient background
      const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
      gradient.addColorStop(0, '#0F1018');
      gradient.addColorStop(1, '#1A1F2C');
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Draw clouds
      clouds.forEach(cloud => {
        cloud.x += cloud.speed;
        if (cloud.x > canvas.width + cloud.width) {
          cloud.x = -cloud.width;
        }

        ctx.save();
        ctx.beginPath();
        ctx.fillStyle = `rgba(30, 30, 45, ${cloud.opacity})`;
        ctx.filter = 'blur(40px)';
        ctx.ellipse(
          cloud.x,
          cloud.y,
          cloud.width / 2,
          cloud.height / 2,
          0,
          0,
          Math.PI * 2
        );
        ctx.fill();
        ctx.restore();
      });

      // Draw stars
      stars.forEach(star => {
        star.alpha += star.speed;
        if (star.alpha > 1) {
          star.alpha = 0;
        }

        ctx.beginPath();
        ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 255, 255, ${Math.abs(Math.sin(star.alpha))})`;
        ctx.fill();
      });

      requestAnimationFrame(animate);
    }

    animate();
  }

  function initFloatingLanterns() {
    const container = document.getElementById('lanterns-container');
    const lanternCount = 8;

    // Create lanterns
    for (let i = 0; i < lanternCount; i++) {
      const lantern = document.createElement('div');
      lantern.className = 'lantern';

      // Random position
      const left = Math.random() * 100;
      const top = Math.random() * 90; // Position in top half
      const delay = Math.random() * 5;
      const duration = 10 + Math.random() * 10;
      const size = 0.5 + Math.random() * 0.2;

      // Set lantern styles
      lantern.style.left = `${left}%`;
      lantern.style.top = `${top}%`;
      lantern.style.transform = `scale(${size})`;
      lantern.style.animation = `float ${duration}s ease-in-out ${delay}s infinite alternate`;

      // Create glow
      const glow = document.createElement('div');
      glow.className = 'absolute inset-0 rounded-full';

      // Random light color (vibrant colors for magical effect)
      const colors = [
        { hue: 0, saturation: 100, lightness: 70 },   // Red
        { hue: 30, saturation: 100, lightness: 70 },  // Orange
        { hue: 60, saturation: 100, lightness: 70 },  // Yellow
        { hue: 120, saturation: 100, lightness: 70 }, // Green
        { hue: 180, saturation: 100, lightness: 70 }, // Cyan
        { hue: 240, saturation: 100, lightness: 70 }, // Blue
        { hue: 270, saturation: 100, lightness: 70 }, // Purple
        { hue: 300, saturation: 100, lightness: 70 }, // Magenta
        { hue: 330, saturation: 100, lightness: 70 }, // Pink
        { hue: 15, saturation: 100, lightness: 70 },  // Warm Red
        { hue: 45, saturation: 100, lightness: 70 },  // Warm Orange
        { hue: 90, saturation: 100, lightness: 70 },  // Lime
        { hue: 150, saturation: 100, lightness: 70 }, // Turquoise
        { hue: 210, saturation: 100, lightness: 70 }, // Sky Blue
        { hue: 255, saturation: 100, lightness: 70 }, // Royal Blue
        { hue: 285, saturation: 100, lightness: 70 }  // Deep Purple
      ];
      
      const randomColor = colors[Math.floor(Math.random() * colors.length)];
      const lightColor = `hsl(${randomColor.hue}, ${randomColor.saturation}%, ${randomColor.lightness}%)`;

      glow.style.boxShadow = `0 0 20px 15px ${lightColor}`;
      glow.style.backgroundColor = lightColor;
      glow.style.opacity = `${0.6 + Math.random() * 0.2}`;

      // Pulse animation
      glow.style.animation = `pulse ${3 + Math.random() * 2}s ease-in-out infinite alternate`;

      lantern.appendChild(glow);
      container.appendChild(lantern);
    }
  }
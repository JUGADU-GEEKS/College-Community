// document.addEventListener('DOMContentLoaded', function() {
//     const form = document.getElementById('signup-form');
//     const btnText = document.querySelector('.btn-text');
//     const loadingSpinner = document.querySelector('.loading-spinner');
    
//     if (form) {
//         form.addEventListener('submit', function(e) {
//             e.preventDefault();
            
//             // Show loading state
//             btnText.style.display = 'none';
//             loadingSpinner.style.display = 'flex';
            
//             // Simulate form submission
//             setTimeout(function() {
//                 // Hide loading state
//                 btnText.style.display = 'block';
//                 loadingSpinner.style.display = 'none';
                
//                 // Show success message or redirect
//                 alert('Account created successfully!');
//                 window.location.href = 'login.html';
//             }, 1500);
//         });
//     }
    
//     // Add focus effects to inputs
//     const inputs = document.querySelectorAll('.form-input, .form-select');
//     inputs.forEach(input => {
//         input.addEventListener('focus', function() {
//             this.parentElement.classList.add('focused');
//         });
        
//         input.addEventListener('blur', function() {
//             if (!this.value) {
//                 this.parentElement.classList.remove('focused');
//             }
//         });
//     });
// });

// // 🛠 FIX: Move togglePassword function OUTSIDE DOMContentLoaded
// function togglePassword(inputId, eyeIcon) {
//     let passwordField = document.getElementById(inputId);
//     if (passwordField.type === "password") {
//         passwordField.type = "text";
//         eyeIcon.classList.remove("fa-eye");
//         eyeIcon.classList.add("fa-eye-slash");
//     } else {
//         passwordField.type = "password";
//         eyeIcon.classList.remove("fa-eye-slash");
//         eyeIcon.classList.add("fa-eye");
//     }
// }
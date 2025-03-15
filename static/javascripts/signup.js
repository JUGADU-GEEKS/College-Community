const sendOTPBtn = document.querySelector('.sendotp');
const OTPdiv = document.querySelector('.otp');
const errorMessage = document.getElementById('error-message');

// Validate the form fields
function validateForm() {
    const email = document.getElementById('email').value;
    const enrollment = document.getElementById('enrollment').value;
    const contact = document.getElementById('contact').value;

    const emailRegex = /^[^\s@]+@(gmail\.com|outlook\.com)$/i;
    const digitRegex = /^\d{10}$/;

    // Email validation
    if (!emailRegex.test(email)) {
        errorMessage.innerText = "Only Gmail or Outlook emails are allowed.";
        errorMessage.style.display = 'block';
        return false;
    }

    // Enrollment validation
    if (!digitRegex.test(enrollment)) {
        errorMessage.innerText = "Enrollment number must be exactly 10 digits.";
        errorMessage.style.display = 'block';
        return false;
    }

    // Contact number validation
    if (!digitRegex.test(contact)) {
        errorMessage.innerText = "Contact number must be exactly 10 digits.";
        errorMessage.style.display = 'block';
        return false;
    }

    // No error
    errorMessage.style.display = 'none';
    return true;
}

// Handle OTP Button Click
sendOTPBtn.addEventListener("click", (e) => {
    if (validateForm()) {
        OTPdiv.style.display = "block";
        errorMessage.style.display = 'none';
    } else {
        OTPdiv.style.display = "none";
    }
});

// Final Form Submission (OTP Check can be added here if needed)
function finalFormSubmit() {
    const otp = document.querySelector('input[name="otp"]').value;
    if (!otp || otp.length < 4) {
        errorMessage.innerText = "Please enter a valid OTP.";
        errorMessage.style.display = 'block';
        return false;
    }
    errorMessage.style.display = 'none';
    return true;  // Proceed with form submission
}
// DOM Elements
const form = document.getElementById('sellForm');
const itemTypeSelect = document.getElementById('itemType');
const equipmentSection = document.getElementById('equipmentSection');
const calculatorSection = document.getElementById('calculatorSection');
const priceSection = document.getElementById('priceSection');
const monthsOldInput = document.getElementById('monthsOld');
const monthsValue = document.getElementById('monthsValue');
const calculatorMonthsOldInput = document.getElementById('calculatorMonthsOld');
const calculatorMonthsValue = document.getElementById('calculatorMonthsValue');
const conditionSelect = document.getElementById('condition');
const calculatorTypeSelect = document.getElementById('calculatorType');
const predictedPriceElement = document.getElementById('predictedPrice');
const submitButton = document.getElementById('submitButton');
const toast = document.getElementById('toast');
const toastDescription = document.getElementById('toast-description');
const toastTitle = document.querySelector('.toast-title');

// Initialize form state
let itemType = '';
let selectedEquipment = '';

document.addEventListener('DOMContentLoaded', () => {
  // Set current year in footer if present
  const yearEl = document.getElementById('current-year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

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
    navLinks.forEach(link => link.classList.remove('active'));
    mobileNavLinks.forEach(link => link.classList.remove('active'));
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
  setActiveLink();

  // Event Listeners
  itemTypeSelect.addEventListener('change', updateFormBasedOnSelection);
  monthsOldInput.addEventListener('input', updateMonthsUI);
  calculatorMonthsOldInput.addEventListener('input', updateCalculatorMonthsUI);

  // Equipment selection
  const equipmentRadios = document.querySelectorAll('input[name="equipmentItem"]');
  equipmentRadios.forEach(radio => {
    radio.addEventListener('change', function() {
      selectedEquipment = this.value;
    });
  });

  // Add event listener to the form for submission
  form.addEventListener('submit', function(e) {
    // Show a toast notification before form submission
    showToast(
      'Form Submitted',
      `Your ${itemType} data has been submitted successfully`
    );
    
    // Let the form submit naturally - no preventDefault()
  });
});

// Function to update the form based on selected item type
function updateFormBasedOnSelection() {
  const itemType = itemTypeSelect.value;
  
  // Hide all sections
  equipmentSection.classList.add('hidden');
  calculatorSection.classList.add('hidden');
  priceSection.classList.add('hidden');
  
  // Show relevant section based on item type
  if (itemType) {
    if (itemType === 'equipment') {
      equipmentSection.classList.remove('hidden');
    } else if (itemType === 'calculator') {
      calculatorSection.classList.remove('hidden');
    }
    priceSection.classList.remove('hidden');
    submitButton.disabled = false;
  } else {
    submitButton.disabled = true;
  }
}

// Function to update the displayed value of the "months old" slider (for equipment)
function updateMonthsUI() {
  monthsValue.textContent = monthsOldInput.value;
}

// Function to update the displayed value of the "months old" slider (for calculators)
function updateCalculatorMonthsUI() {
  calculatorMonthsValue.textContent = calculatorMonthsOldInput.value;
}

// Function to show toast notification
function showToast(title, description) {
  toastTitle.textContent = title;
  toastDescription.textContent = description;
  toast.classList.add('show');
  
  // Hide toast after 5 seconds
  setTimeout(() => {
    toast.classList.remove('show');
  }, 5000);
}

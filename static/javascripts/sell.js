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

// Add animations on load
document.addEventListener('DOMContentLoaded', function() {
  const formSections = document.querySelectorAll('.form-section');
  formSections.forEach(section => {
    setTimeout(() => {
      section.style.animationPlayState = 'running';
    }, 100);
  });
});

// Initialize form state
let itemType = '';
let selectedEquipment = '';

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

// Add event listener to the form for submission
form.addEventListener('submit', function(e) {
  // The form will naturally submit to your backend
  // You can add any pre-submission logic here if needed
  
  // Show a toast notification before form submission
  showToast(
    'Form Submitted',
    `Your ${itemType} data has been submitted successfully`
  );
  
  // Let the form submit naturally - no preventDefault()
});

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


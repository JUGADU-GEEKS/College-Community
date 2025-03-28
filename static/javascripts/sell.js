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

// Add animations on load
document.addEventListener('DOMContentLoaded', function() {
  const formSections = document.querySelectorAll('.form-section');
  formSections.forEach(section => {
    section.style.animationPlayState = 'running';
  });
});

// Initialize form state
let itemType = '';
let selectedEquipment = '';
let predictedPrice = '';

// Event Listeners
itemTypeSelect.addEventListener('change', updateFormBasedOnSelection);
monthsOldInput.addEventListener('input', updateMonthsUI);
calculatorMonthsOldInput.addEventListener('input', updateCalculatorMonthsUI);
conditionSelect.addEventListener('change', updateUI);
calculatorTypeSelect.addEventListener('change', updateUI);

// Equipment selection
const equipmentRadios = document.querySelectorAll('input[name="equipmentItem"]');
equipmentRadios.forEach(radio => {
  radio.addEventListener('change', function() {
    selectedEquipment = this.value;
    updateUI();
  });
});

// Function to update the form based on selected item type
function updateFormBasedOnSelection() {
  itemType = itemTypeSelect.value;
  equipmentSection.classList.add('hidden');
  calculatorSection.classList.add('hidden');
  priceSection.classList.remove('hidden');  // Always show price section
  submitButton.disabled = !itemType;

  if (itemType) {
    if (itemType === 'equipment') {
      equipmentSection.classList.remove('hidden');
    } else if (itemType === 'calculator') {
      calculatorSection.classList.remove('hidden');
    }
    submitButton.disabled = false;
  }
}

// Function to update the UI with the predicted price
function updateUI() {
  predictedPriceElement.textContent = predictedPrice;
  predictedPriceElement.classList.remove('animate-glow');
  void predictedPriceElement.offsetWidth;
  predictedPriceElement.classList.add('animate-glow');
}

// Function to update the displayed value of the "months old" slider (for normal items)
function updateMonthsUI() {
  monthsValue.textContent = monthsOldInput.value;
  updateUI();
}

// Function to update the displayed value of the "months old" slider (for calculators)
function updateCalculatorMonthsUI() {
  calculatorMonthsValue.textContent = calculatorMonthsOldInput.value;
  updateUI();
}

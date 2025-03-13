// DOM Elements
document.addEventListener('DOMContentLoaded', function() {
    // Featured Items - Sample Data (In a real app, this would come from a backend/API)
    const featuredItems = [
        {
            id: 1,
            title: 'Sheet Holder',
            price: 120.00,
            category: 'Lab Equipment',
            location: 'Science Building',
            image: 'https://m.media-amazon.com/images/I/31rJUNejimL._AC_UF1000,1000_QL80_.jpg'
        },
        {
            id: 2,
            title: 'Drafter',
            price: 199.99,
            category: 'Drafting Tools',
            location: 'Engineering Dept',
            image: 'https://rukminim3.flixcart.com/image/850/1000/xif0q/drafting-kit/m/b/y/1-mini-drafter-for-engineering-drawing-book-birds-original-imagyq3pqqqkyptt.jpeg?q=90&crop=false'
        },
        {
            id: 3,
            title: 'Lab Coat (Size M)',
            price: 35.00,
            category: 'Lab Wear',
            location: 'Chemistry Dept',
            image: 'https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcS8gWidvzT7kiYHhDZcsvoG6aLgTHDnLqf6qY-lsn9T6p11TZ5BJuKC7k8qcXSB8CJXVnN7zvdfJHJa7PjwvrXgFGMlSJ_oJqR0JS9kt2ZQQVeAlhE2LFhmR3Eku9O3zczTfcZFoQ&usqp=CAc'
        },
        {
            id: 4,
            title: 'Chemistry Textbook 2023 Edition',
            price: 75.50,
            category: 'Textbooks',
            location: 'Library',
            image: 'https://images.unsplash.com/photo-1532012197267-da84d127e765?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60'
        }
    ];

    // Populate Featured Items on Home Page
    const featuredItemsContainer = document.getElementById('featured-items');
    if (featuredItemsContainer) {
        featuredItems.forEach(item => {
            const itemCard = document.createElement('div');
            itemCard.className = 'item-card';
            itemCard.innerHTML = `
                <div class="item-image">
                    <img src="${item.image}" alt="${item.title}">
                </div>
                <div class="item-info">
                    <h3 class="item-title">${item.title}</h3>
                    <p class="item-price">$${item.price.toFixed(2)}</p>
                    <div class="item-meta">
                        <span>${item.category}</span>
                        <span>${item.location}</span>
                    </div>
                </div>
            `;
            featuredItemsContainer.appendChild(itemCard);
        });
    }

    // Contact Form Submission
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            // In a real app, you'd send this data to your server/API
            const formData = new FormData(contactForm);
            const formValues = Object.fromEntries(formData.entries());
            
            console.log('Contact form submitted:', formValues);
            
            // Show success message and reset form
            alert('Thank you for your message. We will get back to you soon!');
            contactForm.reset();
        });
    }

    // Newsletter Form Submission
    const newsletterForms = document.querySelectorAll('#newsletter-form');
    if (newsletterForms.length > 0) {
        newsletterForms.forEach(form => {
            form.addEventListener('submit', function(event) {
                event.preventDefault();
                
                const email = form.querySelector('input[type="email"]').value;
                
                // In a real app, you'd send this to your server/API
                console.log('Newsletter subscription:', email);
                
                // Show success message and reset form
                alert('Thank you for subscribing to our newsletter!');
                form.reset();
            });
        });
    }

    // Sell Item Form
    const sellItemForm = document.getElementById('sell-item-form');
    const successModal = document.getElementById('success-modal');
    
    if (sellItemForm) {
        // Image Upload Preview
        const imageUploadContainer = document.getElementById('image-upload-container');
        const imagePreviewContainer = document.getElementById('image-preview-container');
        const imageInputs = document.querySelectorAll('.image-input');
        
        // Handle image uploads
        imageInputs.forEach((input, index) => {
            input.addEventListener('change', function(event) {
                const file = event.target.files[0];
                if (file && file.type.startsWith('image/')) {
                    // Create preview
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        // Create preview element
                        const preview = document.createElement('div');
                        preview.className = 'image-preview';
                        preview.innerHTML = `
                            <img src="${e.target.result}" alt="Image preview">
                            <span class="remove-image">&times;</span>
                        `;
                        
                        // Add remove functionality
                        preview.querySelector('.remove-image').addEventListener('click', function() {
                            input.value = '';
                            preview.remove();
                            
                            // Show the upload input again if it was the last one
                            const uploadDiv = document.querySelector(`.image-upload:nth-child(${index + 1})`);
                            if (uploadDiv) {
                                uploadDiv.style.display = 'block';
                            }
                        });
                        
                        imagePreviewContainer.appendChild(preview);
                        
                        // Hide the upload input
                        const uploadDiv = document.querySelector(`.image-upload:nth-child(${index + 1})`);
                        if (uploadDiv) {
                            uploadDiv.style.display = 'none';
                        }
                        
                        // Add another upload input if less than 5 images
                        const totalImages = document.querySelectorAll('.image-preview').length;
                        if (totalImages < 5 && document.querySelectorAll('.image-upload').length < 5) {
                            addImageUpload();
                        }
                    };
                    reader.readAsDataURL(file);
                }
            });
        });
        
        // Function to add new image upload
        function addImageUpload() {
            const uploadCount = document.querySelectorAll('.image-upload').length;
            if (uploadCount < 5) {
                const newUpload = document.createElement('div');
                newUpload.className = 'image-upload';
                newUpload.innerHTML = `
                    <label for="image${uploadCount + 1}" class="image-upload-label">
                        <span class="upload-icon">+</span>
                        <span>Upload Image</span>
                    </label>
                    <input type="file" id="image${uploadCount + 1}" name="image${uploadCount + 1}" accept="image/*" class="image-input">
                `;
                
                imageUploadContainer.appendChild(newUpload);
                
                // Add event listener to the new input
                const newInput = newUpload.querySelector('.image-input');
                newInput.addEventListener('change', function(event) {
                    const file = event.target.files[0];
                    if (file && file.type.startsWith('image/')) {
                        // Create preview
                        const reader = new FileReader();
                        reader.onload = function(e) {
                            // Create preview element
                            const preview = document.createElement('div');
                            preview.className = 'image-preview';
                            preview.innerHTML = `
                                <img src="${e.target.result}" alt="Image preview">
                                <span class="remove-image">&times;</span>
                            `;
                            
                            // Add remove functionality
                            preview.querySelector('.remove-image').addEventListener('click', function() {
                                newInput.value = '';
                                preview.remove();
                                newUpload.style.display = 'block';
                            });
                            
                            imagePreviewContainer.appendChild(preview);
                            
                            // Hide the upload input
                            newUpload.style.display = 'none';
                            
                            // Add another upload input if less than 5 images
                            const totalImages = document.querySelectorAll('.image-preview').length;
                            if (totalImages < 5 && document.querySelectorAll('.image-upload').length < 5) {
                                addImageUpload();
                            }
                        };
                        reader.readAsDataURL(file);
                    }
                });
            }
        }
        
        // Form submission
        sellItemForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            // Validate that at least one contact method is selected
            const contactMethods = document.querySelectorAll('input[name="contact-method"]:checked');
            if (contactMethods.length === 0) {
                alert('Please select at least one preferred contact method.');
                return;
            }
            
            // In a real app, you'd send this data to your server/API
            const formData = new FormData(sellItemForm);
            const formValues = Object.fromEntries(formData.entries());
            
            console.log('Item submitted:', formValues);
            
            // Show success modal
            if (successModal) {
                successModal.style.display = 'flex';
            } else {
                alert('Your item has been listed successfully!');
                sellItemForm.reset();
            }
        });
        
        // Clear form button
        const clearFormButton = document.getElementById('clear-form');
        if (clearFormButton) {
            clearFormButton.addEventListener('click', function() {
                sellItemForm.reset();
                
                // Clear image previews
                imagePreviewContainer.innerHTML = '';
                
                // Reset image uploads
                imageUploadContainer.innerHTML = '';
                const initialUpload = document.createElement('div');
                initialUpload.className = 'image-upload';
                initialUpload.innerHTML = `
                    <label for="image1" class="image-upload-label">
                        <span class="upload-icon">+</span>
                        <span>Upload Image</span>
                    </label>
                    <input type="file" id="image1" name="image1" accept="image/*" class="image-input">
                `;
                imageUploadContainer.appendChild(initialUpload);
                
                // Add event listener to the reset input
                const newInput = initialUpload.querySelector('.image-input');
                newInput.addEventListener('change', function(event) {
                    // Reuse the same change handler logic as above
                    const file = event.target.files[0];
                    if (file && file.type.startsWith('image/')) {
                        const reader = new FileReader();
                        reader.onload = function(e) {
                            const preview = document.createElement('div');
                            preview.className = 'image-preview';
                            preview.innerHTML = `
                                <img src="${e.target.result}" alt="Image preview">
                                <span class="remove-image">&times;</span>
                            `;
                            
                            preview.querySelector('.remove-image').addEventListener('click', function() {
                                newInput.value = '';
                                preview.remove();
                                initialUpload.style.display = 'block';
                            });
                            
                            imagePreviewContainer.appendChild(preview);
                            initialUpload.style.display = 'none';
                            
                            if (document.querySelectorAll('.image-preview').length < 5) {
                                addImageUpload();
                            }
                        };
                        reader.readAsDataURL(file);
                    }
                });
            });
        }
    }
    
    // Modal functionality
    const modal = document.getElementById('success-modal');
    if (modal) {
        const closeModal = document.querySelector('.close-modal');
        const modalCloseBtn = document.getElementById('modal-close-btn');
        
        function hideModal() {
            modal.style.display = 'none';
            // Redirect to home page in a real app
            window.location.href = 'index.html';
        }
        
        if (closeModal) {
            closeModal.addEventListener('click', hideModal);
        }
        
        if (modalCloseBtn) {
            modalCloseBtn.addEventListener('click', hideModal);
        }
        
        // Close modal when clicking outside
        window.addEventListener('click', function(event) {
            if (event.target === modal) {
                hideModal();
            }
        });
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(event) {
            if (this.getAttribute('href') !== '#') {
                event.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
});
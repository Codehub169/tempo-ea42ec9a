// Personal Budget Tracker - main.js

document.addEventListener('DOMContentLoaded', function() {
    // General UI enhancements or dynamic behaviors can be added here.

    // Example: Auto-dismiss flash messages after a few seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function(message) {
        // Add click event to close buttons if they exist
        const closeButton = message.querySelector('.close-flash');
        if (closeButton) {
            closeButton.addEventListener('click', function() {
                message.style.opacity = '0';
                setTimeout(() => message.remove(), 500); // Remove after fade out
            });
        }

        // Optional: Auto-dismiss after a delay (e.g., 5 seconds)
        // Uncomment the following lines to enable auto-dismiss
        /*
        setTimeout(function() {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 500); // Remove after fade out
        }, 5000);
        */
    });

    // Example: Add active class to current nav link based on URL
    const navLinks = document.querySelectorAll('.nav-link');
    const currentPath = window.location.pathname;

    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
        // Special handling for base path and /index or /dashboard
        if ((currentPath === '/' || currentPath === '/index') && link.getAttribute('href') === '/dashboard') {
             link.classList.add('active');
        }
    });

    // Toggle password visibility
    const togglePasswordButtons = document.querySelectorAll('.toggle-password');
    togglePasswordButtons.forEach(button => {
        button.addEventListener('click', function() {
            const passwordInput = this.previousElementSibling;
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                this.textContent = 'Hide'; // Or use an icon
            } else {
                passwordInput.type = 'password';
                this.textContent = 'Show'; // Or use an icon
            }
        });
    });

    console.log('Personal Budget Tracker JS Loaded');
});

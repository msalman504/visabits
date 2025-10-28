document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle functionality
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    const mobileMenuIcon = document.getElementById('mobile-menu-icon');
    
    if (mobileMenuButton && mobileMenu && mobileMenuIcon) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
            
            // Change icon from bars to X when menu is open
            if (mobileMenu.classList.contains('hidden')) {
                mobileMenuIcon.className = 'fas fa-bars text-xl';
            } else {
                mobileMenuIcon.className = 'fas fa-times text-xl';
            }
        });
    }
});


/**
 * Corporate Theme JavaScript
 * Handles corporate-specific interactions and animations
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Corporate theme loaded');
    
    // Initialize corporate theme features
    initializeCorporateAnimations();
    initializeCorporateInteractions();
    initializeCorporateCharts();
});

/**
 * Initialize corporate-specific animations
 */
function initializeCorporateAnimations() {
    // Animate content blocks on scroll
    const contentBlocks = document.querySelectorAll('.corporate-theme .content-block');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-corporate');
            }
        });
    }, {
        threshold: 0.1
    });
    
    contentBlocks.forEach(block => {
        observer.observe(block);
    });
    
    // Animate hero section elements
    const heroElements = document.querySelectorAll('.corporate-hero h1, .corporate-hero .lead, .corporate-hero .btn');
    heroElements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            element.style.transition = 'all 0.8s ease';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, index * 200);
    });
}

/**
 * Initialize corporate-specific interactions
 */
function initializeCorporateInteractions() {
    // Enhanced button hover effects
    const buttons = document.querySelectorAll('.corporate-theme .btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px) scale(1.05)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // Card hover effects
    const cards = document.querySelectorAll('.corporate-theme .card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 12px 25px rgba(0,0,0,0.2)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
        });
    });
    
    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Initialize corporate charts and data visualizations
 */
function initializeCorporateCharts() {
    // Simple progress bars animation
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const width = bar.style.width || bar.getAttribute('data-width') || '0%';
        bar.style.width = '0%';
        
        setTimeout(() => {
            bar.style.transition = 'width 2s ease-in-out';
            bar.style.width = width;
        }, 500);
    });
    
    // Animate counters
    const counters = document.querySelectorAll('[data-counter]');
    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-counter'));
        const duration = 2000;
        const increment = target / (duration / 16);
        let current = 0;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            counter.textContent = Math.floor(current).toLocaleString();
        }, 16);
    });
}

/**
 * Corporate theme utility functions
 */
const CorporateTheme = {
    // Show loading state
    showLoading: function(element) {
        element.classList.add('loading');
    },
    
    // Hide loading state
    hideLoading: function(element) {
        element.classList.remove('loading');
    },
    
    // Show notification
    showNotification: function(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.top = '20px';
        notification.style.right = '20px';
        notification.style.zIndex = '9999';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    },
    
    // Animate element entrance
    animateIn: function(element, delay = 0) {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            element.style.transition = 'all 0.6s ease';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, delay);
    }
};

// Export for use in other scripts
window.CorporateTheme = CorporateTheme;

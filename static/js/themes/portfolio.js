/**
 * Portfolio Theme JavaScript
 * Handles portfolio-specific interactions, animations, and gallery features
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Portfolio theme loaded');
    
    // Initialize portfolio theme features
    initializePortfolioAnimations();
    initializePortfolioInteractions();
    initializePortfolioGallery();
});

/**
 * Initialize portfolio-specific animations
 */
function initializePortfolioAnimations() {
    // Animate content blocks with creative timing
    const contentBlocks = document.querySelectorAll('.portfolio-theme .content-block');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add('fade-in-portfolio');
                    entry.target.style.transform = 'translateY(0) scale(1)';
                }, index * 150);
            }
        });
    }, {
        threshold: 0.1
    });
    
    contentBlocks.forEach(block => {
        block.style.transform = 'translateY(40px) scale(0.95)';
        observer.observe(block);
    });
    
    // Parallax effect for hero section
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const hero = document.querySelector('.portfolio-hero');
        if (hero) {
            hero.style.transform = `translateY(${scrolled * 0.5}px)`;
        }
    });
    
    // Floating animation for portfolio items
    const portfolioItems = document.querySelectorAll('.portfolio-item');
    portfolioItems.forEach((item, index) => {
        item.style.animationDelay = `${index * 0.2}s`;
        item.classList.add('float-animation');
    });
}

/**
 * Initialize portfolio-specific interactions
 */
function initializePortfolioInteractions() {
    // Enhanced hover effects for portfolio items
    const portfolioItems = document.querySelectorAll('.portfolio-item');
    portfolioItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-15px) scale(1.05)';
            this.style.boxShadow = '0 25px 50px rgba(0,0,0,0.3)';
            this.style.zIndex = '10';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            this.style.boxShadow = '0 8px 25px rgba(0,0,0,0.1)';
            this.style.zIndex = '1';
        });
    });
    
    // Interactive skill tags
    const skillTags = document.querySelectorAll('.skill-tag');
    skillTags.forEach(tag => {
        tag.addEventListener('click', function() {
            this.style.transform = 'scale(1.1)';
            this.style.boxShadow = '0 4px 15px rgba(232,62,140,0.4)';
            
            setTimeout(() => {
                this.style.transform = 'scale(1)';
                this.style.boxShadow = 'none';
            }, 200);
        });
    });
    
    // Smooth reveal for contact section
    const contactSection = document.querySelector('.contact-section');
    if (contactSection) {
        const contactObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        });
        
        contactSection.style.opacity = '0';
        contactSection.style.transform = 'translateY(50px)';
        contactSection.style.transition = 'all 1s ease';
        contactObserver.observe(contactSection);
    }
}

/**
 * Initialize portfolio gallery features
 */
function initializePortfolioGallery() {
    // Create lightbox for portfolio images
    createLightbox();
    
    // Filter functionality for portfolio items
    createPortfolioFilter();
    
    // Masonry layout for portfolio grid
    initializeMasonryLayout();
}

/**
 * Create lightbox for portfolio images
 */
function createLightbox() {
    const portfolioImages = document.querySelectorAll('.portfolio-item img');
    
    portfolioImages.forEach(img => {
        img.style.cursor = 'pointer';
        img.addEventListener('click', function() {
            PortfolioTheme.openLightbox(this.src, this.alt);
        });
    });
}

/**
 * Create portfolio filter functionality
 */
function createPortfolioFilter() {
    const portfolioGrid = document.querySelector('.portfolio-grid');
    if (!portfolioGrid) return;
    
    // Extract unique categories from portfolio items
    const categories = new Set();
    const portfolioItems = document.querySelectorAll('.portfolio-item');
    
    portfolioItems.forEach(item => {
        const category = item.getAttribute('data-category') || 'all';
        categories.add(category);
    });
    
    if (categories.size <= 1) return;
    
    // Create filter buttons
    const filterContainer = document.createElement('div');
    filterContainer.className = 'portfolio-filter';
    filterContainer.style.cssText = `
        text-align: center;
        margin-bottom: 3rem;
    `;
    
    const allButton = document.createElement('button');
    allButton.className = 'btn btn-outline-primary active';
    allButton.textContent = 'All';
    allButton.onclick = () => PortfolioTheme.filterPortfolio('all');
    filterContainer.appendChild(allButton);
    
    categories.forEach(category => {
        if (category !== 'all') {
            const button = document.createElement('button');
            button.className = 'btn btn-outline-primary';
            button.textContent = category.charAt(0).toUpperCase() + category.slice(1);
            button.onclick = () => PortfolioTheme.filterPortfolio(category);
            filterContainer.appendChild(button);
        }
    });
    
    portfolioGrid.parentNode.insertBefore(filterContainer, portfolioGrid);
}

/**
 * Initialize masonry layout
 */
function initializeMasonryLayout() {
    const grid = document.querySelector('.portfolio-grid');
    if (!grid) return;
    
    // Simple masonry-like effect with CSS Grid
    grid.style.display = 'grid';
    grid.style.gridTemplateColumns = 'repeat(auto-fit, minmax(300px, 1fr))';
    grid.style.gridAutoRows = 'masonry'; // Future CSS feature
    grid.style.gap = '2rem';
}

/**
 * Portfolio theme utility functions
 */
const PortfolioTheme = {
    // Open lightbox
    openLightbox: function(src, alt) {
        const lightbox = document.createElement('div');
        lightbox.className = 'portfolio-lightbox';
        lightbox.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.9);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            opacity: 0;
            transition: opacity 0.3s ease;
        `;
        
        const img = document.createElement('img');
        img.src = src;
        img.alt = alt;
        img.style.cssText = `
            max-width: 90%;
            max-height: 90%;
            object-fit: contain;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        `;
        
        const closeBtn = document.createElement('button');
        closeBtn.innerHTML = '&times;';
        closeBtn.style.cssText = `
            position: absolute;
            top: 20px;
            right: 30px;
            background: none;
            border: none;
            color: white;
            font-size: 3rem;
            cursor: pointer;
            z-index: 10000;
        `;
        
        closeBtn.onclick = () => this.closeLightbox(lightbox);
        lightbox.onclick = (e) => {
            if (e.target === lightbox) this.closeLightbox(lightbox);
        };
        
        lightbox.appendChild(img);
        lightbox.appendChild(closeBtn);
        document.body.appendChild(lightbox);
        
        // Animate in
        setTimeout(() => {
            lightbox.style.opacity = '1';
        }, 10);
        
        // Prevent body scroll
        document.body.style.overflow = 'hidden';
    },
    
    // Close lightbox
    closeLightbox: function(lightbox) {
        lightbox.style.opacity = '0';
        setTimeout(() => {
            if (lightbox.parentNode) {
                lightbox.remove();
            }
            document.body.style.overflow = '';
        }, 300);
    },
    
    // Filter portfolio items
    filterPortfolio: function(category) {
        const items = document.querySelectorAll('.portfolio-item');
        const buttons = document.querySelectorAll('.portfolio-filter .btn');
        
        // Update active button
        buttons.forEach(btn => btn.classList.remove('active'));
        event.target.classList.add('active');
        
        // Filter items
        items.forEach(item => {
            const itemCategory = item.getAttribute('data-category') || 'all';
            
            if (category === 'all' || itemCategory === category) {
                item.style.display = 'block';
                item.style.opacity = '0';
                item.style.transform = 'scale(0.8)';
                
                setTimeout(() => {
                    item.style.transition = 'all 0.5s ease';
                    item.style.opacity = '1';
                    item.style.transform = 'scale(1)';
                }, Math.random() * 200);
            } else {
                item.style.opacity = '0';
                item.style.transform = 'scale(0.8)';
                setTimeout(() => {
                    item.style.display = 'none';
                }, 300);
            }
        });
    },
    
    // Animate element with custom effect
    animateElement: function(element, effect = 'fadeIn') {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            element.style.transition = 'all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, 100);
    },
    
    // Create particle effect
    createParticles: function(container) {
        for (let i = 0; i < 20; i++) {
            const particle = document.createElement('div');
            particle.style.cssText = `
                position: absolute;
                width: 4px;
                height: 4px;
                background: var(--portfolio-accent);
                border-radius: 50%;
                pointer-events: none;
                opacity: 0.7;
                animation: float 3s ease-in-out infinite;
                animation-delay: ${Math.random() * 3}s;
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
            `;
            
            container.appendChild(particle);
        }
    }
};

// Export for use in other scripts
window.PortfolioTheme = PortfolioTheme;

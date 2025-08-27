/**
 * Base JavaScript for Mullet Method Demo
 * 
 * This file provides common functionality across all themes and sites
 * in the database-driven multi-site architecture.
 */

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initializeDemo();
});

/**
 * Initialize demo functionality
 */
function initializeDemo() {
    // Add smooth scrolling to anchor links
    initializeSmoothScrolling();
    
    // Add loading states to forms
    initializeFormHandling();
    
    // Add animation to content blocks
    initializeContentAnimations();
    
    // Add demo-specific features
    initializeDemoFeatures();
    
    // Initialize theme-specific features
    initializeThemeFeatures();
    
    console.log('Mullet Method Demo initialized');
}

/**
 * Add smooth scrolling to anchor links
 */
function initializeSmoothScrolling() {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Add loading states to forms
 */
function initializeFormHandling() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitButton = form.querySelector('button[type="submit"]');
            
            if (submitButton) {
                // Add loading state
                submitButton.disabled = true;
                submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Loading...';
                
                // Remove loading state after 3 seconds (demo purposes)
                setTimeout(() => {
                    submitButton.disabled = false;
                    submitButton.innerHTML = submitButton.dataset.originalText || 'Submit';
                }, 3000);
            }
        });
        
        // Store original button text
        const submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) {
            submitButton.dataset.originalText = submitButton.innerHTML;
        }
    });
}

/**
 * Add animations to content blocks as they come into view
 */
function initializeContentAnimations() {
    // Check if Intersection Observer is supported
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });
        
        // Observe all content blocks
        const contentBlocks = document.querySelectorAll('.content-block');
        contentBlocks.forEach(block => {
            observer.observe(block);
        });
    }
}

/**
 * Initialize demo-specific features
 */
function initializeDemoFeatures() {
    // Add site switcher functionality
    addSiteSwitcher();
    
    // Add architecture info tooltip
    addArchitectureTooltips();
    
    // Add copy-to-clipboard for code examples
    addCodeCopyButtons();
}

/**
 * Add site switcher in the corner for easy navigation
 */
function addSiteSwitcher() {
    // Only add on demo pages, not on the main index
    if (window.location.pathname === '/') return;
    
    const switcher = document.createElement('div');
    switcher.className = 'site-switcher';
    switcher.innerHTML = `
        <div class="switcher-toggle">
            <i class="fas fa-exchange-alt"></i>
        </div>
        <div class="switcher-menu">
            <h6>Switch Demo Site</h6>
            <a href="/corporate" class="switcher-link corporate">
                <i class="fas fa-building"></i> Corporate
            </a>
            <a href="/blog" class="switcher-link blog">
                <i class="fas fa-blog"></i> Blog
            </a>
            <a href="/portfolio" class="switcher-link portfolio">
                <i class="fas fa-palette"></i> Portfolio
            </a>
            <hr>
            <a href="/" class="switcher-link home">
                <i class="fas fa-home"></i> Demo Home
            </a>
        </div>
    `;
    
    // Add styles
    const style = document.createElement('style');
    style.textContent = `
        .site-switcher {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1050;
        }
        
        .switcher-toggle {
            width: 50px;
            height: 50px;
            background: rgba(0,0,0,0.7);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .switcher-toggle:hover {
            background: rgba(0,0,0,0.9);
            transform: scale(1.1);
        }
        
        .switcher-menu {
            position: absolute;
            top: 60px;
            right: 0;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            padding: 20px;
            min-width: 200px;
            opacity: 0;
            visibility: hidden;
            transform: translateY(-10px);
            transition: all 0.3s ease;
        }
        
        .site-switcher.active .switcher-menu {
            opacity: 1;
            visibility: visible;
            transform: translateY(0);
        }
        
        .switcher-menu h6 {
            margin-bottom: 15px;
            color: #495057;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .switcher-link {
            display: block;
            padding: 10px 15px;
            color: #495057;
            text-decoration: none;
            border-radius: 8px;
            margin-bottom: 5px;
            transition: all 0.3s ease;
        }
        
        .switcher-link:hover {
            background: #f8f9fa;
            color: #007bff;
            transform: translateX(5px);
        }
        
        .switcher-link.corporate:hover { color: #007bff; }
        .switcher-link.blog:hover { color: #6f42c1; }
        .switcher-link.portfolio:hover { color: #e83e8c; }
        .switcher-link.home:hover { color: #28a745; }
        
        @media (max-width: 768px) {
            .site-switcher {
                top: 10px;
                right: 10px;
            }
            
            .switcher-toggle {
                width: 40px;
                height: 40px;
            }
            
            .switcher-menu {
                right: -10px;
                min-width: 180px;
            }
        }
    `;
    
    document.head.appendChild(style);
    document.body.appendChild(switcher);
    
    // Add click handler
    const toggle = switcher.querySelector('.switcher-toggle');
    toggle.addEventListener('click', () => {
        switcher.classList.toggle('active');
    });
    
    // Close when clicking outside
    document.addEventListener('click', (e) => {
        if (!switcher.contains(e.target)) {
            switcher.classList.remove('active');
        }
    });
}

/**
 * Add tooltips explaining the architecture
 */
function addArchitectureTooltips() {
    // Add tooltip to powered by link
    const poweredByLinks = document.querySelectorAll('a[href="/"]');
    poweredByLinks.forEach(link => {
        if (link.textContent.includes('Mullet Method')) {
            link.title = 'Database-driven routing: This page was resolved through database lookups, not hardcoded routes!';
        }
    });
}

/**
 * Add copy buttons to code examples
 */
function addCodeCopyButtons() {
    const codeBlocks = document.querySelectorAll('.content-block-code pre, .code-example');
    
    codeBlocks.forEach(block => {
        const button = document.createElement('button');
        button.className = 'copy-code-btn';
        button.innerHTML = '<i class="fas fa-copy"></i>';
        button.title = 'Copy code';
        
        button.addEventListener('click', () => {
            const code = block.textContent;
            navigator.clipboard.writeText(code).then(() => {
                button.innerHTML = '<i class="fas fa-check"></i>';
                button.style.color = '#28a745';
                
                setTimeout(() => {
                    button.innerHTML = '<i class="fas fa-copy"></i>';
                    button.style.color = '';
                }, 2000);
            });
        });
        
        // Add styles for copy button
        if (!document.querySelector('#copy-button-styles')) {
            const style = document.createElement('style');
            style.id = 'copy-button-styles';
            style.textContent = `
                .content-block-code, .code-example {
                    position: relative;
                }
                
                .copy-code-btn {
                    position: absolute;
                    top: 10px;
                    right: 10px;
                    background: rgba(0,0,0,0.7);
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 10px;
                    cursor: pointer;
                    font-size: 0.8rem;
                    transition: all 0.3s ease;
                }
                
                .copy-code-btn:hover {
                    background: rgba(0,0,0,0.9);
                }
            `;
            document.head.appendChild(style);
        }
        
        block.style.position = 'relative';
        block.appendChild(button);
    });
}

/**
 * Initialize theme-specific features based on body class
 */
function initializeThemeFeatures() {
    const body = document.body;
    
    if (body.classList.contains('corporate-theme')) {
        initializeCorporateFeatures();
    } else if (body.classList.contains('blog-theme')) {
        initializeBlogFeatures();
    } else if (body.classList.contains('portfolio-theme')) {
        initializePortfolioFeatures();
    }
}

/**
 * Corporate theme specific features
 */
function initializeCorporateFeatures() {
    // Add hover effects to feature boxes
    const featureBoxes = document.querySelectorAll('.feature-box');
    featureBoxes.forEach(box => {
        box.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });
        
        box.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
}

/**
 * Blog theme specific features
 */
function initializeBlogFeatures() {
    // Add reading progress bar
    addReadingProgressBar();
    
    // Add estimated reading time
    addReadingTime();
}

/**
 * Portfolio theme specific features
 */
function initializePortfolioFeatures() {
    // Add parallax effect to hero section
    addParallaxEffect();
    
    // Add skill bar animations
    animateSkillBars();
}

/**
 * Add reading progress bar for blog posts
 */
function addReadingProgressBar() {
    if (!document.body.classList.contains('blog-theme')) return;
    
    const progressBar = document.createElement('div');
    progressBar.className = 'reading-progress';
    progressBar.innerHTML = '<div class="reading-progress-fill"></div>';
    
    const style = document.createElement('style');
    style.textContent = `
        .reading-progress {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: rgba(111, 66, 193, 0.2);
            z-index: 1000;
        }
        
        .reading-progress-fill {
            height: 100%;
            background: #6f42c1;
            width: 0%;
            transition: width 0.3s ease;
        }
    `;
    
    document.head.appendChild(style);
    document.body.appendChild(progressBar);
    
    // Update progress on scroll
    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrollPercent = (scrollTop / docHeight) * 100;
        
        const fill = progressBar.querySelector('.reading-progress-fill');
        fill.style.width = Math.min(scrollPercent, 100) + '%';
    });
}

/**
 * Add estimated reading time to blog posts
 */
function addReadingTime() {
    const content = document.querySelector('.blog-post-content');
    if (!content) return;
    
    const text = content.textContent;
    const wordsPerMinute = 200;
    const wordCount = text.split(/\s+/).length;
    const readingTime = Math.ceil(wordCount / wordsPerMinute);
    
    const timeElements = document.querySelectorAll('.meta-item:last-child');
    timeElements.forEach(element => {
        if (element.textContent.includes('min read')) {
            element.innerHTML = `<i class="fas fa-clock me-1"></i>${readingTime} min read`;
        }
    });
}

/**
 * Add parallax effect to portfolio hero
 */
function addParallaxEffect() {
    const hero = document.querySelector('.portfolio-hero');
    if (!hero) return;
    
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const rate = scrolled * -0.5;
        hero.style.transform = `translateY(${rate}px)`;
    });
}

/**
 * Animate skill bars when they come into view
 */
function animateSkillBars() {
    const skillBars = document.querySelectorAll('.skill-fill');
    
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const fill = entry.target;
                    const width = fill.style.width;
                    fill.style.width = '0%';
                    
                    setTimeout(() => {
                        fill.style.width = width;
                    }, 100);
                    
                    observer.unobserve(fill);
                }
            });
        });
        
        skillBars.forEach(bar => observer.observe(bar));
    }
}

// Export functions for potential use by theme-specific scripts
window.MulletDemo = {
    initializeDemo,
    initializeSmoothScrolling,
    initializeFormHandling,
    initializeContentAnimations
};

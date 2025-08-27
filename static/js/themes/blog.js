/**
 * Blog Theme JavaScript
 * Handles blog-specific interactions and reading experience enhancements
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Blog theme loaded');
    
    // Initialize blog theme features
    initializeBlogAnimations();
    initializeBlogInteractions();
    initializeReadingExperience();
});

/**
 * Initialize blog-specific animations
 */
function initializeBlogAnimations() {
    // Animate content blocks with staggered timing
    const contentBlocks = document.querySelectorAll('.blog-theme .content-block');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add('fade-in-blog');
                }, index * 100);
            }
        });
    }, {
        threshold: 0.1
    });
    
    contentBlocks.forEach(block => {
        observer.observe(block);
    });
    
    // Animate hero section with typewriter effect
    const heroTitle = document.querySelector('.blog-hero h1');
    if (heroTitle) {
        const text = heroTitle.textContent;
        heroTitle.textContent = '';
        heroTitle.style.opacity = '1';
        
        let i = 0;
        const typeWriter = () => {
            if (i < text.length) {
                heroTitle.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 100);
            }
        };
        
        setTimeout(typeWriter, 500);
    }
}

/**
 * Initialize blog-specific interactions
 */
function initializeBlogInteractions() {
    // Enhanced reading progress indicator
    createReadingProgressBar();
    
    // Smooth hover effects for cards
    const cards = document.querySelectorAll('.blog-theme .card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
            this.style.boxShadow = '0 12px 30px rgba(0,0,0,0.2)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 4px 15px rgba(0,0,0,0.08)';
        });
    });
    
    // Interactive navigation underlines
    const navLinks = document.querySelectorAll('.blog-header .nav-link');
    navLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            const underline = this.querySelector('::after') || this;
            underline.style.width = '100%';
        });
    });
    
    // Quote highlighting
    const blockquotes = document.querySelectorAll('.blog-theme blockquote');
    blockquotes.forEach(quote => {
        quote.addEventListener('click', function() {
            this.style.background = 'linear-gradient(135deg, #f8f9fa 0%, #e3f2fd 100%)';
            this.style.borderLeftColor = '#2196f3';
            
            setTimeout(() => {
                this.style.background = '#f8f9fa';
                this.style.borderLeftColor = 'var(--blog-accent)';
            }, 2000);
        });
    });
}

/**
 * Initialize reading experience enhancements
 */
function initializeReadingExperience() {
    // Estimated reading time calculator
    calculateReadingTime();
    
    // Table of contents generator
    generateTableOfContents();
    
    // Social sharing buttons
    addSocialSharing();
    
    // Font size adjuster
    addFontSizeControls();
}

/**
 * Create reading progress bar
 */
function createReadingProgressBar() {
    const progressBar = document.createElement('div');
    progressBar.id = 'reading-progress';
    progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 0%;
        height: 3px;
        background: var(--blog-gradient);
        z-index: 9999;
        transition: width 0.3s ease;
    `;
    
    document.body.appendChild(progressBar);
    
    window.addEventListener('scroll', () => {
        const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        progressBar.style.width = scrolled + '%';
    });
}

/**
 * Calculate and display reading time
 */
function calculateReadingTime() {
    const content = document.querySelector('.content-block-body');
    if (!content) return;
    
    const text = content.textContent || content.innerText;
    const wordsPerMinute = 200;
    const words = text.trim().split(/\s+/).length;
    const readingTime = Math.ceil(words / wordsPerMinute);
    
    const readingTimeElement = document.createElement('div');
    readingTimeElement.className = 'reading-time';
    readingTimeElement.innerHTML = `
        <i class="fas fa-clock"></i>
        ${readingTime} min read
    `;
    readingTimeElement.style.cssText = `
        color: var(--blog-secondary);
        font-size: 0.9rem;
        margin-bottom: 1rem;
        font-style: italic;
    `;
    
    const header = document.querySelector('.content-block-header');
    if (header) {
        header.appendChild(readingTimeElement);
    }
}

/**
 * Generate table of contents
 */
function generateTableOfContents() {
    const headings = document.querySelectorAll('.content-block-body h1, .content-block-body h2, .content-block-body h3');
    if (headings.length < 3) return;
    
    const toc = document.createElement('div');
    toc.className = 'table-of-contents';
    toc.innerHTML = '<h4>Table of Contents</h4>';
    
    const tocList = document.createElement('ul');
    tocList.style.cssText = `
        list-style: none;
        padding-left: 0;
        margin-top: 1rem;
    `;
    
    headings.forEach((heading, index) => {
        const id = `heading-${index}`;
        heading.id = id;
        
        const listItem = document.createElement('li');
        listItem.style.marginBottom = '0.5rem';
        
        const link = document.createElement('a');
        link.href = `#${id}`;
        link.textContent = heading.textContent;
        link.style.cssText = `
            color: var(--blog-primary);
            text-decoration: none;
            font-size: 0.9rem;
            transition: color 0.3s ease;
        `;
        
        link.addEventListener('click', function(e) {
            e.preventDefault();
            heading.scrollIntoView({ behavior: 'smooth' });
        });
        
        listItem.appendChild(link);
        tocList.appendChild(listItem);
    });
    
    toc.appendChild(tocList);
    toc.style.cssText = `
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 2rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 4px solid var(--blog-primary);
    `;
    
    const firstContentBlock = document.querySelector('.content-block-body');
    if (firstContentBlock) {
        firstContentBlock.insertBefore(toc, firstContentBlock.firstChild);
    }
}

/**
 * Add social sharing buttons
 */
function addSocialSharing() {
    const shareContainer = document.createElement('div');
    shareContainer.className = 'social-sharing';
    shareContainer.innerHTML = `
        <h5>Share this post</h5>
        <div class="share-buttons">
            <button class="btn btn-outline-primary btn-sm" onclick="BlogTheme.shareOn('twitter')">
                <i class="fab fa-twitter"></i> Twitter
            </button>
            <button class="btn btn-outline-primary btn-sm" onclick="BlogTheme.shareOn('facebook')">
                <i class="fab fa-facebook"></i> Facebook
            </button>
            <button class="btn btn-outline-primary btn-sm" onclick="BlogTheme.shareOn('linkedin')">
                <i class="fab fa-linkedin"></i> LinkedIn
            </button>
        </div>
    `;
    
    shareContainer.style.cssText = `
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 2rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 4px solid var(--blog-accent);
        text-align: center;
    `;
    
    const contentBlock = document.querySelector('.content-block-body');
    if (contentBlock) {
        contentBlock.appendChild(shareContainer);
    }
}

/**
 * Add font size controls
 */
function addFontSizeControls() {
    const fontControls = document.createElement('div');
    fontControls.className = 'font-size-controls';
    fontControls.innerHTML = `
        <span>Font size:</span>
        <button class="btn btn-sm btn-outline-secondary" onclick="BlogTheme.adjustFontSize(-1)">A-</button>
        <button class="btn btn-sm btn-outline-secondary" onclick="BlogTheme.adjustFontSize(1)">A+</button>
        <button class="btn btn-sm btn-outline-secondary" onclick="BlogTheme.resetFontSize()">Reset</button>
    `;
    
    fontControls.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        z-index: 1000;
    `;
    
    document.body.appendChild(fontControls);
}

/**
 * Blog theme utility functions
 */
const BlogTheme = {
    currentFontSize: 1.1,
    
    // Share on social media
    shareOn: function(platform) {
        const url = encodeURIComponent(window.location.href);
        const title = encodeURIComponent(document.title);
        
        let shareUrl;
        switch(platform) {
            case 'twitter':
                shareUrl = `https://twitter.com/intent/tweet?url=${url}&text=${title}`;
                break;
            case 'facebook':
                shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${url}`;
                break;
            case 'linkedin':
                shareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${url}`;
                break;
        }
        
        if (shareUrl) {
            window.open(shareUrl, '_blank', 'width=600,height=400');
        }
    },
    
    // Adjust font size
    adjustFontSize: function(delta) {
        this.currentFontSize += delta * 0.1;
        this.currentFontSize = Math.max(0.8, Math.min(1.6, this.currentFontSize));
        
        const contentBody = document.querySelector('.content-block-body');
        if (contentBody) {
            contentBody.style.fontSize = this.currentFontSize + 'rem';
        }
    },
    
    // Reset font size
    resetFontSize: function() {
        this.currentFontSize = 1.1;
        const contentBody = document.querySelector('.content-block-body');
        if (contentBody) {
            contentBody.style.fontSize = this.currentFontSize + 'rem';
        }
    }
};

// Export for use in other scripts
window.BlogTheme = BlogTheme;

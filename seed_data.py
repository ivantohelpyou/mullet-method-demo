#!/home/ivanadamin/mullet-method-demo-standalone/.venv/bin/python
"""
Seed Data Script for Mullet Method Demo

This script populates the database with sample data for three different demo sites:
1. Corporate business website
2. Personal technology blog
3. Creative portfolio site

Each site demonstrates different themes, content types, and navigation structures
while being served by the same Flask application through database-driven routing.
"""

import sys
from pathlib import Path
from datetime import datetime, timezone

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from app import create_app
from models import db, Site, Page, ContentBlock, NavigationItem
from config import get_script_config


def create_sample_data():
    """Create sample data for all three demo sites."""
    
    print("Creating sample data for Mullet Method Demo...")
    
    # Create sites
    corporate_site = create_corporate_site()
    blog_site = create_blog_site()
    portfolio_site = create_portfolio_site()
    
    # Commit all changes
    db.session.commit()
    
    print(f"✅ Created {Site.query.count()} sites")
    print(f"✅ Created {Page.query.count()} pages")
    print(f"✅ Created {ContentBlock.query.count()} content blocks")
    print(f"✅ Created {NavigationItem.query.count()} navigation items")
    print("\n🎉 Sample data creation complete!")
    print("\nDemo sites available at:")
    print("- Corporate: http://localhost:5000/corporate")
    print("- Blog: http://localhost:5000/blog")
    print("- Portfolio: http://localhost:5000/portfolio")


def create_corporate_site():
    """Create the corporate business website."""
    
    print("Creating corporate site...")
    
    # Create site
    site = Site(
        path_prefix='corporate',
        name='Acme Corporation',
        description='Professional business website showcasing services and expertise',
        template_theme='corporate',
        config={
            'colors': {
                'primary': '#007bff',
                'secondary': '#6c757d',
                'success': '#28a745'
            },
            'layout': {
                'header_style': 'fixed',
                'sidebar': False
            },
            'features': ['contact_form', 'newsletter', 'testimonials']
        }
    )
    db.session.add(site)
    db.session.flush()  # Get the site ID
    
    # Create navigation
    nav_items = [
        NavigationItem(site_id=site.id, label='Home', url='home', order_index=1),
        NavigationItem(site_id=site.id, label='About', url='about', order_index=2),
        NavigationItem(site_id=site.id, label='Services', url='services', order_index=3),
        NavigationItem(site_id=site.id, label='Contact', url='contact', order_index=4),
    ]
    for nav_item in nav_items:
        db.session.add(nav_item)
    
    # Create pages
    create_corporate_pages(site)
    
    return site


def create_corporate_pages(site):
    """Create pages for the corporate site."""
    
    # Home page
    home_page = Page(
        site_id=site.id,
        path='home',
        title='Welcome to Acme Corporation',
        description='Leading provider of innovative business solutions',
        content_type='landing_page'
    )
    db.session.add(home_page)
    db.session.flush()
    
    home_blocks = [
        ContentBlock(page_id=home_page.id, block_type='html', order_index=1,
                    title='Hero Section',
                    content='<div class="hero"><h1>Innovative Business Solutions</h1><p class="lead">We help businesses transform and grow through cutting-edge technology and strategic consulting.</p><a href="/corporate/contact" class="btn btn-primary">Get Started</a></div>'),
        ContentBlock(page_id=home_page.id, block_type='text', order_index=2,
                    title='Our Mission',
                    content='At Acme Corporation, we believe in empowering businesses to reach their full potential. Our team of experts combines deep industry knowledge with innovative technology solutions to deliver exceptional results for our clients.'),
        ContentBlock(page_id=home_page.id, block_type='list', order_index=3,
                    title='Why Choose Us',
                    content='20+ years of industry experience\nProven track record with Fortune 500 companies\n24/7 customer support\nCutting-edge technology solutions\nCustomized approach for each client'),
    ]
    
    # About page
    about_page = Page(
        site_id=site.id,
        path='about',
        title='About Acme Corporation',
        description='Learn about our company history, values, and team',
        content_type='standard'
    )
    db.session.add(about_page)
    db.session.flush()
    
    about_blocks = [
        ContentBlock(page_id=about_page.id, block_type='text', order_index=1,
                    title='Our Story',
                    content='Founded in 2000, Acme Corporation has grown from a small startup to a leading provider of business solutions. Our journey began with a simple mission: to help businesses leverage technology for competitive advantage.'),
        ContentBlock(page_id=about_page.id, block_type='quote', order_index=2,
                    content='Innovation is not just about technology—it\'s about transforming the way businesses operate and serve their customers.'),
        ContentBlock(page_id=about_page.id, block_type='text', order_index=3,
                    title='Our Values',
                    content='We are committed to excellence, integrity, and innovation in everything we do. Our team of dedicated professionals works tirelessly to ensure our clients achieve their business objectives.'),
    ]
    
    # Services page
    services_page = Page(
        site_id=site.id,
        path='services',
        title='Our Services',
        description='Comprehensive business solutions tailored to your needs',
        content_type='standard'
    )
    db.session.add(services_page)
    db.session.flush()
    
    services_blocks = [
        ContentBlock(page_id=services_page.id, block_type='text', order_index=1,
                    title='Service Overview',
                    content='We offer a comprehensive suite of services designed to help businesses of all sizes achieve their goals. From strategic consulting to technology implementation, we have the expertise to drive your success.'),
        ContentBlock(page_id=services_page.id, block_type='list', order_index=2,
                    title='Strategic Consulting',
                    content='Business strategy development\nMarket analysis and research\nOperational efficiency optimization\nDigital transformation planning'),
        ContentBlock(page_id=services_page.id, block_type='list', order_index=3,
                    title='Technology Solutions',
                    content='Custom software development\nCloud migration and management\nData analytics and business intelligence\nCybersecurity and compliance'),
        ContentBlock(page_id=services_page.id, block_type='list', order_index=4,
                    title='Support Services',
                    content='24/7 technical support\nTraining and knowledge transfer\nOngoing maintenance and updates\nPerformance monitoring and optimization'),
    ]
    
    # Contact page
    contact_page = Page(
        site_id=site.id,
        path='contact',
        title='Contact Us',
        description='Get in touch with our team of experts',
        content_type='standard'
    )
    db.session.add(contact_page)
    db.session.flush()
    
    contact_blocks = [
        ContentBlock(page_id=contact_page.id, block_type='text', order_index=1,
                    title='Get In Touch',
                    content='Ready to transform your business? Our team of experts is here to help. Contact us today to discuss your needs and learn how we can help you achieve your goals.'),
        ContentBlock(page_id=contact_page.id, block_type='html', order_index=2,
                    title='Contact Information',
                    content='<div class="contact-info"><h3>Contact Information</h3><p><strong>Phone:</strong> (555) 123-4567</p><p><strong>Email:</strong> info@acmecorp.com</p><p><strong>Address:</strong> 123 Business Ave, Suite 100<br>Corporate City, CC 12345</p></div>'),
        ContentBlock(page_id=contact_page.id, block_type='html', order_index=3,
                    title='Business Hours',
                    content='<div class="hours"><h3>Business Hours</h3><p>Monday - Friday: 9:00 AM - 6:00 PM</p><p>Saturday: 10:00 AM - 4:00 PM</p><p>Sunday: Closed</p></div>'),
    ]
    
    # Add all content blocks
    for blocks in [home_blocks, about_blocks, services_blocks, contact_blocks]:
        for block in blocks:
            db.session.add(block)


def create_blog_site():
    """Create the personal technology blog."""
    
    print("Creating blog site...")
    
    # Create site
    site = Site(
        path_prefix='blog',
        name='Tech Insights Blog',
        description='Personal blog about web development, AI, and technology trends',
        template_theme='blog',
        config={
            'colors': {
                'primary': '#6f42c1',
                'secondary': '#495057',
                'accent': '#fd7e14'
            },
            'layout': {
                'sidebar': True,
                'header_style': 'simple'
            },
            'features': ['comments', 'tags', 'archive', 'search']
        }
    )
    db.session.add(site)
    db.session.flush()
    
    # Create navigation
    nav_items = [
        NavigationItem(site_id=site.id, label='Home', url='home', order_index=1),
        NavigationItem(site_id=site.id, label='Recent Posts', url='recent', order_index=2),
        NavigationItem(site_id=site.id, label='Archive', url='archive', order_index=3),
        NavigationItem(site_id=site.id, label='About', url='about', order_index=4),
    ]
    for nav_item in nav_items:
        db.session.add(nav_item)
    
    # Create pages
    create_blog_pages(site)
    
    return site


def create_blog_pages(site):
    """Create pages for the blog site."""
    
    # Home page
    home_page = Page(
        site_id=site.id,
        path='home',
        title='Tech Insights Blog',
        description='Exploring the latest in web development, AI, and technology',
        content_type='blog_post'
    )
    db.session.add(home_page)
    db.session.flush()
    
    home_blocks = [
        ContentBlock(page_id=home_page.id, block_type='text', order_index=1,
                    title='Welcome',
                    content='Welcome to Tech Insights, where we explore the cutting edge of technology, web development, and artificial intelligence. Join me on this journey as we dive deep into the tools, techniques, and trends shaping our digital future.'),
        ContentBlock(page_id=home_page.id, block_type='list', order_index=2,
                    title='Recent Posts',
                    content='Database-Driven Architecture: The Mullet Method\nBuilding Scalable Flask Applications\nAI-Powered Content Management Systems\nThe Future of Web Development\nMicroservices vs Monoliths: A Practical Guide'),
    ]
    
    # Recent posts page
    recent_page = Page(
        site_id=site.id,
        path='recent',
        title='Recent Posts',
        description='Latest blog posts and articles',
        content_type='blog_post'
    )
    db.session.add(recent_page)
    db.session.flush()
    
    recent_blocks = [
        ContentBlock(page_id=recent_page.id, block_type='html', order_index=1,
                    title='Latest Article',
                    content='<article><h2>Database-Driven Architecture: The Mullet Method</h2><p class="meta">Published on March 15, 2024</p><p>Discover how to build scalable web applications using database-driven routing. This architectural pattern allows a single application to serve multiple completely different websites...</p><a href="#" class="read-more">Read More</a></article>'),
        ContentBlock(page_id=recent_page.id, block_type='html', order_index=2,
                    title='Previous Article',
                    content='<article><h2>Building Scalable Flask Applications</h2><p class="meta">Published on March 10, 2024</p><p>Learn best practices for structuring Flask applications that can grow with your needs. From blueprints to database design, we cover it all...</p><a href="#" class="read-more">Read More</a></article>'),
    ]
    
    # About page
    about_page = Page(
        site_id=site.id,
        path='about',
        title='About the Author',
        description='Learn about the person behind Tech Insights Blog',
        content_type='standard'
    )
    db.session.add(about_page)
    db.session.flush()
    
    about_blocks = [
        ContentBlock(page_id=about_page.id, block_type='text', order_index=1,
                    title='About Me',
                    content='Hi! I\'m a passionate software developer with over 10 years of experience in web development, database design, and system architecture. I love exploring new technologies and sharing what I learn with the community.'),
        ContentBlock(page_id=about_page.id, block_type='list', order_index=2,
                    title='Expertise',
                    content='Python and Flask development\nDatabase design and optimization\nCloud architecture and deployment\nAI and machine learning integration\nOpen source contributions'),
        ContentBlock(page_id=about_page.id, block_type='quote', order_index=3,
                    content='The best way to learn is to build, break, and rebuild. Every failure is a step toward mastery.'),
    ]
    
    # Add all content blocks
    for blocks in [home_blocks, recent_blocks, about_blocks]:
        for block in blocks:
            db.session.add(block)


def create_portfolio_site():
    """Create the creative portfolio site."""
    
    print("Creating portfolio site...")
    
    # Create site
    site = Site(
        path_prefix='portfolio',
        name='Creative Portfolio',
        description='Showcasing design and development projects',
        template_theme='portfolio',
        config={
            'colors': {
                'primary': '#e83e8c',
                'secondary': '#343a40',
                'accent': '#20c997'
            },
            'layout': {
                'header_style': 'overlay',
                'sidebar': False
            },
            'features': ['gallery', 'lightbox', 'animations', 'contact']
        }
    )
    db.session.add(site)
    db.session.flush()
    
    # Create navigation
    nav_items = [
        NavigationItem(site_id=site.id, label='Home', url='home', order_index=1),
        NavigationItem(site_id=site.id, label='Projects', url='projects', order_index=2),
        NavigationItem(site_id=site.id, label='Gallery', url='gallery', order_index=3),
        NavigationItem(site_id=site.id, label='Resume', url='resume', order_index=4),
        NavigationItem(site_id=site.id, label='Contact', url='contact', order_index=5),
    ]
    for nav_item in nav_items:
        db.session.add(nav_item)
    
    # Create pages
    create_portfolio_pages(site)
    
    return site


def create_portfolio_pages(site):
    """Create pages for the portfolio site."""
    
    # Home page
    home_page = Page(
        site_id=site.id,
        path='home',
        title='Creative Portfolio',
        description='Designer and developer portfolio showcasing innovative projects',
        content_type='portfolio_item'
    )
    db.session.add(home_page)
    db.session.flush()
    
    home_blocks = [
        ContentBlock(page_id=home_page.id, block_type='html', order_index=1,
                    title='Hero',
                    content='<div class="portfolio-hero"><h1>Creative Designer & Developer</h1><p class="lead">Bringing ideas to life through innovative design and cutting-edge technology</p></div>'),
        ContentBlock(page_id=home_page.id, block_type='text', order_index=2,
                    title='About',
                    content='I\'m a creative professional who bridges the gap between design and technology. With a passion for user experience and technical excellence, I create digital solutions that are both beautiful and functional.'),
    ]
    
    # Projects page
    projects_page = Page(
        site_id=site.id,
        path='projects',
        title='Featured Projects',
        description='A showcase of recent design and development work',
        content_type='portfolio_item'
    )
    db.session.add(projects_page)
    db.session.flush()
    
    projects_blocks = [
        ContentBlock(page_id=projects_page.id, block_type='html', order_index=1,
                    title='Project 1',
                    content='<div class="project"><h3>E-commerce Platform Redesign</h3><p>Complete redesign and development of a modern e-commerce platform with improved user experience and mobile responsiveness.</p><div class="tech-stack">React • Node.js • MongoDB • Stripe</div></div>'),
        ContentBlock(page_id=projects_page.id, block_type='html', order_index=2,
                    title='Project 2',
                    content='<div class="project"><h3>AI-Powered Content Management System</h3><p>Custom CMS with AI-assisted content creation and automated SEO optimization for content creators and marketers.</p><div class="tech-stack">Python • Flask • OpenAI API • PostgreSQL</div></div>'),
        ContentBlock(page_id=projects_page.id, block_type='html', order_index=3,
                    title='Project 3',
                    content='<div class="project"><h3>Mobile App for Local Businesses</h3><p>Cross-platform mobile application helping local businesses connect with customers and manage their online presence.</p><div class="tech-stack">React Native • Firebase • Stripe • Google Maps API</div></div>'),
    ]
    
    # Resume page
    resume_page = Page(
        site_id=site.id,
        path='resume',
        title='Resume',
        description='Professional experience and skills',
        content_type='standard'
    )
    db.session.add(resume_page)
    db.session.flush()
    
    resume_blocks = [
        ContentBlock(page_id=resume_page.id, block_type='text', order_index=1,
                    title='Professional Summary',
                    content='Creative designer and full-stack developer with 8+ years of experience creating digital solutions for startups and established companies. Expertise in user experience design, web development, and project management.'),
        ContentBlock(page_id=resume_page.id, block_type='list', order_index=2,
                    title='Technical Skills',
                    content='Frontend: React, Vue.js, HTML5, CSS3, JavaScript\nBackend: Python, Node.js, Flask, Django, Express\nDatabases: PostgreSQL, MongoDB, Redis\nCloud: AWS, Google Cloud, Docker, Kubernetes\nDesign: Figma, Adobe Creative Suite, Sketch'),
        ContentBlock(page_id=resume_page.id, block_type='list', order_index=3,
                    title='Experience Highlights',
                    content='Led design and development of 20+ web applications\nManaged cross-functional teams of 5-10 people\nImproved user engagement by 40% through UX optimization\nReduced development time by 30% through process improvements'),
    ]
    
    # Add all content blocks
    for blocks in [home_blocks, projects_blocks, resume_blocks]:
        for block in blocks:
            db.session.add(block)


if __name__ == '__main__':
    # Create Flask app and database
    app = create_app(get_script_config())
    
    with app.app_context():
        # Drop and recreate all tables
        print("Initializing database...")
        db.drop_all()
        db.create_all()
        
        # Create sample data
        create_sample_data()
        
        print("\n🚀 Database initialized successfully!")
        print("Run 'python app.py' to start the demo application.")

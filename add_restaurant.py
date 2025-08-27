#!/usr/bin/env python3
"""
Add New Restaurant Site Dynamically

Usage: python add_restaurant.py "Restaurant Name" "Description"
Example: python add_restaurant.py "Mario's Pizzeria" "Authentic New York style pizza since 1952"

This script demonstrates the power of database-driven routing by adding
a new restaurant site WITHOUT any code changes to the main application.
"""

import sys
import os
import re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, Site, Page, ContentBlock, NavigationItem

def create_path_prefix(name):
    """Convert restaurant name to a URL-safe path prefix."""
    # Remove special characters and convert to lowercase
    prefix = re.sub(r'[^a-zA-Z0-9\s]', '', name)
    # Replace spaces with hyphens
    prefix = re.sub(r'\s+', '-', prefix.strip())
    # Convert to lowercase
    prefix = prefix.lower()
    # Limit length
    if len(prefix) > 20:
        prefix = prefix[:20].rstrip('-')
    return prefix

def add_restaurant_site(name, description):
    """Add a new restaurant site using the provided name and description."""
    
    path_prefix = create_path_prefix(name)
    
    print(f"🍽️  Adding new restaurant site: {name}")
    print(f"   Path: /{path_prefix}")
    print(f"   Description: {description}")
    print("   (No code changes required!)")
    print()
    
    # Check if site already exists
    existing_site = Site.query.filter_by(path_prefix=path_prefix).first()
    if existing_site:
        print(f"❌ Site with path '/{path_prefix}' already exists!")
        print(f"   Existing site: {existing_site.name}")
        return False
    
    # Create the new site
    site = Site(
        path_prefix=path_prefix,
        name=name,
        description=description,
        template_theme='corporate',  # Reuse existing template
        config={
            'colors': {
                'primary': '#d4691a',      # Warm orange
                'secondary': '#2c5530',    # Deep green  
                'accent': '#f4e4c1'        # Cream
            },
            'layout': {
                'header_style': 'centered',
                'sidebar': False
            },
            'features': ['reservations', 'menu', 'gallery']
        }
    )
    db.session.add(site)
    db.session.flush()  # Get the site ID
    
    # Create navigation
    nav_items = [
        NavigationItem(site_id=site.id, label='Home', url='home', order_index=1),
        NavigationItem(site_id=site.id, label='Menu', url='menu', order_index=2),
        NavigationItem(site_id=site.id, label='About', url='about', order_index=3),
        NavigationItem(site_id=site.id, label='Reservations', url='reservations', order_index=4),
    ]
    for nav_item in nav_items:
        db.session.add(nav_item)
    
    # Create pages
    pages_data = [
        {
            'path': 'home',
            'title': name,
            'description': description,
            'content_type': 'standard'
        },
        {
            'path': 'menu',
            'title': 'Our Menu',
            'description': f'Delicious dishes at {name}',
            'content_type': 'standard'
        },
        {
            'path': 'about',
            'title': 'About Us',
            'description': f'Learn about the story behind {name}',
            'content_type': 'standard'
        },
        {
            'path': 'reservations',
            'title': 'Make a Reservation',
            'description': f'Book your table at {name}',
            'content_type': 'standard'
        }
    ]
    
    pages = []
    for page_data in pages_data:
        page = Page(
            site_id=site.id,
            path=page_data['path'],
            title=page_data['title'],
            description=page_data['description'],
            content_type=page_data['content_type']
        )
        db.session.add(page)
        pages.append(page)
    
    db.session.flush()  # Get page IDs
    
    # Add content blocks
    home_page = pages[0]
    menu_page = pages[1]
    about_page = pages[2]
    reservations_page = pages[3]
    
    # Home page content
    home_blocks = [
        ContentBlock(page_id=home_page.id, block_type='text', title=f'Welcome to {name}',
                    content=f'{description}. Join us for an exceptional dining experience with carefully crafted dishes and warm hospitality.',
                    order_index=1),
        ContentBlock(page_id=home_page.id, block_type='list', title=f'Why Choose {name}',
                    content='Fresh, high-quality ingredients\nExceptional service and atmosphere\nCarefully crafted menu\nWelcoming environment for all occasions\nCommitment to culinary excellence',
                    order_index=2),
    ]
    
    # Menu page content
    menu_blocks = [
        ContentBlock(page_id=menu_page.id, block_type='text', title='Our Signature Dishes',
                    content=f'At {name}, every dish is prepared with passion and attention to detail using the finest ingredients.',
                    order_index=1),
        ContentBlock(page_id=menu_page.id, block_type='list', title='Featured Items',
                    content='Chef\'s Special of the Day - Market Price\nSignature Appetizer Platter - $18\nHouse Specialty Entree - $26\nSeasonal Dessert Selection - $12',
                    order_index=2),
        ContentBlock(page_id=menu_page.id, block_type='text', title='Dietary Options',
                    content='We offer vegetarian, vegan, and gluten-free options. Please inform your server of any dietary restrictions.',
                    order_index=3),
    ]
    
    # About page content
    about_blocks = [
        ContentBlock(page_id=about_page.id, block_type='text', title='Our Story',
                    content=f'{name} was founded with a passion for exceptional cuisine and hospitality. We believe that great food brings people together and creates lasting memories.',
                    order_index=1),
        ContentBlock(page_id=about_page.id, block_type='quote', title=None,
                    content='Great food is not just about taste—it\'s about creating experiences that bring joy to every moment.',
                    order_index=2),
    ]
    
    # Reservations page content
    reservations_blocks = [
        ContentBlock(page_id=reservations_page.id, block_type='text', title='Book Your Table',
                    content=f'We invite you to join us at {name} for an unforgettable dining experience. Reservations are recommended, especially for weekend evenings.',
                    order_index=1),
        ContentBlock(page_id=reservations_page.id, block_type='html', title='Contact Information',
                    content=f'<div class="contact-info"><h3>Reservations</h3><p><strong>Phone:</strong> (555) 123-DINE</p><p><strong>Email:</strong> reservations@{path_prefix.replace("-", "")}.com</p><p><strong>Address:</strong> 123 Restaurant Row<br>Culinary District, NY 10001</p></div>',
                    order_index=2),
    ]
    
    # Add all content blocks
    all_blocks = home_blocks + menu_blocks + about_blocks + reservations_blocks
    for block in all_blocks:
        db.session.add(block)
    
    # Commit all changes
    db.session.commit()
    
    print("✅ Restaurant site added successfully!")
    print(f"🌐 New site available at: http://localhost:5000/{path_prefix}")
    print("📄 Pages created:")
    print(f"   - http://localhost:5000/{path_prefix}/home")
    print(f"   - http://localhost:5000/{path_prefix}/menu") 
    print(f"   - http://localhost:5000/{path_prefix}/about")
    print(f"   - http://localhost:5000/{path_prefix}/reservations")
    print()
    print("🎯 KEY POINT: No code changes were needed!")
    print("   - No new route functions")
    print("   - No application restart required")
    print("   - Just database changes")
    
    return True

def main():
    """Main function to add the new restaurant site."""
    if len(sys.argv) != 3:
        print("Usage: python add_restaurant.py \"Restaurant Name\" \"Description\"")
        print("Example: python add_restaurant.py \"Mario's Pizzeria\" \"Authentic New York style pizza since 1952\"")
        sys.exit(1)
    
    name = sys.argv[1]
    description = sys.argv[2]
    
    if not name.strip():
        print("❌ Restaurant name cannot be empty!")
        sys.exit(1)
    
    if not description.strip():
        print("❌ Description cannot be empty!")
        sys.exit(1)
    
    app = create_app()
    
    with app.app_context():
        success = add_restaurant_site(name, description)
        if not success:
            sys.exit(1)

if __name__ == '__main__':
    main()

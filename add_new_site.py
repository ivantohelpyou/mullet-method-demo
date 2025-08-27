#!/home/ivanadamin/mullet-method-demo-standalone/.venv/bin/python
"""
Live Demo: Add New Site Dynamically

This script demonstrates the power of database-driven routing by adding
a new site WITHOUT any code changes to the main application.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, Site, Page, ContentBlock, NavigationItem
from config import get_script_config

def add_restaurant_site():
    """Add a new restaurant site using existing templates."""
    
    print("🍕 Adding new restaurant site dynamically...")
    print("   (No code changes required!)")
    
    # Create the new site
    site = Site(
        path_prefix='restaurant',
        name='Bella Vista Restaurant',
        description='Authentic Italian cuisine in the heart of the city',
        template_theme='restaurant',  # Use restaurant-specific template
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
            'title': 'Bella Vista Restaurant',
            'description': 'Authentic Italian cuisine in the heart of the city',
            'content_type': 'standard'
        },
        {
            'path': 'menu',
            'title': 'Our Menu',
            'description': 'Delicious Italian dishes made with fresh ingredients',
            'content_type': 'standard'
        },
        {
            'path': 'about',
            'title': 'About Us',
            'description': 'Our story and passion for Italian cuisine',
            'content_type': 'standard'
        },
        {
            'path': 'reservations',
            'title': 'Make a Reservation',
            'description': 'Book your table for an unforgettable dining experience',
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
        ContentBlock(page_id=home_page.id, block_type='text', title='Welcome to Bella Vista',
                    content='Experience authentic Italian cuisine in an elegant atmosphere. Our family recipes have been passed down through generations, bringing you the true taste of Italy.',
                    order_index=1),
        ContentBlock(page_id=home_page.id, block_type='list', title='Why Choose Bella Vista',
                    content='Fresh ingredients imported from Italy\nFamily recipes from Tuscany\nWarm, welcoming atmosphere\nExtensive wine selection\nPrivate dining rooms available',
                    order_index=2),
    ]
    
    # Menu page content
    menu_blocks = [
        ContentBlock(page_id=menu_page.id, block_type='text', title='Our Signature Dishes',
                    content='From handmade pasta to wood-fired pizzas, every dish is crafted with passion and the finest ingredients.',
                    order_index=1),
        ContentBlock(page_id=menu_page.id, block_type='list', title='Appetizers',
                    content='Bruschetta Classica - $12\nAntipasto Misto - $18\nCarpaccio di Manzo - $16\nCaprese Salad - $14',
                    order_index=2),
        ContentBlock(page_id=menu_page.id, block_type='list', title='Main Courses',
                    content='Spaghetti Carbonara - $22\nOsso Buco alla Milanese - $32\nRisotto ai Porcini - $24\nBranzino al Sale - $28',
                    order_index=3),
    ]
    
    # About page content
    about_blocks = [
        ContentBlock(page_id=about_page.id, block_type='text', title='Our Story',
                    content='Founded in 1985 by the Rossi family, Bella Vista has been serving authentic Italian cuisine for over three decades. Our commitment to quality and tradition has made us a beloved destination for food lovers.',
                    order_index=1),
        ContentBlock(page_id=about_page.id, block_type='quote', title=None,
                    content='Cooking is not just about feeding the body, but nourishing the soul with love and tradition.',
                    order_index=2),
    ]
    
    # Reservations page content
    reservations_blocks = [
        ContentBlock(page_id=reservations_page.id, block_type='text', title='Book Your Table',
                    content='Join us for an unforgettable dining experience. We recommend making reservations, especially for weekend evenings.',
                    order_index=1),
        ContentBlock(page_id=reservations_page.id, block_type='html', title='Contact Information',
                    content='<div class="contact-info"><h3>Reservations</h3><p><strong>Phone:</strong> (555) 123-FOOD</p><p><strong>Email:</strong> reservations@bellavista.com</p><p><strong>Address:</strong> 456 Italian Way<br>Little Italy, NY 10013</p></div>',
                    order_index=2),
    ]
    
    # Add all content blocks
    all_blocks = home_blocks + menu_blocks + about_blocks + reservations_blocks
    for block in all_blocks:
        db.session.add(block)
    
    # Commit all changes
    db.session.commit()
    
    print("✅ Restaurant site added successfully!")
    print("🌐 New site available at: http://localhost:5000/restaurant")
    print("📄 Pages created:")
    print("   - http://localhost:5000/restaurant/home")
    print("   - http://localhost:5000/restaurant/menu") 
    print("   - http://localhost:5000/restaurant/about")
    print("   - http://localhost:5000/restaurant/reservations")
    print()
    print("🎯 KEY POINT: No code changes were needed!")
    print("   - No new route functions")
    print("   - No application restart required")
    print("   - Just database changes")


def main():
    """Main function to add the new site."""
    app = create_app(get_script_config())
    
    with app.app_context():
        # Check if restaurant site already exists
        existing_site = Site.query.filter_by(path_prefix='restaurant').first()
        if existing_site:
            print("🍕 Restaurant site already exists!")
            print("🌐 Visit: http://localhost:5000/restaurant")
            return
        
        add_restaurant_site()


if __name__ == '__main__':
    main()

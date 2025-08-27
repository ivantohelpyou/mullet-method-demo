#!/home/ivanadamin/mullet-method-demo-standalone/.venv/bin/python
"""
Add Template Script for Mullet Method Demo

Creates industry-specific theme templates by copying and customizing existing themes.
This ensures that restaurant sites don't show "Industry Leader" and "Expert Team" content.

Usage: python add_template.py <base_theme> <new_theme> <industry>
Example: python add_template.py corporate restaurant restaurant
Example: python add_template.py corporate retail retail
Example: python add_template.py blog news news

This script demonstrates how the Mullet Method can support unlimited themes
without any code changes to the main application.
"""

import sys
import os
import shutil
from pathlib import Path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_restaurant_template(base_theme='corporate', new_theme='restaurant'):
    """Create a restaurant-specific template from the corporate theme."""
    
    print(f"🍽️  Creating {new_theme} theme from {base_theme} theme")
    print("   (Customizing content for restaurant industry)")
    print()
    
    # Define paths
    base_path = Path('templates/themes') / base_theme
    new_path = Path('templates/themes') / new_theme
    
    # Check if base theme exists
    if not base_path.exists():
        print(f"❌ Base theme '{base_theme}' not found at {base_path}")
        return False
    
    # Check if new theme already exists
    if new_path.exists():
        print(f"⚠️  Theme '{new_theme}' already exists at {new_path}")
        response = input("Overwrite? (y/N): ").strip().lower()
        if response != 'y':
            print("❌ Cancelled")
            return False
        shutil.rmtree(new_path)
    
    # Copy the base theme
    print(f"📁 Copying {base_theme} theme to {new_theme}...")
    shutil.copytree(base_path, new_path)
    
    # Customize the layout.html for restaurants
    layout_file = new_path / 'layout.html'
    if layout_file.exists():
        print(f"🎨 Customizing {new_theme} layout for restaurant industry...")
        
        with open(layout_file, 'r') as f:
            content = f.read()
        
        # Replace corporate-specific content with restaurant content
        restaurant_content = content.replace(
            # Replace the hard-coded corporate features section
            '''        <!-- Corporate features section (only on home page) -->
        {% if page and page.path == 'home' %}
        <div class="corporate-features">
            <div class="row">
                <div class="col-md-4 mb-4">
                    <div class="feature-box">
                        <div class="feature-icon">
                            <i class="fas fa-award"></i>
                        </div>
                        <h4>Industry Leader</h4>
                        <p>20+ years of proven excellence in delivering innovative business solutions.</p>
                    </div>
                </div>
                <div class="col-md-4 mb-4">
                    <div class="feature-box">
                        <div class="feature-icon">
                            <i class="fas fa-users"></i>
                        </div>
                        <h4>Expert Team</h4>
                        <p>Dedicated professionals with deep expertise across multiple industries.</p>
                    </div>
                </div>
                <div class="col-md-4 mb-4">
                    <div class="feature-box">
                        <div class="feature-icon">
                            <i class="fas fa-headset"></i>
                        </div>
                        <h4>24/7 Support</h4>
                        <p>Round-the-clock customer support to ensure your success.</p>
                    </div>
                </div>
            </div>
        </div>''',
            # With restaurant-specific features
            '''        <!-- Restaurant features section (only on home page) -->
        {% if page and page.path == 'home' %}
        <div class="restaurant-features">
            <div class="row">
                <div class="col-md-4 mb-4">
                    <div class="feature-box">
                        <div class="feature-icon">
                            <i class="fas fa-utensils"></i>
                        </div>
                        <h4>Fresh Ingredients</h4>
                        <p>We source the finest, freshest ingredients daily to ensure exceptional quality.</p>
                    </div>
                </div>
                <div class="col-md-4 mb-4">
                    <div class="feature-box">
                        <div class="feature-icon">
                            <i class="fas fa-chef-hat"></i>
                        </div>
                        <h4>Expert Chefs</h4>
                        <p>Our experienced culinary team brings passion and expertise to every dish.</p>
                    </div>
                </div>
                <div class="col-md-4 mb-4">
                    <div class="feature-box">
                        <div class="feature-icon">
                            <i class="fas fa-heart"></i>
                        </div>
                        <h4>Family Atmosphere</h4>
                        <p>Warm, welcoming environment perfect for family dining and special occasions.</p>
                    </div>
                </div>
            </div>
        </div>'''
        ).replace(
            # Replace corporate CTA section
            '''        <!-- Call-to-action section -->
        <div class="corporate-cta">
            <div class="row">
                <div class="col-12 text-center">
                    <div class="cta-box">
                        <h3>Ready to Transform Your Business?</h3>
                        <p class="lead">Let our experts help you achieve your goals with innovative solutions.</p>
                        <a href="/{{ site.path_prefix }}/contact" class="btn btn-primary btn-lg">
                            <i class="fas fa-rocket me-2"></i>Get Started Today
                        </a>
                    </div>
                </div>
            </div>
        </div>''',
            # With restaurant CTA
            '''        <!-- Call-to-action section -->
        <div class="restaurant-cta">
            <div class="row">
                <div class="col-12 text-center">
                    <div class="cta-box">
                        <h3>Ready for an Unforgettable Dining Experience?</h3>
                        <p class="lead">Reserve your table today and taste the difference quality makes.</p>
                        <a href="/{{ site.path_prefix }}/reservations" class="btn btn-primary btn-lg">
                            <i class="fas fa-calendar-alt me-2"></i>Make Reservation
                        </a>
                    </div>
                </div>
            </div>
        </div>'''
        ).replace(
            # Replace footer services
            '''                <h6>Services</h6>
                <ul class="list-unstyled">
                    <li><a href="/{{ site.path_prefix }}/services" class="text-white-50">Consulting</a></li>
                    <li><a href="/{{ site.path_prefix }}/services" class="text-white-50">Technology</a></li>
                    <li><a href="/{{ site.path_prefix }}/services" class="text-white-50">Support</a></li>
                </ul>''',
            # With restaurant menu items
            '''                <h6>Menu</h6>
                <ul class="list-unstyled">
                    <li><a href="/{{ site.path_prefix }}/menu" class="text-white-50">Appetizers</a></li>
                    <li><a href="/{{ site.path_prefix }}/menu" class="text-white-50">Main Courses</a></li>
                    <li><a href="/{{ site.path_prefix }}/menu" class="text-white-50">Desserts</a></li>
                </ul>'''
        ).replace(
            # Replace generic contact info
            '''                <p class="text-white-50 mb-1">
                    <i class="fas fa-phone me-2"></i>(555) 123-4567
                </p>
                <p class="text-white-50 mb-1">
                    <i class="fas fa-envelope me-2"></i>info@acmecorp.com
                </p>
                <p class="text-white-50">
                    <i class="fas fa-map-marker-alt me-2"></i>123 Business Ave, Corporate City
                </p>''',
            # With restaurant contact info
            '''                <p class="text-white-50 mb-1">
                    <i class="fas fa-phone me-2"></i>(555) 123-FOOD
                </p>
                <p class="text-white-50 mb-1">
                    <i class="fas fa-envelope me-2"></i>info@restaurant.com
                </p>
                <p class="text-white-50">
                    <i class="fas fa-map-marker-alt me-2"></i>123 Culinary Street, Food District
                </p>'''
        ).replace(
            # Update CSS class names
            'corporate-features',
            'restaurant-features'
        ).replace(
            'corporate-cta',
            'restaurant-cta'
        ).replace(
            # Update navigation button
            'Get Quote',
            'Reservations'
        ).replace(
            # Update hero buttons
            'Our Services',
            'View Menu'
        ).replace(
            '/services',
            '/menu'
        )
        
        # Write the customized content
        with open(layout_file, 'w') as f:
            f.write(restaurant_content)
    
    print(f"✅ Restaurant theme created successfully!")
    print(f"📁 Theme location: {new_path}")
    print()
    print("🎯 KEY POINT: No code changes were needed!")
    print("   - No new route functions")
    print("   - No application restart required")
    print("   - Just template files")
    print()
    print("🍽️  Restaurant-specific customizations:")
    print("   - Fresh Ingredients (instead of Industry Leader)")
    print("   - Expert Chefs (instead of Expert Team)")
    print("   - Family Atmosphere (instead of 24/7 Support)")
    print("   - Make Reservation CTA (instead of Get Started)")
    print("   - Menu links (instead of Services)")
    print("   - Restaurant contact info")
    
    return True

def main():
    """Main function to create the template."""
    if len(sys.argv) < 4:
        print("Usage: python add_template.py <base_theme> <new_theme> <industry>")
        print("Example: python add_template.py corporate restaurant restaurant")
        print("Example: python add_template.py corporate retail retail")
        print("Example: python add_template.py blog news news")
        print()
        print("Available base themes:")
        themes_dir = Path('templates/themes')
        if themes_dir.exists():
            for theme in themes_dir.iterdir():
                if theme.is_dir():
                    print(f"   - {theme.name}")
        sys.exit(1)
    
    base_theme = sys.argv[1].strip()
    new_theme = sys.argv[2].strip()
    industry = sys.argv[3].strip()
    
    if not base_theme or not new_theme or not industry:
        print("❌ All arguments are required!")
        sys.exit(1)
    
    # For now, only support restaurant industry
    if industry.lower() == 'restaurant':
        success = create_restaurant_template(base_theme, new_theme)
    else:
        print(f"❌ Industry '{industry}' not yet supported.")
        print("Currently supported: restaurant")
        print("Coming soon: retail, healthcare, education, etc.")
        sys.exit(1)
    
    if not success:
        sys.exit(1)

if __name__ == '__main__':
    main()

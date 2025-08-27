#!/home/ivanadamin/mullet-method-demo-standalone/.venv/bin/python
"""
Show all sites in the database - demonstrates database-driven routing
"""

import sys
import os
import logging
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Disable SQLAlchemy logging for cleaner output
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

from app import create_app
from models import Site, Page
from config import get_script_config

def show_sites():
    """Display all sites and their pages from the database."""
    
    print("🗄️  Database-Driven Sites:")
    print("=" * 50)
    
    sites = Site.query.filter_by(is_active=True).all()
    
    if not sites:
        print("No sites found in database.")
        return
    
    for site in sites:
        print(f"\n🌐 {site.name}")
        print(f"   Path: /{site.path_prefix}")
        print(f"   Theme: {site.template_theme}")
        print(f"   Description: {site.description}")
        
        # Show pages for this site
        pages = Page.query.filter_by(site_id=site.id, is_active=True).all()
        print(f"   Pages ({len(pages)}):")
        for page in pages:
            print(f"     - /{site.path_prefix}/{page.path} → {page.title}")
    
    print("\n" + "=" * 50)
    print(f"✅ Total: {len(sites)} sites, all served by ONE Flask route!")
    print("🎯 Key Point: Adding new sites = database changes only")

def main():
    """Main function."""
    app = create_app(get_script_config())
    
    with app.app_context():
        show_sites()

if __name__ == '__main__':
    main()

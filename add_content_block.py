#!/home/ivanadamin/mullet-method-demo-standalone/.venv/bin/python
"""
Add Content Block to Existing Page

Usage: python add_content_block.py <site_prefix> <page_path> <block_type> <title> <content>
Example: python add_content_block.py corporate home text "Welcome" "This is our homepage content"
Example: python add_content_block.py blog home list "Features" "Fast loading\nSEO optimized\nMobile responsive"

Supported block types: text, html, list, quote, code, image, video, gallery

This script demonstrates the power of database-driven content management
by adding new content blocks WITHOUT any code changes to the main application.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, Site, Page, ContentBlock
from config import get_script_config

# Supported content block types
SUPPORTED_TYPES = ['text', 'html', 'list', 'quote', 'code', 'image', 'video', 'gallery']

def add_content_block(site_prefix, page_path, block_type, title, content):
    """Add a content block to the specified page."""
    
    print(f"📝 Adding {block_type} block to /{site_prefix}/{page_path}")
    print(f"   Title: {title}")
    print("   (No code changes required!)")
    print()
    
    # Validate block type
    if block_type not in SUPPORTED_TYPES:
        print(f"❌ Unsupported block type: {block_type}")
        print(f"Supported types: {', '.join(SUPPORTED_TYPES)}")
        return False
    
    # Find the site
    site = Site.query.filter_by(path_prefix=site_prefix, is_active=True).first()
    if not site:
        print(f"❌ Site with path '/{site_prefix}' not found!")
        print("Available sites:")
        sites = Site.query.filter_by(is_active=True).all()
        for s in sites:
            print(f"   - {s.path_prefix} ({s.name})")
        return False
    
    # Find the page
    page = Page.query.filter_by(site_id=site.id, path=page_path, is_active=True).first()
    if not page:
        print(f"❌ Page '/{page_path}' not found in site '{site.name}'!")
        print("Available pages:")
        pages = Page.query.filter_by(site_id=site.id, is_active=True).all()
        for p in pages:
            print(f"   - {p.path} ({p.title})")
        return False
    
    print(f"✅ Found site: {site.name}")
    print(f"✅ Found page: {page.title}")
    print()
    
    # Get the next order index
    max_order = db.session.query(db.func.max(ContentBlock.order_index)).filter_by(
        page_id=page.id, is_active=True
    ).scalar() or 0
    next_order = max_order + 1
    
    # Process content based on block type
    processed_content = process_content_by_type(content, block_type)
    block_config = get_block_config(block_type)
    
    # Create content block
    content_block = ContentBlock(
        page_id=page.id,
        block_type=block_type,
        title=title if title.strip() else None,
        content=processed_content,
        order_index=next_order,
        config=block_config
    )
    
    db.session.add(content_block)
    db.session.commit()
    
    print("✅ Content block added successfully!")
    print(f"🌐 View the updated page at: http://localhost:5000/{site_prefix}/{page_path}")
    print()
    print("🎯 KEY POINT: No code changes were needed!")
    print("   - No new route functions")
    print("   - No application restart required")
    print("   - Just database changes")
    print()
    print("📋 Block Details:")
    print(f"   - Type: {content_block.block_type}")
    print(f"   - Title: {content_block.title or '(no title)'}")
    print(f"   - Order: {content_block.order_index}")
    print(f"   - Page: {page.title} ({site.name})")
    print(f"   - Content length: {len(processed_content)} characters")
    
    return True

def process_content_by_type(content, block_type):
    """Process content based on block type."""

    if block_type == 'list':
        # Convert escaped newlines to actual newlines, then process
        content = content.replace('\\n', '\n')
        items = [item.strip() for item in content.split('\n') if item.strip()]
        return '\n'.join(items)

    elif block_type == 'quote':
        # Process escaped newlines and wrap in quote formatting
        content = content.replace('\\n', '\n')
        return content.strip()

    elif block_type == 'code':
        # Process escaped newlines and preserve code formatting
        content = content.replace('\\n', '\n')
        return content

    elif block_type == 'html':
        # Process escaped newlines for HTML content
        content = content.replace('\\n', '\n')
        return content

    else:
        # For text, image, video, gallery - process escaped newlines
        content = content.replace('\\n', '\n')
        return content.strip()

def get_block_config(block_type):
    """Get default configuration for block type."""
    
    configs = {
        'list': {
            'list_style': 'bulleted',
            'show_icons': True
        },
        'quote': {
            'style': 'blockquote',
            'show_attribution': False
        },
        'code': {
            'language': 'auto',
            'show_line_numbers': False,
            'theme': 'default'
        },
        'image': {
            'alt_text': '',
            'caption': '',
            'alignment': 'center'
        },
        'video': {
            'autoplay': False,
            'controls': True,
            'width': '100%'
        },
        'gallery': {
            'columns': 3,
            'show_captions': True,
            'lightbox': True
        }
    }
    
    return configs.get(block_type, {})

def show_usage():
    """Show usage information and examples."""
    print("Usage: python add_content_block.py <site_prefix> <page_path> <block_type> <title> <content>")
    print()
    print("Arguments:")
    print("  site_prefix  - Site path prefix (e.g., 'corporate', 'blog', 'portfolio')")
    print("  page_path    - Page path within site (e.g., 'home', 'about', 'contact')")
    print("  block_type   - Type of content block")
    print("  title        - Block title (use quotes if contains spaces, or '' for no title)")
    print("  content      - Block content (use quotes if contains spaces)")
    print()
    print(f"Supported block types: {', '.join(SUPPORTED_TYPES)}")
    print()
    print("Examples:")
    print('  python add_content_block.py corporate home text "Welcome" "This is our homepage"')
    print('  python add_content_block.py blog home list "Features" "Fast loading\\nSEO optimized\\nMobile responsive"')
    print('  python add_content_block.py portfolio home quote "" "Design is not just what it looks like - design is how it works."')
    print('  python add_content_block.py corporate about code "Example" "def hello():\\n    print(\\"Hello World\\")"')

def main():
    """Main function to add the content block."""
    if len(sys.argv) != 6:
        show_usage()
        print()
        print("Available sites and pages:")
        
        # Show available sites and pages
        try:
            app = create_app(get_script_config())
            with app.app_context():
                sites = Site.query.filter_by(is_active=True).all()
                for site in sites:
                    print(f"   📁 {site.path_prefix} ({site.name})")
                    pages = Page.query.filter_by(site_id=site.id, is_active=True).all()
                    for page in pages:
                        print(f"      └─ {page.path} ({page.title})")
        except Exception as e:
            print(f"   (Could not load sites: {e})")
        
        sys.exit(1)
    
    site_prefix = sys.argv[1].strip()
    page_path = sys.argv[2].strip()
    block_type = sys.argv[3].strip().lower()
    title = sys.argv[4].strip()
    content = sys.argv[5]
    
    # Validate inputs
    if not site_prefix:
        print("❌ Site path prefix cannot be empty!")
        sys.exit(1)
    
    if not page_path:
        print("❌ Page path cannot be empty!")
        sys.exit(1)
    
    if not block_type:
        print("❌ Block type cannot be empty!")
        sys.exit(1)
    
    if not content.strip():
        print("❌ Content cannot be empty!")
        sys.exit(1)
    
    app = create_app(get_script_config())
    
    with app.app_context():
        success = add_content_block(site_prefix, page_path, block_type, title, content)
        if not success:
            sys.exit(1)

if __name__ == '__main__':
    main()

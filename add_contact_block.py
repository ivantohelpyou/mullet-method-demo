#!/home/ivanadamin/mullet-method-demo-standalone/.venv/bin/python
"""
Add Contact Form Block to Existing Page

Usage: python add_contact_block.py <site_path_prefix> <page_path>
Example: python add_contact_block.py corporate home
Example: python add_contact_block.py portfolio contact

This script demonstrates adding new content blocks to existing pages
WITHOUT any code changes to the main application - just database changes!
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, Site, Page, ContentBlock
from config import get_script_config

def add_contact_form_block(site_prefix, page_path):
    """Add a contact form content block to the specified page."""
    
    print(f"📧 Adding contact form block to /{site_prefix}/{page_path}")
    print("   (No code changes required!)")
    print()
    
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
    
    # Create contact form content block
    contact_block = ContentBlock(
        page_id=page.id,
        block_type='html',
        title='Contact Us',
        content='''<div class="contact-form-section">
    <div class="row">
        <div class="col-md-8">
            <form class="contact-form" action="/contact/submit" method="post">
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label for="name" class="form-label">Name *</label>
                        <input type="text" class="form-control" id="name" name="name" required>
                    </div>
                    <div class="col-md-6 mb-3">
                        <label for="email" class="form-label">Email *</label>
                        <input type="email" class="form-control" id="email" name="email" required>
                    </div>
                </div>
                <div class="mb-3">
                    <label for="subject" class="form-label">Subject</label>
                    <input type="text" class="form-control" id="subject" name="subject">
                </div>
                <div class="mb-3">
                    <label for="message" class="form-label">Message *</label>
                    <textarea class="form-control" id="message" name="message" rows="5" required></textarea>
                </div>
                <button type="submit" class="btn btn-primary">
                    <i class="fas fa-paper-plane me-2"></i>Send Message
                </button>
            </form>
        </div>
        <div class="col-md-4">
            <div class="contact-info">
                <h5>Get in Touch</h5>
                <div class="contact-item">
                    <i class="fas fa-envelope text-primary me-2"></i>
                    <span>hello@example.com</span>
                </div>
                <div class="contact-item">
                    <i class="fas fa-phone text-primary me-2"></i>
                    <span>+1 (555) 123-4567</span>
                </div>
                <div class="contact-item">
                    <i class="fas fa-map-marker-alt text-primary me-2"></i>
                    <span>123 Business St<br>City, State 12345</span>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
.contact-form-section {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    margin: 2rem 0;
}

.contact-info {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 8px;
    height: fit-content;
}

.contact-item {
    margin-bottom: 1rem;
    display: flex;
    align-items: flex-start;
}

.contact-item:last-child {
    margin-bottom: 0;
}

.contact-form .form-control:focus {
    border-color: var(--bs-primary);
    box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
}

.contact-form .btn-primary {
    padding: 12px 30px;
    font-weight: 500;
}
</style>''',
        order_index=next_order,
        config={
            'form_action': '/contact/submit',
            'success_message': 'Thank you for your message! We\'ll get back to you soon.',
            'required_fields': ['name', 'email', 'message']
        }
    )
    
    db.session.add(contact_block)
    db.session.commit()
    
    print("✅ Contact form block added successfully!")
    print(f"🌐 View the updated page at: http://localhost:5000/{site_prefix}/{page_path}")
    print()
    print("🎯 KEY POINT: No code changes were needed!")
    print("   - No new route functions")
    print("   - No application restart required")
    print("   - Just database changes")
    print()
    print("📋 Block Details:")
    print(f"   - Type: {contact_block.block_type}")
    print(f"   - Title: {contact_block.title}")
    print(f"   - Order: {contact_block.order_index}")
    print(f"   - Page: {page.title} ({site.name})")
    
    return True

def main():
    """Main function to add the contact form block."""
    if len(sys.argv) != 3:
        print("Usage: python add_contact_block.py <site_path_prefix> <page_path>")
        print("Example: python add_contact_block.py corporate home")
        print("Example: python add_contact_block.py portfolio contact")
        print()
        print("Available sites:")
        
        # Show available sites
        app = create_app(get_script_config())
        with app.app_context():
            sites = Site.query.filter_by(is_active=True).all()
            for site in sites:
                print(f"   - {site.path_prefix} ({site.name})")
                pages = Page.query.filter_by(site_id=site.id, is_active=True).all()
                for page in pages:
                    print(f"     └─ {page.path} ({page.title})")
        
        sys.exit(1)
    
    site_prefix = sys.argv[1].strip()
    page_path = sys.argv[2].strip()
    
    if not site_prefix:
        print("❌ Site path prefix cannot be empty!")
        sys.exit(1)
    
    if not page_path:
        print("❌ Page path cannot be empty!")
        sys.exit(1)
    
    app = create_app(get_script_config())
    
    with app.app_context():
        success = add_contact_form_block(site_prefix, page_path)
        if not success:
            sys.exit(1)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Test-Driven Development for Contact Form Functionality

This file contains tests for the contact form feature.
Following TDD principles: Red -> Green -> Refactor

Run tests with: python -m pytest test_contact_form.py -v
"""

import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, Site, Page, ContentBlock
from config import get_config

@pytest.fixture
def app():
    """Create and configure a test app."""
    config = get_config()
    config.TESTING = True
    config.SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory test database
    
    app = create_app(config)
    
    with app.app_context():
        db.create_all()
        
        # Create test site and page
        test_site = Site(
            name='Test Site',
            path_prefix='test',
            template_theme='corporate',
            is_active=True
        )
        db.session.add(test_site)
        db.session.commit()
        
        test_page = Page(
            site_id=test_site.id,
            title='Test Page',
            path='home',
            content_type='standard',
            is_active=True
        )
        db.session.add(test_page)
        db.session.commit()
        
        yield app
        
        db.drop_all()

@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()

class TestContactFormRoute:
    """Test the contact form submission route."""
    
    def test_contact_submit_route_exists(self, client):
        """Test that the contact form submission route exists."""
        # This should initially FAIL (Red phase)
        response = client.post('/contact/submit')
        assert response.status_code != 404, "Contact form route should exist"
    
    def test_contact_submit_requires_post(self, client):
        """Test that contact form only accepts POST requests."""
        # GET should not be allowed
        response = client.get('/contact/submit')
        assert response.status_code == 405, "Contact form should only accept POST"
    
    def test_contact_submit_with_valid_data(self, client):
        """Test contact form submission with valid data."""
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message.'
        }
        
        response = client.post('/contact/submit', 
                             data=form_data,
                             headers={'Referer': '/test/home'})
        
        # Should redirect back to referring page
        assert response.status_code == 302, "Should redirect after successful submission"
        assert '/test/home' in response.location, "Should redirect to referring page"
    
    def test_contact_submit_missing_required_fields(self, client):
        """Test contact form submission with missing required fields."""
        # Missing name
        form_data = {
            'email': 'john@example.com',
            'message': 'This is a test message.'
        }
        
        response = client.post('/contact/submit', 
                             data=form_data,
                             headers={'Referer': '/test/home'})
        
        assert response.status_code == 302, "Should redirect on validation error"
        
        # Missing email
        form_data = {
            'name': 'John Doe',
            'message': 'This is a test message.'
        }
        
        response = client.post('/contact/submit', 
                             data=form_data,
                             headers={'Referer': '/test/home'})
        
        assert response.status_code == 302, "Should redirect on validation error"
        
        # Missing message
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com'
        }
        
        response = client.post('/contact/submit', 
                             data=form_data,
                             headers={'Referer': '/test/home'})
        
        assert response.status_code == 302, "Should redirect on validation error"
    
    def test_contact_submit_logs_submission(self, client, caplog):
        """Test that contact form submissions are logged."""
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message.'
        }
        
        with caplog.at_level('INFO'):
            response = client.post('/contact/submit', 
                                 data=form_data,
                                 headers={'Referer': '/test/home'})
        
        # Check that submission was logged
        assert 'Contact form submission' in caplog.text
        assert 'John Doe' in caplog.text
        assert 'john@example.com' in caplog.text

class TestContactFormIntegration:
    """Test contact form integration with the Mullet Method."""
    
    def test_contact_form_renders_on_page(self, client, app):
        """Test that contact form content block renders properly."""
        with app.app_context():
            # Get the test site and page
            site = Site.query.filter_by(path_prefix='test').first()
            page = Page.query.filter_by(site_id=site.id, path='home').first()
            
            # Add contact form content block
            contact_block = ContentBlock(
                page_id=page.id,
                block_type='html',
                title='Contact Us',
                content='<form action="/contact/submit" method="post">...</form>',
                order_index=1
            )
            db.session.add(contact_block)
            db.session.commit()
        
        # Request the page
        response = client.get('/test/home')
        assert response.status_code == 200
        assert b'action="/contact/submit"' in response.data
        assert b'method="post"' in response.data
    
    def test_contact_form_works_across_different_sites(self, client, app):
        """Test that contact form works from different sites."""
        with app.app_context():
            # Create another test site
            site2 = Site(
                name='Test Site 2',
                path_prefix='test2',
                template_theme='blog',
                is_active=True
            )
            db.session.add(site2)
            db.session.commit()
            
            page2 = Page(
                site_id=site2.id,
                title='Test Page 2',
                path='contact',
                content_type='standard',
                is_active=True
            )
            db.session.add(page2)
            db.session.commit()
        
        # Test form submission from site 1
        form_data = {
            'name': 'User One',
            'email': 'user1@example.com',
            'message': 'Message from site 1'
        }
        
        response = client.post('/contact/submit', 
                             data=form_data,
                             headers={'Referer': '/test/home'})
        assert response.status_code == 302
        assert '/test/home' in response.location
        
        # Test form submission from site 2
        form_data = {
            'name': 'User Two',
            'email': 'user2@example.com',
            'message': 'Message from site 2'
        }
        
        response = client.post('/contact/submit', 
                             data=form_data,
                             headers={'Referer': '/test2/contact'})
        assert response.status_code == 302
        assert '/test2/contact' in response.location

class TestContactFormSecurity:
    """Test contact form security features."""
    
    def test_contact_form_handles_xss_attempts(self, client):
        """Test that contact form handles XSS attempts safely."""
        malicious_data = {
            'name': '<script>alert("xss")</script>',
            'email': 'test@example.com',
            'message': '<img src="x" onerror="alert(1)">'
        }
        
        response = client.post('/contact/submit', 
                             data=malicious_data,
                             headers={'Referer': '/test/home'})
        
        # Should still process (but in real implementation, would sanitize)
        assert response.status_code == 302
    
    def test_contact_form_handles_large_input(self, client):
        """Test that contact form handles very large input."""
        large_message = 'A' * 10000  # 10KB message
        
        form_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': large_message
        }
        
        response = client.post('/contact/submit', 
                             data=form_data,
                             headers={'Referer': '/test/home'})
        
        # Should handle gracefully
        assert response.status_code == 302

class TestContactFormUsability:
    """Test contact form usability features."""
    
    def test_contact_form_preserves_referer(self, client):
        """Test that form redirects back to the correct page."""
        form_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'Test message'
        }
        
        # Test with different referers
        referers = ['/test/home', '/test2/contact', '/corporate/about']
        
        for referer in referers:
            response = client.post('/contact/submit', 
                                 data=form_data,
                                 headers={'Referer': referer})
            
            assert response.status_code == 302
            assert referer in response.location
    
    def test_contact_form_handles_missing_referer(self, client):
        """Test that form handles missing referer gracefully."""
        form_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'Test message'
        }
        
        response = client.post('/contact/submit', data=form_data)
        
        # Should redirect to home page when no referer
        assert response.status_code == 302
        assert response.location == '/'

if __name__ == '__main__':
    # Run tests
    pytest.main([__file__, '-v'])

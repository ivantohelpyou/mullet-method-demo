"""
Test suite for Mullet Method Demo

This test suite covers the core functionality of the database-driven
multi-site architecture, ensuring that routing, content management,
and theme switching work correctly.
"""

import pytest
import sys
from pathlib import Path

# Add the demo directory to Python path
demo_dir = Path(__file__).parent.parent
sys.path.insert(0, str(demo_dir))

from app import create_app
from models import db, Site, Page, ContentBlock, NavigationItem
from config import TestingConfig


@pytest.fixture
def app():
    """Create and configure a test Flask application."""
    app = create_app(TestingConfig)
    
    with app.app_context():
        db.create_all()
        create_test_data()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()


def create_test_data():
    """Create test data for the demo."""
    # Create test site
    site = Site(
        path_prefix='test',
        name='Test Site',
        description='Test site for unit testing',
        template_theme='corporate'
    )
    db.session.add(site)
    db.session.flush()
    
    # Create test page
    page = Page(
        site_id=site.id,
        path='home',
        title='Test Home Page',
        description='Test page description',
        content_type='standard'
    )
    db.session.add(page)
    db.session.flush()
    
    # Create test content block
    content_block = ContentBlock(
        page_id=page.id,
        block_type='text',
        title='Test Content',
        content='This is test content for the demo.',
        order_index=1
    )
    db.session.add(content_block)
    
    # Create test navigation
    nav_item = NavigationItem(
        site_id=site.id,
        label='Home',
        url='home',
        order_index=1
    )
    db.session.add(nav_item)
    
    db.session.commit()


class TestDatabaseModels:
    """Test database model functionality."""
    
    def test_site_creation(self, app):
        """Test site model creation and validation."""
        with app.app_context():
            site = Site(
                path_prefix='example',
                name='Example Site',
                template_theme='blog'
            )
            db.session.add(site)
            db.session.commit()
            
            assert site.id is not None
            assert site.path_prefix == 'example'
            assert site.name == 'Example Site'
            assert site.template_theme == 'blog'
            assert site.is_active is True
    
    def test_site_path_prefix_validation(self, app):
        """Test site path prefix validation."""
        with app.app_context():
            # Valid path prefix
            site = Site(path_prefix='valid-prefix', name='Test', template_theme='corporate')
            db.session.add(site)
            db.session.commit()
            assert site.path_prefix == 'valid-prefix'
            
            # Invalid path prefix should be handled by validation
            with pytest.raises(ValueError):
                invalid_site = Site(path_prefix='invalid prefix!', name='Test', template_theme='corporate')
                db.session.add(invalid_site)
                db.session.commit()
    
    def test_page_creation(self, app):
        """Test page model creation."""
        with app.app_context():
            site = Site(path_prefix='test2', name='Test Site 2', template_theme='portfolio')
            db.session.add(site)
            db.session.flush()
            
            page = Page(
                site_id=site.id,
                path='about',
                title='About Page',
                content_type='standard'
            )
            db.session.add(page)
            db.session.commit()
            
            assert page.id is not None
            assert page.site_id == site.id
            assert page.path == 'about'
            assert page.title == 'About Page'
    
    def test_content_block_creation(self, app):
        """Test content block model creation."""
        with app.app_context():
            site = Site.query.filter_by(path_prefix='test').first()
            page = Page.query.filter_by(site_id=site.id).first()
            
            block = ContentBlock(
                page_id=page.id,
                block_type='html',
                content='<p>HTML content</p>',
                order_index=2
            )
            db.session.add(block)
            db.session.commit()
            
            assert block.id is not None
            assert block.page_id == page.id
            assert block.block_type == 'html'
            assert block.order_index == 2


class TestRouting:
    """Test database-driven routing functionality."""
    
    def test_home_page(self, client):
        """Test the demo home page."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Mullet Method' in response.data
        assert b'Database-Driven Multi-Site Architecture' in response.data
    
    def test_site_resolution(self, client):
        """Test site resolution through database lookup."""
        response = client.get('/test/home')
        assert response.status_code == 200
        assert b'Test Home Page' in response.data
        assert b'Test site for unit testing' in response.data
    
    def test_invalid_site(self, client):
        """Test handling of invalid site prefix."""
        response = client.get('/nonexistent/page')
        assert response.status_code == 404
    
    def test_invalid_page(self, client):
        """Test handling of invalid page within valid site."""
        response = client.get('/test/nonexistent')
        assert response.status_code == 404
    
    def test_api_sites_endpoint(self, client):
        """Test the API endpoint for listing sites."""
        response = client.get('/api/sites')
        assert response.status_code == 200
        
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) >= 1
        
        # Check test site is in the response
        test_site = next((site for site in data if site['path_prefix'] == 'test'), None)
        assert test_site is not None
        assert test_site['name'] == 'Test Site'


class TestContentRendering:
    """Test content block rendering functionality."""
    
    def test_text_content_rendering(self, app):
        """Test text content block rendering."""
        with app.app_context():
            block = ContentBlock(
                page_id=1,
                block_type='text',
                content='This is plain text content.',
                order_index=1
            )
            
            rendered = block.render()
            assert '<div class="content-block text">' in rendered
            assert 'This is plain text content.' in rendered
    
    def test_html_content_rendering(self, app):
        """Test HTML content block rendering."""
        with app.app_context():
            block = ContentBlock(
                page_id=1,
                block_type='html',
                content='<h2>HTML Heading</h2><p>HTML paragraph</p>',
                order_index=1
            )
            
            rendered = block.render()
            assert '<div class="content-block html">' in rendered
            assert '<h2>HTML Heading</h2>' in rendered
    
    def test_list_content_rendering(self, app):
        """Test list content block rendering."""
        with app.app_context():
            block = ContentBlock(
                page_id=1,
                block_type='list',
                content='Item 1\nItem 2\nItem 3',
                order_index=1
            )
            
            rendered = block.render()
            assert '<ul>' in rendered
            assert '<li>Item 1</li>' in rendered
            assert '<li>Item 2</li>' in rendered
            assert '<li>Item 3</li>' in rendered
    
    def test_quote_content_rendering(self, app):
        """Test quote content block rendering."""
        with app.app_context():
            block = ContentBlock(
                page_id=1,
                block_type='quote',
                content='This is a quote.',
                order_index=1
            )
            
            rendered = block.render()
            assert '<blockquote>' in rendered
            assert 'This is a quote.' in rendered


class TestThemeSystem:
    """Test theme switching and template resolution."""
    
    def test_corporate_theme_resolution(self, client):
        """Test that corporate theme templates are used correctly."""
        # This would require creating a corporate site in test data
        # For now, we test the theme resolution logic
        pass
    
    def test_template_path_resolution(self, app):
        """Test template path resolution based on site theme."""
        from app import get_template_path
        
        with app.app_context():
            site = Site(template_theme='corporate')
            template_path = get_template_path(site, 'page.html')
            assert template_path == 'themes/corporate/page.html'
            
            site.template_theme = 'blog'
            template_path = get_template_path(site, 'layout.html')
            assert template_path == 'themes/blog/layout.html'


class TestNavigationSystem:
    """Test navigation generation and hierarchy."""
    
    def test_navigation_building(self, app):
        """Test navigation menu building from database."""
        from app import build_navigation
        
        with app.app_context():
            site = Site.query.filter_by(path_prefix='test').first()
            navigation = build_navigation(site)
            
            assert isinstance(navigation, list)
            assert len(navigation) >= 1
            
            # Check the test navigation item
            home_nav = navigation[0]
            assert home_nav['label'] == 'Home'
            assert home_nav['url'] == 'home'
    
    def test_hierarchical_navigation(self, app):
        """Test hierarchical navigation with parent-child relationships."""
        with app.app_context():
            site = Site.query.filter_by(path_prefix='test').first()
            
            # Create parent navigation item
            parent_nav = NavigationItem(
                site_id=site.id,
                label='Services',
                url='services',
                order_index=2
            )
            db.session.add(parent_nav)
            db.session.flush()
            
            # Create child navigation item
            child_nav = NavigationItem(
                site_id=site.id,
                label='Web Development',
                url='services/web-development',
                parent_id=parent_nav.id,
                order_index=1
            )
            db.session.add(child_nav)
            db.session.commit()
            
            from app import build_navigation
            navigation = build_navigation(site)
            
            # Find the services item
            services_nav = next((item for item in navigation if item['label'] == 'Services'), None)
            assert services_nav is not None
            assert len(services_nav['children']) == 1
            assert services_nav['children'][0]['label'] == 'Web Development'


class TestErrorHandling:
    """Test error handling and edge cases."""
    
    def test_database_error_handling(self, client):
        """Test handling of database errors."""
        # This would require mocking database failures
        pass
    
    def test_invalid_content_block_type(self, app):
        """Test handling of invalid content block types."""
        with app.app_context():
            block = ContentBlock(
                page_id=1,
                block_type='unknown_type',
                content='Some content',
                order_index=1
            )
            
            # Should fall back to default rendering
            rendered = block.render()
            assert 'content-block unknown_type' in rendered
            assert 'Some content' in rendered


class TestExtensionPoints:
    """Test AI agent extension points."""
    
    def test_content_block_registration(self, app):
        """Test content block type registration system."""
        from models import register_content_block_type, get_content_block_class, ContentBlock
        
        # Create custom content block class
        class CustomBlock(ContentBlock):
            def render(self):
                return f"<div class='custom-block'>{self.content}</div>"
        
        # Register the custom type
        register_content_block_type('custom', CustomBlock)
        
        # Test retrieval
        block_class = get_content_block_class('custom')
        assert block_class == CustomBlock
        
        # Test fallback for unknown type
        fallback_class = get_content_block_class('unknown')
        assert fallback_class == ContentBlock
    
    def test_plugin_architecture(self, app):
        """Test the plugin registration system."""
        from app import register_content_renderer, CONTENT_RENDERERS
        
        class TestRenderer:
            @staticmethod
            def render(block):
                return f"<div class='test-render'>{block.content}</div>"
        
        register_content_renderer('test_type', TestRenderer)
        assert 'test_type' in CONTENT_RENDERERS
        assert CONTENT_RENDERERS['test_type'] == TestRenderer


if __name__ == '__main__':
    pytest.main([__file__])

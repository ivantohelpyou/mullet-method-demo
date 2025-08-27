"""
Mullet Method Demo - Database-Driven Multi-Site Flask Application

This application demonstrates the "Mullet Method" architecture where a single Flask
backend serves multiple completely different websites through database-driven routing.

Key Features:
- Dynamic route resolution through database lookups
- Multi-site template system with theme switching
- Content management through database only
- Easy extension points for AI agents
"""

import os
import logging
from flask import Flask, request, render_template, abort, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError

# Import our models and configuration
from models import db, Site, Page, ContentBlock, NavigationItem
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app(config_class=Config):
    """
    Application factory function.
    Creates a new Flask app instance with the specified configuration.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Register routes
    register_routes(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app


def register_routes(app):
    """Register all application routes."""
    
    @app.route('/')
    def index():
        """Home page showing available demo sites."""
        sites = Site.query.filter_by(is_active=True).all()
        return render_template('index.html', sites=sites)
    
    @app.route('/api/sites')
    def api_sites():
        """API endpoint to list all available sites."""
        sites = Site.query.filter_by(is_active=True).all()
        return jsonify([{
            'id': site.id,
            'name': site.name,
            'path_prefix': site.path_prefix,
            'template_theme': site.template_theme,
            'url': f"/{site.path_prefix}"
        } for site in sites])
    
    @app.route('/<path:url_path>')
    def dynamic_route(url_path):
        """
        Dynamic route handler - the core of the Mullet Method.
        
        This function resolves all requests through database lookups,
        demonstrating database-driven routing.
        """
        logger.info(f"Processing request for path: {url_path}")
        
        try:
            # Parse the URL path
            path_parts = url_path.strip('/').split('/')
            if len(path_parts) < 1:
                abort(404)
            
            site_prefix = path_parts[0]
            page_path = path_parts[1] if len(path_parts) > 1 else 'home'
            
            # Step 1: Resolve site through database lookup
            site = resolve_site(site_prefix)
            if not site:
                logger.warning(f"Site not found for prefix: {site_prefix}")
                abort(404)
            
            # Step 2: Resolve page within the site
            page = resolve_page(site, page_path)
            if not page:
                logger.warning(f"Page not found: {page_path} for site: {site.name}")
                abort(404)
            
            # Step 3: Get content blocks for the page
            content_blocks = get_content_blocks(page)
            
            # Step 4: Get navigation for the site
            navigation = build_navigation(site)
            
            # Step 5: Select template based on site theme
            template_path = get_template_path(site, 'page.html')
            
            # Step 6: Render with theme-specific template
            return render_template(
                template_path,
                site=site,
                page=page,
                content_blocks=content_blocks,
                navigation=navigation
            )
            
        except SQLAlchemyError as e:
            logger.error(f"Database error processing {url_path}: {e}")
            abort(500)
        except Exception as e:
            logger.error(f"Unexpected error processing {url_path}: {e}")
            abort(500)
    
    @app.errorhandler(404)
    def not_found(error):
        """Custom 404 handler."""
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Custom 500 handler."""
        db.session.rollback()
        return render_template('errors/500.html'), 500


def resolve_site(site_prefix):
    """
    Resolve site through database lookup.
    
    Args:
        site_prefix (str): The site prefix from the URL (e.g., 'corporate')
    
    Returns:
        Site: The site object or None if not found
    """
    return Site.query.filter_by(
        path_prefix=site_prefix,
        is_active=True
    ).first()


def resolve_page(site, page_path):
    """
    Resolve page within a site through database lookup.
    
    Args:
        site (Site): The site object
        page_path (str): The page path (e.g., 'about')
    
    Returns:
        Page: The page object or None if not found
    """
    return Page.query.filter_by(
        site_id=site.id,
        path=page_path,
        is_active=True
    ).first()


def get_content_blocks(page):
    """
    Get content blocks for a page, ordered by order_index.
    
    Args:
        page (Page): The page object
    
    Returns:
        list: List of content blocks
    """
    return ContentBlock.query.filter_by(
        page_id=page.id,
        is_active=True
    ).order_by(ContentBlock.order_index).all()


def build_navigation(site):
    """
    Build navigation menu from database.
    
    Args:
        site (Site): The site object
    
    Returns:
        list: Hierarchical navigation structure
    """
    # Get top-level navigation items
    nav_items = NavigationItem.query.filter_by(
        site_id=site.id,
        parent_id=None,
        is_active=True
    ).order_by(NavigationItem.order_index).all()
    
    # Build hierarchical structure
    navigation = []
    for item in nav_items:
        nav_item = {
            'id': item.id,
            'label': item.label,
            'url': item.url,
            'children': get_nav_children(item.id)
        }
        navigation.append(nav_item)
    
    return navigation


def get_nav_children(parent_id):
    """
    Get child navigation items for a parent.
    
    Args:
        parent_id (int): Parent navigation item ID
    
    Returns:
        list: List of child navigation items
    """
    children = NavigationItem.query.filter_by(
        parent_id=parent_id,
        is_active=True
    ).order_by(NavigationItem.order_index).all()
    
    return [{
        'id': child.id,
        'label': child.label,
        'url': child.url,
        'children': get_nav_children(child.id)  # Recursive for nested menus
    } for child in children]


def get_template_path(site, template_name):
    """
    Resolve template path based on site theme.
    
    Args:
        site (Site): The site object
        template_name (str): Base template name (e.g., 'page.html')
    
    Returns:
        str: Theme-specific template path
    """
    theme = site.template_theme
    return f"themes/{theme}/{template_name}"


def render_content_blocks(content_blocks):
    """
    Render content blocks into HTML.
    
    Args:
        content_blocks (list): List of ContentBlock objects
    
    Returns:
        str: Rendered HTML content
    """
    rendered_content = []
    
    for block in content_blocks:
        if block.block_type == 'text':
            rendered_content.append(f"<div class='content-block text'>{block.content}</div>")
        elif block.block_type == 'html':
            rendered_content.append(f"<div class='content-block html'>{block.content}</div>")
        elif block.block_type == 'image':
            rendered_content.append(f"<div class='content-block image'><img src='{block.content}' alt='Content Image'></div>")
        elif block.block_type == 'list':
            items = block.content.split('\n')
            list_html = '<ul>' + ''.join([f'<li>{item}</li>' for item in items if item.strip()]) + '</ul>'
            rendered_content.append(f"<div class='content-block list'>{list_html}</div>")
        else:
            # Default rendering for unknown block types
            rendered_content.append(f"<div class='content-block unknown'>{block.content}</div>")
    
    return '\n'.join(rendered_content)


# Extension points for AI agents
class ContentBlockRenderer:
    """Base class for content block renderers - easy extension point for AI agents."""
    
    @staticmethod
    def render(block):
        """Override this method to add new content block types."""
        return f"<div class='content-block'>{block.content}</div>"


class ThemeCustomizer:
    """Base class for theme customization - easy extension point for AI agents."""
    
    @staticmethod
    def customize_theme(site_config):
        """Override to add AI-generated theme customizations."""
        return site_config


# Plugin registration system for AI agents
CONTENT_RENDERERS = {}
THEME_CUSTOMIZERS = {}

def register_content_renderer(block_type, renderer_class):
    """Register new content renderers that AI can create."""
    CONTENT_RENDERERS[block_type] = renderer_class

def register_theme_customizer(theme_name, customizer_class):
    """Register new theme customizers that AI can create."""
    THEME_CUSTOMIZERS[theme_name] = customizer_class


# Create the Flask application
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

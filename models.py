"""
Database Models for Mullet Method Demo

This module defines the SQLAlchemy models that enable database-driven routing
and multi-site content management. The schema is simplified from production
systems while maintaining the core architectural patterns.

Key Models:
- Site: Defines different websites served by the same Flask app
- Page: Individual pages within each site
- ContentBlock: Flexible content blocks for dynamic page composition
- NavigationItem: Hierarchical navigation menus for each site
"""

from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON, Index
from sqlalchemy.orm import relationship, validates

# Initialize SQLAlchemy
db = SQLAlchemy()


class TimestampMixin:
    """Mixin to add timestamp fields to models."""
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                          onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class Site(db.Model, TimestampMixin):
    """
    Site model - represents different websites served by the same Flask app.
    
    This is the core of the Mullet Method: each site has a different theme,
    navigation, and content, but they're all served by the same application
    through database-driven routing.
    """
    __tablename__ = 'sites'

    id = db.Column(db.Integer, primary_key=True)
    path_prefix = db.Column(db.String(100), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    template_theme = db.Column(db.String(100), nullable=False, default='default')
    config = db.Column(db.JSON)  # Theme configuration, colors, layout options
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Relationships
    pages = db.relationship("Page", back_populates="site", cascade="all, delete-orphan")
    navigation_items = db.relationship("NavigationItem", back_populates="site", cascade="all, delete-orphan")

    # Indexes for performance
    __table_args__ = (
        db.Index('idx_site_active', is_active),
        db.Index('idx_site_theme', template_theme),
    )
    
    @validates('path_prefix')
    def validate_path_prefix(self, key, path_prefix):
        """Validate path prefix format."""
        if not path_prefix or not path_prefix.replace('-', '').replace('_', '').isalnum():
            raise ValueError("Path prefix must contain only alphanumeric characters, hyphens, and underscores")
        return path_prefix.lower()
    
    @validates('template_theme')
    def validate_template_theme(self, key, template_theme):
        """Validate template theme."""
        allowed_themes = ['corporate', 'blog', 'portfolio', 'default']
        if template_theme not in allowed_themes:
            raise ValueError(f"Template theme must be one of: {', '.join(allowed_themes)}")
        return template_theme
    
    def __repr__(self):
        return f"<Site(id={self.id}, name='{self.name}', prefix='{self.path_prefix}')>"


class Page(db.Model, TimestampMixin):
    """
    Page model - represents individual pages within each site.
    
    Pages are resolved through database lookups based on the URL path.
    Each page can have multiple content blocks for flexible composition.
    """
    __tablename__ = 'pages'

    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id', ondelete='CASCADE'), nullable=False)
    path = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    content_type = db.Column(db.String(50), default='standard', nullable=False)
    page_metadata = db.Column(db.JSON)  # SEO metadata, custom fields, etc.
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Relationships
    site = db.relationship("Site", back_populates="pages")
    content_blocks = db.relationship("ContentBlock", back_populates="page", cascade="all, delete-orphan")

    # Indexes for performance
    __table_args__ = (
        db.Index('idx_page_site_path', site_id, path),
        db.Index('idx_page_active', is_active),
        db.Index('idx_page_content_type', content_type),
    )
    
    @validates('path')
    def validate_path(self, key, path):
        """Validate page path format."""
        if not path or not path.replace('-', '').replace('_', '').replace('/', '').isalnum():
            raise ValueError("Page path must contain only alphanumeric characters, hyphens, underscores, and slashes")
        return path.lower()
    
    @validates('content_type')
    def validate_content_type(self, key, content_type):
        """Validate content type."""
        allowed_types = ['standard', 'blog_post', 'portfolio_item', 'landing_page']
        if content_type not in allowed_types:
            raise ValueError(f"Content type must be one of: {', '.join(allowed_types)}")
        return content_type
    
    def get_full_url(self):
        """Get the full URL path for this page."""
        return f"/{self.site.path_prefix}/{self.path}"
    
    def __repr__(self):
        return f"<Page(id={self.id}, title='{self.title}', path='{self.path}')>"


class ContentBlock(db.Model, TimestampMixin):
    """
    ContentBlock model - flexible content blocks for dynamic page composition.
    
    This enables database-driven content management where pages are composed
    of multiple content blocks that can be reordered and customized.
    """
    __tablename__ = 'content_blocks'

    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey('pages.id', ondelete='CASCADE'), nullable=False)
    block_type = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(255))
    content = db.Column(db.Text, nullable=False)
    order_index = db.Column(db.Integer, default=0, nullable=False)
    config = db.Column(db.JSON)  # Block-specific configuration
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Relationships
    page = db.relationship("Page", back_populates="content_blocks")

    # Indexes for performance
    __table_args__ = (
        db.Index('idx_content_block_page_order', page_id, order_index),
        db.Index('idx_content_block_type', block_type),
        db.Index('idx_content_block_active', is_active),
    )
    
    @validates('block_type')
    def validate_block_type(self, key, block_type):
        """Validate content block type."""
        allowed_types = ['text', 'html', 'image', 'list', 'quote', 'code', 'video', 'gallery']
        if block_type not in allowed_types:
            raise ValueError(f"Block type must be one of: {', '.join(allowed_types)}")
        return block_type
    
    def render(self):
        """
        Render the content block to HTML.
        This method can be overridden by AI agents to add custom rendering.
        """
        if self.block_type == 'text':
            return f"<div class='content-block text'><p>{self.content}</p></div>"
        elif self.block_type == 'html':
            return f"<div class='content-block html'>{self.content}</div>"
        elif self.block_type == 'image':
            alt_text = self.title or 'Content Image'
            return f"<div class='content-block image'><img src='{self.content}' alt='{alt_text}'></div>"
        elif self.block_type == 'list':
            items = [item.strip() for item in self.content.split('\n') if item.strip()]
            list_html = '<ul>' + ''.join([f'<li>{item}</li>' for item in items]) + '</ul>'
            return f"<div class='content-block list'>{list_html}</div>"
        elif self.block_type == 'quote':
            return f"<div class='content-block quote'><blockquote>{self.content}</blockquote></div>"
        elif self.block_type == 'code':
            return f"<div class='content-block code'><pre><code>{self.content}</code></pre></div>"
        else:
            return f"<div class='content-block {self.block_type}'>{self.content}</div>"
    
    def __repr__(self):
        return f"<ContentBlock(id={self.id}, type='{self.block_type}', order={self.order_index})>"


class NavigationItem(db.Model, TimestampMixin):
    """
    NavigationItem model - hierarchical navigation menus for each site.
    
    Enables database-driven navigation that can be different for each site,
    supporting nested menu structures.
    """
    __tablename__ = 'navigation_items'

    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id', ondelete='CASCADE'), nullable=False)
    label = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('navigation_items.id', ondelete='CASCADE'))
    order_index = db.Column(db.Integer, default=0, nullable=False)
    icon = db.Column(db.String(100))  # CSS class for icons
    is_external = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Relationships
    site = db.relationship("Site", back_populates="navigation_items")
    parent = db.relationship("NavigationItem", remote_side=[id], backref="children")

    # Indexes for performance
    __table_args__ = (
        db.Index('idx_nav_site_parent_order', site_id, parent_id, order_index),
        db.Index('idx_nav_active', is_active),
    )
    
    @validates('url')
    def validate_url(self, key, url):
        """Validate navigation URL."""
        if not url:
            raise ValueError("Navigation URL cannot be empty")
        # Allow both relative and absolute URLs
        if not (url.startswith('/') or url.startswith('http')):
            url = '/' + url
        return url
    
    def get_full_url(self):
        """Get the full URL for this navigation item."""
        if self.is_external or self.url.startswith('http'):
            return self.url
        elif self.url.startswith('/'):
            return self.url
        else:
            return f"/{self.site.path_prefix}/{self.url}"
    
    def __repr__(self):
        return f"<NavigationItem(id={self.id}, label='{self.label}', url='{self.url}')>"


# Extension point for AI agents - custom content block types
class AIContentBlock(ContentBlock):
    """
    Extended content block class that AI agents can inherit from
    to create custom content block types with specialized rendering.
    """
    
    def ai_render(self, context=None):
        """
        AI-specific rendering method that can use context for smart rendering.
        
        Args:
            context (dict): Additional context for rendering (user preferences, etc.)
        
        Returns:
            str: Rendered HTML content
        """
        # Default implementation - override in subclasses
        return self.render()


# Plugin registry for AI agents
CONTENT_BLOCK_TYPES = {
    'text': ContentBlock,
    'html': ContentBlock,
    'image': ContentBlock,
    'list': ContentBlock,
    'quote': ContentBlock,
    'code': ContentBlock,
    'video': ContentBlock,
    'gallery': ContentBlock,
}

def register_content_block_type(block_type, block_class):
    """
    Register a new content block type that AI agents can create.
    
    Args:
        block_type (str): The block type identifier
        block_class (class): The content block class
    """
    CONTENT_BLOCK_TYPES[block_type] = block_class

def get_content_block_class(block_type):
    """
    Get the content block class for a given type.
    
    Args:
        block_type (str): The block type identifier
    
    Returns:
        class: The content block class
    """
    return CONTENT_BLOCK_TYPES.get(block_type, ContentBlock)

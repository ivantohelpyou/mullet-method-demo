"""
Configuration Management for Mullet Method Demo

This module provides configuration classes for different environments
and settings management for the database-driven multi-site application.
"""

import os
from pathlib import Path

# Get the base directory of the application
basedir = Path(__file__).parent.absolute()


class Config:
    """Base configuration class with common settings."""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mullet-method-demo-secret-key-change-in-production'
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{basedir / "mullet_demo.db"}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # Set to True for SQL query logging
    
    # Application settings
    DEBUG = False
    TESTING = False
    
    # Template settings
    TEMPLATES_AUTO_RELOAD = True
    
    # Security settings
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    
    # Logging settings
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    # Demo-specific settings
    DEMO_SITES = {
        'corporate': {
            'name': 'Acme Corporation',
            'description': 'Professional business website',
            'theme': 'corporate',
            'config': {
                'colors': {
                    'primary': '#007bff',
                    'secondary': '#6c757d',
                    'success': '#28a745',
                    'danger': '#dc3545'
                },
                'layout': {
                    'sidebar': False,
                    'header_style': 'fixed',
                    'footer_style': 'simple'
                },
                'features': ['contact_form', 'newsletter', 'social_links']
            }
        },
        'blog': {
            'name': 'Tech Insights Blog',
            'description': 'Personal technology blog',
            'theme': 'blog',
            'config': {
                'colors': {
                    'primary': '#6f42c1',
                    'secondary': '#495057',
                    'accent': '#fd7e14'
                },
                'layout': {
                    'sidebar': True,
                    'header_style': 'simple',
                    'footer_style': 'minimal'
                },
                'features': ['comments', 'tags', 'archive', 'search']
            }
        },
        'portfolio': {
            'name': 'Creative Portfolio',
            'description': 'Designer and developer portfolio',
            'theme': 'portfolio',
            'config': {
                'colors': {
                    'primary': '#e83e8c',
                    'secondary': '#343a40',
                    'accent': '#20c997'
                },
                'layout': {
                    'sidebar': False,
                    'header_style': 'overlay',
                    'footer_style': 'creative'
                },
                'features': ['gallery', 'lightbox', 'animations', 'contact']
            }
        }
    }
    
    @staticmethod
    def init_app(app):
        """Initialize application with this configuration."""
        pass


class DevelopmentConfig(Config):
    """Development environment configuration."""
    
    DEBUG = True
    SQLALCHEMY_ECHO = True  # Enable SQL query logging in development
    TEMPLATES_AUTO_RELOAD = True
    
    # Development-specific database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or f'sqlite:///{basedir / "mullet_demo_dev.db"}'
    
    @staticmethod
    def init_app(app):
        """Initialize development-specific settings."""
        Config.init_app(app)
        
        # Enable debug toolbar if available
        try:
            from flask_debugtoolbar import DebugToolbarExtension
            toolbar = DebugToolbarExtension(app)
        except ImportError:
            pass


class TestingConfig(Config):
    """Testing environment configuration."""
    
    TESTING = True
    WTF_CSRF_ENABLED = False
    
    # Use in-memory database for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_ECHO = False
    
    @staticmethod
    def init_app(app):
        """Initialize testing-specific settings."""
        Config.init_app(app)


class ProductionConfig(Config):
    """Production environment configuration."""
    
    # Production database - should be set via environment variable
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{basedir / "mullet_demo_prod.db"}'
    
    # Security settings for production
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'production-secret-key-change-me'
    
    # Logging configuration for production
    LOG_LEVEL = 'WARNING'
    
    @staticmethod
    def init_app(app):
        """Initialize production-specific settings."""
        Config.init_app(app)
        
        # Configure logging for production
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not app.debug and not app.testing:
            # Create logs directory if it doesn't exist
            logs_dir = basedir / 'logs'
            logs_dir.mkdir(exist_ok=True)
            
            # Set up file handler
            file_handler = RotatingFileHandler(
                logs_dir / 'mullet_demo.log',
                maxBytes=10240000,  # 10MB
                backupCount=10
            )
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            
            app.logger.setLevel(logging.INFO)
            app.logger.info('Mullet Method Demo startup')


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(config_name=None):
    """
    Get configuration class based on environment.
    
    Args:
        config_name (str): Configuration name ('development', 'testing', 'production')
    
    Returns:
        Config: Configuration class
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    return config.get(config_name, DevelopmentConfig)


# Database configuration helpers
class DatabaseConfig:
    """Database-specific configuration and utilities."""
    
    @staticmethod
    def get_database_uri(environment='development'):
        """
        Get database URI for specific environment.
        
        Args:
            environment (str): Environment name
        
        Returns:
            str: Database URI
        """
        if environment == 'testing':
            return 'sqlite:///:memory:'
        elif environment == 'production':
            return os.environ.get('DATABASE_URL') or f'sqlite:///{basedir / "mullet_demo_prod.db"}'
        else:  # development
            return os.environ.get('DEV_DATABASE_URL') or f'sqlite:///{basedir / "mullet_demo_dev.db"}'
    
    @staticmethod
    def get_migration_directory():
        """Get the directory for database migrations."""
        return basedir / 'migrations'


# Theme configuration
class ThemeConfig:
    """Theme-specific configuration and utilities."""
    
    AVAILABLE_THEMES = ['corporate', 'blog', 'portfolio', 'default']
    
    THEME_SETTINGS = {
        'corporate': {
            'name': 'Corporate',
            'description': 'Clean, professional business theme',
            'color_scheme': 'blue',
            'layout': 'fixed-header',
            'features': ['contact_form', 'newsletter', 'testimonials']
        },
        'blog': {
            'name': 'Blog',
            'description': 'Blog-style layout with sidebar',
            'color_scheme': 'purple',
            'layout': 'sidebar',
            'features': ['comments', 'tags', 'archive', 'search']
        },
        'portfolio': {
            'name': 'Portfolio',
            'description': 'Creative portfolio with gallery',
            'color_scheme': 'pink',
            'layout': 'overlay-header',
            'features': ['gallery', 'lightbox', 'animations']
        },
        'default': {
            'name': 'Default',
            'description': 'Simple default theme',
            'color_scheme': 'gray',
            'layout': 'simple',
            'features': ['basic_navigation']
        }
    }
    
    @classmethod
    def get_theme_config(cls, theme_name):
        """
        Get configuration for a specific theme.
        
        Args:
            theme_name (str): Theme name
        
        Returns:
            dict: Theme configuration
        """
        return cls.THEME_SETTINGS.get(theme_name, cls.THEME_SETTINGS['default'])
    
    @classmethod
    def validate_theme(cls, theme_name):
        """
        Validate if a theme name is supported.
        
        Args:
            theme_name (str): Theme name to validate
        
        Returns:
            bool: True if theme is valid
        """
        return theme_name in cls.AVAILABLE_THEMES


# Content configuration
class ContentConfig:
    """Content-specific configuration."""
    
    ALLOWED_CONTENT_TYPES = ['standard', 'blog_post', 'portfolio_item', 'landing_page']
    ALLOWED_BLOCK_TYPES = ['text', 'html', 'image', 'list', 'quote', 'code', 'video', 'gallery']
    
    # Maximum content lengths
    MAX_TITLE_LENGTH = 255
    MAX_DESCRIPTION_LENGTH = 1000
    MAX_CONTENT_LENGTH = 50000
    
    # Default content for new pages
    DEFAULT_CONTENT = {
        'standard': 'Welcome to this page. Add your content here.',
        'blog_post': 'Write your blog post content here...',
        'portfolio_item': 'Describe your project or portfolio item...',
        'landing_page': 'Create an engaging landing page...'
    }
    
    @classmethod
    def get_default_content(cls, content_type):
        """Get default content for a content type."""
        return cls.DEFAULT_CONTENT.get(content_type, cls.DEFAULT_CONTENT['standard'])


# Export the main configuration class
__all__ = ['Config', 'DevelopmentConfig', 'TestingConfig', 'ProductionConfig', 'config', 'get_config']

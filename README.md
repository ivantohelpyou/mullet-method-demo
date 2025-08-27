# Mullet Method Demo - Database-Driven Multi-Site Architecture

A minimal but functional demonstration of the "Mullet Method" architecture: a single Flask backend that serves multiple completely different websites through database-driven routing.

## 🎯 What This Demonstrates

Instead of hardcoded routes like:
```python
@app.route('/about')
def about():
    return render_template('about.html')
```

This demo shows dynamic routing like:
```python
@app.route('/<path:url_path>')
def dynamic_route(url_path):
    # Resolve route through database lookup
    page = db.session.query(Page).filter_by(path=url_path).first()
    return render_page(page)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip or uv for package management

### Installation
```bash
# Clone the repository
git clone https://github.com/your-username/mullet-method-demo.git
cd mullet-method-demo

# Install dependencies
pip install -r requirements.txt

# Initialize the database
python seed_data.py

# Run the application
python app.py
```

### Demo Sites
Visit these URLs to see three completely different websites served by the same Flask app:

- **Corporate Site**: http://localhost:5000/corporate
  - Clean, professional business template
  - Pages: About, Services, Contact
  
- **Personal Blog**: http://localhost:5000/blog
  - Blog-style layout with posts
  - Pages: Recent posts, Archive, About author
  
- **Portfolio Site**: http://localhost:5000/portfolio
  - Creative portfolio layout
  - Pages: Projects, Gallery, Resume

## 🏗️ Architecture Overview

### Database-Driven Routing
All routing decisions are made through database lookups:

1. **URL Analysis**: `/corporate/about` → site=`corporate`, page=`about`
2. **Database Lookup**: Find site with `path_prefix='corporate'`
3. **Page Resolution**: Find page with `path='about'` for that site
4. **Template Selection**: Use site's `template_theme` to select templates
5. **Content Rendering**: Render page with theme-specific templates

### Core Components

#### Sites Table
```sql
sites (
    id INTEGER PRIMARY KEY,
    path_prefix VARCHAR(255) UNIQUE,  -- 'corporate', 'blog', 'portfolio'
    name VARCHAR(255),
    template_theme VARCHAR(100),
    config JSON
);
```

#### Pages Table
```sql
pages (
    id INTEGER PRIMARY KEY,
    site_id INTEGER REFERENCES sites(id),
    path VARCHAR(255),               -- 'about', 'services', 'contact'
    title VARCHAR(255),
    content_type VARCHAR(50),
    metadata JSON
);
```

#### Content Blocks Table
```sql
content_blocks (
    id INTEGER PRIMARY KEY,
    page_id INTEGER REFERENCES pages(id),
    block_type VARCHAR(50),          -- 'text', 'image', 'list'
    content TEXT,
    order_index INTEGER
);
```

## 🎨 Template System

Each site uses a different theme with completely different styling:

```
templates/
├── base.html           # Base template
├── themes/
│   ├── corporate/      # Business site theme
│   │   ├── layout.html
│   │   ├── page.html
│   │   └── components/
│   ├── blog/          # Blog site theme
│   │   ├── layout.html
│   │   ├── post.html
│   │   └── components/
│   └── portfolio/     # Portfolio site theme
│       ├── layout.html
│       ├── project.html
│       └── components/
```

## 🤖 AI Agent Integration

### Easy Extension Points
```python
# Add new content block types
class CustomContentBlock(ContentBlock):
    def render(self):
        """Override this method to add new content block types"""
        return f"<div class='custom'>{self.content}</div>"

# Register new content types
register_content_type('ai_generated', AIGeneratedBlock)
```

### Configuration-Driven Customization
```python
# JSON configuration that AI agents can easily modify
site_config = {
    "theme": "corporate",
    "colors": {"primary": "#007bff", "secondary": "#6c757d"},
    "layout": {"sidebar": True, "header_style": "fixed"},
    "features": ["contact_form", "newsletter", "social_links"]
}
```

## 📁 Project Structure

```
mullet-method-demo/
├── README.md                 # This file
├── requirements.txt          # Dependencies
├── app.py                   # Main Flask application
├── models.py                # SQLAlchemy database models
├── config.py                # Configuration management
├── seed_data.py             # Sample data for demo
├── migrations/              # Alembic migration files
├── templates/               # Jinja2 templates
│   ├── base.html
│   └── themes/
│       ├── corporate/
│       ├── blog/
│       └── portfolio/
├── static/                  # CSS, JS, images
│   ├── css/
│   ├── js/
│   └── themes/
└── tests/                   # Test suite
```

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

Tests cover:
- Route resolution for different scenarios
- Template rendering for each theme
- Database model relationships
- Multi-site functionality

## 🚀 Deployment

### Local Development
```bash
export FLASK_ENV=development
python app.py
```

### Production Deployment
```bash
# Using Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# Using uWSGI
pip install uwsgi
uwsgi --http :8000 --module app:app
```

## 🔧 Adding New Sites

1. **Add site to database**:
```python
new_site = Site(
    path_prefix='newsite',
    name='New Site',
    template_theme='custom',
    config={'color_scheme': 'dark'}
)
```

2. **Create theme templates**:
```
templates/themes/custom/
├── layout.html
├── page.html
└── components/
```

3. **Add pages and content**:
```python
page = Page(
    site_id=new_site.id,
    path='home',
    title='Welcome',
    content_type='standard'
)
```

## 🚀 Next Steps

This demo provides a complete foundation for building database-driven multi-site applications. The architecture is designed to be easily extended by AI agents or developers who want to add new sites, content types, or functionality.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

**Built for AI Tinkerers** - This demo is designed to be immediately understandable and extensible by AI coding agents.

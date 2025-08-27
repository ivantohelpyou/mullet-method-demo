"""
Traditional Flask Routing Example - The OLD WAY

This shows how you would typically build multiple sites in Flask
with hardcoded routes. Compare this to the Mullet Method approach!
"""

from flask import Flask, render_template

app = Flask(__name__)

# ❌ PROBLEM: Every new site requires CODE CHANGES

# Corporate Site Routes - HARDCODED
@app.route('/corporate')
@app.route('/corporate/')
@app.route('/corporate/home')
def corporate_home():
    return render_template('corporate/home.html')

@app.route('/corporate/about')
def corporate_about():
    return render_template('corporate/about.html')

@app.route('/corporate/services')
def corporate_services():
    return render_template('corporate/services.html')

@app.route('/corporate/contact')
def corporate_contact():
    return render_template('corporate/contact.html')


# Blog Site Routes - MORE HARDCODED ROUTES
@app.route('/blog')
@app.route('/blog/')
@app.route('/blog/home')
def blog_home():
    return render_template('blog/home.html')

@app.route('/blog/recent')
def blog_recent():
    return render_template('blog/recent.html')

@app.route('/blog/archive')
def blog_archive():
    return render_template('blog/archive.html')

@app.route('/blog/about')
def blog_about():
    return render_template('blog/about.html')


# Portfolio Site Routes - EVEN MORE HARDCODED ROUTES
@app.route('/portfolio')
@app.route('/portfolio/')
@app.route('/portfolio/home')
def portfolio_home():
    return render_template('portfolio/home.html')

@app.route('/portfolio/projects')
def portfolio_projects():
    return render_template('portfolio/projects.html')

@app.route('/portfolio/gallery')
def portfolio_gallery():
    return render_template('portfolio/gallery.html')

@app.route('/portfolio/resume')
def portfolio_resume():
    return render_template('portfolio/resume.html')

@app.route('/portfolio/contact')
def portfolio_contact():
    return render_template('portfolio/contact.html')


# ❌ PROBLEMS WITH THIS APPROACH:
# 1. Every new site = CODE CHANGES + DEPLOYMENT
# 2. Every new page = CODE CHANGES + DEPLOYMENT  
# 3. Can't add sites dynamically
# 4. No content management without code changes
# 5. Developers required for simple content updates
# 6. Hard to maintain as sites grow
# 7. No way for AI agents to add new sites/pages

if __name__ == '__main__':
    print("❌ Traditional Flask: Hardcoded routes")
    print("   - 15+ route functions for just 3 sites")
    print("   - Every new site requires code changes")
    print("   - No dynamic content management")
    app.run(debug=True, port=5001)

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import requests
import json
import os
from urllib.parse import quote
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for sessions

# Memegen API base URL
MEMEGEN_API_BASE = "https://api.memegen.link"

# Hardcoded admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "meme123"

# File to store custom memes
CUSTOM_MEMES_FILE = "custom_memes.json"

def load_custom_memes():
    """Load custom memes from JSON file"""
    if os.path.exists(CUSTOM_MEMES_FILE):
        with open(CUSTOM_MEMES_FILE, 'r') as f:
            return json.load(f)
    return []

def save_custom_memes(memes):
    """Save custom memes to JSON file"""
    with open(CUSTOM_MEMES_FILE, 'w') as f:
        json.dump(memes, f, indent=2)

def is_admin_logged_in():
    """Check if admin is logged in"""
    return session.get('admin_logged_in', False)

@app.route('/')
def index():
    """Main page with template selection"""
    return render_template('index.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error="Invalid credentials")
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard"""
    if not is_admin_logged_in():
        return redirect(url_for('admin_login'))
    
    custom_memes = load_custom_memes()
    return render_template('admin_dashboard.html', memes=custom_memes)

@app.route('/admin/submit', methods=['GET', 'POST'])
def admin_submit_meme():
    """Admin meme submission page"""
    if not is_admin_logged_in():
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        image_url = request.form.get('image_url')
        keywords = request.form.get('keywords', '').split(',')
        keywords = [k.strip() for k in keywords if k.strip()]
        
        if not name or not image_url:
            return render_template('admin_submit.html', error="Name and image URL are required")
        
        # Create custom meme template
        custom_meme = {
            'id': f"custom_{len(load_custom_memes()) + 1}",
            'name': name,
            'image_url': image_url,
            'keywords': keywords,
            'lines': 2,  # Default to 2 lines
            'custom': True,
            'created_at': datetime.now().isoformat()
        }
        
        # Save to custom memes
        custom_memes = load_custom_memes()
        custom_memes.append(custom_meme)
        save_custom_memes(custom_memes)
        
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin_submit.html')

@app.route('/api/templates')
def get_templates():
    """Fetch all available templates from Memegen API and include custom memes"""
    try:
        response = requests.get(f"{MEMEGEN_API_BASE}/templates")
        if response.status_code == 200:
            templates = response.json()
            
            # Add custom memes
            custom_memes = load_custom_memes()
            for meme in custom_memes:
                # Convert custom meme to template format
                template = {
                    'id': meme['id'],
                    'name': meme['name'],
                    'lines': meme['lines'],
                    'overlays': 0,
                    'styles': [],
                    'blank': meme['image_url'],
                    'example': {
                        'text': ['Top Text', 'Bottom Text'],
                        'url': f"{MEMEGEN_API_BASE}/images/custom/top_text/bottom_text.png?background={meme['image_url']}"
                    },
                    'source': None,
                    'keywords': meme['keywords'],
                    'custom': True
                }
                templates.append(template)
            
            # Sort templates by name for better UX
            templates.sort(key=lambda x: x.get('name', '').lower())
            return jsonify(templates)
        else:
            return jsonify({'error': 'Failed to fetch templates'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/templates/<template_id>')
def get_template_details(template_id):
    """Fetch details for a specific template"""
    try:
        # Check if it's a custom meme
        if template_id.startswith('custom_'):
            custom_memes = load_custom_memes()
            for meme in custom_memes:
                if meme['id'] == template_id:
                    return jsonify({
                        'id': meme['id'],
                        'name': meme['name'],
                        'lines': meme['lines'],
                        'blank': meme['image_url'],
                        'custom': True
                    })
            return jsonify({'error': 'Custom template not found'}), 404
        
        # Regular template from API
        response = requests.get(f"{MEMEGEN_API_BASE}/templates/{template_id}")
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'Template not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/create', methods=['GET', 'POST'])
def create_meme():
    """Create meme page with form"""
    if request.method == 'POST':
        template_id = request.form.get('template_id')
        text_lines = request.form.getlist('text[]')
        extension = request.form.get('extension', 'png')
        
        # Check if it's a custom meme
        if template_id.startswith('custom_'):
            custom_memes = load_custom_memes()
            custom_meme = None
            for meme in custom_memes:
                if meme['id'] == template_id:
                    custom_meme = meme
                    break
            
            if custom_meme:
                # Build custom meme URL
                if len(text_lines) == 1:
                    text_part = quote(text_lines[0].replace(' ', '_'))
                    meme_url = f"{MEMEGEN_API_BASE}/images/custom/{text_part}.{extension}?background={custom_meme['image_url']}"
                elif len(text_lines) == 2:
                    top_text = quote(text_lines[0].replace(' ', '_'))
                    bottom_text = quote(text_lines[1].replace(' ', '_'))
                    meme_url = f"{MEMEGEN_API_BASE}/images/custom/{top_text}/{bottom_text}.{extension}?background={custom_meme['image_url']}"
                else:
                    return jsonify({'error': 'Please provide 1 or 2 lines of text'}), 400
                
                return jsonify({'url': meme_url})
        
        # Regular template
        if len(text_lines) == 1:
            # Single line of text
            text_part = quote(text_lines[0].replace(' ', '_'))
            meme_url = f"{MEMEGEN_API_BASE}/images/{template_id}/{text_part}.{extension}"
        elif len(text_lines) == 2:
            # Two lines of text
            top_text = quote(text_lines[0].replace(' ', '_'))
            bottom_text = quote(text_lines[1].replace(' ', '_'))
            meme_url = f"{MEMEGEN_API_BASE}/images/{template_id}/{top_text}/{bottom_text}.{extension}"
        else:
            return jsonify({'error': 'Please provide 1 or 2 lines of text'}), 400
        
        return jsonify({'url': meme_url})
    
    template_id = request.args.get('template_id')
    return render_template('create.html', template_id=template_id)

@app.route('/preview/<template_id>')
def preview_template(template_id):
    """Show template preview"""
    return render_template('preview.html', template_id=template_id)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port) 
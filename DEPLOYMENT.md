# Deployment Guide

## Option 1: Deploy to Heroku (Recommended)

### Prerequisites
- Heroku account
- Git installed
- Heroku CLI installed

### Steps:
1. **Install Heroku CLI** (if not already installed):
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Windows
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**:
   ```bash
   heroku login
   ```

3. **Create Heroku app**:
   ```bash
   heroku create your-meme-generator-app
   ```

4. **Deploy**:
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   ```

5. **Open your app**:
   ```bash
   heroku open
   ```

## Option 2: Deploy to Railway

### Steps:
1. Go to [Railway.app](https://railway.app)
2. Connect your GitHub repository
3. Railway will automatically detect it's a Python app
4. Deploy with one click

## Option 3: Deploy to Render

### Steps:
1. Go to [Render.com](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `gunicorn meme_generator_app:app`
6. Deploy

## Option 4: Static Version for GitHub Pages

### Steps:
1. **Use the static version** (`index_static.html`):
   ```bash
   # Rename the static file
   mv index_static.html index.html
   ```

2. **Create a new repository** for the static version:
   ```bash
   mkdir meme-generator-static
   cd meme-generator-static
   cp ../index.html .
   ```

3. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/meme-generator-static.git
   git push -u origin main
   ```

4. **Enable GitHub Pages**:
   - Go to repository Settings
   - Scroll to "Pages" section
   - Select "Deploy from a branch"
   - Choose "main" branch
   - Save

### Static Version Features:
- ✅ Works on GitHub Pages
- ✅ All meme templates
- ✅ Search functionality
- ✅ Live preview
- ✅ Shareable URLs
- ❌ No admin panel (static limitation)

## Option 5: Deploy to PythonAnywhere

### Steps:
1. Create account at [PythonAnywhere.com](https://www.pythonanywhere.com)
2. Upload your files
3. Create a new web app
4. Set the WSGI file to point to your Flask app
5. Deploy

## Environment Variables

For cloud deployments, you may need to set these environment variables:

```bash
# For Heroku/Railway/Render
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
```

## File Structure for Deployment

```
meme-generator-app/
├── meme_generator_app.py    # Main Flask app
├── requirements.txt         # Python dependencies
├── Procfile                # Heroku deployment
├── runtime.txt             # Python version
├── custom_memes.json       # Custom memes data
├── templates/              # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── create.html
│   ├── admin_login.html
│   ├── admin_dashboard.html
│   └── admin_submit.html
└── README_meme_app.md      # Documentation
```

## Admin Access After Deployment

Once deployed, you can access the admin panel at:
- `https://your-app.herokuapp.com/admin/login`
- Username: `admin`
- Password: `meme123`

## Troubleshooting

### Common Issues:

1. **Port issues**: The app automatically uses the PORT environment variable
2. **Static files**: Make sure all template files are included
3. **Dependencies**: Ensure requirements.txt is up to date
4. **Custom memes**: The custom_memes.json file will be created automatically

### Debug Mode:
For local development, change the last line in `meme_generator_app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

For production deployment:
```python
app.run(debug=False, host='0.0.0.0', port=port)
```

## Recommended Deployment

**For full functionality**: Use Heroku, Railway, or Render
**For static hosting**: Use GitHub Pages with the static version
**For learning**: Start with Heroku (free tier available) 
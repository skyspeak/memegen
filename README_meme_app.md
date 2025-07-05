# Meme Generator Web App

A simple web application that lets you choose from hundreds of meme templates, add your own text, and generate shareable meme URLs using the Memegen API.

## Features

- 🎭 **Browse 200+ Meme Templates**: Search and browse through popular meme templates
- ✏️ **Easy Text Input**: Add top and bottom text to your memes
- 🖼️ **Multiple Formats**: Generate memes in PNG, JPG, GIF, or WebP formats
- 🔗 **Shareable URLs**: Get direct links to your generated memes
- 📱 **Responsive Design**: Works on desktop and mobile devices
- ⚡ **Real-time Preview**: See your meme as you type
- 👑 **Admin Panel**: Submit custom memes (Username: `admin`, Password: `meme123`)

## Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download this repository**
   ```bash
   # If you have the files locally, navigate to the directory
   cd /path/to/meme-generator-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python meme_generator_app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

## How to Use

### For Users:
1. **Choose a Template**: Browse through the available meme templates on the home page
2. **Search**: Use the search bar to find specific templates by name or keywords
3. **Create Meme**: Click "Create Meme" on any template
4. **Add Text**: Enter your top and bottom text in the form
5. **Generate**: Click "Generate Meme" to create your meme
6. **Share**: Copy the shareable URL or download the image

### For Admins:
1. **Login**: Go to `/admin/login` and use credentials (admin/meme123)
2. **Dashboard**: View all submitted custom memes
3. **Submit Meme**: Add new custom meme templates with image URLs
4. **Manage**: Custom memes appear in the public gallery with a "Custom" badge

## API Integration

This app uses the [Memegen API](https://api.memegen.link/) to generate memes. The API provides:

- **Template List**: `/api/templates` - Get all available templates
- **Template Details**: `/api/templates/{id}` - Get specific template info
- **Meme Generation**: Direct URL generation using the API format

## Example URLs

The app generates URLs in this format:
- Single line: `https://api.memegen.link/images/doge/your_text.png`
- Two lines: `https://api.memegen.link/images/doge/top_text/bottom_text.png`

## File Structure

```
meme-generator-app/
├── meme_generator_app.py    # Main Flask application
├── requirements.txt         # Python dependencies
├── templates/              # HTML templates
│   ├── base.html          # Base template with styling
│   ├── index.html         # Home page with template browser
│   └── create.html        # Meme creation page
└── README_meme_app.md     # This file
```

## Customization

### Adding New Templates
The app automatically fetches templates from the Memegen API, so new templates added to the API will appear in your app.

### Styling
Modify the CSS in `templates/base.html` to customize the appearance.

### Features
Add new features by modifying the Flask routes in `meme_generator_app.py`.

## Troubleshooting

### Common Issues

1. **Port already in use**
   - Change the port in `meme_generator_app.py` line 67
   - Or kill the process using the port

2. **API not responding**
   - Check your internet connection
   - Verify the Memegen API is accessible at https://api.memegen.link

3. **Dependencies not found**
   - Run `pip install -r requirements.txt` again
   - Check your Python version (3.7+ required)

### Error Messages

- **"Failed to load templates"**: API connection issue
- **"Template not found"**: Invalid template ID
- **"Please provide 1 or 2 lines of text"**: Form validation error

## Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## License

This project uses the Memegen API which is open source. The web app wrapper is provided as-is for educational purposes.

## Support

For issues with the Memegen API, visit: https://github.com/jacebrowning/memegen

For issues with this web app, check the troubleshooting section above. 
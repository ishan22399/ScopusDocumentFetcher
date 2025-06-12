# Scopus Document Search Web Application

A beautiful and modern web interface for searching academic publications using the Scopus API.

## Features

- 🔍 Search publications by Author ID
- 📚 Beautiful, responsive card-based layout
- 📊 Display key publication metrics (citations, journal, year)
- 🔗 Direct links to DOI
- 📱 Mobile-friendly design
- ⚡ Fast, AJAX-based search
- 🎨 Modern gradient design with smooth animations

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
Edit the `API_KEY` variable in `app.py` with your Elsevier Developer Portal API key:
```python
API_KEY = 'your_api_key_here'
```

### 3. Run the Application
```bash
python app.py
```

The application will be available at: `http://localhost:5000`

## Usage

1. Open your web browser and go to `http://localhost:5000`
2. Enter an Author ID in the search box (e.g., 58907937200)
3. Click "Search" or press Enter
4. Browse through the results displayed in beautiful cards
5. Click on DOI links to view the full publication

## Example Author IDs

- `58907937200` - Sample author
- `7004212771` - Another sample author
- `35079293200` - Third sample author

## API Information

This application uses the Elsevier Scopus API. You need to:
1. Register at the Elsevier Developer Portal
2. Get your API key
3. Replace the API_KEY in app.py

## File Structure

```
Scopus/
├── app.py              # Flask application
├── scoups.py          # Original script
├── requirements.txt   # Python dependencies
├── templates/
│   └── index.html     # Main HTML template
└── README.md          # This file
```

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Modern CSS with gradients and animations
- **Icons**: Font Awesome
- **API**: Elsevier Scopus API

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## Troubleshooting

1. **API Key Issues**: Make sure your API key is valid and active
2. **Network Issues**: Check your internet connection
3. **Port Conflicts**: Change the port in app.py if 5000 is already in use
4. **Dependencies**: Make sure all packages are installed correctly

## Contributing

Feel free to contribute to this project by:
- Improving the UI/UX
- Adding more search filters
- Implementing pagination
- Adding export functionality

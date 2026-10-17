# Le Chonk - Cat Health & Weight Tracker

A lightweight Flask-based web application for tracking your cats' weights, vaccinations, and documents.

## Features

- **Cat Management**: Add, edit, and delete cats with profiles
- **Weight Tracking**: Record and visualize weight over time with interactive charts
- **Document Storage**: Store vaccination records, medical documents, photos, and more
- **Modular Design**: Easy to extend with new entry types
- **SQLite Database**: Lightweight, file-based database (no server required)
- **Responsive UI**: Works on desktop and mobile

## Quick Start

### 1. Install Dependencies

```bash
cd leChonk
pip install -r requirements.txt
```

### 2. Initialize Database

```bash
# Set up the database
python3 -c "from app import create_app, db; app = create_app(); with app.app_context(): db.create_all(); print('Database initialized!')"
```

Or use Flask-Migrate for database migrations:

```bash
flask db init  # Only once
flask db migrate
flask db upgrade
```

### 3. Run the Application

```bash
python run.py
```

Then open your browser to: http://localhost:5000

## Usage

### Adding a Cat
1. Click "Add New Cat" on the homepage
2. Fill in the cat's name, breed, birth date, and any notes
3. Save the cat

### Adding Weight Entries
1. View a cat's profile
2. Click "Add Weight"
3. Enter the weight in kg, select a date, and add any notes
4. Save the entry

The weight chart will automatically update to show the cat's weight history.

### Adding Documents
1. View a cat's profile
2. Click "Add Document"
3. Select the document type (Vaccination, Medical Record, Insurance, Photo, Other)
4. Fill in the title, date, description
5. Optionally upload a file
6. Save the document

## Project Structure

```
leChonk/
├── app/
│   ├── __init__.py          # Application factory
│   ├── config.py            # Configuration settings
│   ├── models.py            # Database models
│   ├── routes.py            # URL routes and view functions
│   ├── static/
│   │   └── style.css        # CSS styles
│   └── templates/
│       ├── base.html        # Base template
│       ├── index.html       # Homepage (list all cats)
│       ├── cat.html         # Cat profile with entries
│       ├── cat_form.html    # Add/edit cat form
│       ├── weight_form.html # Add/edit weight form
│       └── document_form.html # Add/edit document form
├── config.py                # Configuration
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
└── README.md
```

## Modularity & Extensibility

The app is designed to be modular. You can add new entry types by:

1. **Adding a new model** in `models.py`
2. **Adding routes** in `routes.py`
3. **Adding templates** for the new entry type
4. **Registering the entry type** using `register_entry_type()`

Example:

```python
# In models.py
from app.models import ENTRY_TYPES, register_entry_type

class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat_id = db.Column(db.Integer, db.ForeignKey('cat.id'))
    # ... your fields

# Register the new type
register_entry_type(
    type_key='medication',
    name='Medication',
    model=Medication,
    icon='💊',
    route='medication',
    color='#FF9800'
)
```

## Configuration

You can customize the app by creating a `.env` file or modifying `config.py`:

```python
# Database
SQLALCHEMY_DATABASE_URI = 'sqlite:///lechonk.db'  # Default

# Upload settings
UPLOAD_FOLDER = 'path/to/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'png'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

# Secret key (change this in production!)
SECRET_KEY = 'your-secret-key-here'
```

## API Endpoints

The app includes simple JSON API endpoints:

- `GET /api/cats` - List all cats
- `GET /api/cat/<cat_id>/weights` - Get weight history for a cat

## Production Deployment

For production, use:

```bash
# Install a production WSGI server
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

Or with environment variables:

```bash
export FLASK_ENV=production
export SECRET_KEY='your-production-secret-key'
python run.py
```

## License

MIT License - Feel free to use and modify as needed.

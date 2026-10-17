# Le Chonk - Cat Health & Weight Tracker

A lightweight Flask-based web application for tracking your cats' weights, vaccinations, documents, and complete health history.

## Features

### 🐱 Core Features
- **Cat Management**: Add, edit, and delete cats with comprehensive profiles
- **Weight Tracking**: Record and visualize weight over time with interactive charts
- **Document Storage**: Store vaccination records, medical documents, photos, and more
- **Modular Design**: Easy to extend with new entry types
- **SQLite Database**: Lightweight, file-based database (no server required)
- **Responsive UI**: Works on desktop and mobile

### 👤 Cat Profile Details
- **Profile Pictures**: Upload and display photos for each cat
- **Owner Information**: Track who owns each cat
- **Microchip Number**: Record microchip IDs for identification
- **Place of Birth**: Document where each cat was born
- **Current Address**: Track where each cat currently lives

### ⚙️ Settings & Configuration
- **GUI Settings Page**: Configure application settings through the web interface
- **Database Migration**: Move your database and uploaded files to a new location
- **Custom Uploads Folder**: Specify where uploaded files are stored
- **Browse Helpers**: Quick path selection tools for migration

### 📊 User Interface
- **Collapsible Sections**: Expand/collapse weight entries and documents to save screen space
- **Interactive Charts**: Visualize weight history with Chart.js
- **Clean Design**: Modern, intuitive interface
- **Responsive**: Works on all screen sizes

## Quick Start

### 1. Install Dependencies

```bash
cd leChonk
pip install -r requirements.txt
```

### 2. Database Configuration

By default, the app uses SQLite and stores the database at `instance/lechonk.db`. 

**To use a custom database path:**
- Create a `.env` file (copy from `.env.example`)
- Set `DATABASE_URL` to your desired path:
  ```bash
  # SQLite at a custom location
  DATABASE_URL=sqlite:////path/to/your/database.db
  
  # PostgreSQL
  DATABASE_URL=postgresql://user:password@localhost/lechonk
  
  # MySQL
  DATABASE_URL=mysql+pymysql://user:password@localhost/lechonk
  ```

**Default:** The first time you run the app, it automatically creates the database at `instance/lechonk.db`.

### 3. Run the Application

```bash
python run.py
```

Then open your browser to: http://localhost:5000

**Note:** If you're on Windows, all paths work the same way - the app uses `os.path.join()` for cross-platform compatibility.

## GUI Settings

You can also configure the database path through the web interface:

1. Click the **⚙️ Settings** button in the top-right corner
2. Enter your desired **Database URI**
3. Optionally specify a custom **Uploads Folder** path
4. Click **Save Settings**
5. **Restart the application** for changes to take effect

The configuration is saved to `lechonk_config.json` (ignored by git).

## Database Migration

To move your database and uploaded files to a new location:

1. Click **⚙️ Settings** in the top-right corner
2. Scroll to the **Migrate Database** section
3. Enter the new **Database URI** (e.g., `sqlite:////new/path/to/lechonk.db`)
4. Check **Migrate uploaded files** to also copy your document uploads
5. Optionally specify a **New Uploads Folder Path** or leave blank to auto-create next to the database
6. Click **Migrate Database**
7. **Restart the application** to use the new database location

**Important Notes:**
- Browser security prevents automatic folder browsing - you must type the full absolute path
- Use the helper buttons ("Use Current Path", "Use Home Directory") for easier path entry
- The migration copies the SQLite database file and all uploaded documents
- Always restart the application after migration
- The old database and files are NOT deleted - you can keep them as backup

## Usage

### Adding a Cat
1. Click "➕ Add New Cat" on the homepage
2. Fill in the cat's details:
   - **Name** (required)
   - **Breed**
   - **Birth Date**
   - **Owner** - Who owns this cat
   - **Microchip Number** - Unique identification number
   - **Place of Birth** - Where the cat was born
   - **Current Address** - Where the cat currently lives
   - **Profile Picture** - Upload a photo
   - **Notes** - Any additional information
3. Click "Save Cat"

### Managing Profile Pictures
- Upload a photo when adding or editing a cat
- Profile pictures appear as circular images in:
  - Cat tiles on the homepage
  - Cat profile page header
- Remove profile pictures using the "Remove current picture" checkbox

### Adding Weight Entries
1. View a cat's profile
2. Click "➕ Add Weight"
3. Enter the weight in kg, select a date, and add any notes
4. Click "Save"

The weight chart will automatically update to show the cat's weight history.

### Adding Documents
1. View a cat's profile
2. Click "📄 Add Document"
3. Select the document type (Vaccination, Medical Record, Insurance, Photo, Other)
4. Fill in the title, date, description
5. Optionally upload a file
6. Click "Save"

### Using Collapsible Sections
- **Weight Entries** and **Documents** sections can be collapsed
- Click the section header to toggle visibility
- Useful for focusing on specific information
- Icons show collapse (▶) or expand (▼) state

## Project Structure

```
leChonk/
├── app/
│   ├── __init__.py          # Application factory
│   ├── config.py            # Configuration settings
│   ├── models.py            # Database models (Cat, WeightEntry, Document)
│   ├── routes.py            # URL routes and view functions
│   ├── static/
│   │   └── style.css        # CSS styles
│   └── templates/
│       ├── base.html        # Base template
│       ├── index.html       # Homepage (list all cats)
│       ├── cat.html         # Cat profile with entries
│       ├── cat_form.html    # Add/edit cat form
│       ├── weight_form.html # Add/edit weight form
│       ├── document_form.html # Add/edit document form
│       └── settings.html    # Application settings page
├── config.py                # Configuration
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── ROADMAP.md              # Feature roadmap and development plan
├── MIGRATION_GUIDE.md      # Database migration guide
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

## Cat Profile Fields

Each cat can have the following information stored:

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| name | String | Cat's name | ✅ Yes |
| breed | String | Cat's breed | ❌ No |
| birth_date | Date | Date of birth | ❌ No |
| owner | String | Name of the owner | ❌ No |
| microchip_number | String | Microchip identification | ❌ No |
| place_of_birth | String | Where the cat was born | ❌ No |
| current_address | String | Current location | ❌ No |
| profile_picture | String | Filename of profile image | ❌ No |
| notes | Text | Additional notes | ❌ No |

**Note:** All fields except **name** are optional. You can add information as you have it available.

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

## Development

### Feature Roadmap

Check out the [ROADMAP.md](ROADMAP.md) file for:
- Planned features and timeline
- Technical implementation details
- Contribution guidelines

### Database Migration Guide

See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for detailed instructions on:
- Moving your database to a new location
- Migrating uploaded documents
- Configuration options

## License

MIT License - Feel free to use and modify as needed.

# Database Migration Guide

## Overview

Le Chonk now supports **database migration through the GUI**, allowing you to:
- Change the database location
- Move uploaded documents to a new location
- Configure custom uploads folder

## Migration Methods

### Method 1: Using the Settings Page (Recommended)

1. **Open Settings**
   - Click the **⚙️ Settings** button in the top-right corner
   
2. **Configure Database URI**
   - In the "Database Configuration" section, enter your new database path
   - Example: `sqlite:////home/yourname/Documents/lechonk.db`
   - Click **Save Settings**
   
3. **Restart the Application**
   - Stop the Flask server (Ctrl+C)
   - Start it again: `python run.py`
   
4. **Migrate Existing Data (if needed)**
   - Use the "Migrate Database" tool in the Settings page
   - Enter the new database URI
   - Check "Migrate uploaded files" to also move documents
   - Optionally specify a custom uploads folder
   - Click **Migrate Database**
   - Restart the application

### Method 2: Using Configuration File

1. **Edit `lechonk_config.json`**
   ```json
   {
     "DATABASE_URL": "sqlite:////path/to/your/database.db",
     "UPLOAD_FOLDER": "/path/to/your/uploads"
   }
   ```

2. **Restart the application**

### Method 3: Manual Migration

1. **Stop the application**
2. **Copy the database file**
   ```bash
   cp instance/lechonk.db /new/path/to/lechonk.db
   ```
3. **Copy uploaded files** (if needed)
   ```bash
   cp -r app/static/uploads /new/path/to/uploads
   ```
4. **Update configuration**
   - Edit `lechonk_config.json` or use the Settings page
5. **Restart the application**

## Path Formats

### SQLite Database Paths

**Linux/Mac:**
```
sqlite:////home/username/lechonk/lechonk.db
```

**Windows:**
```
sqlite:///C:/Users/YourName/Documents/lechonk.db
# or
sqlite:///C:\Users\YourName\Documents\lechonk.db
```

**Relative Path (from project root):**
```
sqlite:///data/lechonk.db
```

### Uploads Folder Paths

Use **absolute paths** for reliability:
- Linux/Mac: `/home/username/lechonk_uploads`
- Windows: `C:\Users\YourName\lechonk_uploads`

## Quick Path Helpers

In the Settings page, use the helper buttons:
- **"Use Current Path"** - Inserts the current database path with a new filename
- **"Use Home Directory"** - Inserts a path in your home directory (edit the username)

## Important Notes

### Browser Security Limitations
- **Browser security prevents automatic folder browsing** - you must type the full path
- This is a security feature to prevent websites from accessing your local files
- The path helpers make this easier

### Migration Behavior
- **Database file is copied** (SQLite only for now)
- **Uploaded files are copied** if "Migrate uploaded files" is checked
- **Configuration is updated** in `lechonk_config.json`
- **Old files are NOT deleted** - you can keep them as backup
- **Application must be restarted** to use the new configuration

### File Permissions
- Ensure the new database directory is **writable** by your user
- Ensure the new uploads directory is **writable** by your user
- Test by creating a file manually:
  ```bash
  touch /new/path/test.txt
  ```

## Troubleshooting

### Migration Failed
- Check that the target directory exists
- Check that you have write permissions
- Check that the database file is not open in another application

### Data Not Showing After Migration
- Did you **restart the application**?
- Is the new database path correct in `lechonk_config.json`?
- Check the application logs for errors

### Uploaded Files Not Found
- Did you check "Migrate uploaded files"?
- Did you specify the correct uploads folder path?
- Check that files exist in the new location

## Advanced Configuration

### Multiple Databases
You can maintain multiple databases by:
1. Creating separate config files
2. Switching between them by editing `lechonk_config.json`
3. Restarting the application

### Custom Database Types
The app supports:
- SQLite (default)
- PostgreSQL
- MySQL

For PostgreSQL/MySQL, you'll need to:
1. Install the appropriate Python package
2. Set the DATABASE_URL in the correct format
3. The migration tool currently only supports SQLite

## Examples

### Example 1: Move to External Drive
```
Database URI: sqlite:////mnt/external/lechonk/lechonk.db
Uploads Folder: /mnt/external/lechonk/uploads
```

### Example 2: Move to Dropbox/Cloud Folder
```
Database URI: sqlite:////home/username/Dropbox/lechonk/lechonk.db
Uploads Folder: /home/username/Dropbox/lechonk/uploads
```

### Example 3: Custom Structure
```
Database URI: sqlite:////home/username/cat_data/database.db
Uploads Folder: /home/username/cat_data/documents
```

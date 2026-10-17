from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, current_app
from werkzeug.utils import secure_filename
from app.models import Cat, WeightEntry, Document, ENTRY_TYPES
from app import db
from datetime import datetime
import os

main = Blueprint('main', __name__)


def allowed_file(filename):
    """Check if the file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@main.route('/')
def index():
    """List all cats"""
    cats = Cat.query.order_by(Cat.name).all()
    return render_template('index.html', cats=cats, entry_types=ENTRY_TYPES)


@main.route('/cat/<int:cat_id>')
def view_cat(cat_id):
    """View a cat's details and all entries"""
    cat = Cat.query.get_or_404(cat_id)
    
    # Get all weight entries
    weights = WeightEntry.query.filter_by(cat_id=cat_id).order_by(WeightEntry.date.desc()).all()
    
    # Get all documents
    documents = Document.query.filter_by(cat_id=cat_id).order_by(Document.date.desc()).all()
    
    return render_template('cat.html', cat=cat, weights=weights, documents=documents, entry_types=ENTRY_TYPES)


@main.route('/cat/<int:cat_id>/delete', methods=['POST'])
def delete_cat(cat_id):
    """Delete a cat and all its entries"""
    cat = Cat.query.get_or_404(cat_id)
    
    # Delete profile picture if exists
    if cat.profile_picture and os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], cat.profile_picture)):
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], cat.profile_picture))
    
    # Delete associated files
    for doc in cat.documents:
        if doc.file_path and os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], doc.file_path)):
            os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], doc.file_path))
    
    db.session.delete(cat)
    db.session.commit()
    flash(f'Cat "{cat.name}" and all its data have been deleted.', 'success')
    return redirect(url_for('main.index'))


# =====================
# CAT MANAGEMENT
# =====================

@main.route('/cat/add', methods=['GET', 'POST'])
def add_cat():
    """Add a new cat"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        breed = request.form.get('breed', '').strip()
        birth_date_str = request.form.get('birth_date')
        owner = request.form.get('owner', '').strip()
        microchip_number = request.form.get('microchip_number', '').strip()
        place_of_birth = request.form.get('place_of_birth', '').strip()
        current_address = request.form.get('current_address', '').strip()
        notes = request.form.get('notes', '').strip()
        
        if not name:
            flash('Cat name is required.', 'error')
            return render_template('cat_form.html', cat=None)
        
        birth_date = None
        if birth_date_str:
            try:
                birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid birth date format.', 'error')
                return render_template('cat_form.html', cat=None)
        
        # Handle profile picture upload
        profile_picture_path = None
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to prevent conflicts
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                unique_filename = f"{timestamp}_{filename}"
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename))
                profile_picture_path = unique_filename
        
        cat = Cat(
            name=name,
            breed=breed or None,
            birth_date=birth_date,
            owner=owner or None,
            microchip_number=microchip_number or None,
            place_of_birth=place_of_birth or None,
            current_address=current_address or None,
            profile_picture=profile_picture_path,
            notes=notes or None
        )
        db.session.add(cat)
        db.session.commit()
        flash(f'Cat "{name}" added successfully!', 'success')
        return redirect(url_for('main.view_cat', cat_id=cat.id))
    
    return render_template('cat_form.html', cat=None)


@main.route('/cat/<int:cat_id>/edit', methods=['GET', 'POST'])
def edit_cat(cat_id):
    """Edit an existing cat"""
    cat = Cat.query.get_or_404(cat_id)
    
    if request.method == 'POST':
        cat.name = request.form.get('name', '').strip()
        cat.breed = request.form.get('breed', '').strip() or None
        cat.owner = request.form.get('owner', '').strip() or None
        
        birth_date_str = request.form.get('birth_date')
        if birth_date_str:
            try:
                cat.birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid birth date format.', 'error')
        else:
            cat.birth_date = None
        
        cat.microchip_number = request.form.get('microchip_number', '').strip() or None
        cat.place_of_birth = request.form.get('place_of_birth', '').strip() or None
        cat.current_address = request.form.get('current_address', '').strip() or None
        cat.notes = request.form.get('notes', '').strip() or None
        
        # Handle profile picture upload/replace
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file and file.filename != '' and allowed_file(file.filename):
                # Delete old profile picture if exists
                if cat.profile_picture and os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], cat.profile_picture)):
                    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], cat.profile_picture))
                
                # Save new picture
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                unique_filename = f"{timestamp}_{filename}"
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename))
                cat.profile_picture = unique_filename
        
        # Handle profile picture removal
        if request.form.get('remove_profile_pic') == '1':
            if cat.profile_picture and os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], cat.profile_picture)):
                os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], cat.profile_picture))
            cat.profile_picture = None
        
        db.session.commit()
        flash(f'Cat "{cat.name}" updated successfully!', 'success')
        return redirect(url_for('main.view_cat', cat_id=cat.id))
    
    return render_template('cat_form.html', cat=cat)


# =====================
# WEIGHT ENTRIES
# =====================

@main.route('/cat/<int:cat_id>/weight/add', methods=['GET', 'POST'])
def add_weight(cat_id):
    """Add a weight entry for a cat"""
    cat = Cat.query.get_or_404(cat_id)
    today = datetime.utcnow().strftime('%Y-%m-%d')
    
    if request.method == 'POST':
        try:
            weight_kg = float(request.form.get('weight_kg'))
        except (ValueError, TypeError):
            flash('Please enter a valid weight.', 'error')
            return render_template('weight_form.html', cat=cat, weight=None, today=today)
        
        date_str = request.form.get('date')
        notes = request.form.get('notes', '').strip()
        
        if date_str:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format.', 'error')
                return render_template('weight_form.html', cat=cat, weight=None, today=today)
        else:
            date = datetime.utcnow().date()
        
        entry = WeightEntry(
            cat_id=cat_id,
            weight_kg=weight_kg,
            date=date,
            notes=notes or None
        )
        db.session.add(entry)
        db.session.commit()
        flash(f'Weight entry added: {weight_kg}kg on {date}', 'success')
        return redirect(url_for('main.view_cat', cat_id=cat_id))
    
    return render_template('weight_form.html', cat=cat, weight=None, today=today)


@main.route('/weight/<int:weight_id>/edit', methods=['GET', 'POST'])
def edit_weight(weight_id):
    """Edit a weight entry"""
    weight = WeightEntry.query.get_or_404(weight_id)
    today = datetime.utcnow().strftime('%Y-%m-%d')
    
    if request.method == 'POST':
        try:
            weight.weight_kg = float(request.form.get('weight_kg'))
        except (ValueError, TypeError):
            flash('Please enter a valid weight.', 'error')
            return render_template('weight_form.html', cat=weight.cat, weight=weight, today=today)
        
        date_str = request.form.get('date')
        if date_str:
            try:
                weight.date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format.', 'error')
                return render_template('weight_form.html', cat=weight.cat, weight=weight, today=today)
        
        weight.notes = request.form.get('notes', '').strip() or None
        db.session.commit()
        flash('Weight entry updated!', 'success')
        return redirect(url_for('main.view_cat', cat_id=weight.cat_id))
    
    return render_template('weight_form.html', cat=weight.cat, weight=weight, today=today)


@main.route('/weight/<int:weight_id>/delete', methods=['POST'])
def delete_weight(weight_id):
    """Delete a weight entry"""
    weight = WeightEntry.query.get_or_404(weight_id)
    cat_id = weight.cat_id
    db.session.delete(weight)
    db.session.commit()
    flash('Weight entry deleted.', 'success')
    return redirect(url_for('main.view_cat', cat_id=cat_id))


# =====================
# DOCUMENTS
# =====================

@main.route('/cat/<int:cat_id>/document/add', methods=['GET', 'POST'])
def add_document(cat_id):
    """Add a document for a cat"""
    cat = Cat.query.get_or_404(cat_id)
    today = datetime.utcnow().strftime('%Y-%m-%d')
    
    if request.method == 'POST':
        doc_type = request.form.get('doc_type')
        title = request.form.get('title', '').strip()
        date_str = request.form.get('date')
        description = request.form.get('description', '').strip()
        
        if not doc_type:
            flash('Document type is required.', 'error')
            return render_template('document_form.html', cat=cat, document=None, today=today, doc_types=Document.DOC_TYPES)
        
        if not title:
            flash('Title is required.', 'error')
            return render_template('document_form.html', cat=cat, document=None, today=today, doc_types=Document.DOC_TYPES)
        
        date = None
        if date_str:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format.', 'error')
                return render_template('document_form.html', cat=cat, document=None, today=today, doc_types=Document.DOC_TYPES)
        
        # Handle file upload
        file_path = None
        original_filename = None
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to prevent conflicts
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                unique_filename = f"{timestamp}_{filename}"
                file_path = unique_filename
                original_filename = file.filename
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename))
        
        doc = Document(
            cat_id=cat_id,
            doc_type=doc_type,
            title=title,
            date=date,
            description=description or None,
            file_path=file_path,
            original_filename=original_filename
        )
        db.session.add(doc)
        db.session.commit()
        flash(f'Document "{title}" added successfully!', 'success')
        return redirect(url_for('main.view_cat', cat_id=cat_id))
    
    return render_template('document_form.html', cat=cat, document=None, today=today, doc_types=Document.DOC_TYPES)


@main.route('/document/<int:doc_id>/edit', methods=['GET', 'POST'])
def edit_document(doc_id):
    """Edit a document"""
    doc = Document.query.get_or_404(doc_id)
    today = datetime.utcnow().strftime('%Y-%m-%d')
    
    if request.method == 'POST':
        doc.doc_type = request.form.get('doc_type')
        doc.title = request.form.get('title', '').strip()
        
        date_str = request.form.get('date')
        if date_str:
            try:
                doc.date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format.', 'error')
                return render_template('document_form.html', cat=doc.cat, document=doc, today=today, doc_types=Document.DOC_TYPES)
        else:
            doc.date = None
        
        doc.description = request.form.get('description', '').strip() or None
        
        # Handle file upload (replace existing file)
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename != '' and allowed_file(file.filename):
                # Delete old file if exists
                if doc.file_path and os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], doc.file_path)):
                    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], doc.file_path))
                
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                unique_filename = f"{timestamp}_{filename}"
                doc.file_path = unique_filename
                doc.original_filename = file.filename
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename))
        
        db.session.commit()
        flash('Document updated!', 'success')
        return redirect(url_for('main.view_cat', cat_id=doc.cat_id))
    
    return render_template('document_form.html', cat=doc.cat, document=doc, today=today, doc_types=Document.DOC_TYPES)
    return render_template('document_form.html', cat=doc.cat, document=doc, doc_types=Document.DOC_TYPES)


@main.route('/document/<int:doc_id>/delete', methods=['POST'])
def delete_document(doc_id):
    """Delete a document and its file"""
    doc = Document.query.get_or_404(doc_id)
    cat_id = doc.cat_id
    
    # Delete file if exists
    if doc.file_path and os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], doc.file_path)):
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], doc.file_path))
    
    db.session.delete(doc)
    db.session.commit()
    flash('Document deleted.', 'success')
    return redirect(url_for('main.view_cat', cat_id=cat_id))


@main.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


# =====================
# API ENDPOINTS (for future modularity)
# =====================

@main.route('/api/cats')
def api_cats():
    """JSON API: list all cats"""
    cats = Cat.query.all()
    return {
        'cats': [{
            'id': cat.id,
            'name': cat.name,
            'breed': cat.breed,
            'birth_date': cat.birth_date.isoformat() if cat.birth_date else None
        } for cat in cats]
    }


@main.route('/api/cat/<int:cat_id>/weights')
def api_weights(cat_id):
    """JSON API: get weight history for a cat"""
    weights = WeightEntry.query.filter_by(cat_id=cat_id).order_by(WeightEntry.date).all()
    return {
        'weights': [{
            'date': w.date.isoformat(),
            'weight_kg': w.weight_kg,
            'notes': w.notes
        } for w in weights]
    }


# =====================
# SETTINGS
# =====================

@main.route('/settings', methods=['GET', 'POST'])
def settings():
    """Configuration settings page"""
    import json
    import os
    
    # Config file path
    config_file = os.path.join(current_app.root_path, '..', 'lechonk_config.json')
    
    # Load existing config or use defaults
    config = {}
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
        except:
            config = {}
    
    if request.method == 'POST':
        # Get the new database URI
        db_uri = request.form.get('db_uri', '').strip()
        upload_folder = request.form.get('upload_folder', '').strip()
        
        if db_uri:
            config['DATABASE_URL'] = db_uri
        
        if upload_folder:
            config['UPLOAD_FOLDER'] = upload_folder
        
        # Save to config file
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        flash('Settings saved! Please restart the application for changes to take effect.', 'success')
        return redirect(url_for('main.settings'))
    
    # Get current database URI
    current_db_uri = config.get('DATABASE_URL', current_app.config['SQLALCHEMY_DATABASE_URI'])
    current_upload_folder = config.get('UPLOAD_FOLDER', current_app.config['UPLOAD_FOLDER'])
    
    return render_template('settings.html', current_db_uri=current_db_uri, 
                         current_upload_folder=current_upload_folder,
                         default_upload_folder=current_app.config['UPLOAD_FOLDER'])


@main.route('/settings/reset-db', methods=['POST'])
def reset_db():
    """Reset the database configuration to default"""
    import os
    config_file = os.path.join(current_app.root_path, '..', 'lechonk_config.json')
    
    if os.path.exists(config_file):
        os.remove(config_file)
        flash('Database configuration reset to default. Please restart the application.', 'success')
    else:
        flash('No custom database configuration found.', 'info')
    
    return redirect(url_for('main.settings'))


@main.route('/migrate-db', methods=['POST'])
def migrate_db():
    """Migrate all data to a new database location"""
    import json
    import os
    import shutil
    
    new_db_uri = request.form.get('new_db_uri', '').strip()
    migrate_uploads = request.form.get('migrate_uploads') == 'yes'
    new_uploads_path = request.form.get('new_uploads_path', '').strip()
    
    if not new_db_uri:
        flash('New database URI is required.', 'error')
        return redirect(url_for('main.settings'))
    
    # Get current database path
    current_db_uri = current_app.config['SQLALCHEMY_DATABASE_URI']
    
    # Parse database URIs to get file paths
    def get_db_path(uri):
        """Extract file path from SQLite URI"""
        if uri.startswith('sqlite:///'):
            return uri.replace('sqlite:///', '')
        return None
    
    current_db_path = get_db_path(current_db_uri)
    new_db_path = get_db_path(new_db_uri)
    
    if not current_db_path or not new_db_path:
        flash('Only SQLite database migration is supported through this interface.', 'error')
        return redirect(url_for('main.settings'))
    
    # Check if new database already exists
    if os.path.exists(new_db_path):
        flash(f'Database file already exists at {new_db_path}. Please choose a different location.', 'error')
        return redirect(url_for('main.settings'))
    
    try:
        # Step 1: Ensure the directory for the new database exists
        new_db_dir = os.path.dirname(new_db_path)
        if new_db_dir:
            os.makedirs(new_db_dir, exist_ok=True)
        
        # Step 2: Copy the database file (SQLite supports this)
        shutil.copy2(current_db_path, new_db_path)
        
        # Step 3: Handle uploads migration if requested
        if migrate_uploads:
            current_uploads = current_app.config['UPLOAD_FOLDER']
            
            if new_uploads_path:
                target_uploads = new_uploads_path
            else:
                # Use the same relative structure as the new db location
                # Extract the base directory from the new db path
                target_uploads = os.path.join(new_db_dir, 'app', 'static', 'uploads')
            
            # Check if target uploads directory exists
            if os.path.exists(target_uploads):
                # Check if there are files there
                if os.listdir(target_uploads):
                    flash(f'Target uploads directory {target_uploads} already exists and is not empty. Uploads not migrated.', 'warning')
                else:
                    # Directory exists but empty, we can use it
                    pass
            else:
                # Create the target uploads directory
                os.makedirs(target_uploads, exist_ok=True)
            
            # Copy all files from current uploads to target uploads
            if os.path.exists(current_uploads) and os.path.isdir(current_uploads):
                for item in os.listdir(current_uploads):
                    src = os.path.join(current_uploads, item)
                    dst = os.path.join(target_uploads, item)
                    if os.path.isfile(src):
                        shutil.copy2(src, dst)
            
            # Update the config to point to the new uploads location
            # Store relative path from the app directory
            import os.path
            app_dir = os.path.dirname(current_app.root_path)
            rel_uploads_path = os.path.relpath(target_uploads, app_dir)
        
        # Step 4: Save new config
        config_file = os.path.join(current_app.root_path, '..', 'lechonk_config.json')
        config = {}
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
        config['DATABASE_URL'] = new_db_uri
        if migrate_uploads and new_uploads_path:
            # Store the uploads path if a custom one was specified
            config['UPLOAD_FOLDER'] = new_uploads_path
        elif migrate_uploads:
            # Otherwise store the relative path
            config['UPLOAD_FOLDER'] = rel_uploads_path
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        msg = f'Successfully migrated database to {new_db_uri}'
        if migrate_uploads:
            msg += f' and uploaded files to {target_uploads}'
        msg += '. Please restart the application.'
        flash(msg, 'success')
        return redirect(url_for('main.settings'))
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        flash(f'Migration failed: {str(e)}', 'error')
        return redirect(url_for('main.settings'))

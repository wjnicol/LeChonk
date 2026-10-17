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
        
        cat = Cat(
            name=name,
            breed=breed or None,
            birth_date=birth_date,
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
        
        birth_date_str = request.form.get('birth_date')
        if birth_date_str:
            try:
                cat.birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid birth date format.', 'error')
        else:
            cat.birth_date = None
        
        cat.notes = request.form.get('notes', '').strip() or None
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

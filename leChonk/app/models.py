from app import db
from datetime import datetime
import os


class Cat(db.Model):
    """Represents a cat in the database"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    breed = db.Column(db.String(100))
    birth_date = db.Column(db.Date)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    weight_entries = db.relationship('WeightEntry', backref='cat', lazy=True, cascade='all, delete-orphan')
    documents = db.relationship('Document', backref='cat', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Cat {self.name}>'
    
    def latest_weight(self):
        """Get the most recent weight entry"""
        return WeightEntry.query.filter_by(cat_id=self.id).order_by(WeightEntry.date.desc()).first()
    
    def weight_history(self):
        """Get all weight entries sorted by date"""
        return WeightEntry.query.filter_by(cat_id=self.id).order_by(WeightEntry.date).all()


class WeightEntry(db.Model):
    """Represents a weight measurement for a cat"""
    id = db.Column(db.Integer, primary_key=True)
    cat_id = db.Column(db.Integer, db.ForeignKey('cat.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    weight_kg = db.Column(db.Float, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<WeightEntry {self.cat.name}: {self.weight_kg}kg on {self.date}>'


class Document(db.Model):
    """Represents a document (vaccination, medical record, etc.) for a cat"""
    id = db.Column(db.Integer, primary_key=True)
    cat_id = db.Column(db.Integer, db.ForeignKey('cat.id'), nullable=False)
    doc_type = db.Column(db.String(50), nullable=False)  # e.g., 'vaccination', 'medical_record', 'insurance', 'photo'
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date)
    description = db.Column(db.Text)
    file_path = db.Column(db.String(255))  # Relative path to uploaded file
    original_filename = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    DOC_TYPES = [
        ('vaccination', 'Vaccination'),
        ('medical_record', 'Medical Record'),
        ('insurance', 'Insurance'),
        ('photo', 'Photo'),
        ('other', 'Other')
    ]
    
    @classmethod
    def get_type_label(cls, doc_type):
        """Get human-readable label for document type"""
        for value, label in cls.DOC_TYPES:
            if value == doc_type:
                return label
        return doc_type
    
    def __repr__(self):
        return f'<Document {self.title} ({self.doc_type}) for {self.cat.name}>'
    
    def file_exists(self):
        """Check if the file still exists on disk"""
        if not self.file_path:
            return False
        import os
        from flask import current_app
        full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], self.file_path)
        return os.path.exists(full_path)
    
    def file_url(self):
        """Get URL for the file"""
        if self.file_path:
            return f'/static/uploads/{self.file_path}'
        return None


# Entry type registry for modularity
ENTRY_TYPES = {
    'weight': {
        'name': 'Weight',
        'model': WeightEntry,
        'icon': '⚖️',
        'route': 'weight',
        'color': '#4CAF50'
    },
    'document': {
        'name': 'Document',
        'model': Document,
        'icon': '📄',
        'route': 'document',
        'color': '#2196F3'
    }
}


def register_entry_type(type_key, name, model, icon='📝', route=None, color='#9E9E9E'):
    """Register a new entry type for modular extension"""
    ENTRY_TYPES[type_key] = {
        'name': name,
        'model': model,
        'icon': icon,
        'route': route or type_key,
        'color': color
    }

# Le Chonk - Feature Roadmap

This document outlines the planned features and development roadmap for Le Chonk, the cat health and weight tracking application.

---

## 🗺️ Current Features

### ✅ Implemented
- [x] **Cat Management** - Add, edit, delete cats
- [x] **Weight Tracking** - Record and visualize weight over time
- [x] **Document Storage** - Upload and manage cat documents
- [x] **Profile Pictures** - Upload and display cat profile pictures
- [x] **Database Migration** - Move database and files to new location via GUI
- [x] **GUI Settings** - Configure database path and uploads folder
- [x] **Collapsible Sections** - Weight entries and documents can be collapsed
- [x] **Microchip Number** - Track microchip IDs for each cat
- [x] **Place of Birth** - Record where each cat was born
- [x] **Current Address** - Track where each cat lives
- [x] **Owner Information** - Assign an owner to each cat

---

## 🎯 Upcoming Features

### 📅 Timeline Feature (High Priority)

**Objective**: Automatically extract dates and medical events from uploaded documents to create a comprehensive timeline for each cat.

#### Phase 1: Foundation (1-2 hours)
- [ ] Add `TimelineEntry` model to database
  - Fields: date, action, description, source_document, source_text, confidence
  - Relationship: belongs to Cat
- [ ] Create database migration for TimelineEntry
- [ ] Add timeline section to cat profile page
- [ ] Basic timeline UI (list view)
- [ ] Manual timeline entry creation form

#### Phase 2: Document Processing (3-4 hours)
- [ ] Install required dependencies (PyPDF2, pdfplumber, dateparser)
- [ ] Create text extraction utilities
  - [ ] PDF parser
  - [ ] Image OCR (optional, requires tesseract)
  - [ ] Word document parser
- [ ] Implement date detection
  - [ ] Use `dateparser` library for flexible date parsing
  - [ ] Handle multiple date formats
  - [ ] Validate dates are medical-related
- [ ] Implement action detection
  - [ ] Keyword-based matching (vaccination, medication, etc.)
  - [ ] Medical action classification
- [ ] Create processing pipeline
  - [ ] Function to process document and extract entries
  - [ ] Duplicate detection

#### Phase 3: Processing Triggers (1-2 hours)
- [ ] Automatic processing on document upload
- [ ] Manual processing button per document
- [ ] Batch processing for all cat documents
- [ ] Processing status tracking

#### Phase 4: Enhanced UI (2-3 hours)
- [ ] Visual timeline with Chart.js
- [ ] Filter timeline by type (vaccinations, treatments, etc.)
- [ ] Search timeline entries
- [ ] Export timeline to PDF/CSV
- [ ] Timeline as default view option

#### Phase 5: Advanced Features (Optional)
- [ ] NLP-based action detection with spaCy
- [ ] Improved OCR for images
- [ ] Context-aware date validation
- [ ] Confidence scoring for extracted data
- [ ] Timeline comparison between cats
- [ ] Reminder system based on timeline (next vaccination due)

#### Phase 6: Testing & Refinement
- [ ] Test with various document formats
- [ ] Validate date extraction accuracy
- [ ] Test with real-world documents
- [ ] Performance optimization for large timelines

**Total Estimated Time**: 8-14 hours (depending on scope)

---

## 📋 Feature Backlog

### Medium Priority
- [ ] **Multi-user Support** - Separate cat ownership by user accounts
- [ ] **Search & Filter** - Search cats by name, breed, microchip, etc.
- [ ] **Export Data** - Export cat data to CSV/JSON/PDF
- [ ] **Import from CSV** - Bulk import cat data
- [ ] **Reminders** - Set reminders for vaccinations, checkups, etc.
- [ ] **Breed Database** - Standardized breed list with information
- [ ] **Age Calculator** - Automatically calculate cat age from birth date

### Low Priority
- [ ] **Mobile App** - Native mobile application
- [ ] **API** - REST API for third-party integration
- [ ] **Webhooks** - Notifications for events
- [ ] **Themes** - Dark/light mode and custom themes
- [ ] **Statistics** - Advanced analytics and insights
- [ ] **Backup/Restore** - Automated backup system
- [ ] **Multi-cat Operations** - Bulk actions on multiple cats

---

## 🛠️ Technical Improvements

### Infrastructure
- [ ] **Docker Support** - Containerized deployment
- [ ] **Test Suite** - Automated testing
- [ ] **CI/CD Pipeline** - Automated deployment
- [ ] **Performance Optimization** - Database indexing, caching
- [ ] **Error Tracking** - Sentry or similar integration

### Security
- [ ] **Authentication** - User login system
- [ ] **Authorization** - Role-based access control
- [ ] **Data Encryption** - Encrypt sensitive data at rest
- [ ] **Audit Logging** - Track changes to data

---

## 📦 Dependencies for Timeline Feature

### Required Python Packages
```
PyPDF2==3.0.0+          # PDF text extraction
pdfplumber==0.10.0+    # Advanced PDF extraction (optional)
pillow==10.0.0+        # Image processing
pytesseract==0.3.10+  # OCR for images (optional)
python-docx==1.1.0+    # Word document parsing
dateparser==1.1.0+     # Flexible date parsing
```

### Optional Packages
```
spacy==3.7.0+          # NLP for advanced text processing
en-core-web-sm        # spaCy English language model
```

### System Dependencies
- **Tesseract OCR** (for image text extraction)
  - Linux: `sudo apt-get install tesseract-ocr`
  - Mac: `brew install tesseract`
  - Windows: Download installer from [Tesseract GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

---

## 🎨 UI/UX Improvements

- [ ] **Dashboard** - Overview page with all cat stats
- [ ] **Responsive Design** - Better mobile experience
- [ ] **Animations** - Smoother transitions
- [ ] **Accessibility** - WCAG compliance
- [ ] **Internationalization** - Multiple language support

---

## 📅 Version History

### v1.0.0 (Current)
- Initial release with cat management, weight tracking, and document storage

### v1.1.0
- Added: Profile pictures, microchip number, place of birth, current address, owner
- Added: Collapsible sections, database migration GUI

### v1.2.0 (Planned)
- Timeline feature (Phase 1-3)

### v1.3.0 (Planned)
- Timeline feature (Phase 4-6)
- Multi-user support

---

## 💡 Contribution Guidelines

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/timeline`)
3. Make your changes
4. Add tests for new functionality
5. Update documentation
6. Submit a pull request

### Feature Requests
- Open an issue with a clear description
- Include use cases and examples
- Discuss before implementation

### Bug Reports
- Include steps to reproduce
- Add error messages
- Note browser/OS if applicable

---

## 📊 Priority Levels

- **🔴 High Priority**: Core functionality, bug fixes, security issues
- **🟡 Medium Priority**: Important features, improvements
- **🟢 Low Priority**: Nice-to-have, enhancements

---

## 🎯 Next Steps

The **Timeline Feature** is the next major feature to be implemented. It will:

1. **Automatically extract** medical events from documents
2. **Create visual timelines** for each cat
3. **Provide insights** into health history
4. **Enable reminders** for upcoming treatments

**Expected Timeline**: 1-2 weeks for basic implementation

---

*Last Updated: October 16, 2026*

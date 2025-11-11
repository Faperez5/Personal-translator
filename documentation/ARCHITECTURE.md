# System Architecture

## High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     USER BROWSER                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Frontend (HTML/CSS/JavaScript)                        │ │
│  │  - File Upload UI                                      │ │
│  │  - Translation Controls                                │ │
│  │  - Audio Player                                        │ │
│  │  - Text Highlighting                                   │ │
│  └─────────────┬──────────────────────────────────────────┘ │
└────────────────┼────────────────────────────────────────────┘
                 │ HTTP/AJAX
                 │ (JSON)
┌────────────────▼────────────────────────────────────────────┐
│              FLASK BACKEND SERVER                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  API Routes                                          │   │
│  │  - /api/upload           - /api/translate            │   │
│  │  - /api/translate/doc    - /api/tts/generate         │   │
│  └─────┬──────────┬──────────────┬─────────────────────┘   │
│        │          │              │                          │
│  ┌─────▼────┐ ┌──▼──────────┐ ┌─▼──────────────┐          │
│  │   PDF    │ │ Translation │ │      TTS       │          │
│  │Processor │ │   Service   │ │    Service     │          │
│  └─────┬────┘ └──┬──────────┘ └─┬──────────────┘          │
└────────┼─────────┼───────────────┼─────────────────────────┘
         │         │               │
         │         │               │
┌────────▼─────────▼───────────────▼─────────────────────────┐
│              EXTERNAL SERVICES                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  pdfplumber  │  │  googletrans │  │     gTTS     │      │
│  │   PyPDF2     │  │    DeepL     │  │  (Google)    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└──────────────────────────────────────────────────────────────┘
         │               │               │
         ▼               ▼               ▼
┌──────────────────────────────────────────────────────────────┐
│                    FILE STORAGE                               │
│  uploads/          output/translations/     output/audio/     │
│  - original.pdf    - doc_en.json           - segment_0.mp3   │
│                    - doc_es.json           - segment_1.mp3   │
└──────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### 1. PDF Upload Flow

```
User selects PDF
     │
     ▼
Frontend sends file via FormData
     │
     ▼
Backend /api/upload endpoint
     │
     ├─→ Validate file (type, size)
     ├─→ Generate unique filename
     ├─→ Save to uploads/
     │
     ▼
PDFProcessor.extract_text()
     │
     ├─→ Try pdfplumber first
     ├─→ Fallback to PyPDF2 if fails
     │
     ▼
Extract metadata & text by page
     │
     ▼
Save to output/translations/doc_extracted.json
     │
     ▼
Return document_id + metadata to frontend
     │
     ▼
Frontend displays document info
```

### 2. Translation Flow

```
User selects target language
     │
     ▼
Frontend sends translate request
     │
     ▼
Backend /api/translate/document
     │
     ├─→ Load extracted text
     ├─→ Split into chunks (5000 chars)
     │
     ▼
TranslationService.translate_chunks()
     │
     ├─→ For each chunk:
     │   ├─→ Call googletrans API
     │   └─→ Return translated text
     │
     ▼
Combine translated chunks
     │
     ▼
Save to output/translations/doc_es_translation.json
     │
     ▼
Return translated text to frontend
     │
     ▼
Frontend displays translation preview
```

### 3. Text-to-Speech Flow

```
User requests audio generation
     │
     ▼
Frontend sends TTS request
     │
     ▼
Backend /api/tts/generate-document
     │
     ├─→ Load translation
     ├─→ Create sentence segments
     │
     ▼
For each sentence:
     │
     ├─→ TextToSpeechService.text_to_speech()
     │   │
     │   ├─→ Call gTTS API
     │   └─→ Save MP3 file
     │
     ▼
Create segment metadata
     │
     ├─→ segment_id
     ├─→ text
     ├─→ start_char
     ├─→ end_char
     ├─→ audio_path
     │
     ▼
Save segments.json
     │
     ▼
Return segment info to frontend
     │
     ▼
Frontend creates Audio elements
     │
     └─→ Loads audio URLs
```

### 4. Playback & Highlighting Flow

```
User clicks Play
     │
     ▼
Frontend: state.isPlaying = true
     │
     ▼
playCurrentSegment()
     │
     ├─→ Get audio element for current segment
     ├─→ audio.play()
     ├─→ highlightSegment(index)
     │
     ▼
Text highlighting applied
     │
     ├─→ Remove previous highlights
     ├─→ Add 'active' class to current sentence
     ├─→ Scroll to visible
     │
     ▼
Audio 'ended' event fires
     │
     ▼
playNextSegment()
     │
     ├─→ Increment currentSegmentIndex
     ├─→ playCurrentSegment() (recursive)
     │
     ▼
Continue until all segments played
```

---

## Component Architecture

### Backend Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Flask Application                         │
├─────────────────────────────────────────────────────────────┤
│  app/__init__.py                                             │
│  - create_app()                                              │
│  - Register blueprints                                       │
│  - Configure CORS                                            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    Routes (Blueprints)                       │
├─────────────────────────────────────────────────────────────┤
│  upload.py          translate.py           tts.py            │
│  - upload_file()    - translate_text()     - generate_tts() │
│  - get_document()   - translate_doc()      - get_audio()    │
│                     - detect_language()    - get_segments() │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    Services (Business Logic)                 │
├─────────────────────────────────────────────────────────────┤
│  PDFProcessor              TranslationService               │
│  - extract_text()          - translate_text()               │
│  - split_sentences()       - translate_chunks()             │
│  - split_chunks()          - detect_language()              │
│                                                              │
│  TextToSpeechService                                        │
│  - text_to_speech()                                         │
│  - generate_with_timestamps()                               │
│  - create_sentence_segments()                               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    Utilities                                 │
├─────────────────────────────────────────────────────────────┤
│  helpers.py                                                  │
│  - allowed_file()                                            │
│  - generate_unique_filename()                                │
│  - sanitize_filename()                                       │
└─────────────────────────────────────────────────────────────┘
```

### Frontend Components

```
┌─────────────────────────────────────────────────────────────┐
│                    index.html (Structure)                    │
├─────────────────────────────────────────────────────────────┤
│  - Header                                                    │
│  - Upload Section                                            │
│  - Translation Section                                       │
│  - Audio Player Section                                      │
│  - Text Display                                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    styles.css (Presentation)                 │
├─────────────────────────────────────────────────────────────┤
│  - Gradient theme                                            │
│  - Responsive layout                                         │
│  - Animation styles                                          │
│  - Highlighting effects                                      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    app.js (Behavior)                         │
├─────────────────────────────────────────────────────────────┤
│  State Management                                            │
│  - documentId, segments, currentSegmentIndex                │
│                                                              │
│  Event Handlers                                              │
│  - handleFileSelect(), handleTranslate()                    │
│  - handleGenerateAudio(), handlePlay()                      │
│                                                              │
│  API Communication                                           │
│  - fetch() calls to backend                                 │
│                                                              │
│  Audio Control                                               │
│  - playCurrentSegment(), playNextSegment()                  │
│  - seekToSegment(), updateProgress()                        │
│                                                              │
│  UI Updates                                                  │
│  - highlightSegment(), displayTextWithSegments()            │
└─────────────────────────────────────────────────────────────┘
```

---

## File Structure

```
Personal translator/
│
├── backend/                        # Python Flask API
│   ├── app/
│   │   ├── __init__.py            # App factory
│   │   ├── routes/                # HTTP endpoints
│   │   │   ├── upload.py          # PDF upload & retrieval
│   │   │   ├── translate.py       # Translation endpoints
│   │   │   └── tts.py             # TTS endpoints
│   │   ├── services/              # Core logic
│   │   │   ├── pdf_processor.py   # PDF → Text
│   │   │   ├── translator.py      # Text → Translation
│   │   │   └── text_to_speech.py  # Text → Audio
│   │   └── utils/
│   │       └── helpers.py         # Utilities
│   ├── config.py                  # Configuration
│   ├── requirements.txt           # Dependencies
│   └── run.py                     # Entry point
│
├── frontend/                       # Web UI
│   ├── index.html                 # Main page
│   ├── styles.css                 # Styling
│   └── app.js                     # Interactivity
│
├── documentation/                  # Docs
│   ├── project-plan.md            # Original plan
│   ├── TESTING_GUIDE.md           # Testing
│   ├── IMPLEMENTATION_SUMMARY.md  # Summary
│   └── ARCHITECTURE.md            # This file
│
├── uploads/                        # Uploaded PDFs
├── output/
│   ├── audio/                     # Generated MP3s
│   └── translations/              # Cached JSON
│
├── README.md                       # Main docs
├── QUICKSTART.md                   # Setup guide
├── QUICK_REFERENCE.md              # Cheat sheet
├── .env.example                    # Env template
├── .gitignore                      # Git ignore
├── start_backend.bat               # Quick start
└── start_frontend.bat              # Quick start
```

---

## API Architecture

### RESTful Endpoints

```
Base URL: http://localhost:5000/api

┌─────────────────┬──────┬────────────────────────────────┐
│ Endpoint        │ Verb │ Purpose                        │
├─────────────────┼──────┼────────────────────────────────┤
│ /health         │ GET  │ Server health check            │
├─────────────────┼──────┼────────────────────────────────┤
│ /upload         │ POST │ Upload PDF file                │
│ /document/:id   │ GET  │ Get extracted text             │
├─────────────────┼──────┼────────────────────────────────┤
│ /translate      │ POST │ Translate text snippet         │
│ /translate/doc  │ POST │ Translate full document        │
│ /detect-lang    │ POST │ Detect language                │
│ /supported-langs│ GET  │ List supported languages       │
├─────────────────┼──────┼────────────────────────────────┤
│ /tts/generate   │ POST │ Generate TTS audio             │
│ /tts/generate-doc│POST │ Generate with segments         │
│ /tts/audio/:file│ GET  │ Serve audio file               │
│ /tts/segments/:id│GET  │ Get segment metadata           │
└─────────────────┴──────┴────────────────────────────────┘
```

### Request/Response Format

**Upload PDF**
```
Request:
  POST /api/upload
  Content-Type: multipart/form-data
  Body: { file: <binary> }

Response:
  {
    "success": true,
    "document_id": "doc_20251110_123456_abc123",
    "filename": "document.pdf",
    "total_pages": 5,
    "total_chars": 2500,
    "full_text": "...",
    "pages": [...]
  }
```

**Translate Document**
```
Request:
  POST /api/translate/document
  Content-Type: application/json
  Body: {
    "document_id": "doc_123",
    "target_lang": "es",
    "source_lang": "auto"
  }

Response:
  {
    "success": true,
    "translation": {
      "full_text": "...",
      "pages": [...],
      "source_lang": "en",
      "target_lang": "es"
    }
  }
```

**Generate Audio**
```
Request:
  POST /api/tts/generate-document
  Content-Type: application/json
  Body: {
    "document_id": "doc_123",
    "language": "es",
    "segment_type": "sentence"
  }

Response:
  {
    "success": true,
    "document_id": "doc_123",
    "total_segments": 25,
    "segments": [
      {
        "segment_id": 0,
        "text": "Hola mundo.",
        "start_char": 0,
        "end_char": 11,
        "audio_path": "output/audio/doc_123/segment_0.mp3"
      },
      ...
    ]
  }
```

---

## State Management

### Backend State
- **Stateless**: No session management
- **File-based**: All state in filesystem
- **Caching**: Translations & audio cached

### Frontend State
```javascript
state = {
    // Document tracking
    documentId: null,              // UUID of current doc
    translatedText: null,          // Full translated text

    // Audio tracking
    segments: [],                  // Array of segment objects
    audioElements: [],             // Audio() objects
    currentSegmentIndex: 0,        // Current playback position

    // Playback state
    isPlaying: false,              // Boolean flag
    targetLanguage: 'es'           // Selected language code
}
```

---

## Technology Choices

### Why Flask?
- ✅ Lightweight & fast
- ✅ Easy to understand
- ✅ Great for APIs
- ✅ Good Python integration

### Why Vanilla JS?
- ✅ No build step
- ✅ Fast development
- ✅ Easy debugging
- ✅ Works everywhere
- ⚠️ Can be upgraded to React/Vue later

### Why googletrans?
- ✅ Free (no API key)
- ✅ Good quality
- ✅ Easy to use
- ⚠️ Rate limited
- 💡 Can upgrade to DeepL/Google Cloud

### Why gTTS?
- ✅ Free (no API key)
- ✅ Natural voices
- ✅ Many languages
- ⚠️ Basic features only
- 💡 Can upgrade to ElevenLabs/Google Cloud

---

## Scaling Considerations

### Current Limitations
- Single-threaded (no async)
- File-based storage (no database)
- Synchronous API calls
- No caching layer
- No load balancing

### Scaling Path

**Phase 1: Optimize Current**
- Add Redis for caching
- Implement Celery for background jobs
- Add request queuing
- Enable gzip compression

**Phase 2: Database**
- PostgreSQL for documents
- User authentication
- Document library
- Usage tracking

**Phase 3: Cloud**
- Docker containerization
- AWS/GCP deployment
- S3/Cloud Storage for files
- CloudFront CDN for audio
- Horizontal scaling with load balancer

**Phase 4: Microservices**
- Separate PDF service
- Separate translation service
- Separate TTS service
- Message queue (RabbitMQ/Kafka)
- Service mesh

---

## Security Architecture

### Current Security Measures

```
┌─────────────────────────────────────────────────────────────┐
│                    Security Layers                           │
├─────────────────────────────────────────────────────────────┤
│  Input Validation                                            │
│  - File type checking (.pdf only)                            │
│  - File size limits (16MB)                                   │
│  - Filename sanitization                                     │
│                                                              │
│  File Security                                               │
│  - Unique filename generation (UUID)                         │
│  - Secure directory paths                                    │
│  - No directory traversal                                    │
│                                                              │
│  CORS Protection                                             │
│  - Whitelist origins                                         │
│  - localhost only (development)                              │
│                                                              │
│  Error Handling                                              │
│  - No sensitive info in errors                               │
│  - Proper HTTP status codes                                  │
│  - Graceful failures                                         │
└─────────────────────────────────────────────────────────────┘
```

### Production Security Additions
- HTTPS/SSL certificates
- API rate limiting
- User authentication (JWT)
- File virus scanning
- SQL injection prevention (when DB added)
- XSS protection
- CSRF tokens
- Content Security Policy headers

---

## Performance Characteristics

### Time Complexity
- PDF extraction: O(n) where n = pages
- Translation: O(n) where n = characters
- TTS generation: O(n) where n = sentences
- Audio playback: O(1) per segment

### Space Complexity
- PDF storage: ~1-10 MB per document
- Extracted text: ~100 KB per document
- Translation cache: ~100 KB per translation
- Audio files: ~10-50 KB per sentence

### Bottlenecks
1. **TTS Generation**: Slowest operation (20-40 seconds)
2. **Translation API**: Network latency
3. **PDF Extraction**: CPU-bound for large PDFs
4. **Audio Loading**: Network bandwidth

---

## Error Handling

### Error Flow

```
User Action
    │
    ▼
Frontend Error Check
    │
    ├─→ Validation Error
    │   └─→ Show user-friendly message
    │
    ▼
API Call
    │
    ├─→ Network Error
    │   └─→ Show connection error
    │
    ▼
Backend Processing
    │
    ├─→ Service Error (PDF/Translation/TTS)
    │   └─→ Try fallback method
    │   └─→ Return error response
    │
    ▼
Frontend Error Handler
    │
    └─→ Display error with details
    └─→ Suggest retry/solution
```

---

## Monitoring & Logging

### Current Logging
- Flask console output
- HTTP status codes
- Exception tracebacks
- Browser console errors

### Production Monitoring
- Application logs (Winston/Log4j)
- Error tracking (Sentry)
- Performance monitoring (New Relic)
- Uptime monitoring (Pingdom)
- User analytics (Google Analytics)

---

## Deployment Architecture

### Development (Current)
```
Localhost:5000 (Backend)
Localhost:3000 (Frontend)
Local filesystem (Storage)
```

### Production (Future)
```
Domain: app.languagelearning.com
Backend: AWS EC2 / Heroku / DigitalOcean
Frontend: Vercel / Netlify / S3 + CloudFront
Database: AWS RDS PostgreSQL
Storage: AWS S3
CDN: CloudFront
```

---

This architecture provides a solid foundation for a language learning platform with clear separation of concerns, scalable design, and room for future enhancements.

# Quick Reference Card

## 🚀 Getting Started (3 Commands)

```bash
# 1. Install dependencies
cd backend && pip install -r requirements.txt

# 2. Start backend
python run.py

# 3. Start frontend (new terminal)
cd ../frontend && python -m http.server 3000
```

Then open: **http://localhost:3000**

---

## 📁 Project Structure

```
Personal translator/
├── backend/              → Flask API (Python)
├── frontend/             → Web UI (HTML/CSS/JS)
├── documentation/        → Guides & plans
├── uploads/              → PDF storage
└── output/               → Generated files
    ├── audio/            → TTS audio files
    └── translations/     → Cached translations
```

---

## 🔗 API Endpoints

### Upload
- `POST /api/upload` - Upload PDF

### Translation
- `POST /api/translate` - Translate text
- `POST /api/translate/document` - Translate full document

### Text-to-Speech
- `POST /api/tts/generate-document` - Generate audio with segments
- `GET /api/tts/audio/<filename>` - Get audio file

### Utilities
- `GET /api/health` - Check server status
- `GET /api/supported-languages` - List languages

---

## 🌍 Supported Languages

**12 Main Languages** (in dropdown):
- 🇬🇧 English (en)
- 🇪🇸 Spanish (es)
- 🇫🇷 French (fr)
- 🇩🇪 German (de)
- 🇮🇹 Italian (it)
- 🇵🇹 Portuguese (pt)
- 🇷🇺 Russian (ru)
- 🇯🇵 Japanese (ja)
- 🇰🇷 Korean (ko)
- 🇨🇳 Chinese (zh-cn)
- 🇸🇦 Arabic (ar)
- 🇮🇳 Hindi (hi)

**Plus 20+ more available via API!**

---

## 🎯 User Workflow

1. **Upload PDF** → Drag & drop or click
2. **Translate** → Select target language
3. **Generate Audio** → Click button & wait
4. **Play** → Listen with text highlighting

---

## ⚙️ Configuration

### Backend (.env)
```bash
PORT=5000
FLASK_ENV=development
SECRET_KEY=your-secret-key
```

### Frontend (app.js)
```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

---

## 🛠️ Common Commands

### Backend
```bash
# Start server
cd backend && python run.py

# Install dependencies
pip install -r requirements.txt

# Check dependencies
pip list
```

### Frontend
```bash
# Simple server
python -m http.server 3000

# Open in browser
start http://localhost:3000  # Windows
open http://localhost:3000   # Mac
```

### Testing
```bash
# Health check
curl http://localhost:5000/api/health

# Test translation
curl -X POST http://localhost:5000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello", "target_lang": "es"}'
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Backend won't start | Activate venv: `venv\Scripts\activate` |
| Module not found | Install deps: `pip install -r requirements.txt` |
| CORS error | Check ports: Backend=5000, Frontend=3000 |
| Translation fails | Check internet connection |
| Audio won't play | Check `output/audio/` directory exists |
| PDF upload fails | Max size 16MB, must be text-based PDF |

---

## 📊 Performance

| Task | Typical Time |
|------|--------------|
| Upload 5-page PDF | 2-5 sec |
| Translate 2000 chars | 5-10 sec |
| Generate audio (20 sentences) | 20-40 sec |
| Audio playback | Real-time |

---

## 🔑 Key Features

✅ PDF upload & text extraction
✅ 30+ language translation
✅ AI voice generation
✅ Real-time text highlighting
✅ Click-to-seek audio
✅ Speed control (0.5x - 2x)
✅ Responsive design
✅ No API keys needed (free tier)

---

## 📦 Dependencies

### Backend (Python)
```
Flask==3.0.0
flask-cors==4.0.0
pdfplumber==0.11.0
PyPDF2==3.0.1
googletrans==4.0.0rc1
gTTS==2.5.1
```

### Frontend
- Pure HTML5/CSS3/JavaScript
- No build step required!

---

## 🎨 UI Features

- **Beautiful gradient design** (purple/blue)
- **Drag & drop** file upload
- **Progress indicators** for all operations
- **Real-time status** messages
- **Auto-scrolling** text display
- **Sentence highlighting** synchronized with audio
- **Responsive layout** (desktop + mobile)

---

## 🔒 Security

- File type validation (.pdf only)
- File size limits (16MB)
- Secure filename generation
- CORS protection
- Input sanitization
- Error message sanitization

---

## 📚 Documentation

- **README.md** - Full documentation
- **QUICKSTART.md** - 5-minute setup
- **project-plan.md** - Original design
- **TESTING_GUIDE.md** - How to test
- **IMPLEMENTATION_SUMMARY.md** - What was built

---

## 🎓 Architecture

```
User Browser (Frontend)
    ↓ HTTP/AJAX
Flask Server (Backend)
    ↓
PDF Processing → Translation → TTS
    ↓              ↓             ↓
File Storage   Google API    gTTS API
```

---

## 💡 Tips & Tricks

1. **Large PDFs**: May take 1-2 minutes for audio generation
2. **Speed Control**: Slow down (0.5x) for learning
3. **Click Sentences**: Jump to any part of the document
4. **Auto-detect**: Leave source language as "Auto"
5. **Test First**: Try with a simple 1-page PDF first

---

## 🔄 Typical API Flow

```
1. POST /api/upload (PDF file)
   → Returns: document_id

2. POST /api/translate/document
   → Body: {document_id, target_lang}
   → Returns: translated text

3. POST /api/tts/generate-document
   → Body: {document_id, language}
   → Returns: audio segments

4. GET /api/tts/audio/{doc_id}/segment_X.mp3
   → Returns: MP3 audio file
```

---

## 📝 State Management (Frontend)

```javascript
state = {
    documentId: null,           // Current document
    translatedText: null,       // Translated content
    segments: [],               // Audio segments
    currentSegmentIndex: 0,     // Playback position
    audioElements: [],          // Audio objects
    isPlaying: false,           // Playback state
    targetLanguage: 'es'        // Selected language
}
```

---

## 🎬 Demo Script

```
1. Start: "Let me show you how this works"
2. Upload: Drag a PDF file
3. Wait: "Extracting text..."
4. Translate: Select Spanish, click Translate
5. Wait: "Translating document..."
6. Audio: Click Generate Audio
7. Wait: "Creating speech segments..."
8. Play: Press play button
9. Watch: Text highlights as it reads!
10. Interact: Click any sentence to jump
```

---

## 🚀 Windows Quick Start Scripts

### Option 1: Startup Scripts
```bash
# Double-click these files:
start_backend.bat
start_frontend.bat
```

### Option 2: Manual Commands
```bash
# Terminal 1
cd backend
venv\Scripts\activate
python run.py

# Terminal 2
cd frontend
python -m http.server 3000
```

---

## 📞 Getting Help

1. Check browser console (F12)
2. Check backend terminal logs
3. Review QUICKSTART.md
4. Read TESTING_GUIDE.md
5. Check README.md FAQ section

---

## ✨ Cool Features to Try

1. **Multi-language support** - Try translating to Japanese!
2. **Speed control** - Listen at 1.5x speed
3. **Click-to-seek** - Click any sentence
4. **Smooth highlighting** - Watch the text follow along
5. **Drag & drop** - So easy to use!

---

## 🎯 Use Cases

- 📖 **Language Learning** - Read & listen simultaneously
- 📄 **Document Translation** - Quick PDF translation
- 🎧 **Audiobooks** - Turn PDFs into audiobooks
- 🌍 **Travel Prep** - Learn phrases in target language
- 📚 **Study Aid** - Hear pronunciation of foreign texts

---

**Built with ❤️ using Python & JavaScript**

**Ready to help you learn languages!** 🌟

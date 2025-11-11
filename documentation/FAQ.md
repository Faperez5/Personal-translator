# Frequently Asked Questions (FAQ)

## General Questions

### What is this application?
A language learning platform that lets you upload PDF documents, translate them to another language, and listen to the translation with synchronized text highlighting - helping you learn by reading and listening simultaneously.

### Do I need to pay for API services?
No! The default configuration uses free services:
- **googletrans** for translation (free Google Translate)
- **gTTS** for text-to-speech (free Google TTS)

However, you can optionally upgrade to premium services like DeepL or ElevenLabs for better quality.

### What languages are supported?
30+ languages including:
- English, Spanish, French, German, Italian, Portuguese
- Russian, Japanese, Korean, Chinese (Simplified/Traditional)
- Arabic, Hindi, Dutch, Polish, Turkish, and many more

### Is my data private?
Yes! Everything runs locally on your machine. Your PDFs and translations are stored only on your computer. The only external calls are to the free translation and TTS APIs.

---

## Installation & Setup

### What do I need to install?
- Python 3.8 or higher
- pip (Python package manager)
- A modern web browser

### How do I install it?
```bash
# 1. Install dependencies
cd backend
pip install -r requirements.txt

# 2. Start backend
python run.py

# 3. Start frontend (new terminal)
cd ../frontend
python -m http.server 3000
```

See [QUICKSTART.md](../QUICKSTART.md) for detailed instructions.

### The backend won't start. What should I do?
1. Make sure you're in the `backend` directory
2. Activate the virtual environment: `venv\Scripts\activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Check Python version: `python --version` (must be 3.8+)
5. Look for error messages in the terminal

### I get "ModuleNotFoundError". How do I fix this?
```bash
# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

### Do I need to create a .env file?
It's optional. The app works with default settings. If you want to customize settings:
```bash
copy .env.example .env  # Windows
cp .env.example .env    # Mac/Linux
```

---

## PDF Upload

### What PDF formats are supported?
Any standard PDF with extractable text. The app uses two methods:
1. **pdfplumber** (primary)
2. **PyPDF2** (fallback)

### Why does my PDF upload fail?
Common reasons:
- **File too large**: Max 16MB (configurable in `config.py`)
- **Wrong file type**: Only .pdf files accepted
- **Scanned PDF**: Image-based PDFs need OCR (not yet implemented)
- **Password-protected**: Encrypted PDFs not supported

### Can I upload scanned PDFs?
Not yet. The current version only extracts text from text-based PDFs. OCR support is planned for future releases.

### How do I test if my PDF will work?
Try opening it and selecting text. If you can copy/paste text from the PDF, it should work with this app.

### Where are uploaded files stored?
In the `uploads/` directory in your project folder.

---

## Translation

### Why does translation take so long?
Translation time depends on:
- Document length (more text = more time)
- Internet speed (calls external API)
- API rate limits

Typical times:
- 1 page: 5-10 seconds
- 5 pages: 15-30 seconds
- 10 pages: 30-60 seconds

### Translation failed. What should I check?
1. **Internet connection**: Translation requires internet
2. **Document size**: Try a smaller PDF first
3. **API limits**: googletrans may have rate limits
4. **Language codes**: Verify source/target languages are supported
5. **Backend logs**: Check terminal for error messages

### Can I translate from any language to any language?
Yes! The app supports:
- **Auto-detection**: Automatically detect source language
- **30+ languages**: See supported language list
- **Any pair**: Translate between any supported languages

### How accurate are the translations?
Using googletrans (free Google Translate):
- Generally good for common language pairs
- May struggle with idioms or context
- Better for formal/technical text
- For premium quality, upgrade to DeepL API

### Where are translations saved?
In `output/translations/` as JSON files, named like:
- `document_20251110_123456_extracted.json` (original text)
- `document_20251110_123456_es_translation.json` (Spanish translation)

---

## Text-to-Speech (TTS)

### How long does audio generation take?
Depends on document length:
- 10 sentences: 20-30 seconds
- 25 sentences: 40-60 seconds
- 50+ sentences: 1-2 minutes

Be patient! The app generates a separate audio file for each sentence.

### Why does it generate multiple audio files?
To enable synchronized text highlighting! Each sentence gets its own audio file, allowing:
- Word-by-word highlighting
- Click-to-seek to any sentence
- Smooth playback coordination

### Can I download the audio files?
Yes! Audio files are saved in `output/audio/<document_id>/`:
- `segment_0.mp3`
- `segment_1.mp3`
- `segment_2.mp3`
- etc.

You can copy these files and use them elsewhere.

### The audio sounds robotic. Can I improve it?
The free gTTS has basic quality. For better voices:
1. Upgrade to Google Cloud TTS (premium)
2. Use Azure Speech Services (premium)
3. Use ElevenLabs (highest quality, premium)

Edit `backend/app/services/text_to_speech.py` to add premium service support.

### What audio format is used?
MP3 format by default. This can be changed in `backend/config.py`.

---

## Audio Playback

### The audio won't play. What's wrong?
1. **Check CORS**: Backend must be on port 5000, frontend on 3000
2. **Check audio files**: Look in `output/audio/<document_id>/`
3. **Browser console**: Press F12, look for errors
4. **Audio generation**: Make sure "Generate Audio" completed successfully
5. **File paths**: Verify audio files were created

### Text highlighting is out of sync with audio
This shouldn't happen with proper setup. If it does:
1. Check browser console for JavaScript errors
2. Verify segments.json was created correctly
3. Try restarting the backend server
4. Clear browser cache and reload page

### Can I control playback speed?
Yes! Use the speed dropdown:
- 0.5x (slow - good for learning)
- 0.75x
- 1x (normal)
- 1.25x
- 1.5x
- 2x (fast)

### Can I skip to a specific part?
Yes! Click on any sentence in the text display to jump to that position.

### The progress bar doesn't move
Check that:
1. Audio is actually playing (you hear sound)
2. No JavaScript errors in console
3. Audio duration is being calculated correctly

---

## Frontend Issues

### I see CORS errors in the browser console
CORS errors mean the frontend can't connect to the backend. Fix:
1. Verify backend is running on port 5000
2. Verify frontend is on port 3000 (or update config)
3. Check `backend/config.py` CORS_ORIGINS includes your frontend URL
4. Restart both servers

### The page looks broken
1. Make sure you opened `index.html` through a web server
2. If using `file://` protocol, some features may not work
3. Use Python server: `python -m http.server 3000`
4. Check browser console for CSS/JS loading errors

### Nothing happens when I click buttons
1. Open browser DevTools (F12)
2. Check Console tab for JavaScript errors
3. Verify `app.js` loaded correctly
4. Check Network tab to see if API calls are made

---

## Performance

### The app is slow. How can I speed it up?
1. **Use smaller PDFs**: Start with 1-2 pages
2. **Faster internet**: Improves API calls
3. **Close other apps**: Free up RAM
4. **Upgrade APIs**: Premium services are faster
5. **Add caching**: Results are cached automatically

### How much disk space do I need?
Typical usage per document:
- Original PDF: 1-10 MB
- Extracted text: ~100 KB
- Translation: ~100 KB
- Audio files: ~10-50 KB per sentence

Example: A 5-page PDF with 25 sentences = ~5-15 MB total

### Can I process multiple documents at once?
Not currently. The app is designed for one document at a time. For batch processing, you'd need to:
1. Add queue system (Celery)
2. Add background jobs
3. Modify UI for multiple uploads

---

## Customization

### Can I change the UI colors?
Yes! Edit `frontend/styles.css`:
```css
/* Change gradient colors */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Can I add more languages to the dropdown?
Yes! Edit `frontend/index.html`, add options to the `<select>` elements.

### Can I change the maximum file size?
Yes! Edit `backend/config.py`:
```python
MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32MB
```

### Can I use a different translation service?
Yes! The app supports:
- googletrans (default, free)
- DeepL (premium)
- Google Cloud Translation (premium)

Edit translation service in API calls or modify `backend/app/services/translator.py`.

### Can I add OCR for scanned PDFs?
Yes, but requires additional work:
1. Install Tesseract OCR
2. Install pytesseract Python library
3. Modify `pdf_processor.py` to add OCR support

---

## Errors & Troubleshooting

### "Connection refused" error
Backend isn't running or on wrong port:
```bash
# Check if backend is running
curl http://localhost:5000/api/health

# Should return: {"status": "healthy"}
```

### "File not found" error
Check that required directories exist:
```bash
uploads/
output/audio/
output/translations/
```

### "Translation service unavailable"
1. Check internet connection
2. googletrans may be down or rate-limited
3. Try again in a few minutes
4. Consider upgrading to premium API

### "Audio generation failed"
1. Check `output/audio/` directory exists and is writable
2. Verify translation completed successfully
3. Check backend logs for specific error
4. Try with shorter text first

### "Invalid language code"
Use standard language codes:
- en (English)
- es (Spanish)
- fr (French)
- etc.

Check supported languages: `GET /api/supported-languages`

---

## Development

### How do I contribute?
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### How do I run tests?
Tests are not yet implemented. To add tests:
```bash
pip install pytest
pytest backend/tests/
```

### How do I debug the backend?
1. Check terminal output for errors
2. Add print statements in Python code
3. Use Python debugger (pdb)
4. Enable Flask debug mode (already enabled in development)

### How do I debug the frontend?
1. Open browser DevTools (F12)
2. Check Console tab for errors
3. Check Network tab for API calls
4. Use breakpoints in Sources tab
5. Add console.log() statements

### Can I deploy this to production?
Yes, but you need to:
1. Set `FLASK_ENV=production`
2. Use a production WSGI server (Gunicorn)
3. Set up HTTPS
4. Configure proper CORS origins
5. Add user authentication
6. Set up proper database
7. Use environment variables for secrets

---

## Best Practices

### What's the best workflow?
1. **Start small**: Test with a 1-page PDF first
2. **Check extraction**: Verify text extracted correctly
3. **Translate**: Choose target language and translate
4. **Preview**: Read translation preview
5. **Generate audio**: Click generate and wait
6. **Listen**: Play audio and follow highlighting
7. **Adjust**: Use speed controls as needed

### How should I organize my documents?
The app automatically organizes files:
- Uploads → `uploads/`
- Translations → `output/translations/`
- Audio → `output/audio/<document_id>/`

You can manually organize uploaded PDFs in the uploads folder.

### Should I delete old files?
The app doesn't auto-delete. Manually clean up:
```bash
# Delete old uploads
del uploads\*  # Windows
rm uploads/*   # Linux/Mac

# Delete old translations
del output\translations\*
rm output/translations/*

# Delete old audio
del output\audio\*
rm -rf output/audio/*
```

---

## Future Features

### What's coming next?
Planned features:
- [ ] User authentication & accounts
- [ ] Document library
- [ ] OCR for scanned PDFs
- [ ] Background processing
- [ ] Progress indicators
- [ ] Vocabulary extraction
- [ ] Flashcard generation
- [ ] Mobile app

### Can I request a feature?
Yes! Open an issue on GitHub with:
- Feature description
- Use case
- Why it's useful

### How can I help?
- Test the app and report bugs
- Suggest improvements
- Contribute code
- Write documentation
- Share with others

---

## Comparison with Other Tools

### vs Google Translate website
**Advantages:**
- Read and listen simultaneously
- Synchronized highlighting
- PDF support
- Offline storage
- Customizable

**Disadvantages:**
- Requires setup
- Local installation

### vs Duolingo/Babbel
**Advantages:**
- Use your own content
- No subscription
- Any language pair
- Full document translation

**Disadvantages:**
- No structured lessons
- No gamification
- No progress tracking (yet)

### vs Professional translation services
**Advantages:**
- Free
- Instant
- Good for learning
- TTS included

**Disadvantages:**
- Lower quality
- No human review
- Better for learning than professional use

---

## Support

### Where can I get help?
1. Read [QUICKSTART.md](../QUICKSTART.md)
2. Check this FAQ
3. Review [TESTING_GUIDE.md](TESTING_GUIDE.md)
4. Check backend terminal for errors
5. Check browser console for errors
6. Open an issue on GitHub

### How do I report a bug?
Include:
1. Steps to reproduce
2. Expected behavior
3. Actual behavior
4. Error messages
5. Screenshots
6. System info (OS, Python version, browser)

### Is there a community?
Not yet! This is a new project. Help build the community:
- Share the project
- Contribute code
- Help others with issues
- Write tutorials

---

**Still have questions?** Open an issue on GitHub or check the documentation files!

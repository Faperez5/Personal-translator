# Testing Guide

This guide will help you test all features of the Language Learning Platform.

## Prerequisites

Before testing, ensure:
1. Backend server is running on `http://localhost:5000`
2. Frontend is accessible on `http://localhost:3000` or via file
3. You have a sample PDF file to test with

## Manual Testing Checklist

### 1. Backend API Testing

#### Health Check
```bash
curl http://localhost:5000/api/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "message": "Language Learning API is running"
}
```

#### Test Translation (Simple Text)
```bash
curl -X POST http://localhost:5000/api/translate \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Hello, how are you?\", \"target_lang\": \"es\", \"source_lang\": \"en\"}"
```

**Expected Response:**
```json
{
  "success": true,
  "translation": {
    "translated_text": "Hola, ¿cómo estás?",
    "source_lang": "en",
    "target_lang": "es",
    "service": "google"
  }
}
```

#### Test Language Detection
```bash
curl -X POST http://localhost:5000/api/detect-language \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Bonjour, comment allez-vous?\"}"
```

**Expected Response:**
```json
{
  "success": true,
  "detection": {
    "language": "fr",
    "confidence": 0.99
  }
}
```

#### Test TTS Generation
```bash
curl -X POST http://localhost:5000/api/tts/generate \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"This is a test\", \"language\": \"en\"}"
```

**Expected Response:**
```json
{
  "success": true,
  "audio": {
    "audio_path": "path/to/audio.mp3",
    "language": "en",
    "service": "gtts"
  }
}
```

### 2. Frontend Testing

#### Step 1: PDF Upload
1. Open the frontend in your browser
2. Click "Choose File" or drag and drop a PDF
3. Wait for extraction to complete

**Expected Results:**
- Upload status shows "success" message
- Document information appears with:
  - Filename
  - Number of pages
  - Character count
- "Translate" button becomes enabled

**Common Issues:**
- PDF fails to upload → Check file size (max 16MB)
- Text extraction fails → PDF might be scanned/image-based
- Upload gets stuck → Check backend terminal for errors

#### Step 2: Translation
1. Select source language (or leave as "Auto Detect")
2. Select target language (e.g., Spanish)
3. Click "Translate"
4. Wait for translation to complete

**Expected Results:**
- Translation status shows "loading" then "success"
- Preview of translated text appears
- "Generate Audio" button becomes enabled

**Common Issues:**
- Translation fails → Check internet connection
- Timeout error → Try smaller PDF or chunk size
- Wrong translation → Verify language codes

#### Step 3: Audio Generation
1. Click "Generate Audio"
2. Wait for TTS processing (may take 30s-2min for large documents)

**Expected Results:**
- Audio status shows progress
- Success message with segment count
- Audio player appears
- Text display shows segmented sentences

**Common Issues:**
- Generation fails → Check audio output directory permissions
- Audio cuts off → Check segment generation in backend logs
- No segments created → Verify translated text exists

#### Step 4: Playback & Highlighting
1. Click the play button
2. Observe text highlighting as audio plays
3. Test clicking on sentences to jump
4. Test speed controls (0.5x to 2x)
5. Test pause/resume

**Expected Results:**
- Audio plays smoothly
- Current sentence highlights in color
- Text auto-scrolls to follow playback
- Clicking sentences jumps to that position
- Speed changes take effect immediately

**Common Issues:**
- No highlighting → Check segment data in browser console
- Audio won't play → Check CORS settings
- Segments out of sync → Check audio generation logs

### 3. Integration Testing

#### Full Workflow Test

1. **Upload**: Upload a 1-2 page PDF
2. **Translate**: Translate from English to Spanish
3. **Generate**: Create audio with segments
4. **Play**: Play through entire document
5. **Navigate**: Click on middle sentence
6. **Speed**: Change speed to 1.5x
7. **Pause/Resume**: Test pause and resume

**Success Criteria:**
- All steps complete without errors
- Audio-text synchronization is accurate
- UI responds smoothly to all interactions
- No console errors in browser

### 4. Cross-Language Testing

Test with different language pairs:

| Source | Target | Notes |
|--------|--------|-------|
| English | Spanish | Most common, should work well |
| English | French | Test special characters (é, à, etc.) |
| English | Japanese | Test non-Latin scripts |
| Spanish | English | Test reverse translation |
| Auto | Spanish | Test language detection |

### 5. Edge Cases

#### Large Documents
- Test with 10+ page PDFs
- Check memory usage
- Verify all pages translate
- Ensure audio generation completes

#### Special Characters
- Test PDFs with:
  - Accented characters (é, ñ, ü)
  - Non-Latin scripts (中文, العربية, हिंदी)
  - Emoji and symbols
  - Mathematical notation

#### Network Issues
- Test with slow connection
- Test with intermittent connection
- Verify error handling and retry logic

#### Browser Compatibility
Test on:
- Chrome/Edge
- Firefox
- Safari (if on Mac)
- Mobile browsers (responsive design)

### 6. Performance Testing

#### Metrics to Track

1. **Upload & Extraction**
   - 1-page PDF: < 2 seconds
   - 10-page PDF: < 10 seconds

2. **Translation**
   - 1000 characters: < 5 seconds
   - 5000 characters: < 15 seconds

3. **Audio Generation**
   - 10 sentences: < 30 seconds
   - 50 sentences: < 2 minutes

4. **Playback**
   - Audio loads: < 1 second per segment
   - Highlighting: No visible lag

### 7. Error Handling Testing

#### Test Scenarios

1. **Invalid PDF**
   - Upload a non-PDF file
   - Expected: Error message displayed

2. **Corrupted PDF**
   - Upload damaged PDF
   - Expected: Graceful error, fallback to PyPDF2

3. **Network Failure**
   - Disconnect internet during translation
   - Expected: Error message with retry option

4. **Server Restart**
   - Restart backend during operation
   - Expected: Appropriate error message

### 8. Security Testing

1. **File Upload**
   - Try uploading files > 16MB
   - Try uploading executable files
   - Try uploading files with special characters in names

2. **API Injection**
   - Test SQL injection in text fields
   - Test XSS in translation text
   - Test path traversal in document IDs

### 9. Automated Testing (Future)

Create test scripts for:
```python
# backend/tests/test_api.py
def test_health_check():
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_upload_pdf():
    # Test PDF upload
    pass

def test_translate_text():
    # Test translation
    pass
```

## Test Results Template

```
Date: ________
Tester: ________

Backend Tests:
[ ] Health check - PASS/FAIL
[ ] Translation API - PASS/FAIL
[ ] TTS API - PASS/FAIL
[ ] Language detection - PASS/FAIL

Frontend Tests:
[ ] PDF upload - PASS/FAIL
[ ] Translation UI - PASS/FAIL
[ ] Audio generation - PASS/FAIL
[ ] Playback & highlighting - PASS/FAIL

Integration Tests:
[ ] Full workflow - PASS/FAIL
[ ] Cross-language - PASS/FAIL

Performance:
[ ] Response times acceptable - PASS/FAIL
[ ] Large files handled - PASS/FAIL

Issues Found:
1.
2.
3.

Notes:
```

## Debugging Tips

### Check Backend Logs
```bash
# In backend terminal, look for:
- 200 responses (success)
- 400/500 errors (failures)
- Exception tracebacks
```

### Check Browser Console
```javascript
// Open DevTools (F12), look for:
- Network errors (failed requests)
- JavaScript errors
- CORS issues
```

### Common Debug Commands
```bash
# Check if backend is running
curl http://localhost:5000/api/health

# List uploaded files
ls uploads/

# List generated audio
ls output/audio/

# Check backend process
tasklist | findstr python  # Windows
ps aux | grep python       # Linux/Mac
```

## Reporting Issues

When reporting bugs, include:
1. Steps to reproduce
2. Expected behavior
3. Actual behavior
4. Browser and OS version
5. Backend logs (if applicable)
6. Screenshots (if UI issue)

## Next Steps

After testing:
1. Document any bugs found
2. Create GitHub issues for problems
3. Suggest improvements
4. Add automated tests for critical paths

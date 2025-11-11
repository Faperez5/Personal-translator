# Quick Start Guide

Get your Language Learning Platform up and running in 5 minutes!

## Step 1: Install Python Dependencies

1. Open a terminal/command prompt in the project directory
2. Create and activate a virtual environment:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install backend dependencies:

```bash
cd backend
pip install -r requirements.txt
```

## Step 2: Configure Environment

1. Copy the example environment file:

```bash
# From project root
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux
```

2. The default configuration works out of the box! No API keys needed for basic functionality.

## Step 3: Start the Backend Server

```bash
# Make sure you're in the backend directory
cd backend

# Run the Flask server
python run.py
```

You should see:
```
* Running on http://127.0.0.1:5000
```

## Step 4: Open the Frontend

1. Open a new terminal/command prompt
2. Navigate to the frontend directory:

```bash
cd frontend
```

3. Open `index.html` in your web browser:

**Option A: Simple HTTP Server (Recommended)**
```bash
# Python 3
python -m http.server 3000

# Then open: http://localhost:3000
```

**Option B: Direct File**
- Just double-click `index.html` or open it in your browser
- Note: Some features may require a local server

## Step 5: Use the Application

1. **Upload a PDF**: Drag and drop or click to select a PDF file
2. **Translate**: Choose your target language and click "Translate"
3. **Listen**: Click "Generate Audio" to create speech with text highlighting
4. **Play**: Press the play button and watch the text highlight as it reads!

## Troubleshooting

### Backend won't start
- Make sure you activated the virtual environment
- Check that all dependencies installed correctly: `pip list`
- Verify you're in the `backend` directory

### "Module not found" errors
```bash
pip install -r requirements.txt --force-reinstall
```

### CORS errors in browser
- Make sure both backend (port 5000) and frontend (port 3000) are running
- Check that `CORS_ORIGINS` in `backend/config.py` includes your frontend URL

### Translation fails
- Check your internet connection (googletrans requires internet)
- Try a smaller PDF file first
- Check backend terminal for error messages

### Audio won't play
- Verify the translation completed successfully
- Check that the `output/audio` directory exists and is writable
- Look for errors in the browser console (F12)

### PDF upload fails
- Ensure the PDF is not password-protected
- Try a simpler PDF file
- Check file size (max 16MB by default)

## Testing the API

You can test individual API endpoints using curl or Postman:

```bash
# Health check
curl http://localhost:5000/api/health

# Upload a PDF
curl -X POST -F "file=@path/to/your/document.pdf" http://localhost:5000/api/upload

# Translate text
curl -X POST http://localhost:5000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "target_lang": "es"}'
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [documentation/project-plan.md](documentation/project-plan.md) for architecture details
- Explore the code in `backend/app/` to customize functionality
- Modify `frontend/styles.css` to change the appearance

## Need Help?

- Check the backend terminal for server logs
- Open browser DevTools (F12) to see frontend errors
- Review the API documentation in [README.md](README.md)

Enjoy learning languages!

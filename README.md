# Language Learning Platform

A web-based language learning platform that allows users to upload PDF files, translate them into their desired language, and listen to the translated text with synchronized text highlighting.

## Features

- **PDF Upload & Text Extraction**: Upload PDF files and automatically extract text content
- **Multi-Language Translation**: Translate documents to various languages using Google Translate or DeepL
- **Text-to-Speech**: Convert translated text to natural-sounding speech
- **Synchronized Highlighting**: Real-time text highlighting that follows the audio playback
- **Sentence Segmentation**: Break down documents into sentences for better control and highlighting

## Technology Stack

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **pdfplumber & PyPDF2** - PDF text extraction
- **googletrans** - Free translation (Google Translate)
- **gTTS** - Free text-to-speech (Google TTS)
- **deepl** - Premium translation (optional)

### Frontend
- **HTML/CSS/JavaScript** or **React** (in progress)
- **Bootstrap/Tailwind CSS** - UI styling
- **HTML5 Audio API** - Audio playback

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Backend Setup

1. Clone the repository:
```bash
cd "c:\Users\faper\OneDrive\Escritorio\Insanity\projects\Personal translator"
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

5. Create a `.env` file from the example:
```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

6. Run the Flask application:
```bash
python run.py
```

The backend server will start at `http://localhost:5000`

## API Endpoints

### Upload Endpoints
- `POST /api/upload` - Upload and extract text from PDF
- `GET /api/document/<document_id>` - Get extracted document text

### Translation Endpoints
- `POST /api/translate` - Translate text
- `POST /api/translate/document` - Translate entire document
- `POST /api/detect-language` - Detect language of text
- `GET /api/supported-languages` - Get list of supported languages

### Text-to-Speech Endpoints
- `POST /api/tts/generate` - Generate TTS for text
- `POST /api/tts/generate-document` - Generate TTS for document with segments
- `GET /api/tts/audio/<filename>` - Retrieve audio file
- `GET /api/tts/segments/<document_id>` - Get segment information
- `GET /api/tts/supported-languages` - Get TTS supported languages

### Health Check
- `GET /api/health` - Check API status

## Usage Example

### 1. Upload a PDF
```bash
curl -X POST -F "file=@document.pdf" http://localhost:5000/api/upload
```

### 2. Translate the Document
```bash
curl -X POST http://localhost:5000/api/translate/document \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "your_document_id",
    "target_lang": "es",
    "source_lang": "auto"
  }'
```

### 3. Generate TTS with Segments
```bash
curl -X POST http://localhost:5000/api/tts/generate-document \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "your_document_id",
    "language": "es",
    "segment_type": "sentence"
  }'
```

### 4. Play Audio
Access the audio file at: `http://localhost:5000/api/tts/audio/<document_id>/segment_0.mp3`

## Supported Languages

The platform supports 30+ languages including:
- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- Russian (ru)
- Japanese (ja)
- Korean (ko)
- Chinese (zh-cn, zh-tw)
- Arabic (ar)
- Hindi (hi)
- And many more...

## Project Structure

```
language-learning-platform/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── upload.py
│   │   │   ├── translate.py
│   │   │   └── tts.py
│   │   ├── services/
│   │   │   ├── pdf_processor.py
│   │   │   ├── translator.py
│   │   │   └── text_to_speech.py
│   │   └── utils/
│   │       └── helpers.py
│   ├── config.py
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   └── (in progress)
├── uploads/
├── output/
│   ├── audio/
│   └── translations/
├── documentation/
│   └── project-plan.md
├── .env.example
├── .gitignore
└── README.md
```

## Configuration

Edit the `.env` file to configure:
- API keys for premium services (optional)
- Server port
- Secret key for Flask

## Free Tier vs Premium

### Free Tier (Default)
- **Translation**: googletrans (free Google Translate API)
- **TTS**: gTTS (free Google Text-to-Speech)
- No API keys required
- Suitable for personal use and testing

### Premium Tier (Optional)
- **Translation**: DeepL API, Google Cloud Translation
- **TTS**: Google Cloud TTS, Azure Speech, ElevenLabs
- Requires API keys and billing
- Better quality and more features

## Development

### Running Tests
```bash
# Coming soon
pytest
```

### Code Style
```bash
# Format code
black backend/

# Lint code
flake8 backend/
```

## Roadmap

- [x] PDF upload and text extraction
- [x] Translation service integration
- [x] Text-to-speech generation
- [x] Sentence segmentation
- [ ] Frontend UI with React
- [ ] Real-time audio-text synchronization
- [ ] User accounts and saved documents
- [ ] Progress tracking
- [ ] Vocabulary extraction
- [ ] Mobile app

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Troubleshooting

### Issue: PDF text extraction fails
**Solution**: Some PDFs may be scanned images. Consider adding OCR support with Tesseract.

### Issue: Translation API errors
**Solution**: Check your internet connection. For premium services, verify API keys.

### Issue: Audio generation is slow
**Solution**: This is normal for long documents. Consider using smaller chunks or background processing.

## Support

For issues and questions, please open an issue on the GitHub repository.

## Acknowledgments

- Flask - Web framework
- pdfplumber - PDF text extraction
- googletrans - Translation
- gTTS - Text-to-speech

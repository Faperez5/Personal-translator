from flask import Blueprint, request, jsonify, current_app
import os
import json
from app.services.translator import TranslationService
from app.services.pdf_processor import PDFProcessor

translate_bp = Blueprint('translate', __name__)

@translate_bp.route('/translate', methods=['POST'])
def translate_text():
    """
    Translate text to target language

    Request body:
        {
            "text": "Text to translate",
            "target_lang": "es",
            "source_lang": "auto",
            "service": "google"
        }

    Returns:
        JSON response with translation result
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        text = data.get('text', '')
        target_lang = data.get('target_lang', 'en')
        source_lang = data.get('source_lang', 'auto')
        service = data.get('service', 'google')

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        # Initialize translator
        translator = TranslationService(service=service)

        # Translate text
        result = translator.translate_text(text, target_lang, source_lang)

        return jsonify({
            'success': True,
            'translation': result
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Translation failed',
            'details': str(e)
        }), 500

@translate_bp.route('/translate/document', methods=['POST'])
def translate_document():
    """
    Translate an entire document

    Request body:
        {
            "document_id": "unique_doc_id",
            "target_lang": "es",
            "source_lang": "auto",
            "service": "google"
        }

    Returns:
        JSON response with translated document
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        document_id = data.get('document_id')
        target_lang = data.get('target_lang', 'en')
        source_lang = data.get('source_lang', 'auto')
        service = data.get('service', 'google')

        if not document_id:
            return jsonify({'error': 'No document_id provided'}), 400

        # Load extracted text
        text_file_path = os.path.join(
            current_app.config['TRANSLATION_OUTPUT_FOLDER'],
            f"{document_id}_extracted.json"
        )

        if not os.path.exists(text_file_path):
            return jsonify({'error': 'Document not found'}), 404

        with open(text_file_path, 'r', encoding='utf-8') as f:
            text_data = json.load(f)

        # Initialize translator
        translator = TranslationService(service=service)
        pdf_processor = PDFProcessor()

        # Split text into chunks for better handling
        chunks = pdf_processor.split_into_chunks(
            text_data['full_text'],
            max_chars=5000
        )

        # Translate chunks
        translated_chunks = translator.translate_chunks(chunks, target_lang, source_lang)

        # Combine translated chunks
        translated_text = ' '.join([
            chunk['translated_text']
            for chunk in translated_chunks
            if 'translated_text' in chunk
        ])

        # Also translate page by page for better structure
        translated_pages = []
        for page in text_data['pages']:
            page_translation = translator.translate_text(
                page['text'],
                target_lang,
                source_lang
            )
            translated_pages.append({
                'page_number': page['page_number'],
                'original_text': page['text'],
                'translated_text': page_translation['translated_text'],
                'char_count': len(page_translation['translated_text'])
            })

        # Prepare response with both original and translated text
        translation_result = {
            'document_id': document_id,
            'source_lang': translated_chunks[0]['source_lang'] if translated_chunks else source_lang,
            'target_lang': target_lang,
            'service': service,
            'original_text': text_data['full_text'],  # Include original text
            'translated_text': translated_text,
            'full_text': translated_text,  # Keep for backward compatibility
            'pages': translated_pages,
            'total_pages': len(translated_pages),
            'total_chars': len(translated_text),
            'original_pages': text_data['pages']  # Include original pages
        }

        # Save translation result
        translation_file_path = os.path.join(
            current_app.config['TRANSLATION_OUTPUT_FOLDER'],
            f"{document_id}_{target_lang}_translation.json"
        )

        with open(translation_file_path, 'w', encoding='utf-8') as f:
            json.dump(translation_result, f, ensure_ascii=False, indent=2)

        return jsonify({
            'success': True,
            'translation': translation_result
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Document translation failed',
            'details': str(e)
        }), 500

@translate_bp.route('/detect-language', methods=['POST'])
def detect_language():
    """
    Detect the language of input text

    Request body:
        {
            "text": "Text to detect language for"
        }

    Returns:
        JSON response with detected language
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        text = data.get('text', '')

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        # Initialize translator (using Google for language detection)
        translator = TranslationService(service='google')

        # Detect language
        result = translator.detect_language(text)

        return jsonify({
            'success': True,
            'detection': result
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Language detection failed',
            'details': str(e)
        }), 500

@translate_bp.route('/supported-languages', methods=['GET'])
def get_supported_languages():
    """
    Get list of supported languages

    Query params:
        service: Translation service (default: 'google')

    Returns:
        JSON response with supported languages
    """
    try:
        service = request.args.get('service', 'google')

        translator = TranslationService(service=service)
        languages = translator.get_supported_languages()

        return jsonify({
            'success': True,
            'service': service,
            'languages': languages
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to get supported languages',
            'details': str(e)
        }), 500

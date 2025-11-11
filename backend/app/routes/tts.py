from flask import Blueprint, request, jsonify, current_app, send_file
import os
import json
from app.services.text_to_speech import TextToSpeechService

tts_bp = Blueprint('tts', __name__)

@tts_bp.route('/tts/generate', methods=['POST'])
def generate_tts():
    """
    Generate text-to-speech audio for given text

    Request body:
        {
            "text": "Text to convert to speech",
            "language": "en",
            "service": "gtts",
            "slow": false
        }

    Returns:
        JSON response with audio file path
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        text = data.get('text', '')
        language = data.get('language', 'en')
        service = data.get('service', 'gtts')
        slow = data.get('slow', False)

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        # Initialize TTS service
        tts_service = TextToSpeechService(service=service)

        # Generate unique filename
        from app.utils.helpers import generate_unique_filename
        output_filename = generate_unique_filename(f"tts_{language}.mp3")
        output_path = os.path.join(current_app.config['AUDIO_OUTPUT_FOLDER'], output_filename)

        # Generate audio
        audio_info = tts_service.text_to_speech(text, language, output_path, slow)

        # Estimate duration
        estimated_duration = tts_service.estimate_duration(text)
        audio_info['estimated_duration'] = estimated_duration

        return jsonify({
            'success': True,
            'audio': audio_info,
            'audio_filename': output_filename
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'TTS generation failed',
            'details': str(e)
        }), 500

@tts_bp.route('/tts/generate-document', methods=['POST'])
def generate_document_tts():
    """
    Generate text-to-speech for an entire translated document with sentence segments

    Request body:
        {
            "document_id": "unique_doc_id",
            "language": "es",
            "service": "gtts",
            "segment_type": "sentence"
        }

    Returns:
        JSON response with audio files and segment information
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        document_id = data.get('document_id')
        language = data.get('language', 'en')
        service = data.get('service', 'gtts')
        segment_type = data.get('segment_type', 'sentence')  # 'sentence' or 'full'

        if not document_id:
            return jsonify({'error': 'No document_id provided'}), 400

        # Load translation file
        translation_file_path = os.path.join(
            current_app.config['TRANSLATION_OUTPUT_FOLDER'],
            f"{document_id}_{language}_translation.json"
        )

        if not os.path.exists(translation_file_path):
            return jsonify({'error': 'Translation not found. Please translate the document first.'}), 404

        with open(translation_file_path, 'r', encoding='utf-8') as f:
            translation_data = json.load(f)

        # Initialize TTS service
        tts_service = TextToSpeechService(service=service)

        if segment_type == 'sentence':
            # Generate sentence segments for synchronized highlighting
            translated_text = translation_data.get('translated_text', translation_data.get('full_text', ''))
            original_text = translation_data.get('original_text', '')

            # Create segments for both original and translated text
            translated_segments = tts_service.create_sentence_segments(translated_text)
            original_segments = tts_service.create_sentence_segments(original_text) if original_text else []

            # Create document-specific audio directory
            doc_audio_dir = os.path.join(
                current_app.config['AUDIO_OUTPUT_FOLDER'],
                document_id
            )
            os.makedirs(doc_audio_dir, exist_ok=True)

            # Generate audio for each translated segment
            audio_segments = tts_service.generate_with_timestamps(
                translated_segments,
                language,
                doc_audio_dir
            )

            # Add original text to each segment
            for i, audio_segment in enumerate(audio_segments):
                if i < len(original_segments):
                    audio_segment['original_text'] = original_segments[i]['text']
                else:
                    audio_segment['original_text'] = ''

            # Save segment info
            segment_info_path = os.path.join(doc_audio_dir, 'segments.json')
            with open(segment_info_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'document_id': document_id,
                    'language': language,
                    'segment_type': segment_type,
                    'segments': audio_segments
                }, f, ensure_ascii=False, indent=2)

            return jsonify({
                'success': True,
                'document_id': document_id,
                'language': language,
                'segment_type': segment_type,
                'total_segments': len(audio_segments),
                'segments': audio_segments,
                'audio_directory': document_id
            }), 200

        else:
            # Generate single audio file for entire document
            from app.utils.helpers import generate_unique_filename
            output_filename = f"{document_id}_{language}_full.mp3"
            output_path = os.path.join(current_app.config['AUDIO_OUTPUT_FOLDER'], output_filename)

            full_text = translation_data['full_text']
            audio_info = tts_service.text_to_speech(full_text, language, output_path)

            return jsonify({
                'success': True,
                'document_id': document_id,
                'language': language,
                'segment_type': 'full',
                'audio': audio_info,
                'audio_filename': output_filename
            }), 200

    except Exception as e:
        return jsonify({
            'error': 'Document TTS generation failed',
            'details': str(e)
        }), 500

@tts_bp.route('/tts/audio/<path:filename>', methods=['GET'])
def get_audio_file(filename):
    """
    Serve audio file

    Args:
        filename: Audio filename (can include subdirectories)

    Returns:
        Audio file
    """
    try:
        audio_path = os.path.join(current_app.config['AUDIO_OUTPUT_FOLDER'], filename)

        if not os.path.exists(audio_path):
            return jsonify({'error': 'Audio file not found'}), 404

        return send_file(audio_path, mimetype='audio/mpeg')

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve audio file',
            'details': str(e)
        }), 500

@tts_bp.route('/tts/generate-custom', methods=['POST'])
def generate_custom_tts():
    """
    Generate text-to-speech for custom/edited text with segments

    Request body:
        {
            "document_id": "unique_doc_id",
            "translated_text": "Custom translated text",
            "original_text": "Original text",
            "language": "es",
            "service": "gtts",
            "segment_type": "sentence"
        }

    Returns:
        JSON response with audio files and segment information
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        document_id = data.get('document_id')
        translated_text = data.get('translated_text', '')
        original_text = data.get('original_text', '')
        language = data.get('language', 'en')
        service = data.get('service', 'gtts')
        segment_type = data.get('segment_type', 'sentence')

        if not document_id or not translated_text:
            return jsonify({'error': 'document_id and translated_text are required'}), 400

        # Initialize TTS service
        tts_service = TextToSpeechService(service=service)

        if segment_type == 'sentence':
            # Create segments for both original and translated text
            translated_segments = tts_service.create_sentence_segments(translated_text)
            original_segments = tts_service.create_sentence_segments(original_text) if original_text else []

            # Create document-specific audio directory
            doc_audio_dir = os.path.join(
                current_app.config['AUDIO_OUTPUT_FOLDER'],
                document_id
            )
            os.makedirs(doc_audio_dir, exist_ok=True)

            # Generate audio for each translated segment
            audio_segments = tts_service.generate_with_timestamps(
                translated_segments,
                language,
                doc_audio_dir
            )

            # Add original text to each segment
            for i, audio_segment in enumerate(audio_segments):
                if i < len(original_segments):
                    audio_segment['original_text'] = original_segments[i]['text']
                else:
                    audio_segment['original_text'] = ''

            # Save segment info
            segment_info_path = os.path.join(doc_audio_dir, 'segments.json')
            with open(segment_info_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'document_id': document_id,
                    'language': language,
                    'segment_type': segment_type,
                    'segments': audio_segments
                }, f, ensure_ascii=False, indent=2)

            return jsonify({
                'success': True,
                'document_id': document_id,
                'language': language,
                'segment_type': segment_type,
                'total_segments': len(audio_segments),
                'segments': audio_segments,
                'audio_directory': document_id
            }), 200

        else:
            return jsonify({'error': 'Only sentence segment_type is supported'}), 400

    except Exception as e:
        return jsonify({
            'error': 'Custom TTS generation failed',
            'details': str(e)
        }), 500

@tts_bp.route('/tts/segments/<document_id>', methods=['GET'])
def get_document_segments(document_id):
    """
    Get segment information for a document

    Args:
        document_id: Unique document identifier

    Returns:
        JSON response with segment information
    """
    try:
        segment_info_path = os.path.join(
            current_app.config['AUDIO_OUTPUT_FOLDER'],
            document_id,
            'segments.json'
        )

        if not os.path.exists(segment_info_path):
            return jsonify({'error': 'Segment information not found'}), 404

        with open(segment_info_path, 'r', encoding='utf-8') as f:
            segment_info = json.load(f)

        return jsonify({
            'success': True,
            'segments': segment_info
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve segment information',
            'details': str(e)
        }), 500

@tts_bp.route('/tts/supported-languages', methods=['GET'])
def get_tts_supported_languages():
    """
    Get list of supported languages for TTS

    Query params:
        service: TTS service (default: 'gtts')

    Returns:
        JSON response with supported languages
    """
    try:
        service = request.args.get('service', 'gtts')

        tts_service = TextToSpeechService(service=service)
        languages = tts_service.get_supported_languages()

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

from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from app.services.pdf_processor import PDFProcessor
from app.utils.helpers import allowed_file, generate_unique_filename

upload_bp = Blueprint('upload', __name__)
pdf_processor = PDFProcessor()

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle PDF file upload and text extraction

    Returns:
        JSON response with extracted text data and document ID
    """
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']

        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Validate file type
        if not allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
            return jsonify({'error': 'Invalid file type. Only PDF files are allowed'}), 400

        # Generate unique filename
        filename = secure_filename(file.filename)
        unique_filename = generate_unique_filename(filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)

        # Save uploaded file
        file.save(file_path)

        # Extract text from PDF
        try:
            text_data = pdf_processor.extract_text(file_path, method='pdfplumber')
        except Exception as extract_error:
            # Try fallback method
            try:
                text_data = pdf_processor.extract_text(file_path, method='pypdf2')
            except Exception as fallback_error:
                return jsonify({
                    'error': 'Failed to extract text from PDF',
                    'details': str(fallback_error)
                }), 500

        # Save extracted text
        text_output_path = os.path.join(
            current_app.config['TRANSLATION_OUTPUT_FOLDER'],
            f"{os.path.splitext(unique_filename)[0]}_extracted.json"
        )
        pdf_processor.save_extracted_text(text_data, text_output_path)

        # Generate document ID
        document_id = os.path.splitext(unique_filename)[0]

        # Prepare response
        response = {
            'success': True,
            'document_id': document_id,
            'filename': filename,
            'total_pages': text_data['total_pages'],
            'total_chars': text_data['total_chars'],
            'full_text': text_data['full_text'],
            'pages': text_data['pages'],
            'metadata': text_data['metadata']
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500

@upload_bp.route('/document/<document_id>', methods=['GET'])
def get_document(document_id):
    """
    Retrieve extracted text for a document

    Args:
        document_id: Unique document identifier

    Returns:
        JSON response with document text data
    """
    try:
        text_file_path = os.path.join(
            current_app.config['TRANSLATION_OUTPUT_FOLDER'],
            f"{document_id}_extracted.json"
        )

        if not os.path.exists(text_file_path):
            return jsonify({'error': 'Document not found'}), 404

        import json
        with open(text_file_path, 'r', encoding='utf-8') as f:
            text_data = json.load(f)

        return jsonify({
            'success': True,
            'document_id': document_id,
            'data': text_data
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve document',
            'details': str(e)
        }), 500

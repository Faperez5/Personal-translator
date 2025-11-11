import pdfplumber
import PyPDF2
import os
from typing import Dict, List, Optional
import json

class PDFProcessor:
    """Service for processing PDF files and extracting text"""

    def __init__(self):
        self.supported_methods = ['pdfplumber', 'pypdf2']

    def extract_text(self, pdf_path: str, method: str = 'pdfplumber') -> Dict:
        """
        Extract text from a PDF file

        Args:
            pdf_path: Path to the PDF file
            method: Extraction method to use ('pdfplumber' or 'pypdf2')

        Returns:
            Dictionary containing extracted text and metadata
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        if method == 'pdfplumber':
            return self._extract_with_pdfplumber(pdf_path)
        elif method == 'pypdf2':
            return self._extract_with_pypdf2(pdf_path)
        else:
            raise ValueError(f"Unsupported extraction method: {method}")

    def _extract_with_pdfplumber(self, pdf_path: str) -> Dict:
        """Extract text using pdfplumber (better for complex layouts)"""
        text_data = {
            'full_text': '',
            'pages': [],
            'metadata': {},
            'total_pages': 0
        }

        try:
            with pdfplumber.open(pdf_path) as pdf:
                text_data['total_pages'] = len(pdf.pages)
                text_data['metadata'] = pdf.metadata or {}

                for page_num, page in enumerate(pdf.pages, start=1):
                    page_text = page.extract_text() or ''
                    text_data['pages'].append({
                        'page_number': page_num,
                        'text': page_text,
                        'char_count': len(page_text)
                    })
                    text_data['full_text'] += page_text + '\n\n'

                text_data['full_text'] = text_data['full_text'].strip()
                text_data['total_chars'] = len(text_data['full_text'])

        except Exception as e:
            raise Exception(f"Error extracting text with pdfplumber: {str(e)}")

        return text_data

    def _extract_with_pypdf2(self, pdf_path: str) -> Dict:
        """Extract text using PyPDF2 (fallback method)"""
        text_data = {
            'full_text': '',
            'pages': [],
            'metadata': {},
            'total_pages': 0
        }

        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text_data['total_pages'] = len(pdf_reader.pages)
                text_data['metadata'] = pdf_reader.metadata or {}

                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text() or ''
                    text_data['pages'].append({
                        'page_number': page_num + 1,
                        'text': page_text,
                        'char_count': len(page_text)
                    })
                    text_data['full_text'] += page_text + '\n\n'

                text_data['full_text'] = text_data['full_text'].strip()
                text_data['total_chars'] = len(text_data['full_text'])

        except Exception as e:
            raise Exception(f"Error extracting text with PyPDF2: {str(e)}")

        return text_data

    def split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences for better translation and TTS processing

        Args:
            text: Input text

        Returns:
            List of sentences
        """
        import re

        # Simple sentence splitting (can be improved with nltk or spacy)
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]

    def split_into_chunks(self, text: str, max_chars: int = 5000) -> List[str]:
        """
        Split text into chunks for API processing

        Args:
            text: Input text
            max_chars: Maximum characters per chunk

        Returns:
            List of text chunks
        """
        if len(text) <= max_chars:
            return [text]

        sentences = self.split_into_sentences(text)
        chunks = []
        current_chunk = ''

        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 1 <= max_chars:
                current_chunk += sentence + ' '
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ' '

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def save_extracted_text(self, text_data: Dict, output_path: str) -> str:
        """
        Save extracted text to a JSON file

        Args:
            text_data: Extracted text data
            output_path: Path to save the JSON file

        Returns:
            Path to the saved file
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(text_data, f, ensure_ascii=False, indent=2)
            return output_path
        except Exception as e:
            raise Exception(f"Error saving extracted text: {str(e)}")

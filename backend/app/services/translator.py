from typing import Dict, List, Optional
import os
from deep_translator import GoogleTranslator
import deepl

class TranslationService:
    """Service for translating text using various translation APIs"""

    def __init__(self, service: str = 'google'):
        """
        Initialize translation service

        Args:
            service: Translation service to use ('google', 'deepl', 'google_cloud')
        """
        self.service = service
        self.translator = None
        self._initialize_translator()

    def _initialize_translator(self):
        """Initialize the appropriate translator based on service type"""
        if self.service == 'google':
            # Using deep-translator (free, no API key needed)
            # Translator object is created per request
            self.translator = None
        elif self.service == 'deepl':
            # Using DeepL (requires API key)
            api_key = os.environ.get('DEEPL_API_KEY')
            if api_key:
                self.translator = deepl.Translator(api_key)
            else:
                raise ValueError("DeepL API key not found in environment variables")
        elif self.service == 'google_cloud':
            # Using Google Cloud Translation API (requires API key)
            # Implementation for Google Cloud can be added here
            raise NotImplementedError("Google Cloud Translation not yet implemented")
        else:
            raise ValueError(f"Unsupported translation service: {self.service}")

    def translate_text(
        self,
        text: str,
        target_lang: str,
        source_lang: str = 'auto'
    ) -> Dict:
        """
        Translate text to target language

        Args:
            text: Text to translate
            target_lang: Target language code
            source_lang: Source language code (default: 'auto' for auto-detection)

        Returns:
            Dictionary with translation results
        """
        if not text or not text.strip():
            return {
                'translated_text': '',
                'source_lang': source_lang,
                'target_lang': target_lang,
                'service': self.service
            }

        try:
            if self.service == 'google':
                return self._translate_google(text, target_lang, source_lang)
            elif self.service == 'deepl':
                return self._translate_deepl(text, target_lang, source_lang)
            else:
                raise ValueError(f"Unsupported service: {self.service}")
        except Exception as e:
            raise Exception(f"Translation error: {str(e)}")

    def _translate_google(
        self,
        text: str,
        target_lang: str,
        source_lang: str
    ) -> Dict:
        """Translate using Google Translate (free)"""
        try:
            # deep-translator requires source language (use 'auto' for auto-detection)
            translator = GoogleTranslator(
                source=source_lang if source_lang != 'auto' else 'auto',
                target=target_lang
            )
            translated_text = translator.translate(text)

            # Detect source language if auto was used
            detected_source = source_lang
            if source_lang == 'auto':
                try:
                    from deep_translator import single_detection
                    detected_source = single_detection(text, api_key=None)
                except:
                    detected_source = 'unknown'

            return {
                'translated_text': translated_text,
                'source_lang': detected_source,
                'target_lang': target_lang,
                'service': 'google',
                'confidence': None
            }
        except Exception as e:
            raise Exception(f"Google Translate error: {str(e)}")

    def _translate_deepl(
        self,
        text: str,
        target_lang: str,
        source_lang: str
    ) -> Dict:
        """Translate using DeepL API"""
        try:
            # DeepL language codes are uppercase
            target_lang_upper = target_lang.upper()
            source_lang_param = None if source_lang == 'auto' else source_lang.upper()

            result = self.translator.translate_text(
                text,
                target_lang=target_lang_upper,
                source_lang=source_lang_param
            )

            return {
                'translated_text': result.text,
                'source_lang': result.detected_source_lang.lower() if result.detected_source_lang else source_lang,
                'target_lang': target_lang,
                'service': 'deepl'
            }
        except Exception as e:
            raise Exception(f"DeepL translation error: {str(e)}")

    def translate_chunks(
        self,
        chunks: List[str],
        target_lang: str,
        source_lang: str = 'auto'
    ) -> List[Dict]:
        """
        Translate multiple text chunks

        Args:
            chunks: List of text chunks to translate
            target_lang: Target language code
            source_lang: Source language code

        Returns:
            List of translation results for each chunk
        """
        results = []

        for i, chunk in enumerate(chunks):
            try:
                translation = self.translate_text(chunk, target_lang, source_lang)
                translation['chunk_index'] = i
                results.append(translation)
            except Exception as e:
                results.append({
                    'chunk_index': i,
                    'error': str(e),
                    'original_text': chunk
                })

        return results

    def detect_language(self, text: str) -> Dict:
        """
        Detect the language of input text

        Args:
            text: Text to detect language for

        Returns:
            Dictionary with detected language info
        """
        if self.service == 'google':
            try:
                from deep_translator import single_detection
                detected_lang = single_detection(text, api_key=None)
                return {
                    'language': detected_lang,
                    'confidence': None
                }
            except Exception as e:
                raise Exception(f"Language detection error: {str(e)}")
        else:
            # For other services, use translate with auto-detection
            translation = self.translate_text(text, 'en', 'auto')
            return {
                'language': translation['source_lang'],
                'confidence': None
            }

    def get_supported_languages(self) -> List[str]:
        """
        Get list of supported languages for the current service

        Returns:
            List of language codes
        """
        if self.service == 'google':
            return [
                'en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'ko',
                'zh-cn', 'zh-tw', 'ar', 'hi', 'nl', 'pl', 'tr', 'vi',
                'th', 'id', 'ms', 'sv', 'no', 'da', 'fi'
            ]
        elif self.service == 'deepl':
            return [
                'en', 'de', 'fr', 'es', 'pt', 'it', 'nl', 'pl', 'ru',
                'ja', 'zh', 'bg', 'cs', 'da', 'el', 'et', 'fi', 'hu',
                'id', 'ko', 'lt', 'lv', 'nb', 'ro', 'sk', 'sl', 'sv',
                'tr', 'uk'
            ]
        else:
            return []

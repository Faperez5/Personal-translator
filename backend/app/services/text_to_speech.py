from typing import Dict, List, Optional
import os
from gtts import gTTS
import json

class TextToSpeechService:
    """Service for converting text to speech using various TTS engines"""

    def __init__(self, service: str = 'gtts'):
        """
        Initialize TTS service

        Args:
            service: TTS service to use ('gtts', 'google_cloud', 'azure', 'elevenlabs')
        """
        self.service = service
        self.supported_services = ['gtts', 'google_cloud', 'azure', 'elevenlabs']

        if service not in self.supported_services:
            raise ValueError(f"Unsupported TTS service: {service}")

    def text_to_speech(
        self,
        text: str,
        language: str,
        output_path: str,
        slow: bool = False
    ) -> Dict:
        """
        Convert text to speech and save as audio file

        Args:
            text: Text to convert
            language: Language code (e.g., 'en', 'es', 'fr')
            output_path: Path to save the audio file
            slow: Speak slowly (only for gTTS)

        Returns:
            Dictionary with audio file info
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        try:
            if self.service == 'gtts':
                return self._gtts_generate(text, language, output_path, slow)
            elif self.service == 'google_cloud':
                return self._google_cloud_generate(text, language, output_path)
            elif self.service == 'azure':
                return self._azure_generate(text, language, output_path)
            elif self.service == 'elevenlabs':
                return self._elevenlabs_generate(text, language, output_path)
            else:
                raise ValueError(f"Unsupported service: {self.service}")
        except Exception as e:
            raise Exception(f"TTS generation error: {str(e)}")

    def _gtts_generate(
        self,
        text: str,
        language: str,
        output_path: str,
        slow: bool = False
    ) -> Dict:
        """Generate speech using Google Text-to-Speech (free)"""
        try:
            tts = gTTS(text=text, lang=language, slow=slow)
            tts.save(output_path)

            file_size = os.path.getsize(output_path)

            return {
                'success': True,
                'audio_path': output_path,
                'language': language,
                'service': 'gtts',
                'file_size': file_size,
                'duration': None  # gTTS doesn't provide duration
            }
        except Exception as e:
            raise Exception(f"gTTS error: {str(e)}")

    def _google_cloud_generate(
        self,
        text: str,
        language: str,
        output_path: str
    ) -> Dict:
        """Generate speech using Google Cloud TTS (requires API key)"""
        # Placeholder for Google Cloud TTS implementation
        # Requires google-cloud-texttospeech library and credentials
        raise NotImplementedError("Google Cloud TTS not yet implemented. Use 'gtts' for now.")

    def _azure_generate(
        self,
        text: str,
        language: str,
        output_path: str
    ) -> Dict:
        """Generate speech using Azure Speech Services (requires API key)"""
        # Placeholder for Azure TTS implementation
        raise NotImplementedError("Azure TTS not yet implemented. Use 'gtts' for now.")

    def _elevenlabs_generate(
        self,
        text: str,
        language: str,
        output_path: str
    ) -> Dict:
        """Generate speech using ElevenLabs (requires API key)"""
        # Placeholder for ElevenLabs implementation
        raise NotImplementedError("ElevenLabs TTS not yet implemented. Use 'gtts' for now.")

    def generate_with_timestamps(
        self,
        segments: List[Dict],
        language: str,
        output_dir: str
    ) -> List[Dict]:
        """
        Generate TTS for multiple text segments with timestamps

        Args:
            segments: List of text segments with metadata
            language: Language code
            output_dir: Directory to save audio files

        Returns:
            List of audio file info with timestamps
        """
        results = []

        for i, segment in enumerate(segments):
            try:
                text = segment.get('text', '')
                if not text.strip():
                    continue

                # Generate unique filename for each segment
                segment_id = segment.get('id', i)
                output_filename = f"segment_{segment_id}.mp3"
                output_path = os.path.join(output_dir, output_filename)

                # Generate audio
                audio_info = self.text_to_speech(text, language, output_path)

                # Add segment metadata
                audio_info['segment_id'] = segment_id
                audio_info['start_char'] = segment.get('start_char', 0)
                audio_info['end_char'] = segment.get('end_char', len(text))
                audio_info['text'] = text

                results.append(audio_info)

            except Exception as e:
                results.append({
                    'segment_id': segment.get('id', i),
                    'error': str(e),
                    'text': segment.get('text', '')
                })

        return results

    def create_sentence_segments(self, text: str) -> List[Dict]:
        """
        Split text into sentence segments for TTS

        Args:
            text: Input text

        Returns:
            List of sentence segments with position info
        """
        import re

        sentences = re.split(r'(?<=[.!?])\s+', text)
        segments = []
        char_position = 0

        for i, sentence in enumerate(sentences):
            if sentence.strip():
                segment = {
                    'id': i,
                    'text': sentence.strip(),
                    'start_char': char_position,
                    'end_char': char_position + len(sentence)
                }
                segments.append(segment)
                char_position += len(sentence) + 1  # +1 for space

        return segments

    def create_word_segments(self, text: str) -> List[Dict]:
        """
        Split text into word segments for word-by-word highlighting

        Args:
            text: Input text

        Returns:
            List of word segments with position info
        """
        import re

        words = re.findall(r'\S+', text)
        segments = []
        char_position = 0

        for i, word in enumerate(words):
            word_start = text.find(word, char_position)
            if word_start != -1:
                segment = {
                    'id': i,
                    'text': word,
                    'start_char': word_start,
                    'end_char': word_start + len(word)
                }
                segments.append(segment)
                char_position = word_start + len(word)

        return segments

    def get_supported_languages(self) -> List[str]:
        """
        Get list of supported languages for the current service

        Returns:
            List of language codes
        """
        if self.service == 'gtts':
            # Common languages supported by gTTS
            return [
                'en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'ko',
                'zh-cn', 'zh-tw', 'ar', 'hi', 'nl', 'pl', 'tr', 'vi',
                'th', 'id', 'sv', 'no', 'da', 'fi', 'cs', 'el', 'he',
                'hu', 'ro', 'sk', 'uk', 'bn', 'ta', 'te', 'mr', 'gu'
            ]
        else:
            return []

    def estimate_duration(self, text: str, words_per_minute: int = 150) -> float:
        """
        Estimate audio duration based on text length

        Args:
            text: Input text
            words_per_minute: Average speaking speed

        Returns:
            Estimated duration in seconds
        """
        word_count = len(text.split())
        duration_minutes = word_count / words_per_minute
        return duration_minutes * 60

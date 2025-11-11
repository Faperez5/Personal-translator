import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # File upload settings
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    OUTPUT_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
    AUDIO_OUTPUT_FOLDER = os.path.join(OUTPUT_FOLDER, 'audio')
    TRANSLATION_OUTPUT_FOLDER = os.path.join(OUTPUT_FOLDER, 'translations')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf'}

    # API Keys (set these in .env file)
    GOOGLE_TRANSLATE_API_KEY = os.environ.get('GOOGLE_TRANSLATE_API_KEY')
    GOOGLE_TTS_API_KEY = os.environ.get('GOOGLE_TTS_API_KEY')
    DEEPL_API_KEY = os.environ.get('DEEPL_API_KEY')

    # Translation settings
    DEFAULT_SOURCE_LANGUAGE = 'auto'
    SUPPORTED_LANGUAGES = [
        'en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'ko', 'zh', 'ar', 'hi'
    ]

    # TTS settings
    TTS_CHUNK_SIZE = 5000  # Characters per TTS request
    AUDIO_FORMAT = 'mp3'

    # CORS settings
    CORS_ORIGINS = '*'  # Allow all origins in development

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

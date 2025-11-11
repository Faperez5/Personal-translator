from flask import Flask
from flask_cors import CORS
import os

def create_app(config_name='default'):
    app = Flask(__name__)

    # Load configuration
    from config import config
    app.config.from_object(config[config_name])

    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})

    # Create necessary directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['AUDIO_OUTPUT_FOLDER'], exist_ok=True)
    os.makedirs(app.config['TRANSLATION_OUTPUT_FOLDER'], exist_ok=True)

    # Register blueprints
    from app.routes.upload import upload_bp
    from app.routes.translate import translate_bp
    from app.routes.tts import tts_bp

    app.register_blueprint(upload_bp, url_prefix='/api')
    app.register_blueprint(translate_bp, url_prefix='/api')
    app.register_blueprint(tts_bp, url_prefix='/api')

    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy', 'message': 'Language Learning API is running'}, 200

    return app

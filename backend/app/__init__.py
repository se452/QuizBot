import os
from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    
    # Configure CORS
    allowed_origins = os.environ.get('CORS_ALLOWED_ORIGINS', 'http://localhost:3000,https://quizbot-frontend.onrender.com')
    origins = allowed_origins.split(',')
    
    CORS(app, resources={r"/*": {"origins": origins, "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})
    
    from .routes import main
    app.register_blueprint(main)
    
    return app 
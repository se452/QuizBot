from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    
    # Configure CORS to allow all origins during development
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",  # Allow all origins in development
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    from .routes import main
    app.register_blueprint(main)
    
    return app 
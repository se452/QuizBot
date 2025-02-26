from flask import Flask
from flask_cors import CORS
from .error_handlers import register_error_handlers

def create_app():
    app = Flask(__name__)
    
    # Configure CORS to allow requests from frontend
    CORS(app, 
         resources={
             r"/*": {  # Allow CORS for all routes
                 "origins": [
                     "https://quiz-bot-iota.vercel.app",
                     "http://localhost:3000",
                     "https://quiz-bot-iota.vercel.app/"
                 ],
                 "methods": ["GET", "POST", "OPTIONS"],
                 "allow_headers": ["Content-Type", "Authorization"],
                 "expose_headers": ["Content-Type", "Authorization"],
                 "max_age": 3600,
                 "supports_credentials": True,
                 "send_wildcard": False
             }
         }
    )
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register blueprints
    from .routes import main
    app.register_blueprint(main)
    
    return app 
from flask import Flask
from flask_cors import CORS

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
                 "supports_credentials": True,
                 "send_wildcard": False
             }
         }
    )
    
    from .routes import main
    app.register_blueprint(main)
    
    return app 
from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    
    # Configure CORS to allow requests from frontend
    CORS(app, 
         resources={r"/api/*": {
             "origins": [
                 "https://quiz-bot-iota.vercel.app",
                 "http://localhost:3000"
             ],
             "methods": ["GET", "POST", "OPTIONS"],
             "allow_headers": ["Content-Type"],
             "supports_credentials": True
         }},
         supports_credentials=True
    )
    
    from .routes import main
    app.register_blueprint(main)
    
    return app 
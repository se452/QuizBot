import os
import json
import firebase_admin
from firebase_admin import credentials

def initialize_firebase():
    """Initialize Firebase with credentials from environment variable or file"""
    try:
        # First, try to get credentials from environment variable
        if 'FIREBASE_CREDENTIALS' in os.environ:
            cred_dict = json.loads(os.environ.get('FIREBASE_CREDENTIALS'))
            cred = credentials.Certificate(cred_dict)
        # Fallback to local file for development
        else:
            cred_path = os.path.join(os.path.dirname(__file__), '..', 'credentials', 'hackathon-bb3cb-firebase-adminsdk-fbsvc-592d5d0282.json')
            cred = credentials.Certificate(cred_path)
        
        firebase_admin.initialize_app(cred)
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        # You might want to handle this error appropriately in your application 
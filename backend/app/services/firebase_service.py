import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Firebase if credentials are available
firebase_initialized = False
db = None

try:
    # Check if Firebase is already initialized
    firebase_admin.get_app()
    firebase_initialized = True
except ValueError:
    # Initialize Firebase with credentials
    cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
    if cred_path and os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        firebase_initialized = True
    else:
        # Use environment variables if credential file not available
        cred_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
        if cred_json:
            try:
                cred_dict = json.loads(cred_json)
                cred = credentials.Certificate(cred_dict)
                firebase_admin.initialize_app(cred)
                firebase_initialized = True
            except Exception as e:
                print(f"Warning: Failed to initialize Firebase: {str(e)}")
        else:
            print("Warning: Firebase credentials not found. Firebase functionality will be disabled.")

# Get Firestore database if Firebase is initialized
if firebase_initialized:
    try:
        db = firestore.client()
    except Exception as e:
        print(f"Warning: Failed to get Firestore client: {str(e)}")
        firebase_initialized = False

def save_quiz_to_firebase(quiz, user_id, youtube_url):
    """
    Save a generated quiz to Firebase.
    
    Args:
        quiz (dict): The quiz data
        user_id (str): The user ID
        youtube_url (str): The YouTube URL
        
    Returns:
        str: The ID of the saved quiz
    """
    if not firebase_initialized or db is None:
        # Return a dummy ID if Firebase is not available
        return "firebase-not-available"
        
    try:
        # Create a new quiz document
        quiz_ref = db.collection('quizzes').document()
        
        # Add metadata
        quiz_data = {
            'quiz_content': quiz,
            'user_id': user_id,
            'youtube_url': youtube_url,
            'created_at': firestore.SERVER_TIMESTAMP,
            'completed': False
        }
        
        # Save to Firestore
        quiz_ref.set(quiz_data)
        
        return quiz_ref.id
        
    except Exception as e:
        print(f"Warning: Failed to save quiz to Firebase: {str(e)}")
        return "firebase-error"

def get_quiz_results(quiz_id, user_answers):
    """
    Calculate quiz results based on user answers.
    
    Args:
        quiz_id (str): The quiz ID
        user_answers (list): List of user's answer indices
        
    Returns:
        dict: Quiz results with score and feedback
    """
    if not firebase_initialized or db is None:
        # Return dummy results if Firebase is not available
        return {
            "error": "Firebase not available",
            "message": "Quiz results could not be saved to Firebase"
        }
        
    try:
        # Get the quiz from Firestore
        quiz_ref = db.collection('quizzes').document(quiz_id)
        quiz_doc = quiz_ref.get()
        
        if not quiz_doc.exists:
            raise Exception("Quiz not found")
            
        quiz_data = quiz_doc.to_dict()
        quiz_content = quiz_data.get('quiz_content', {})
        questions = quiz_content.get('questions', [])
        
        # Calculate score
        correct_count = 0
        question_results = []
        
        for i, (question, user_answer) in enumerate(zip(questions, user_answers)):
            correct_answer = question.get('correct_answer')
            is_correct = user_answer == correct_answer
            
            if is_correct:
                correct_count += 1
                
            question_results.append({
                'question_index': i,
                'is_correct': is_correct,
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'explanation': question.get('explanation', '')
            })
        
        # Calculate percentage
        total_questions = len(questions)
        score_percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0
        
        # Save results to Firestore
        results = {
            'score': correct_count,
            'total': total_questions,
            'percentage': score_percentage,
            'question_results': question_results,
            'completed_at': firestore.SERVER_TIMESTAMP
        }
        
        quiz_ref.update({
            'results': results,
            'completed': True
        })
        
        return results
        
    except Exception as e:
        print(f"Warning: Failed to get quiz results: {str(e)}")
        return {
            "error": str(e),
            "message": "Failed to process quiz results"
        } 
from flask import Blueprint, request, jsonify
from .services.youtube_service import download_youtube_audio
from .services.quiz_service import generate_quiz
from .services.firebase_service import save_quiz_to_firebase, get_quiz_results

main = Blueprint('main', __name__)

@main.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@main.route('/api/generate-quiz', methods=['POST'])
def create_quiz():
    data = request.json
    youtube_url = data.get('youtube_url')
    user_id = data.get('user_id')
    
    if not youtube_url:
        return jsonify({"error": "YouTube URL is required"}), 400
    
    try:
        # Get transcript from YouTube
        transcript = download_youtube_audio(youtube_url)
        
        # Generate quiz from transcript
        quiz = generate_quiz(transcript)
        
        # Save quiz to Firebase if user_id is provided
        if user_id:
            quiz_id = save_quiz_to_firebase(quiz, user_id, youtube_url)
            if quiz_id:
                quiz['id'] = quiz_id
        
        return jsonify({
            "success": True,
            "transcript": transcript,
            "quiz": quiz
        }), 200
        
    except Exception as e:
        error_message = str(e)
        print(f"Error generating quiz: {error_message}")
        return jsonify({"error": error_message}), 500

@main.route('/api/submit-quiz', methods=['POST'])
def submit_quiz():
    data = request.json
    quiz_id = data.get('quiz_id')
    user_id = data.get('user_id')
    answers = data.get('answers')
    quiz_data = data.get('quiz_data')  # Include quiz data for client-side processing
    
    if not answers:
        return jsonify({"error": "Answers are required"}), 400
    
    try:
        # If we have quiz_id and user_id, try to save to Firebase
        if quiz_id and user_id:
            results = get_quiz_results(quiz_id, answers)
            if "error" in results:
                # Fall back to client-side processing if Firebase fails
                if quiz_data:
                    results = calculate_results_locally(quiz_data, answers)
        else:
            # Process results locally if no Firebase data
            if not quiz_data:
                return jsonify({"error": "Quiz data is required for local processing"}), 400
            results = calculate_results_locally(quiz_data, answers)
        
        return jsonify({
            "success": True,
            "results": results
        }), 200
        
    except Exception as e:
        error_message = str(e)
        print(f"Error submitting quiz: {error_message}")
        return jsonify({"error": error_message}), 500

def calculate_results_locally(quiz_data, user_answers):
    """
    Calculate quiz results locally when Firebase is not available.
    
    Args:
        quiz_data (dict): The quiz data
        user_answers (list): List of user's answer indices
        
    Returns:
        dict: Quiz results with score and feedback
    """
    try:
        questions = quiz_data.get('questions', [])
        
        # Calculate score
        correct_count = 0
        question_results = []
        
        for i, question in enumerate(questions):
            if i < len(user_answers):
                user_answer = user_answers[i]
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
        
        return {
            'score': correct_count,
            'total': total_questions,
            'percentage': score_percentage,
            'question_results': question_results,
            'completed_at': None  # No timestamp for local processing
        }
        
    except Exception as e:
        print(f"Error calculating results locally: {str(e)}")
        return {
            "error": str(e),
            "message": "Failed to process quiz results locally"
        } 
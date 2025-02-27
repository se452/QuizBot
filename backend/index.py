from flask import Flask, jsonify
from app import create_app

app = create_app()

@app.route('/')
def home():
    return jsonify({
        "message": "QuizBot API is running",
        "status": "healthy",
        "endpoints": {
            "generate_quiz": "/api/generate-quiz",
            "submit_quiz": "/api/submit-quiz"
        }
    })

# This is for local development
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True) 
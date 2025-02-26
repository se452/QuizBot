# QuizBot - YouTube Video Quiz Generator

QuizBot is a web application that allows users to generate quizzes from YouTube videos. The application extracts audio from YouTube videos, transcribes it using Whisper, and then generates a quiz using Google's Gemini AI. Users can take the quiz and receive immediate feedback on their performance.

## Features

- Extract audio from YouTube videos
- Transcribe audio to text using OpenAI's Whisper
- Generate quizzes from transcripts using Google's Gemini AI
- Take quizzes with multiple-choice questions
- Get immediate feedback and explanations for answers
- Store quiz results in Firebase (when authenticated)

## Tech Stack

### Frontend
- React.js
- React Router for navigation
- CSS for styling

### Backend
- Python
- Flask for the API
- PyTube for YouTube video processing
- Whisper for audio transcription
- Google Gemini for quiz generation
- Firebase for data storage

## Setup Instructions

### Prerequisites
- Node.js and npm
- Python 3.8+ and pip
- Google Gemini API key
- Firebase project (for authentication and data storage)

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip3 install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example` and add your API keys:
   ```
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. Run the Flask server:
   ```
   python3 run.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```

4. Open your browser and navigate to `http://localhost:3000`

## Usage

1. Log in or sign up for an account
2. Paste a YouTube video URL in the input field
3. Click "Generate Quiz" and wait for the processing to complete
4. Take the quiz by selecting answers for each question
5. Submit your answers to see your results
6. Review explanations for each question

## Future Enhancements

- Add support for different quiz formats (true/false, fill-in-the-blank)
- Implement difficulty levels for quizzes
- Add support for sharing quizzes with others
- Implement a leaderboard for competitive quiz-taking
- Add support for other video platforms besides YouTube

## License

This project is licensed under the MIT License - see the LICENSE file for details.
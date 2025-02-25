import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise Exception("GEMINI_API_KEY not found in environment variables")

# Configure the Gemini API
genai.configure(api_key=api_key)

def generate_quiz(transcript):
    """
    Generate a quiz from the transcript using Google Gemini.
    
    Args:
        transcript (str): The transcript text
        
    Returns:
        dict: A dictionary containing the quiz questions and answers
    """
    try:
        # Print debug information
        print("API Key:", api_key)
        
        # Initialize the model
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        print("Using model: gemini-1.5-flash-latest")
        
        # Create the prompt for quiz generation
        prompt = f"""
        Create a multiple-choice quiz with 10 questions based on this transcript.
        Each question must have exactly 4 options labeled A, B, C, D.
        
        Format each question like this:
        {{
            "question": "What is X?",
            "options": [
                "A) First option",
                "B) Second option", 
                "C) Third option",
                "D) Fourth option"
            ],
            "correct_answers": [0],
            "explanation": "Explanation for why this is correct"
        }}

        Return an array of 10 questions in this exact format:
        [
            // Question 1
            {{
                "question": "...",
                "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
                "correct_answers": [0],
                "explanation": "..."
            }},
            // More questions...
        ]

        Rules:
        1. Each question MUST have exactly 4 options
        2. Options MUST start with A), B), C), D)
        3. correct_answers should be array of indices (0 for A, 1 for B, etc.)
        4. Include clear explanation for correct answer
        5. Return valid JSON array only

        Transcript:
        {transcript}
        """

        # Generate the quiz with debug information
        print("Generating content with prompt:", prompt[:100] + "...")
        response = model.generate_content(prompt)
        print("Response received:", response)
        response_text = response.text.strip()
        print("Response text:", response_text[:100] + "...")
        
        # Clean up the response text
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].strip()
        
        # Remove any comments
        response_text = "\n".join(
            line for line in response_text.split("\n") 
            if not line.strip().startswith("//")
        )
        
        # Parse JSON
        quiz_list = json.loads(response_text)
        
        # Validate questions
        if not isinstance(quiz_list, list):
            raise ValueError("Response must be a list of questions")
        
        for i, question in enumerate(quiz_list):
            # Check required fields
            required_fields = {'question', 'options', 'correct_answers', 'explanation'}
            if not all(field in question for field in required_fields):
                raise ValueError(f"Question {i+1} missing required fields")
            
            # Validate options
            if len(question['options']) != 4:
                raise ValueError(f"Question {i+1} must have exactly 4 options")
            
            # Validate option format
            prefixes = ['A)', 'B)', 'C)', 'D)']
            if not all(opt.startswith(prefix) for opt, prefix in zip(question['options'], prefixes)):
                raise ValueError(f"Question {i+1} options must start with A), B), C), D)")
            
            # Validate correct_answers
            if not isinstance(question['correct_answers'], list):
                raise ValueError(f"Question {i+1} correct_answers must be a list")
            if not all(isinstance(idx, int) and 0 <= idx <= 3 for idx in question['correct_answers']):
                raise ValueError(f"Question {i+1} has invalid correct_answers indices")
        
        return {"questions": quiz_list}

    except json.JSONDecodeError as e:
        print("JSON Parse Error:", str(e))
        print("Response Text:", response_text)
        raise Exception("Failed to parse quiz format. Please try again.")
    except Exception as e:
        print("Detailed error:", str(e))
        raise Exception(f"Error generating quiz: {str(e)}") 
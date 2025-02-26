import os
import sys
import torch
import google.generativeai as genai
from dotenv import load_dotenv

def test_setup():
    print("Testing Python setup...")
    print(f"Python version: {sys.version}")
    
    print("\nTesting PyTorch...")
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    
    print("\nTesting Google Gemini...")
    try:
        # Load environment variables
        load_dotenv()
        
        # Get API key
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("Warning: GEMINI_API_KEY not found in .env file")
            return
            
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        
        # Initialize the model
        model = genai.GenerativeModel('gemini-pro')
        print("Google Gemini loaded successfully!")
    except Exception as e:
        print(f"Error loading Google Gemini: {str(e)}")
    
    print("\nSetup test completed!")

if __name__ == "__main__":
    test_setup() 
import google.generativeai as genai
import time
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")

def test_gemini_api(api_key):
    """Basic test of Gemini API connectivity"""
    try:
        # Configure the API
        genai.configure(api_key=api_key)
        
        # Initialize the model - USING CORRECT MODEL NAME
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Simple test prompt
        prompt = "Respond with just the word 'Success' if you can hear me"
        
        print("Sending test request to Gemini API...")
        start_time = time.time()
        
        # Make the API call
        response = model.generate_content(prompt)
        
        # Calculate response time
        response_time = time.time() - start_time
        print(f"Response received in {response_time:.2f} seconds")
        
        # Return the response text
        return response.text
        
    except Exception as e:
        print(f"API Error: {str(e)}")
        return None

if __name__ == "__main__":
    # Get API key from user
    # Run the test
    result = test_gemini_api(api_key)
    
    # Display results
    if result:
        print("\nAPI Response:")
        print(result)
        print("\n✅ Gemini API connection successful!")
    else:
        print("\n❌ Failed to connect to Gemini API")

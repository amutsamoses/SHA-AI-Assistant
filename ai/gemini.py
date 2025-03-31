import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load API Key from environment variable
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")

# Configure Gemini API
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')
    logging.info("Gemini API configured successfully.")
else:
    logging.error("GOOGLE_API_KEY environment variable not set. Gemini functionality will be limited.")
    model = None

def chat_with_ai(user_input):
    """Communicates with Google Gemini AI to generate responses."""
    if model is None:
        return "Error: Gemini API key not configured."
    try:
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        logging.error(f"Error communicating with Gemini API: {e}")
        return f"Sorry, I encountered an error while trying to get a response from Gemini."

if __name__ == "__main__":
    if GOOGLE_API_KEY:
        while True:
            user_input = input("You (Gemini): ")
            if user_input.lower() in ["exit", "quit", "goodbye"]:
                print("Gemini: Goodbye!")
                break
            response = chat_with_ai(user_input)
            print(f"Gemini: {response}")
    else:
        print("Gemini API key not configured. Cannot run example.")
import string
import google.generativeai as genai
from sklearn.metrics.pairwise import cosine_similarity
import os
import pickle
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path='D:/RETRIEVAL-SHA-CHATBOT/backend/.env')

# Load pre-trained models (TF-IDF and Word2Vec)
with open("D:/RETRIEVAL-SHA-CHATBOT/models/sentence_tokens.pkl", "rb") as f:
    sentence_tokens = pickle.load(f)

with open("D:/RETRIEVAL-SHA-CHATBOT/models/tfidf_vectorizer.pkl", "rb") as f:
    tfidf_vectorizer = pickle.load(f)

# Configure Google Gemini API
GENAI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")
genai.configure(api_key=GENAI_API_KEY)

# gemini model instance and model object
gemini_model = genai.GenerativeModel("gemini-2.0-flash")

def preprocess_text(text):
    """Preprocess the text (remove punctuation, lowercase, etc.)"""
    text = text.lower().translate(str.maketrans('', '', string.punctuation))
    return text

def chat_with_gemini(user_input):
    try:
        response = gemini_model.generate_content(user_input)
        return response.text
    except Exception as e:
        return f"Sorry, I couldn't get that. Error from Gemini: {e}"
        
    

def hybrid_get_response(user_input, threshold=0.6):
    # processing input text using the retrieval-based model
    user_input_processed = preprocess_text(user_input)
    tfidf = tfidf_vectorizer.transform([user_input_processed])
    similarities = cosine_similarity(tfidf, tfidf_vectorizer.transform(sentence_tokens)).flatten()
    max_similarity = similarities.max()
    
    # If similarity score exceeds the threshold, use retrieval-based response
    if max_similarity >= threshold:
        response_idx = similarities.argmax()
        response = sentence_tokens[response_idx]
    else:
        # If similarity is low, use Google Gemini for generative response
        response = chat_with_gemini(user_input)
    
    return response



if __name__ == "__main__":
    while True:
        user_input = input("You : ")
        if user_input.lower() in ["exit", "quit", "goodbye"]:
            print("SHA CHATBOT: Thank you for using the SHA chat!!!, Goodbye!")
            break
        response = hybrid_get_response(user_input)
        print(f"SHA Chatbot: {response}")
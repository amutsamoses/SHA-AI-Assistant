# Uses TF-IDF similarity to find the best response.

import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
import logging
import configparser
import os

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')
models_dir = config.get('paths', 'models_dir', fallback='D:/RETRIEVAL-SHA-CHATBOT/models/')
sentence_tokens_path = os.path.join(models_dir, "sentence_tokens.pkl")
vectorizer_path = os.path.join(models_dir, "tfidf_vectorizer.pkl")

# Load preprocessed data and TF-IDF vectorizer
try:
    with open(sentence_tokens_path, "rb") as f:
        sentence_tokens = pickle.load(f)
    logging.info(f"Sentence tokens loaded from: {sentence_tokens_path}")
except FileNotFoundError:
    logging.error(f"Error: Sentence tokens file not found at {sentence_tokens_path}")
    sentence_tokens = []
except Exception as e:
    logging.error(f"Error loading sentence tokens: {e}")
    sentence_tokens = []

try:
    with open(vectorizer_path, "rb") as f:
        vectorizer = pickle.load(f)
    logging.info(f"TF-IDF vectorizer loaded from: {vectorizer_path}")
except FileNotFoundError:
    logging.error(f"Error: TF-IDF vectorizer file not found at {vectorizer_path}")
    vectorizer = None
except Exception as e:
    logging.error(f"Error loading TF-IDF vectorizer: {e}")
    vectorizer = None

def preprocess_text(text):
    """Convert text to lowercase and remove punctuation"""
    text = text.lower().translate(str.maketrans('', '', string.punctuation))
    return text

def get_response(user_input):
    if vectorizer is None or not sentence_tokens:
        return "Error: Chatbot models not loaded properly."
    user_input = preprocess_text(user_input)
    # Vectorize input and calculate similarity
    tfidf = vectorizer.transform([user_input])
    similarities = cosine_similarity(tfidf, vectorizer.transform(sentence_tokens))

    if not similarities.size or similarities.max() == 0:
        return "I'm sorry, I don't understand your request. Please try rephrasing."

    best_match_index = similarities.argmax()
    return sentence_tokens[best_match_index]

def match_reply(user_input):
    """Match user input with appropriate response"""
    return get_response(user_input)

if __name__ == "__main__":
    logging.info("Starting TF-IDF based chatbot (response.py)...")
    print("SHA Chatbot: Hello! How can I assist you with your healthcare inquiries today?")
    while True:
        user_input = input("You: ").lower()
        if user_input in ["exit", "quit", "goodbye"]:
            print("SHA Chat: Thank you for using SHA Chat. Goodbye!")
            logging.info("Chatbot session ended.")
            break
        response = match_reply(user_input)
        print(f"SHA Chatbot: {response}")
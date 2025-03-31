# Implements the NLTK-based retrieval chatbot logic. Handles user input, tokenization, and response retrieval.

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
import logging
import configparser

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')
models_dir = config.get('paths', 'models_dir', fallback='D:/RETRIEVAL-SHA-CHATBOT/models/')
sentence_tokens_path = os.path.join(models_dir, "sentence_tokens.pkl")
vectorizer_path = os.path.join(models_dir, "tfidf_vectorizer.pkl")

# Load sentence tokens and vectorizer
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
        tfidf_vectorizer = pickle.load(f)
    logging.info(f"TF-IDF vectorizer loaded from: {vectorizer_path}")
except FileNotFoundError:
    logging.error(f"Error: TF-IDF vectorizer file not found at {vectorizer_path}")
    tfidf_vectorizer = None
except Exception as e:
    logging.error(f"Error loading TF-IDF vectorizer: {e}")
    tfidf_vectorizer = None

def get_response(user_input):
    if tfidf_vectorizer is None or not sentence_tokens:
        return "Error: Chatbot models not loaded properly."
    user_input = user_input.lower()
    tfidf = tfidf_vectorizer.transform([user_input])
    similarities = cosine_similarity(tfidf, tfidf_vectorizer.transform(sentence_tokens)).flatten()
    if not similarities.size:
        return "I'm sorry, I didn't understand that."
    response_idx = similarities.argmax()
    return sentence_tokens[response_idx] if similarities[response_idx] > 0 else "I'm sorry, I didn't understand that."

if __name__ == "__main__":
    logging.info("Starting NLTK-based chatbot...")
    while True:
        user_text = input("User: ")
        if user_text.lower() == "exit":
            print("SHA Chatbot: Goodbye!")
            logging.info("Chatbot session ended.")
            break
        response = get_response(user_text)
        print(f"SHA Chatbot: {response}")
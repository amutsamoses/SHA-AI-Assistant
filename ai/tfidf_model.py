
# Specifically trains and saves the TF-IDF model to process user queries.

import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import logging
import os
import configparser

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Define model save path from config (with default)
tfidf_vectorizer_path = config.get('paths', 'tfidf_vectorizer_file', fallback='D:/RETRIEVAL-SHA-CHATBOT/models/tfidf_vectorizer.pkl')
sentence_tokens_path = config.get('paths', 'sentence_tokens_file', fallback='D:/RETRIEVAL-SHA-CHATBOT/models/sentence_tokens.pkl')

def load_sentence_tokens(file_path):
    """Loads the sentence tokens from a pickle file."""
    try:
        with open(file_path, "rb") as f:
            sentence_tokens = pickle.load(f)
        logging.info(f"Sentence tokens loaded successfully from: {file_path}")
        return sentence_tokens
    except FileNotFoundError:
        logging.error(f"Error: Sentence tokens file not found at {file_path}")
        return None
    except IOError as e:
        logging.error(f"Error loading sentence tokens: {e}")
        return None
    except pickle.PickleError as e:
        logging.error(f"Error unpickling sentence tokens: {e}")
        return None

def train_tfidf(sentence_tokens, save_path):
    """Trains the TF-IDF vectorizer and saves it."""
    if sentence_tokens:
        logging.info("Starting TF-IDF model training...")
        vectorizer = TfidfVectorizer()
        vectorizer.fit(sentence_tokens)
        logging.info("TF-IDF model training complete.")
        save_tfidf_model(vectorizer, save_path)
    else:
        logging.warning("No sentence tokens provided for TF-IDF training.")

def save_tfidf_model(vectorizer, file_path):
    """Saves the trained TF-IDF vectorizer to a pickle file."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            pickle.dump(vectorizer, f)
        logging.info(f"TF-IDF vectorizer saved successfully to: {file_path}")
    except IOError as e:
        logging.error(f"Error saving TF-IDF vectorizer: {e}")
    except pickle.PickleError as e:
        logging.error(f"Error pickling TF-IDF vectorizer: {e}")

if __name__ == "__main__":
    logging.info("Starting TF-IDF model training process...")
    sentence_tokens = load_sentence_tokens(sentence_tokens_path)
    if sentence_tokens:
        train_tfidf(sentence_tokens, tfidf_vectorizer_path)
    else:
        logging.error("TF-IDF model training failed due to issues with sentence tokens.")

#   training the chatbot model. Prepares data, vectorizes text, and saves trained models.

import pickle
import nltk
from nltk.tokenize import sent_tokenize
import logging
import os
import configparser  
# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')  # Create a config.ini file in the backend directory

# Define data and model paths from config (with defaults)
data_path = config.get('paths', 'data_file', fallback='D:/RETRIEVAL-SHA-CHATBOT/datasets/data.txt')
sentence_tokens_path = config.get('paths', 'sentence_tokens_file', fallback='D:/RETRIEVAL-SHA-CHATBOT/models/sentence_tokens.pkl')

def download_nltk_resources():
    """Downloads necessary NLTK resources if not already present."""
    try:
        sent_tokenize("This is a sentence.")
    except LookupError:
        logging.info("Downloading NLTK 'punkt' resource...")
        nltk.download('punkt')
        nltk.data.path.append(os.path.join(os.getcwd(), 'nltk_data'))  # Ensure NLTK can find the resource
        nltk.data.path.append(os.path.join(os.getcwd(), 'nltk_data', 'tokenizers'))
        nltk.download('punkt_tab')
        logging.info("NLTK 'punkt' resource downloaded.")

def load_data(file_path):
    """Loads text data from the specified file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text_data = f.read()
        logging.info(f"Data loaded successfully from: {file_path}")
        return text_data
    except FileNotFoundError:
        logging.error(f"Error: Data file not found at {file_path}")
        return None
    except IOError as e:
        logging.error(f"Error reading data file: {e}")
        return None

def tokenize_sentences(text):
    """Splits the text into sentences using NLTK."""
    if text:
        download_nltk_resources()
        sentence_tokens = sent_tokenize(text)
        logging.info(f"Text tokenized into {len(sentence_tokens)} sentences.")
        return sentence_tokens
    return []

def save_tokens(tokens, file_path):
    """Saves the sentence tokens to a pickle file."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure directory exists
        with open(file_path, "wb") as f:
            pickle.dump(tokens, f)
        logging.info(f"Sentence tokens saved successfully to: {file_path}")
    except IOError as e:
        logging.error(f"Error saving sentence tokens: {e}")

if __name__ == "__main__":
    logging.info("Starting training process...")
    text_data = load_data(data_path)
    if text_data:
        sentence_tokens = tokenize_sentences(text_data)
        if sentence_tokens:
            save_tokens(sentence_tokens, sentence_tokens_path)
            logging.info("Training complete!")
        else:
            logging.warning("No sentence tokens were generated.")
    else:
        logging.error("Training failed due to data loading issues.")
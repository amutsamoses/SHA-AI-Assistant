
# Specifically trains and saves the Word2Vec embeddings for response selection.
import nltk
import pickle
import logging
import os
import configparser
import gensim

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Define data and model paths from config (with defaults)
data_path = config.get('paths', 'data_file', fallback='D:/RETRIEVAL-SHA-CHATBOT/datasets/data.txt')
word2vec_model_path = config.get('paths', 'word2vec_model_file', fallback='D:/RETRIEVAL-SHA-CHATBOT/models/word2vec_model.pkl')

def download_nltk_resources():
    """Downloads necessary NLTK resources if not already present."""
    try:
        nltk.word_tokenize("example")
    except LookupError:
        logging.info("Downloading NLTK 'punkt' resource...")
        nltk.download('punkt')
        nltk.download('punkt_tab')
        logging.info("NLTK 'punkt' resource downloaded.")

def load_data(file_path):
    """Loads text data from the specified file."""
    try:
        with open(file_path, "r", errors="ignore") as f:
            raw_doc = f.read().lower()
        logging.info(f"Data loaded successfully from: {file_path}")
        return raw_doc
    except FileNotFoundError:
        logging.error(f"Error: Data file not found at {file_path}")
        return None
    except IOError as e:
        logging.error(f"Error reading data file: {e}")
        return None

def tokenize_words(text):
    """Tokenizes the text into words using NLTK."""
    if text:
        download_nltk_resources()
        word_tokens = nltk.word_tokenize(text)
        logging.info(f"Text tokenized into {len(word_tokens)} words.")
        return word_tokens
    return []

def train_word2vec_model(tokens, vector_size=100, window=5, min_count=1, workers=4):
    """Trains the Word2Vec model."""
    if tokens:
        logging.info("Starting Word2Vec model training...")
        model = gensim.models.Word2Vec([tokens], vector_size=vector_size, window=window, min_count=min_count, workers=workers)
        logging.info("Word2Vec model training complete.")
        return model
    else:
        logging.warning("No word tokens available for training Word2Vec model.")
        return None

def save_model(model, file_path):
    """Saves the trained Word2Vec model to a pickle file."""
    if model:
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "wb") as f:
                pickle.dump(model, f)
            logging.info(f"Word2Vec model saved successfully to: {file_path}")
        except IOError as e:
            logging.error(f"Error saving Word2Vec model: {e}")
    else:
        logging.warning("No Word2Vec model to save.")

if __name__ == "__main__":
    logging.info("Starting Word2Vec model training process...")
    raw_text = load_data(data_path)
    if raw_text:
        word_tokens = tokenize_words(raw_text)
        if word_tokens:
            word2vec_model = train_word2vec_model(word_tokens)
            if word2vec_model:
                save_model(word2vec_model, word2vec_model_path)
            else:
                logging.error("Word2Vec model training failed.")
        else:
            logging.warning("No word tokens were generated. Skipping Word2Vec training.")
    else:
        logging.error("Word2Vec model training failed due to data loading issues.")
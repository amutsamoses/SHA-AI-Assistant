# Implements TF-IDF & Word2Vec for retrieving the most relevant responses from the dataset.

import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import KeyedVectors
import logging
import configparser
import os

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')
models_dir = config.get('paths', 'models_dir', fallback='D:/RETRIEVAL-SHA-CHATBOT/models/')
tfidf_vectorizer_path = os.path.join(models_dir, "tfidf_vectorizer.pkl")
sentence_tokens_path = os.path.join(models_dir, "sentence_tokens.pkl")
word2vec_model_path = os.path.join(models_dir, "word2vec_model.bin")

# Load pre-trained models
try:
    with open(tfidf_vectorizer_path, "rb") as f:
        tfidf_vectorizer = pickle.load(f)
    logging.info(f"TF-IDF vectorizer loaded from: {tfidf_vectorizer_path}")
except FileNotFoundError:
    logging.error(f"Error: TF-IDF vectorizer file not found at {tfidf_vectorizer_path}")
    tfidf_vectorizer = None
except Exception as e:
    logging.error(f"Error loading TF-IDF vectorizer: {e}")
    tfidf_vectorizer = None

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
    word2vec = KeyedVectors.load_word2vec_format(word2vec_model_path, binary=True)
    logging.info(f"Word2Vec model loaded from: {word2vec_model_path}")
except FileNotFoundError:
    logging.error(f"Error: Word2Vec model file not found at {word2vec_model_path}")
    word2vec = None
except Exception as e:
    logging.error(f"Error loading Word2Vec model: {e}")
    word2vec = None

def get_response(user_query):
    """Retrieves the most relevant response using TF-IDF and Word2Vec."""
    if tfidf_vectorizer is None or not sentence_tokens or word2vec is None:
        return "Error: Chatbot models not loaded properly."

    query_vector_tfidf = tfidf_vectorizer.transform([user_query])
    tfidf_similarities = np.dot(query_vector_tfidf, tfidf_vectorizer.transform(sentence_tokens).T).toarray()[0]
    
    # get the most relevant response
    response_idx = tfidf_similarities.argmax()
    
    # check if the highest similarity is above a certain threshhold
    if tfidf_similarities[response_idx] > 0.2:
        return sentence_tokens[response_idx]
    else:
        return "I am sorry. Unable to understand you!"

# Data cleaning and text preprocessing functions (lemmatization, cleaning, spell correction, tokenization, stop removal


import nltk
import string
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from spellchecker import SpellChecker
import logging
import configparser

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Download NLTK resources if not already present
try:
    stopwords.words('english')
except LookupError:
    logging.info("Downloading NLTK 'stopwords'...")
    nltk.download('stopwords')
try:
    WordNetLemmatizer().lemmatize('testing')
except LookupError:
    logging.info("Downloading NLTK 'wordnet'...")
    nltk.download('wordnet')
try:
    word_tokenize("example")
except LookupError:
    logging.info("Downloading NLTK 'punkt'...")
    nltk.download('punkt')

# Initialize lemmatizer, stop words, and spell checker
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
spell = SpellChecker()

def expand_contractions(text):
    """Expands contractions in text."""
    contractions_dict = {
        "i'm": "i am",
        "you're": "you are",
        "he's": "he is",
        "she's": "she is",
        "it's": "it is",
        "we're": "we are",
        "they're": "they are",
        "i've": "i have",
        "you've": "you have",
        "he's": "he has",
        "she's": "she has",
        "we've": "we have",
        "they've": "they have",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "hasn't": "has not",
        "haven't": "have not",
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "cannot",
        "couldn't": "could not",
        "shouldn't": "should not",
        "mightn't": "might not",
        "mustn't": "must not",
        "wouldn't": "would not",
        "it's": "it is",
        "let's": "let us",
        "what's": "what is",
        "who's": "who is",
        "here's": "here is",
        "there's": "there is",
        "that's": "that is",
        "how's": "how is",
        "why's": "why is",
        "i'll": "i will",
        "you'll": "you will",
        "he'll": "he will",
        "she'll": "she will",
        "we'll": "we will",
        "they'll": "they will",
        "i'd": "i would",
        "you'd": "you would",
        "he'd": "he would",
        "she'd": "she would",
        "we'd": "we would",
        "they'd": "they would",
        "i'm": "i am",
        "you're": "you are",
        "he's": "he is"
        # Add more as needed
    }
    
    # Loop through the dictionary and replace contractions with their expanded forms
    words = text.split()
    expanded_text = " ".join([contractions_dict.get(word.lower(), word) for word in words])
    return expanded_text

def remove_special_characters(text):
    """Removes non-alphanumeric characters (excluding spaces) and digits."""
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    return text

def correct_spelling(words):
    """Corrects spelling errors in a list of words."""
    return [spell.correction(word) for word in words]

def lemmatize_words(words):
    """Lemmatizes a list of words."""
    return [lemmatizer.lemmatize(word) for word in words]

def remove_stopwords(words, custom_stopwords=None):
    """Removes stop words from a list of words."""
    if custom_stopwords is None:
        return [word for word in words if word not in stop_words]
    else:
        combined_stopwords = stop_words.union(set(custom_stopwords))
        return [word for word in words if word not in combined_stopwords]

def preprocess_text(text, expand=True, remove_special=True, correct=False, lemmatize=True, remove_stops=True, custom_stopwords=None):
    """
    Performs a comprehensive text preprocessing.

    Args:
        text (str): The input text.
        expand (bool): Whether to expand contractions.
        remove_special (bool): Whether to remove special characters and digits.
        correct (bool): Whether to perform spell correction.
        lemmatize (bool): Whether to lemmatize words.
        remove_stops (bool): Whether to remove stop words.
        custom_stopwords (list, optional): A list of additional stop words to remove.

    Returns:
        list: A list of preprocessed words.
    """
    if not isinstance(text, str):
        logging.warning(f"Input is not a string: {text}. Returning empty list.")
        return []

    text = text.lower()

    if expand:
        text = expand_contractions(text)

    if remove_special:
        text = remove_special_characters(text)

    words = word_tokenize(text)

    if correct:
        words = correct_spelling(words)

    if lemmatize:
        words = lemmatize_words(words)

    if remove_stops:
        words = remove_stopwords(words, custom_stopwords)

    return words

if __name__ == "__main__":
    # Example usage with different options
    sample_text = "This's a tset sentence with running words and 123 for preprocessing! How're you?"
    print(f"Original text: {sample_text}")

    # Default preprocessing
    processed_default = preprocess_text(sample_text)
    print(f"Default processed: {processed_default}")

    # Preprocessing with spell correction and without lemmatization
    processed_spell_corrected = preprocess_text(sample_text, correct=True, lemmatize=False)
    print(f"Spell corrected, no lemma: {processed_spell_corrected}")

    # Preprocessing with custom stop words
    custom_stops = ["test"]
    processed_custom_stops = preprocess_text(sample_text, custom_stopwords=custom_stops)
    print(f"With custom stops: {processed_custom_stops}")

    # Preprocessing with minimal steps
    processed_minimal = preprocess_text(sample_text, expand=False, remove_special=False, correct=False, lemmatize=False, remove_stops=False)
    print(f"Minimal processing: {processed_minimal}")

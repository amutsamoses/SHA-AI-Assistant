
# Utility functions for logging, helper methods, spell checking, and more

import logging
import datetime
import re
from spellchecker import SpellChecker
from typing import Optional
import os

# Initialize logging (configure only once at the application startup)
LOG_FILE = "chatbot.log"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
numeric_level = getattr(logging, LOG_LEVEL, logging.INFO)
logging.basicConfig(
    filename=LOG_FILE,
    level=numeric_level,
    format="%(asctime)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s",
    encoding="utf-8",  
)
logger = logging.getLogger(__name__)

# Initialize spell checker (can be a global instance)
spell = SpellChecker()

def log_query(user_id: int, query: str, response: str) -> None:
    """Logs chatbot interactions to a file."""
    logger.info(f"User ID: {user_id}, Query: '{query}', Response: '{response}'")

def correct_spelling(text: str) -> str:
    """Checks and corrects spelling in user input."""
    if not text:
        return ""
    words = text.split()
    corrected_words = [spell.correction(word) if spell.unknown([word]) else word for word in words]
    return " ".join(corrected_words)

def clean_text(text: str) -> str:
    """Cleans and normalizes user input."""
    if not text:
        return ""
    text = text.lower()  
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    return text.strip()

def get_current_timestamp() -> str:
    """Returns the current timestamp in UTC."""
    return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

def create_session_id(user_id: int, timestamp: datetime.datetime = None) -> str:
    """Creates a unique session ID for a user."""
    if timestamp is None:
        timestamp = datetime.datetime.utcnow()
    return f"user_{user_id}_{timestamp.strftime('%Y%m%d%H%M%S%f')}"

# Helper to safely convert string to integer
def safe_int_conversion(value: str) -> Optional[int]:
    """Safely converts a string to an integer, returns None if conversion fails."""
    try:
        return int(value)
    except ValueError:
        logger.warning(f"Failed to convert '{value}' to integer.")
        return None

# Basic rate limiting helper (can be expanded)
def is_rate_limited(user_id: int, action: str, limit: int, period: int = 60) -> bool:
    """
    Basic in-memory rate limiting. Consider a more robust solution for production.
    """
    if not hasattr(is_rate_limited, 'user_actions'):
        is_rate_limited.user_actions = {}

    now = datetime.datetime.utcnow().timestamp()
    key = (user_id, action)

    if key not in is_rate_limited.user_actions:
        is_rate_limited.user_actions[key] = []

    user_actions = is_rate_limited.user_actions[key]
    # Remove actions older than the rate limit period
    is_rate_limited.user_actions[key] = [t for t in user_actions if t > now - period]

    if len(is_rate_limited.user_actions[key]) >= limit:
        logger.warning(f"User {user_id} rate limited for action '{action}'.")
        return True

    is_rate_limited.user_actions[key].append(now)
    return False
# Chatbot logic API route for retrieval-based responses(handle user input)

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from fastapi import APIRouter, Depends, HTTPException, status
import os
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from backend.app.db import SessionLocal
from backend.app.dependencies import get_db
from backend.app.models import ChatHistory
from backend.ai.hybrid_model import hybrid_get_response
from backend.app.utils import log_query, correct_spelling, clean_text, logger
import logging

# Configure logging to capture important information
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter(prefix="/chat", tags=["Chatbot"])

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # Assuming you have a token URL defined

# async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, Config().JWT_SECRET_KEY, algorithms=[Config().ALGORITHM])
#         user_id: str = payload.get("sub")
#         if user_id is None:
#             raise credentials_exception
#         user = db.query(User).filter(User.id == int(user_id)).first()
#         if user is None:
#             raise credentials_exception
#         return user
#     except Exception:
#         raise credentials_exception

# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if not current_user.is_active:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
#     return current_user
        
# get response from the google gemini api
@router.post("")
async def chatbot_query(
    user_input: str, db: Session = Depends(get_db),
    # current_user: Optional[User] = Depends(get_current_active_user),  # Get authenticated user
    ):
    user_id = None # no authentication for now
    session_id = None
    
    # Ensure user input is valid
    if not user_input.strip():
        raise HTTPException(status_code=400, detail="User input cannot be empty")
    
    try:
        logger.info(f"User (Guest) query: '{user_input}'")
        
        # preprocess user input
        corrected_input = correct_spelling(user_input)
        cleaned_input = clean_text(corrected_input)
        logger.debug(f"Preprocessed input: '{cleaned_input}'")
        
        # get chatbot response from hybrid model
        bot_response = hybrid_get_response(cleaned_input)
        
        if not bot_response:
            logger.warning(f"Hybrid model retruned an empty response for the query: '{cleaned_input}'")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Chatbot failed to generate a response.",
            )
        
        #store the chat history
        chat_record = ChatHistory(
            user_id=user_id,
            query=user_input, # store the original input
            response=bot_response,
            session_id=session_id,
        )
        db.add(chat_record)
        db.commit()
        db.refresh(chat_record)
        logger.info(f"Chat interaction successfully saved to history (ID: {chat_record.id}).")
        
        # will not be executed as user_id is none
        if user_id:
            log_query(user_id, user_input, bot_response)
            
        return {"response": bot_response}
    
    except HTTPException as http_exc:
        raise http_exc
    except SQLAlchemyError as db_exc:
        db.rollback()
        logger.error(f"Database error during chat interaction: {db_exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save chat history due to a database error.",
        )
    except Exception as e:
        logger.error(f"An unexpected error occurred during chat processing: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing your request."
        )
            
            
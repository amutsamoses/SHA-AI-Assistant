# SHA API integration

 # # log the query to the database for analytics
        # log_query(user_id, session_id, user_input, bot_response)
        
        
    
        # google_gemini_api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
        
        # # handle missing api key
        # if not google_gemini_api_key:
        #     raise HTTPException(status_code=500, detail="GOOGLE_GEMINI_API_KEY not set")
        
        # url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={google_gemini_api_key}"
        
        # payload = {
        #     "contents": [{"parts": [{"text": user_input}]}],
        # }
        
        # try:
        #     response = requests.post(url, json=payload)
        #     response.raise_for_status() # raise httperror for bad response
        #     # type hinting for response
        #     response_json:Optional[dict] = response.json()
        #     # response = requests.post(url, json=payload).json()
        #     bot_response = response_json.get("candidates", [{}])[0].get("output", "I'm soory, I couldn't get that!!!")
            
        # except requests.exceptions.RequestException as e:
        #     raise HTTPException(status_code=500, detail=f"Failed to connect to Google Gemini API: {e}") # handle connection error
        
        
        
        # # Dependency to the database session
# # type hint  with sqlalchemy.orm session
# def get_db() -> Generator[Session, None, None]:
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
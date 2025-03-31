# API endpoints for chatbot analytics (e.g., usage metrics)
# track chatbot usage, logging user interaction and providing insights
# Total queries per user
# Most common questions asked
# Chatbot response times
# User engagement trends

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict, Any, Optional
from ..models import ChatHistory
from ..dependencies import get_db 
from ..utils import safe_int_conversion, logger 
from datetime import datetime, timedelta

router = APIRouter(prefix="/analytics", tags=["Analytics"])  
# Get Total Number of Queries
@router.get("/total_queries/", response_model=Dict[str, int])
def get_total_queries(db: Session = Depends(get_db)):
    try:
        total_queries = db.query(ChatHistory).count()
        return {"total_queries": total_queries}
    except SQLAlchemyError as e:
        logger.error(f"Database error while getting total queries: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

# Get Total Queries by User
@router.get("/queries_per_user/{user_id}", response_model=Dict[str, Any])
def get_queries_per_user(user_id: int, db: Session = Depends(get_db)):
    if not isinstance(user_id, int) and not user_id.isdigit():
        raise HTTPException(status_code=400, detail="Invalid user_id")
    user_id = safe_int_conversion(user_id)
    if user_id is None:
        raise HTTPException(status_code=400, detail="Invalid user_id format")
    try:
        user_queries = db.query(ChatHistory).filter(ChatHistory.user_id == user_id).count()
        return {"user_id": user_id, "total_queries": user_queries}
    except SQLAlchemyError as e:
        logger.error(f"Database error while getting queries for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

# Get Most Common Questions
@router.get("/common_questions/", response_model=Dict[str, List[Dict[str, Any]]])
def get_common_questions(limit: int = Query(default=5, le=10), db: Session = Depends(get_db)):
    try:
        common_questions = (
            db.query(ChatHistory.query, func.count(ChatHistory.query).label("count"))
            .group_by(ChatHistory.query)
            .order_by(func.count(ChatHistory.query).desc())
            .limit(limit)
            .all()
        )
        return {"common_questions": [{"question": q[0], "count": q[1]} for q in common_questions]}
    except SQLAlchemyError as e:
        logger.error(f"Database error while getting common questions: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

# Get User Engagement Over Time
@router.get("/user_engagement/", response_model=Dict[str, List[Dict[str, Any]]])
def get_user_engagement(db: Session = Depends(get_db), days: Optional[int] = Query(None, description="Number of past days to retrieve engagement data for")):
    try:
        query = db.query(func.date(ChatHistory.timestamp), func.count(ChatHistory.id))
        if days:
            cutoff = datetime.utcnow() - timedelta(days=days)
            query = query.filter(ChatHistory.timestamp >= cutoff)
        engagement_data = (
            query.group_by(func.date(ChatHistory.timestamp))
            .order_by(func.date(ChatHistory.timestamp))
            .all()
        )
        return {"engagement_trends": [{"date": str(e[0]), "queries": e[1]} for e in engagement_data]}
    except SQLAlchemyError as e:
        logger.error(f"Database error while getting user engagement data: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

# Get Average Chatbot Response Time
@router.get("/response_time/", response_model=Dict[str, Optional[float]])
def get_average_response_time(db: Session = Depends(get_db)):
    try:
        # Assuming 'timestamp' records the time the query was made.
        # To calculate response time, you'd need another field recording the response time.
        # For now, we'll just return the average query timestamp (which isn't a true response time).
        # Consider adding a 'response_timestamp' to your ChatHistory model.
        avg_query_timestamp = db.query(func.avg(func.extract('epoch', ChatHistory.timestamp))).scalar()
        return {"average_query_timestamp_epoch": avg_query_timestamp or 0}
    except SQLAlchemyError as e:
        logger.error(f"Database error while getting average response time: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

# Get Chatbot Response Time for a Specific User
@router.get("/response_time/{user_id}", response_model=Dict[str, Optional[float]])
def get_user_response_time(user_id: int, db: Session = Depends(get_db)):
    if not isinstance(user_id, int) and not user_id.isdigit():
        raise HTTPException(status_code=400, detail="Invalid user_id")
    user_id = safe_int_conversion(user_id)
    if user_id is None:
        raise HTTPException(status_code=400, detail="Invalid user_id format")
    try:
        # Same assumption as above regarding 'timestamp' not being the true response time.
        user_query_timestamp = (
            db.query(func.avg(func.extract('epoch', ChatHistory.timestamp)))
            .filter(ChatHistory.user_id == user_id)
            .scalar()
        )
        return {"user_id": user_id, "average_query_timestamp_epoch": user_query_timestamp or 0}
    except SQLAlchemyError as e:
        logger.error(f"Database error while getting response time for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
# Handles password hashing/verification and JWT token creation/handling
from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext

from backend.app.config import Config



# Load configuration from app.config
config = Config()

# Password hashing settings
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
ALGORITHM = config.ALGORITHM
SECRET_KEY = config.JWT_SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES

# Consistent function names and clear purpose
def get_password_hash(password: str) -> str:
    return PWD_CONTEXT.hash(password)

#  Consistent function names and clear purpose
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return PWD_CONTEXT.verify(plain_password, hashed_password)

#  Create access token with expiration
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ✅ Improvement: Function to decode JWT token and extract subject (e.g., email)
def decode_access_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        return email
    except jwt.PyJWTError:
        return None
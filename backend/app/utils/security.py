from fastapi import HTTPException, Security, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.config import get_settings
import time
from collections import defaultdict
from typing import Dict

settings = get_settings()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT config
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Security
security = HTTPBearer()

# Rate limiting storage (en producción usar Redis)
rate_limit_storage: Dict[str, list] = defaultdict(list)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate password hash"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Dependency to get current authenticated user"""
    token = credentials.credentials
    payload = verify_token(token)
    
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    
    return {"username": username}


def authenticate_user(username: str, password: str) -> bool:
    """Authenticate user with username and password"""
    # En producción, verificar contra base de datos
    if username == settings.admin_username and password == settings.admin_password:
        return True
    return False


def rate_limit_check(request: Request, max_per_minute: int = None, max_per_hour: int = None):
    """
    Rate limiting middleware
    En producción usar Redis para almacenamiento distribuido
    """
    if max_per_minute is None:
        max_per_minute = settings.rate_limit_per_minute
    if max_per_hour is None:
        max_per_hour = settings.rate_limit_per_hour
    
    # Get client IP
    client_ip = request.client.host
    current_time = time.time()
    
    # Clean old entries (older than 1 hour)
    rate_limit_storage[client_ip] = [
        timestamp for timestamp in rate_limit_storage[client_ip]
        if current_time - timestamp < 3600
    ]
    
    # Check rate limits
    recent_requests = rate_limit_storage[client_ip]
    
    # Requests in last minute
    requests_last_minute = sum(1 for t in recent_requests if current_time - t < 60)
    if requests_last_minute >= max_per_minute:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded: {max_per_minute} requests per minute"
        )
    
    # Requests in last hour
    if len(recent_requests) >= max_per_hour:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded: {max_per_hour} requests per hour"
        )
    
    # Add current request
    rate_limit_storage[client_ip].append(current_time)


def verify_chatwoot_webhook(request: Request, signature: str = None) -> bool:
    """Verify Chatwoot webhook signature"""
    if not settings.chatwoot_webhook_secret:
        return True  # Skip verification if no secret configured
    
    # TODO: Implement webhook signature verification
    # import hmac
    # import hashlib
    return True

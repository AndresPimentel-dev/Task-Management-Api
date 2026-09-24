from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.algorithm
TIME_TO_EXPIRE = settings.access_token_expire_minutes

def get_password_hash(plain_password: str):
    by_password = plain_password[:72].encode('utf-8')
    hashed = bcrypt.hashpw(by_password, bcrypt.gensalt())
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_password[:72].encode('utf-8'), hashed_password.encode('utf-8'))


def create_access_token(data: dict):
    to = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=TIME_TO_EXPIRE)
    to.update({"exp": expire})
    return jwt.encode(to, SECRET_KEY, ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
    except jwt.PyJWTError:
        return None
    return email
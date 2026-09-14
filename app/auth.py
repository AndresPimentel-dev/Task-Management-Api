import jwt
import bcrypt
from dotenv import load_dotenv
import os
from datetime import timedelta, datetime

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def get_password_hash(plain_password):
    by_password = plain_password[:72].encode('utf-8')
    hashed = bcrypt.hashpw(by_password, bcrypt.gensalt())
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_password[:72].encode('utf-8'), hashed_password.encode('utf-8'))


def create_access_token(data: dict):
    to = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to.update({"exp": expire})
    return jwt.encode(to, SECRET_KEY, ALGORITHM)
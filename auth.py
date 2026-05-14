from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, Request
from sqlalchemy.orm import Session
import bcrypt

from database import get_db
import models

SECRET_KEY = "nexoralab_secret_key_change_this_later"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


# ── PASSWORD FUNCTIONS ──


def hash_password(password: str) -> str:
    # Encode the password to bytes then hash it
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Check the plain password against the stored hash
    password_bytes = plain_password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)


# ── JWT TOKEN FUNCTIONS ──


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


# ── GET CURRENT LOGGED IN MEMBER ──


def get_current_member(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")

    if not token:
        return None

    payload = decode_access_token(token)

    if payload is None:
        return None

    email = payload.get("sub")

    if not email:
        return None

    member = db.query(models.Member).filter(models.Member.email == email).first()

    return member

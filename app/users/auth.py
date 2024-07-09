import datetime
import bcrypt
import jwt
from fastapi import HTTPException, Request

from app.config import settings


def create_jwt_token(data: dict):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data.update({"exp": expiration})
    return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_jwt_token(token: str):
    try:
        decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return decoded_data
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def cypher_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def check_password(password: str, hashed_password: str) -> bool:
    print(f"Password type: {type(password)}, value: {password}")
    print(f"Hashed Password type: {type(hashed_password)}, value: {hashed_password}")

    if hashed_password.startswith("b'") and hashed_password.endswith("'"):
        hashed_password = hashed_password[2:-1]

    password_bytes = password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')

    print(f"Password bytes type: {type(password_bytes)}, value: {password_bytes}")
    print(f"Hashed Password bytes type: {type(hashed_password_bytes)}, value: {hashed_password_bytes}")

    try:
        return bcrypt.checkpw(password_bytes, hashed_password_bytes)
    except ValueError as e:
        print(f"Error: {e}")
        return False


async def get_user_email_by_token(request: Request):
    token = request.cookies["token"]
    if not token:
        raise HTTPException(detail="No token provided", status_code=401)
    verified = verify_jwt_token(token)
    email = verified["sub"]
    return email

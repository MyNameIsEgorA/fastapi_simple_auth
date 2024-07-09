from fastapi import HTTPException

USER_ALREADY_EXISTS = HTTPException(status_code=401, detail="User with this email already exists")
USER_BAD_LOGIN = HTTPException(status_code=400, detail="Incorrect email or password")

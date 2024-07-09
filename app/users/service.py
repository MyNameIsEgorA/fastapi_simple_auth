from fastapi import HTTPException
from sqlalchemy import select, insert

from app.db import async_session_maker
from app.exceptions import USER_ALREADY_EXISTS, USER_BAD_LOGIN
from app.users.auth import cypher_password, check_password, create_jwt_token
from app.users.model import Users


class UserService:

    model = Users

    @classmethod
    async def create_user( cls, email: str, password: str) -> Users:
        async with async_session_maker() as session:
            await UserService.check_if_user_exists(email)
            await UserService.add_user(email, password)
            return await UserService.find_user_by_email(email)

    @classmethod
    async def add_user(cls, email: str, password: str):
        await UserService.check_if_user_exists(email)
        async with async_session_maker() as session:
            hashed_password = cypher_password(password)
            query = insert(cls.model).values(email=email, password=hashed_password)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def check_if_user_exists(cls, email: str) -> None:
        user = await UserService.find_user_by_email(email)
        if user:
            raise USER_ALREADY_EXISTS

    @classmethod
    async def find_user_by_email(cls, email):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.email == email)
            return (await session.execute(query)).scalar_one_or_none()

    @classmethod
    async def login_user(cls, email, password):
        user = await UserService.find_user_by_email(email)
        if not user:
            raise USER_BAD_LOGIN
        is_correct_password = check_password(password, user.password)
        if not is_correct_password:
            raise USER_BAD_LOGIN
        token = create_jwt_token({"sub": email})
        return token

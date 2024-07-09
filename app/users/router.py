from fastapi import APIRouter, Response, Request, Depends
from sqlalchemy import select

from app.db import async_session_maker
from app.users.DTO import UserRegisterDTO, UserLoginDTO
from app.users.auth import verify_jwt_token, get_user_email_by_token
from app.users.model import Users
from app.users.service import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_users():
    async with async_session_maker() as session:
        result = await session.execute(select(Users))
        return result.scalars().all()


@router.post("/register")
async def register_user(user: UserRegisterDTO):
    result = await UserService.create_user(email=user.email, password=user.password)
    return result


@router.post("/login")
async def login_user(response: Response, user: UserLoginDTO):
    result = await UserService.login_user(email=user.email, password=user.password)
    response.set_cookie(key="token", value=result, httponly=True)
    return {"detail": "Success"}


@router.get("/logout")
async def logout_user(response: Response):
    response.delete_cookie(key="token")
    return {"detail": "Success"}


@router.get("/me")
async def return_user(user_email: str = Depends(get_user_email_by_token)):
    return user_email

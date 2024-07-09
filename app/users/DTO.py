from pydantic import BaseModel, EmailStr


class UserRegisterDTO(BaseModel):
    email: EmailStr
    password: str


class UserLoginDTO(UserRegisterDTO):
    ...

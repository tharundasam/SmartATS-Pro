from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.models.user import RoleEnum


class UserRegisterRequest(BaseModel):
    full_name: str = Field(min_length=1, max_length=200)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: RoleEnum = RoleEnum.STUDENT


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    role: RoleEnum
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # allows UserOut.model_validate(sqlalchemy_user_instance)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

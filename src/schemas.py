from datetime import datetime, date

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator, Field

from src.utils.phone_number import PhoneNumber


# ------------------------------USER SCHEMA------------------------------
class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# ------------------------------CONTACT SCHEMA------------------------------
class ContactRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: date

    @field_validator("phone_number")
    def validate_phone_number(cls, v):
        if not PhoneNumber.is_valid_phone_number(v):
            raise HTTPException(status_code=400,
                                detail="Invalid phone number. The phone number must be in the format +380*******")
        return v


class ContactResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: date

# schemas/user.py
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List

from schemas.common import BaseOutput
from enums.gender import GENDER_EN_TO_KR, GENDER_KR_TO_EN, allowed_gender_en, allowed_gender_kr
from schemas.pet import Pet


class User(BaseModel):
    uid: str
    email: EmailStr
    nickname: str
    photoId: Optional[str] = None
    pets: Optional[List[Pet]] = None

    class Config:
        from_attributes = True
        use_enum_values = True

    def to_korean(self):
        return self

    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)


class CreateUserInput(BaseModel):
    uid: str
    email: EmailStr
    nickname: str
    photoId: Optional[str] = None


class CreateUserOutput(BaseOutput):
    user: Optional[User] = None
    token: Optional[dict] = None


class GetUserOutput(BaseOutput):
    user: Optional[User] = None


class UpdateUserInput(BaseModel):
    nickname: Optional[str] = None
    photoId: Optional[str] = None


class UpdateUserOutput(BaseOutput):
    user: Optional[User] = None


class DeleteUserOutput(BaseOutput):
    pass


class LoginUserInput(BaseModel):
    uid: str
    email: EmailStr


class LoginUserOutput(BaseOutput):
    user: Optional[User] = None
    token: Optional[dict] = None

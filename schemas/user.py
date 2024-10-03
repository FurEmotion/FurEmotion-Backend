# schemas/user.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from schemas.pet import Pet


class User(BaseModel):
    uid: str
    email: str
    nickname: str
    photoId: Optional[str]
    pets: Optional[List[Pet]]

    class Config:
        from_attributes = True
        use_enum_values = True

    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class Cry(BaseModel):
    id: int
    pet_id: int
    time: datetime
    state: str
    audioId: str
    predictMap: dict
    intensity: str
    duration: float

    class Config:
        from_attributes = True
        use_enum_values = True

    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)

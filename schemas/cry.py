# schemas/cry.py
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict
from datetime import datetime

from enums.cry_state import CRY_STATE_EN_TO_KR, CRY_STATE_KR_TO_EN
from enums.cry_intensity import CRY_INTENSITY_EN_TO_KR, CRY_INTENSITY_KR_TO_EN
from validator.cry import validate_state, validate_intensity, validate_duration, validate_time
from schemas.common import BaseOutput


class Cry(BaseModel):
    id: int
    pet_id: int
    time: datetime
    state: str
    audioId: str
    predictMap: Dict
    intensity: str
    duration: float

    class Config:
        from_attributes = True
        use_enum_values = True

    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)

    _validate_state = field_validator('state')(validate_state)
    _validate_intensity = field_validator('intensity')(validate_intensity)
    _validate_duration = field_validator('duration')(validate_duration)
    _validate_time = field_validator('time')(validate_time)

    def to_korean(self):
        """Convert state to Korean if it's in English."""
        if self.state in CRY_STATE_EN_TO_KR:
            self.state = CRY_STATE_EN_TO_KR[self.state]
        if self.intensity in CRY_INTENSITY_EN_TO_KR:
            self.intensity = CRY_INTENSITY_EN_TO_KR[self.intensity]
        return self


class CreateCryInput(BaseModel):
    pet_id: int
    time: datetime
    state: str
    audioId: str
    predictMap: dict
    intensity: Optional[str] = 'medium'
    duration: Optional[float] = 2.0

    _validate_state = field_validator('state')(validate_state)
    _validate_intensity = field_validator('intensity')(validate_intensity)
    _validate_duration = field_validator('duration')(validate_duration)
    _validate_time = field_validator('time')(validate_time)


class CreateCryOutput(BaseOutput):
    cry: Optional[Cry] = None


class GetCryOutput(BaseOutput):
    cry: Optional[Cry] = None


class GetPetCriesOutput(BaseOutput):
    cries: Optional[List[Cry]] = None


class UpdateCryInput(BaseModel):
    time: Optional[datetime] = None
    state: Optional[str] = None
    audioId: Optional[str] = None
    predictMap: Optional[Dict] = None
    intensity: Optional[str] = None
    duration: Optional[float] = None

    _validate_state = field_validator('state')(
        lambda cls, v: validate_state(v) if v is not None else v)
    _validate_intensity = field_validator('intensity')(
        lambda cls, v: validate_intensity(v) if v is not None else v)
    _validate_duration = field_validator('duration')(
        lambda cls, v: validate_duration(v) if v is not None else v)
    _validate_time = field_validator('time')(
        lambda cls, v: validate_time(v) if v is not None else v)


class UpdateCryOutput(BaseOutput):
    cry: Optional[Cry] = None


class DeleteCryOutput(BaseOutput):
    pass  # No additional fields needed


class GetCriesWithStateOutput(BaseOutput):
    cries: Optional[List[Cry]] = None


class GetCriesBetweenTimeOutput(BaseOutput):
    cries: Optional[List[Cry]] = None


class PredictCryOutput(BaseOutput):
    cry: Optional[Cry] = None

# schemas/pet.py
from pydantic import BaseModel, field_validator
from typing import Optional, List, TYPE_CHECKING

from schemas.cry import Cry
from enums.species import *


class Pet(BaseModel):
    id: int
    name: str
    gender: str
    age: int
    species: str
    sub_species: str
    user_id: str
    photo_id: Optional[str] = None
    cries: Optional[List[Cry]] = None

    class Config:
        from_attributes = True
        use_enum_values = True

    @field_validator('species')
    def validate_species(cls, v):
        allowed_species_en = [e.value for e in SpeciesEnum]
        allowed_species_kr = list(EN_TO_KR.values())
        if v not in allowed_species_en and v not in allowed_species_kr:
            raise ValueError(
                f"species must be one of {allowed_species_en} or their Korean equivalents {allowed_species_kr}"
            )
        return KR_TO_EN.get(v, v)

    def to_korean_species(self):
        """Convert species to Korean if it's in English."""
        if self.species in EN_TO_KR:
            self.species = EN_TO_KR[self.species]
        return self

    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)


class CreatePetInput(BaseModel):
    user_id: str
    name: str
    gender: str
    age: int
    species: str
    sub_species: str

    @field_validator('species')
    def validate_species(cls, v):
        allowed_species_en = [e.value for e in SpeciesEnum]
        allowed_species_kr = list(EN_TO_KR.values())
        if v not in allowed_species_en and v not in allowed_species_kr:
            raise ValueError(
                f"species must be one of {allowed_species_en} or their Korean equivalents {allowed_species_kr}"
            )
        return KR_TO_EN.get(v, v)


class CreatePetOutput(BaseModel):
    pet: Optional[Pet] = None
    success: bool
    message: str

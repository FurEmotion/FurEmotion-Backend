# schemas/pet.py
from pydantic import BaseModel, field_validator
from typing import Optional, List

from schemas.cry import Cry
from enums.species import *
from enums.pet_gender import *
from validator.species import *
from schemas.common import BaseOutput


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

    # Apply the reusable validators
    _validate_species = field_validator('species')(validate_species)
    _validate_gender = field_validator('gender')(validate_gender)
    _validate_age = field_validator('age')(validate_age)

    def to_korean(self):
        """Convert species to Korean if it's in English."""
        if self.species in SPECIES_EN_TO_KR:
            self.species = SPECIES_EN_TO_KR[self.species]
        if self.gender in PET_GENDER_EN_TO_KR:
            self.gender = PET_GENDER_EN_TO_KR[self.gender]
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

    # Apply the reusable validators
    _validate_species = field_validator('species')(validate_species)
    _validate_gender = field_validator('gender')(validate_gender)
    _validate_age = field_validator('age')(validate_age)


class CreatePetOutput(BaseOutput):
    pet: Optional[Pet] = None


class GetPetOutput(BaseOutput):
    pet: Optional[Pet] = None


class GetUserPetsOutput(BaseOutput):
    pets: Optional[List[Pet]] = None


class UpdatePetInput(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    species: Optional[str] = None
    sub_species: Optional[str] = None
    photo_id: Optional[str] = None

    # For optional fields, validate only if the value is not None
    _validate_species = field_validator('species')(
        lambda cls, v: validate_species(v) if v is not None else v)
    _validate_gender = field_validator('gender')(
        lambda cls, v: validate_gender(v) if v is not None else v)
    _validate_age = field_validator('age')(
        lambda cls, v: validate_age(v) if v is not None else v)


class UpdatePetOutput(BaseOutput):
    pet: Optional[Pet] = None


class DeletePetOutput(BaseOutput):
    pass  # No additional fields needed

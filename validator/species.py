from enums.species import *
from enums.pet_gender import *


def validate_species(v):
    if v not in allowed_species_en and v not in allowed_species_kr:
        raise ValueError(
            f"species must be one of {allowed_species_en} or their Korean equivalents {allowed_species_kr}"
        )
    return SPECIES_KR_TO_EN.get(v, v)


def validate_gender(v):
    if v not in allowed_petGender_en and v not in allowed_petGender_kr:
        raise ValueError(
            f"gender must be one of {allowed_petGender_en} or their Korean equivalents {allowed_petGender_kr}"
        )
    return PET_GENDER_KR_TO_EN.get(v, v)


def validate_age(v):
    if v < 0:
        raise ValueError("age must be a positive integer")
    return v

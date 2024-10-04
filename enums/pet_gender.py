# enums/pet_gender.py
from enum import Enum


class PetGender(str, Enum):
    MALE = 'male'
    FEMALE = 'female'
    SPAYED = 'spayed'


PET_GENDER_EN_TO_KR = {
    'male': '수컷',
    'female': '암컷',
    'spayed': '중성화됨',
}

PET_GENDER_KR_TO_EN = {v: k for k, v in PET_GENDER_EN_TO_KR.items()}

allowed_petGender_en = tuple(e.value for e in PetGender)
allowed_petGender_kr = tuple(PET_GENDER_EN_TO_KR.values())

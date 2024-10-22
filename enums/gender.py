# enums/gender.py
from enum import Enum


class Gender(str, Enum):
    MALE = 'male'
    FEMALE = 'female'
    UNKNOWN = 'unknown'


GENDER_EN_TO_KR = {
    'male': '남성',
    'female': '여성',
    'unknown': '비공개',
}

GENDER_KR_TO_EN = {v: k for k, v in GENDER_EN_TO_KR.items()}

allowed_gender_en = tuple(e.value for e in Gender)
allowed_gender_kr = tuple(GENDER_EN_TO_KR.values())

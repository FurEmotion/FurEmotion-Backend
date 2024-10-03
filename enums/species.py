# enums/species.py
from enum import Enum


class SpeciesEnum(str, Enum):
    DOG = 'dog'
    CAT = 'cat'


EN_TO_KR = {
    'dog': '개',
    'cat': '고양이',
}

KR_TO_EN = {v: k for k, v in EN_TO_KR.items()}

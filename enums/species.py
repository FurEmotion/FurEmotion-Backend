# enums/species.py
from enum import Enum


class SpeciesEnum(str, Enum):
    DOG = 'dog'
    CAT = 'cat'


SPECIES_EN_TO_KR = {
    'dog': '개',
    'cat': '고양이',
}

SPECIES_KR_TO_EN = {v: k for k, v in SPECIES_EN_TO_KR.items()}

allowed_species_en = tuple(e.value for e in SpeciesEnum)
allowed_species_kr = tuple(SPECIES_EN_TO_KR.values())

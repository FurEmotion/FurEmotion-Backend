# enums/cry_intensity.py
from enum import Enum


class CryIntensityEnum(str, Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'


CRY_INTENSITY_EN_TO_KR = {
    'low': '낮음',
    'medium': '중간',
    'high': '높음',
}

CRY_INTENSITY_KR_TO_EN = {v: k for k, v in CRY_INTENSITY_EN_TO_KR.items()}

allowed_cry_intensity_en = tuple(e.value for e in CryIntensityEnum)
allowed_cry_intensity_kr = tuple(CRY_INTENSITY_EN_TO_KR.values())

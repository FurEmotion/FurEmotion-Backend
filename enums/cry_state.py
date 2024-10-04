# enums/cry_state.py
from enum import Enum


class CryStateEnum(str, Enum):
    ANGER = 'anger'
    HUNGER = 'hunger'
    LONELY = 'lonely'


CRY_STATE_EN_TO_KR = {
    'anger': '화남',
    'hunger': '배고픔',
    'lonely': '외로움',
}

CRY_STATE_KR_TO_EN = {v: k for k, v in CRY_STATE_EN_TO_KR.items()}

allowed_cry_state_en = tuple(e.value for e in CryStateEnum)
allowed_cry_state_kr = tuple(CRY_STATE_EN_TO_KR.values())

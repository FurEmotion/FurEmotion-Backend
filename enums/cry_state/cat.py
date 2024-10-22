# enums/cry_state/cat.py
from enum import Enum


class CatCryStateEnum(str, Enum):
    HAPPY = 'happy'
    HUNGER = 'hunger'
    LONELY = 'lonely'


CAT_CRY_STATE_EN_TO_KR = {
    'happy': '행복함',
    'hunger': '배고픔',
    'lonely': '외로움',
}

CAT_CRY_STATE_KR_TO_EN = {v: k for k, v in CAT_CRY_STATE_EN_TO_KR.items()}

allowed_cat_cry_state_en = tuple(e.value for e in CatCryStateEnum)
allowed_cat_cry_state_kr = tuple(CAT_CRY_STATE_EN_TO_KR.values())

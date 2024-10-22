# enums/cry_state.py
from typing import Optional
from enums.cry_state.dog import *
from enums.cry_state.cat import *

CRY_STATE_EN_TO_KR = {**DOG_CRY_STATE_EN_TO_KR, **CAT_CRY_STATE_EN_TO_KR}
CRY_STATE_KR_TO_EN = {**DOG_CRY_STATE_KR_TO_EN, **CAT_CRY_STATE_KR_TO_EN}

allowed_cry_state_en = tuple(
    set(allowed_dog_cry_state_en + allowed_cat_cry_state_en))
allowed_cry_state_kr = tuple(
    set(allowed_dog_cry_state_kr + allowed_cat_cry_state_kr))


def check_right_cry_state(species: str, state: str) -> Optional[str]:
    if species == 'dog' and state not in allowed_dog_cry_state_en:
        return f"state must be one of {allowed_dog_cry_state_en} or their Korean equivalents {allowed_dog_cry_state_kr}"
    if species == 'cat' and state not in allowed_cat_cry_state_en:
        return f"state must be one of {allowed_cat_cry_state_en} or their Korean equivalents {allowed_cat_cry_state_kr}"
    return None

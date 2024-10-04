# validator/cry.py
from enums.cry_state import allowed_cry_state_en, allowed_cry_state_kr, CRY_STATE_KR_TO_EN
from enums.cry_intensity import allowed_cry_intensity_en, allowed_cry_intensity_kr, CRY_INTENSITY_KR_TO_EN
from datetime import datetime


def validate_state(v: str) -> str:
    if v not in allowed_cry_state_en and v not in allowed_cry_state_kr:
        raise ValueError(
            f"state must be one of {allowed_cry_state_en} or their Korean equivalents {allowed_cry_state_kr}"
        )
    return CRY_STATE_KR_TO_EN.get(v, v)


def validate_intensity(v: str) -> str:
    if v not in allowed_cry_intensity_en and v not in allowed_cry_intensity_kr:
        raise ValueError(
            f"intensity must be one of {allowed_cry_intensity_en} or their Korean equivalents {allowed_cry_intensity_kr}"
        )
    return CRY_INTENSITY_KR_TO_EN.get(v, v)


def validate_duration(v: float) -> float:
    if v <= 0:
        raise ValueError("duration must be a positive float")
    return v


def validate_time(v: datetime) -> datetime:
    return v

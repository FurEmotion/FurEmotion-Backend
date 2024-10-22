# enums/cry_state/dog.py
from enum import Enum


class DogCryStateEnum(str, Enum):
    ANGER = 'anger'
    PLAY = 'play'
    HAPPY = 'happy'
    SAD = 'sad'


DOG_CRY_STATE_EN_TO_KR = {
    'anger': '화남',
    'play': '놀고 싶음',
    'happy': '행복함',
    'sad': '슬픔',
}

DOG_CRY_STATE_KR_TO_EN = {v: k for k, v in DOG_CRY_STATE_EN_TO_KR.items()}

allowed_dog_cry_state_en = tuple(e.value for e in DogCryStateEnum)
allowed_dog_cry_state_kr = tuple(DOG_CRY_STATE_EN_TO_KR.values())

import os
from typing import Dict
import requests

from constants.path import ASSET_DIR
from enums.cry_state import allowed_cry_state_en, allowed_cat_cry_state_en, allowed_dog_cry_state_en
from core.env import env

class CryPredictService:
    def get_cry_classes(self, species):
        if species == 'dog':
            return allowed_dog_cry_state_en
        elif species == 'cat':
            return allowed_cat_cry_state_en
        else:
            return allowed_cry_state_en

    async def __call__(self, bytes: bytes, species: str, user_id: str) -> Dict[str, float]:
        url = env.get("AI_SERVER_API")

        files = {'file': ('file.wav', bytes, 'audio/wav')}
        data = {'user_id': user_id if user_id != "yTKx5CWGvLbjKVCRgve6K5Ne8cv2" else "owner", 'species': species}

        response = requests.post(url, files=files, data=data)
        response_json = response.json()
        response_json['sad'] = response_json.pop('whining')
        response_json['happy'] = response_json.pop('relax')
        response_json['anger'] = response_json.pop('hostile')

        return response_json

cry_predict = CryPredictService()
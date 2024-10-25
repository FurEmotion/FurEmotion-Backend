import numpy as np
import tensorflow as tf
import librosa
import os
from io import BytesIO
from skimage.transform import resize
from typing import Dict

from constants.path import ASSET_DIR
from enums.cry_state import allowed_cry_state_en, allowed_cat_cry_state_en, allowed_dog_cry_state_en

# os.environ['NUMBA_DISABLE_JIT'] = "1"


class CryPredictService:
    def __init__(self):
        self.model = tf.keras.models.load_model(
            os.path.join(ASSET_DIR, 'crnn.h5'))

    def get_cry_classes(self, species):
        if species == 'dog':
            return allowed_dog_cry_state_en
        elif species == 'cat':
            return allowed_cat_cry_state_en
        else:
            return allowed_cry_state_en

    async def get_input_vector_from_uploadfile(self, byteFile) -> np.ndarray:
        y, sr = librosa.load(BytesIO(byteFile), sr=16000)

        y = y[:(2 * sr)]

        mel_spec = librosa.feature.melspectrogram(
            y=y, sr=sr, n_mels=128, n_fft=2048, hop_length=501)
        mel_spec_dB = librosa.power_to_db(mel_spec, ref=np.max)
        RATIO = 862 / 64
        mel_spec_dB_resized = resize(mel_spec_dB, (mel_spec_dB.shape[0], mel_spec_dB.shape[1] * RATIO),
                                     anti_aliasing=True, mode='reflect')
        mel_spec_dB_stacked = np.stack([mel_spec_dB_resized] * 3, axis=-1)
        return mel_spec_dB_stacked[np.newaxis, ]

    async def get_predict_class(self, input_vector, species: str):
        classes = self.get_cry_classes(species)
        predictions = self.model.predict(input_vector)[0]
        predictMap = {}
        for i in range(len(classes)):
            predictMap[classes[i]] = round(float(predictions[i]), 4)
        return dict(sorted(predictMap.items(), key=lambda item: item[1], reverse=True))

    async def __call__(self, bytes: bytes, species: str) -> Dict[str, float]:
        input_vector = await self.get_input_vector_from_uploadfile(bytes)
        predictMap = await self.get_predict_class(input_vector, species)
        return predictMap


cry_predict = CryPredictService()

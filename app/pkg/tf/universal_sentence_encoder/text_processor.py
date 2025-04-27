import tensorflow_hub as hub
import numpy as np
import tensorflow_text
from app.internal.config import USE_MODEL_URL


class TextProcessor:
    def __init__(self):
        self.embed = hub.load(USE_MODEL_URL)

    def process_text(self, sentence: str) -> list:
        embedding = self.embed(sentence)['outputs'][0]
        return np.asarray(embedding).tolist()

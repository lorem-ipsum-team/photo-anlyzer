import tensorflow_hub as hub
import numpy as np
import tensorflow_text
import fasttext
from app.internal.config import USE_MODEL_URL


class TextProcessor:
    def __init__(self):
        self.model = fasttext.load_model('cc.ru.300.bin')
        self.embed = hub.load(USE_MODEL_URL)

    def process_text(self, sentence: str) -> list:
        sentence = sentence.replace('\n', ' ')
        embedding = self.model.get_sentence_vector(sentence)
        return embedding.tolist()

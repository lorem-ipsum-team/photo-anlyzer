"""This module downloads universal sentence encoder model"""
import tensorflow_hub as hub
import tensorflow_text
from app.internal.config import USE_MODEL_URL

embed = hub.load(USE_MODEL_URL)

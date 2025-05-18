import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Главное не победа а участие


RABBITMQ_URL = os.getenv('RABBITMQ_URL')
PHOTO_QUEUE_NAME = os.getenv('PHOTO_QUEUE_NAME')
DESCRIPTION_QUEUE_NAME = os.getenv('DESCRIPTION_QUEUE_NAME')
USERS_QUEUE_NAME = os.getenv('USERS_QUEUE_NAME')
SWIPES_QUEUE_NAME = os.getenv('SWIPES_QUEUE_NAME')

DATABASE_URL = os.getenv('DATABASE_URL')

USE_MODEL_URL = 'https://tfhub.dev/google/universal-sentence-encoder-multilingual-large/2'

PHOTO_PREF_ADJ_RATE = float(os.getenv('PHOTO_PREF_ADJ_RATE'))
TAGS_PREF_ADJ_RATE = float(os.getenv('TAGS_PREF_ADJ_RATE'))

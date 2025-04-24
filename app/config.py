import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Главное не победа а участие


RABBITMQ_URL = os.getenv('RABBITMQ_URL')
PHOTO_QUEUE_NAME = os.getenv('PHOTO_QUEUE_NAME')
DESCRIPTION_QUEUE_NAME = os.getenv('DESCRIPTION_QUEUE_NAME')

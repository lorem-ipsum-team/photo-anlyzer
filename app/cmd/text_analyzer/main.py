import asyncio
from pydantic import ValidationError
from app.config import RABBITMQ_URL, DESCRIPTION_QUEUE_NAME
from app.internal.model.text import Text
from app.internal.consumer import text_consumer
from app.pkg.logging.logger import log_error
from app.pkg.rabbitmq import RabbitmqClient


async def main():
    async with RabbitmqClient(RABBITMQ_URL, DESCRIPTION_QUEUE_NAME) as client:
        async for text_data in client.data_iter():
            try:
                text = Text.model_validate(text_data)
                await text_consumer.consume_text(text)
            except ValidationError:
                log_error("JSON Body cannot be processed as text data")
            except Exception as e:
                log_error(str(e))

if __name__ == '__main__':
    asyncio.run(main())

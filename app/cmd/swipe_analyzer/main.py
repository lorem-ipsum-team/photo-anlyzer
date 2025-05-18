import asyncio
from pydantic import ValidationError
from app.internal.config import RABBITMQ_URL, SWIPES_QUEUE_NAME
from app.internal.model.swipe import Swipe
from app.internal.consumer import swipe_consumer
from app.pkg.logging.logger import log_error
from app.pkg.rabbitmq import RabbitmqClient


async def main():
    async with RabbitmqClient(RABBITMQ_URL, SWIPES_QUEUE_NAME) as client:
        async for swipe_data in client.data_iter():
            try:
                swipe = Swipe.model_validate(swipe_data)
                await swipe_consumer.consume_swipe(swipe)
            except ValidationError:
                log_error("JSON Body cannot be processed as photo data")
            except Exception as e:
                log_error(str(e))


if __name__ == '__main__':
    asyncio.run(main())

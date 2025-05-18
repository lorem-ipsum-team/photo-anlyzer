import asyncio
from pydantic import ValidationError
from app.internal.config import RABBITMQ_URL, USERS_QUEUE_NAME
from app.internal.model.user import User
from app.internal.consumer import user_consumer
from app.pkg.logging.logger import log_error
from app.pkg.rabbitmq import RabbitmqClient


async def main():
    async with RabbitmqClient(RABBITMQ_URL, USERS_QUEUE_NAME) as client:
        async for user_data in client.data_iter():
            try:
                user = User.model_validate(user_data)
                await user_consumer.consume_user(user)
            except ValidationError:
                log_error("JSON Body cannot be processed as photo data")
            except Exception as e:
                log_error(str(e))


if __name__ == '__main__':
    asyncio.run(main())

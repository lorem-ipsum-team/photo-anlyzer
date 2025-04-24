import json
import aio_pika
from app.pkg.logging import log_error


class RabbitmqClient:
    def __init__(self, url: str, queue: str):
        self._url = url
        self._queue_name = queue
        self._connection = None
        self._channel = None
        self._queue = None

    async def __aenter__(self) -> "RabbitmqClient":
        self._connection = await aio_pika.connect_robust(self._url)
        self._channel = await self._connection.channel()
        self._queue = await self._channel.declare_queue(self._queue_name)
        return self

    async def __aexit__(self, *args) -> None:
        await self._channel.close()
        await self._connection.close()

    async def data_iter(self):
        async with self._queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    try:
                        data = json.loads(message.body)
                        yield data
                    except json.JSONDecodeError:
                        log_error("Failed to decode message body as JSON")

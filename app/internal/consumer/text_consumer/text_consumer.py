import asyncio
from app.internal.model.text import Text
from app.pkg.pytorch.bert.text_processor import TextProcessor

processor = TextProcessor()


def process_text(text: Text):
    return processor.process_text(text.description)


async def consume_text(text: Text):
    loop = asyncio.get_event_loop()
    tags = await loop.run_in_executor(None, process_text, text)

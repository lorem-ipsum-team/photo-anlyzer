import asyncio
from app.internal.entity.userdata import UserDescription
from app.internal.model.text import Text
from app.internal.service.description_repository import DescriptionRepository
from app.pkg.asyncpg.database import async_session, AsyncSession
from app.pkg.tf.universal_sentence_encoder.text_processor import TextProcessor

processor = TextProcessor()


def process_text(text: Text):
    return processor.process_text(text.tags)


async def consume_text(text: Text):
    loop = asyncio.get_event_loop()
    tags = await loop.run_in_executor(None, process_text, text)

    async with async_session() as session:
        session: AsyncSession
        descriptions = DescriptionRepository()
        uuid = text.user_id

        item = await descriptions.get_by_id(uuid, session)

        if item is None:
            item = UserDescription(
                id=uuid,
                tags=tags
            )

            session.add(item)

        item.tags = tags
        await session.commit()

from uuid import UUID
from sqlalchemy import select
from app.internal.entity.userdata import UserDescription
from app.pkg.asyncpg import AsyncSession


class DescriptionRepository:
    async def get_by_id(self, id: UUID, db: AsyncSession):
        query = select(UserDescription)\
            .where(UserDescription.id == id)\
            .limit(1)

        scalars = await db.scalars(query)
        return scalars.one_or_none()

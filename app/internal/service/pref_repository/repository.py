from uuid import UUID
from sqlalchemy import select
from app.internal.entity.userdata import UserPreference
from app.pkg.asyncpg import AsyncSession


class UserPrefRepository:
    async def get_by_id(self, id: UUID, db: AsyncSession):
        query = select(UserPreference)\
            .where(UserPreference.id == id)\
            .limit(1)

        scalars = await db.scalars(query)
        return scalars.one_or_none()

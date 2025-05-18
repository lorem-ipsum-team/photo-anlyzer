import datetime
import app.internal.model.user as model
import app.internal.entity.userdata as entity
from app.internal.service.user_repository import UserRepository
from app.pkg.asyncpg import async_session, AsyncSession


def model_to_entity(ent: entity.User, mod: model.User):
    ent.gender = mod.gender.lower() == 'male'
    ent.birthday = datetime.datetime\
        .strptime(mod.birth_date, '%d/%m/%Y').date()


async def consume_user(user: model.User):
    async with async_session() as session:
        session: AsyncSession
        repository = UserRepository()
        item = await repository.get_by_id(user.user_id, session)

        if item is None:
            item = entity.User(
                id=user.user_id
            )

            session.add(item)

        model_to_entity(item, user)
        await session.commit()

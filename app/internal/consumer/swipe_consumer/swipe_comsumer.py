import numpy as np
from app.internal.entity.userdata import UserPreference
from app.internal.model.swipe import Swipe
from app.internal.service.photo_repository import PhotoRepository
from app.internal.service.description_repository import DescriptionRepository
from app.internal.service.pref_repository import UserPrefRepository
from app.internal.config import PHOTO_PREF_ADJ_RATE, TAGS_PREF_ADJ_RATE
from app.pkg.asyncpg import async_session, AsyncSession


def adjust_pref_vector(pref_vector, target_vector, like: bool, rate: float):
    diff = np.subtract(target_vector, pref_vector)
    k = rate if like else -rate
    return k * diff


def out_of_range(vector) -> bool:
    return (np.min(vector) < -1) or (np.max(vector) > 1)


def clip_range(vector):
    return np.clip(vector, -1, 1)


def validate_prefs(pref: UserPreference):
    if out_of_range(pref.photo):
        pref.photo = clip_range(pref.photo)

    if out_of_range(pref.tags):
        pref.tags = clip_range(pref.tags)


async def consume_swipe(swipe: Swipe):
    async with async_session() as session:
        session: AsyncSession
        photos = PhotoRepository()
        tags = DescriptionRepository()
        user_prefs = UserPrefRepository()

        target_photo = await photos.get_by_id(swipe.target, session)
        target_tags = await tags.get_by_id(swipe.target, session)
        prefs = await user_prefs.get_by_id(swipe.init, session)

        if target_photo is None:
            raise Exception(f"Target ({swipe.target}) photo not found")

        if target_tags is None:
            raise Exception(f"Target ({swipe.target}) tags not found")

        if prefs is None:
            prefs = UserPreference(
                id=swipe.init,
                photo=[0]*len(target_photo.photo),
                tags=[0]*len(target_tags.tags)
            )

            session.add(prefs)
            await session.flush()

        prefs.photo = prefs.photo + adjust_pref_vector(
            prefs.photo, target_photo.photo, swipe.like, PHOTO_PREF_ADJ_RATE)

        prefs.tags = prefs.tags + adjust_pref_vector(
            prefs.tags, target_tags.tags, swipe.like, TAGS_PREF_ADJ_RATE)

        validate_prefs(prefs)
        await session.commit()

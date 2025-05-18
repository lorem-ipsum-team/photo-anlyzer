from uuid import UUID
from pydantic import BaseModel


class Swipe(BaseModel):
    init: UUID
    target: UUID
    like: bool

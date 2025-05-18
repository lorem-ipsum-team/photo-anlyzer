from uuid import UUID
from pydantic import BaseModel


class Text(BaseModel):
    user_id: UUID
    tags: str

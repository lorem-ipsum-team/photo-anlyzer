from pydantic import BaseModel


class Text(BaseModel):
    user_id: str
    description: str

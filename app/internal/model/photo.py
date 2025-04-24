from pydantic import BaseModel


class Photo(BaseModel):
    user_id: str
    image_url: str

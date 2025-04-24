from pydantic import Base64Str, BaseModel


class Photo(BaseModel):
    user_id: str
    image_base64: str

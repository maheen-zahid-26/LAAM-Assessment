import uuid

from pydantic import BaseModel, ConfigDict


class AlternativeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    brand: str
    price: float
    image_url: str | None
    size_available: bool

from uuid import UUID

from pydantic import BaseModel


class BodyCategoryCreate(BaseModel):
    name: str


class BodyCategoryUpdate(BaseModel):
    name: str


class BodyCategoryResponse(BaseModel):
    id: UUID
    name: str

    model_config = {"from_attributes": True}

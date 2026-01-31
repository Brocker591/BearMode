from uuid import UUID

from pydantic import BaseModel


class ProfileCreate(BaseModel):
    name: str


class ProfileUpdate(BaseModel):
    name: str | None = None


class ProfileResponse(BaseModel):
    id: UUID
    name: str

    model_config = {"from_attributes": True}

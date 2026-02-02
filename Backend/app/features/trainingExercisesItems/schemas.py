from uuid import UUID

from pydantic import BaseModel


class TrainingExercisesItemCreate(BaseModel):
    description: str
    video_url: str | None = None


class TrainingExercisesItemUpdate(BaseModel):
    description: str | None = None
    video_url: str | None = None


class TrainingExercisesItemResponse(BaseModel):
    id: UUID
    description: str
    video_url: str | None = None

    model_config = {"from_attributes": True}

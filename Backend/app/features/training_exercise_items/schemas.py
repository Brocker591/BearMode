from uuid import UUID

from pydantic import BaseModel


class TrainingExerciseItemCreate(BaseModel):
    description: str
    video_url: str | None = None


class TrainingExerciseItemUpdate(BaseModel):
    id: UUID
    description: str
    video_url: str | None = None


class TrainingExerciseItemResponse(BaseModel):
    id: UUID
    description: str
    video_url: str | None = None

    model_config = {"from_attributes": True}

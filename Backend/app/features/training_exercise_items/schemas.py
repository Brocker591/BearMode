from uuid import UUID

from pydantic import BaseModel


from app.features.body_category.schemas import BodyCategoryResponse

class TrainingExerciseItemCreate(BaseModel):
    description: str
    video_url: str | None = None
    body_category_id: UUID


class TrainingExerciseItemUpdate(BaseModel):
    id: UUID
    description: str
    video_url: str | None = None
    body_category_id: UUID


class TrainingExerciseItemResponse(BaseModel):
    id: UUID
    description: str
    video_url: str | None = None
    body_category: BodyCategoryResponse

    model_config = {"from_attributes": True}

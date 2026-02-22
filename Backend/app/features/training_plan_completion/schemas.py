from uuid import UUID
from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class TrainingPlanCompletion(BaseModel):
    id: UUID
    profile_id: UUID
    training_plan_id: UUID
    training_plan_name: str
    count_completed_exercises: int
    count_open_exercises: int
    training_day: date | None = None

    model_config = ConfigDict(from_attributes=True)

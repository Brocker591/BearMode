from uuid import UUID
from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class TrainingExerciseCompletion(BaseModel):
    id: UUID
    profile_id: UUID
    training_plan_id: UUID
    exercise_id: UUID
    order: int
    equipment: str | None = None
    reps: int = 1
    break_time_seconds: int
    training_exercise_description: str
    training_exercise_video_url: str | None = None
    training_day: date | None = None

    model_config = ConfigDict(from_attributes=True)

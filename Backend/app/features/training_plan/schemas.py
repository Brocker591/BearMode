from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TrainingExerciseCreate(BaseModel):
    order: int
    equipment: str | None = None
    sets: int = 1
    reps: int = 1
    break_time_seconds: int
    training_exercise_item_id: UUID

    model_config = ConfigDict(from_attributes=True)


class TrainingExerciseUpdate(TrainingExerciseCreate):
    id: UUID
    profile_id: UUID
    training_plan_id: UUID

    model_config = ConfigDict(from_attributes=True)


class TrainingPlanCreate(BaseModel):
    name: str
    profile_id: UUID
    training_exercises: list[TrainingExerciseCreate]

    model_config = ConfigDict(from_attributes=True)


class TrainingPlanUpdate(BaseModel):
    id: UUID
    name: str
    profile_id: UUID
    training_exercises: list[TrainingExerciseCreate]

    model_config = ConfigDict(from_attributes=True)


class TrainingExerciseItemResponse(BaseModel):
    id: UUID
    description: str
    video_url: str | None = None

    model_config = ConfigDict(from_attributes=True)


class TrainingExerciseResponse(BaseModel):
    id: UUID
    order: int
    equipment: str | None = None
    sets: int = 1
    reps: int = 1
    break_time_seconds: int
    training_exercise_item: TrainingExerciseItemResponse

    model_config = ConfigDict(from_attributes=True)


class TrainingPlanResponse(BaseModel):
    id: UUID
    name: str
    profile_id: UUID
    exercises: list[TrainingExerciseResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)

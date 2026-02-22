from uuid import UUID
from datetime import datetime, date
from pydantic import BaseModel, ConfigDict


class ProfileSync(BaseModel):
    id: UUID
    name: str
    emoji: str | None = None
    model_config = ConfigDict(from_attributes=True)


class BodyCategorySync(BaseModel):
    id: UUID
    name: str
    model_config = ConfigDict(from_attributes=True)


class TrainingExerciseItemSync(BaseModel):
    id: UUID
    description: str
    video_url: str | None = None
    body_category_id: UUID
    model_config = ConfigDict(from_attributes=True)


class TrainingPlanSync(BaseModel):
    id: UUID
    name: str
    profile_id: UUID
    model_config = ConfigDict(from_attributes=True)


class TrainingExerciseSync(BaseModel):
    id: UUID
    training_plan_id: UUID
    order: int
    equipment: str | None = None
    sets: int
    reps: int
    break_time_seconds: int
    training_exercise_item_id: UUID
    model_config = ConfigDict(from_attributes=True)


class TrainingPlanCompletionSync(BaseModel):
    id: UUID
    profile_id: UUID
    training_plan_id: UUID
    training_plan_name: str
    count_completed_exercises: int
    count_open_exercises: int
    created_at: datetime
    training_day: date
    model_config = ConfigDict(from_attributes=True)


class TrainingExerciseCompletionSync(BaseModel):
    id: UUID
    profile_id: UUID
    training_plan_id: UUID
    exercise_id: UUID
    exercise_description: str
    exercise_video_url: str | None = None
    body_category_id: UUID | None = None
    body_category_name: str | None = None
    order: int
    equipment: str | None = None
    reps: int
    break_time_seconds: int
    created_at: datetime
    training_day: date
    model_config = ConfigDict(from_attributes=True)


class DataSyncExport(BaseModel):
    profiles: list[ProfileSync]
    body_categories: list[BodyCategorySync]
    training_exercise_items: list[TrainingExerciseItemSync]
    training_plans: list[TrainingPlanSync]
    training_exercises: list[TrainingExerciseSync]
    training_plan_completions: list[TrainingPlanCompletionSync]
    training_exercise_completions: list[TrainingExerciseCompletionSync]

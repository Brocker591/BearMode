from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TrainingExerciseItemLink(BaseModel):
    item_id: UUID | None = None
    item_description: str | None = None
    video_url: str | None = None
    
    model_config = ConfigDict(from_attributes=True)


class TrainingExerciseBase(BaseModel):
    order: int
    equipment: str | None = Field(None, alias="Equipment")
    sets: int | None = Field(None, alias="Sets")
    reps: int | None = Field(None, alias="Reps")
    break_time_seconds: int | None = None


class TrainingExerciseCreate(TrainingExerciseBase):
    training_exercise_item: TrainingExerciseItemLink | None = None
    # Alternatively accept ID directly if the item already exists
    training_exercise_item_id: UUID | None = None

    @field_validator('sets', 'reps', mode='before')
    @classmethod
    def set_default_to_one_if_none_or_invalid(cls, v: int | None) -> int:
        if v is None or v < 1:
            return 1
        return v


    # Helper validator or logic in service/router might be needed 
    # if the user passes the nested object but we only need the ID.
    # The prompt says: "Das Objekt training_exercises_item wird schon angelegt... Man kann auch hier nur die Id speichern"


class TrainingExerciseResponse(TrainingExerciseBase):
    id: UUID = Field(..., serialization_alias="exercise_id")
    
    training_exercise_item: TrainingExerciseItemLink | None = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class TrainingPlanCreate(BaseModel):
    name: str
    profile_id: UUID
    training_exercises: list[TrainingExerciseCreate] = []


class TrainingPlanUpdate(BaseModel):
    name: str | None = None
    profile_id: UUID | None = None
    training_exercises: list[TrainingExerciseCreate] | None = None


class TrainingPlanResponse(BaseModel):
    id: UUID
    name: str
    profile_id: UUID
    training_exercises: list[TrainingExerciseResponse] = Field([], validation_alias="exercises")

    model_config = ConfigDict(from_attributes=True)

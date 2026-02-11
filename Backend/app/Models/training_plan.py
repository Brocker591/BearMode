import uuid
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.Models.training_exercise_item import TrainingExerciseItem
from app.Models.profile import Profile

from app.infrastructure.database import Base


class TrainingPlan(Base):
    __tablename__ = "training_plans"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=False)

    profile: Mapped["Profile"] = relationship(
        "Profile", back_populates="training_plans")

    # Relationships
    exercises: Mapped[list["TrainingExercise"]] = relationship("TrainingExercise", back_populates="training_plan", cascade="all, delete-orphan", lazy="selectin",  # Eager load exercises often
                                                               )


class TrainingExercise(Base):
    __tablename__ = "training_exercises"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    training_plan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("training_plans.id"), nullable=False
    )
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment: Mapped[str] = mapped_column(String(255), nullable=True)
    sets: Mapped[int] = mapped_column(Integer, nullable=False)
    reps: Mapped[int] = mapped_column(Integer, nullable=False)
    break_time_seconds: Mapped[int] = mapped_column(Integer, nullable=False)

    training_exercise_item_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("training_exercise_items.id"), nullable=False
    )

    # Relationships
    training_plan: Mapped["TrainingPlan"] = relationship(
        "TrainingPlan", back_populates="exercises"
    )
    training_exercise_item: Mapped["TrainingExerciseItem"] = relationship(
        "TrainingExerciseItem", lazy="selectin"
    )

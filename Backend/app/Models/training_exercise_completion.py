import uuid
from datetime import datetime, date
from venv import create
from sqlalchemy import ForeignKey, Integer, String, DateTime, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship


from app.infrastructure.database import Base


class TrainingExerciseCompletion(Base):
    __tablename__ = "training_exercise_completions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=False
    )
    training_plan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("training_plans.id"), nullable=False
    )
    exercise_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("training_exercises.id"), nullable=False
    )
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment: Mapped[str] = mapped_column(String(255), nullable=True)
    reps: Mapped[int] = mapped_column(Integer, nullable=False)
    break_time_seconds: Mapped[int] = mapped_column(Integer, nullable=False)
    training_exercise_description: Mapped[str] = mapped_column(
        String(255), nullable=False)
    training_exercise_video_url: Mapped[str] = mapped_column(
        String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(),
        nullable=False
    )
    training_day: Mapped[date] = mapped_column(Date, nullable=False)

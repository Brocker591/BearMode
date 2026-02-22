import uuid
from datetime import datetime, date
from sqlalchemy import ForeignKey, Integer, String, DateTime, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base


class TrainingPlanCompletion(Base):
    __tablename__ = "training_plan_completions"

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
    training_plan_name: Mapped[str] = mapped_column(String(255), nullable=False)
    count_completed_exercises: Mapped[int] = mapped_column(Integer, nullable=False)
    count_open_exercises: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(),
        nullable=False
    )
    training_day: Mapped[date] = mapped_column(Date, nullable=False)

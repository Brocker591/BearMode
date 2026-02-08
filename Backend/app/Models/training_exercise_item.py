import uuid
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database import Base


class TrainingExerciseItem(Base):
    __tablename__ = "training_exercise_items"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    description: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False)
    video_url: Mapped[str | None] = mapped_column(String(1200), nullable=True)

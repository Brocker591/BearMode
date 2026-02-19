import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
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

    body_category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("body_categories.id"),
        nullable=False
    )

    body_category: Mapped["BodyCategory"] = relationship(back_populates="training_exercise_items")

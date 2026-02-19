import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.Models.training_plan import TrainingPlan
from app.infrastructure.database import Base

if TYPE_CHECKING:
    from app.Models.training_exercise_item import TrainingExerciseItem


class BodyCategory(Base):
    __tablename__ = "body_categories"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    training_exercise_items: Mapped[list["TrainingExerciseItem"]] = relationship(back_populates="body_category")



# infrastructure/persistence/models.py

from datetime import date, datetime
from uuid import UUID, uuid4

from sqlalchemy import String, Date, SmallInteger, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from Infrastructure.database import Base


class ParticipantModel(Base):
    __tablename__ = "participants"

    participant_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    subject_id: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    study_group: Mapped[str] = mapped_column(String(20), nullable=False)
    enrollment_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    age: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class UserModel(Base):
    __tablename__ = "users"

    user_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
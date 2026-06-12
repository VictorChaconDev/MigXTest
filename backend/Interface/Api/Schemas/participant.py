from datetime import date
from typing import Dict
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

from Domain.ValueObjects.gender import Gender
from Domain.ValueObjects.participant_status import ParticipantStatus
from Domain.ValueObjects.study_group import StudyGroup


class ParticipantCreateSchema(BaseModel):
    subject_id: str = Field(..., max_length=20)
    study_group: StudyGroup
    enrollment_date: date
    status: ParticipantStatus
    age: int = Field(..., ge=0, le=130)
    gender: Gender


class ParticipantUpdateSchema(BaseModel):
    subject_id: str = Field(..., max_length=20)
    study_group: StudyGroup
    enrollment_date: date
    status: ParticipantStatus
    age: int = Field(..., ge=0, le=130)
    gender: Gender


class ParticipantResponseSchema(BaseModel):
    participant_id: UUID
    subject_id: str
    study_group: StudyGroup
    enrollment_date: date
    status: ParticipantStatus
    age: int
    gender: Gender

    model_config = ConfigDict(from_attributes=True)


class MetricsResponseSchema(BaseModel):
    total_participants: int
    study_groups: Dict[str, int]
    statuses: Dict[str, int]
    genders: Dict[str, int]
    average_age: float

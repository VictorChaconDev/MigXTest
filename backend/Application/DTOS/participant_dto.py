from dataclasses import dataclass
from datetime import date

from Domain.ValueObjects.gender import Gender
from Domain.ValueObjects.participant_status import ParticipantStatus
from Domain.ValueObjects.study_group import StudyGroup


@dataclass
class CreateParticipantDTO:
    subject_id: str
    study_group: StudyGroup
    enrollment_date: date
    status: ParticipantStatus
    age: int
    gender: Gender


@dataclass
class UpdateParticipantDTO:
    subject_id: str
    study_group: StudyGroup
    enrollment_date: date
    status: ParticipantStatus
    age: int
    gender: Gender
from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4

from Domain.ValueObjects.gender import Gender
from Domain.ValueObjects.participant_status import ParticipantStatus
from Domain.ValueObjects.study_group import StudyGroup


@dataclass
class Participant:
    subject_id: str
    study_group: StudyGroup
    enrollment_date: date
    status: ParticipantStatus
    age: int
    gender: Gender
    participant_id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        if not self.subject_id:
            raise ValueError("subject_id cannot be empty")
        if self.age < 0 or self.age > 130:
            raise ValueError(f"Invalid age: {self.age}")

    def withdraw(self) -> None:
        if self.status == ParticipantStatus.WITHDRAWN:
            raise ValueError("Participant is already withdrawn")
        self.status = ParticipantStatus.WITHDRAWN

    def complete(self) -> None:
        if self.status != ParticipantStatus.ACTIVE:
            raise ValueError("Only active participants can be completed")
        self.status = ParticipantStatus.COMPLETED
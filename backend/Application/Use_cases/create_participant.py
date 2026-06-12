from Application.DTOS.participant_dto import CreateParticipantDTO
from Application.Ports.participant_repository import ParticipantRepository
from Domain.Entities.participant import Participant


class DuplicateSubjectIdError(Exception):
    pass


class CreateParticipant:
    def __init__(self, repo : ParticipantRepository):
        self._repo = repo

    async def execute(self, dto: CreateParticipantDTO) -> Participant:
        existing = await self._repo.get_by_subject_id(dto.subject_id)
        if existing is not None:
            raise DuplicateSubjectIdError(f"Subject ID {dto.subject_id} already exists")

        participant = Participant(
            subject_id=dto.subject_id,
            study_group=dto.study_group,
            enrollment_date=dto.enrollment_date,
            status=dto.status,
            age=dto.age,
            gender=dto.gender,
        )
        await self._repo.save(participant)
        return participant
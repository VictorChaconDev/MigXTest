from uuid import UUID
from Application.Ports.participant_repository import ParticipantRepository
from Application.DTOS.participant_dto import UpdateParticipantDTO
from Domain.Entities.participant import Participant


class ParticipantNotFoundError(Exception):
    pass


class UpdateParticipant:
    def __init__(self, repo: ParticipantRepository):
        self._repo = repo

    async def execute(self, participant_id: UUID, dto: UpdateParticipantDTO) -> Participant:
        participant = await self._repo.get_by_id(participant_id)
        if not participant:
            raise ParticipantNotFoundError(f"Participant with ID {participant_id} not found")

        # Update attributes
        participant.subject_id = dto.subject_id
        participant.study_group = dto.study_group
        participant.enrollment_date = dto.enrollment_date
        participant.status = dto.status
        participant.age = dto.age
        participant.gender = dto.gender

        # Re-trigger domain validations
        participant.__post_init__()

        await self._repo.update(participant)
        return participant

# application/use_cases/get_participant.py

from uuid import UUID
from Application.Ports.participant_repository import ParticipantRepository
from Domain.Entities.participant import Participant


class GetParticipant:
    def __init__(self, repo: ParticipantRepository):
        self._repo = repo

    async def execute(self, participant_id: UUID) -> Participant | None:
        return await self._repo.get_by_id(participant_id)
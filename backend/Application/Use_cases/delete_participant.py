from uuid import UUID
from Application.Ports.participant_repository import ParticipantRepository


class DeleteParticipant:
    def __init__(self, repo: ParticipantRepository):
        self._repo = repo

    async def execute(self, participant_id: UUID) -> None:
        await self._repo.delete(participant_id)


from Application.Ports.participant_repository import ParticipantRepository
from Domain.Entities.participant import Participant


class ListParticipants:
    def __init__(self, repo: ParticipantRepository):
        self._repo = repo

    async def execute(self) -> list[Participant]:
        return await self._repo.get_all()
from abc import ABC, abstractmethod
from uuid import UUID

from Domain.Entities.participant import Participant


class ParticipantRepository(ABC):
    @abstractmethod
    async def save(self,participant: Participant) -> None: ...

    @abstractmethod
    async def get_by_id(self, participant_id: UUID) -> Participant | None: ...

    @abstractmethod
    async def get_by_subject_id(self, subject_id: str) -> Participant | None: ...

    @abstractmethod
    async def get_all(self) -> list[Participant]: ...

    @abstractmethod
    async def update(self, participant: Participant) -> None: ...

    @abstractmethod
    async def delete(self, participant_id: UUID) -> None: ...
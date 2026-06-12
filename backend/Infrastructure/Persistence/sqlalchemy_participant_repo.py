# infrastructure/persistence/sqlalchemy_participant_repo.py

from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Ports.participant_repository import ParticipantRepository
from Domain.Entities.participant import Participant
from Domain.ValueObjects.study_group import StudyGroup
from Domain.ValueObjects.participant_status import ParticipantStatus
from Domain.ValueObjects.gender import Gender
from Infrastructure.Persistence.models import ParticipantModel


class SqlaParticipantRepo(ParticipantRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, participant: Participant) -> None:
        model = ParticipantModel(
            participant_id=participant.participant_id,
            subject_id=participant.subject_id,
            study_group=participant.study_group.value,
            enrollment_date=participant.enrollment_date,
            status=participant.status.value,
            age=participant.age,
            gender=participant.gender.value,
        )
        self._session.add(model)
        await self._session.commit()

    async def get_by_id(self, participant_id: UUID) -> Participant | None:
        result = await self._session.execute(
            select(ParticipantModel).where(ParticipantModel.participant_id == participant_id)
        )
        model = result.scalar_one_or_none()
        return self._to_Domain(model) if model else None

    async def get_by_subject_id(self, subject_id: str) -> Participant | None:
        result = await self._session.execute(
            select(ParticipantModel).where(ParticipantModel.subject_id == subject_id)
        )
        model = result.scalar_one_or_none()
        return self._to_Domain(model) if model else None

    async def get_all(self) -> list[Participant]:
        result = await self._session.execute(select(ParticipantModel))
        return [self._to_Domain(m) for m in result.scalars().all()]

    async def update(self, participant: Participant) -> None:
        result = await self._session.execute(
            select(ParticipantModel).where(ParticipantModel.participant_id == participant.participant_id)
        )
        model = result.scalar_one_or_none()
        if model:
            model.subject_id = participant.subject_id
            model.study_group = participant.study_group.value
            model.enrollment_date = participant.enrollment_date
            model.status = participant.status.value
            model.age = participant.age
            model.gender = participant.gender.value
            await self._session.commit()

    async def delete(self, participant_id: UUID) -> None:
        result = await self._session.execute(
            select(ParticipantModel).where(ParticipantModel.participant_id == participant_id)
        )
        model = result.scalar_one_or_none()
        if model:
            await self._session.delete(model)
            await self._session.commit()

    @staticmethod
    def _to_Domain(model: ParticipantModel) -> Participant:
        return Participant(
            participant_id=model.participant_id,
            subject_id=model.subject_id,
            study_group=StudyGroup(model.study_group),
            enrollment_date=model.enrollment_date,
            status=ParticipantStatus(model.status),
            age=model.age,
            gender=Gender(model.gender),
        )
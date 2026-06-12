from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from Application.DTOS.participant_dto import CreateParticipantDTO, UpdateParticipantDTO
from Application.Ports.participant_repository import ParticipantRepository
from Application.Use_cases.create_participant import (
    CreateParticipant,
    DuplicateSubjectIdError,
)
from Application.Use_cases.get_participant import GetParticipant
from Application.Use_cases.list_participants import ListParticipants
from Application.Use_cases.update_participant import UpdateParticipant, ParticipantNotFoundError
from Application.Use_cases.delete_participant import DeleteParticipant
from Application.Use_cases.get_participant_metrics import GetParticipantMetrics
from Domain.Entities.user import User
from Interface.Api.dependencies import get_current_user, get_participant_repo
from Interface.Api.Schemas.participant import (
    ParticipantCreateSchema,
    ParticipantUpdateSchema,
    ParticipantResponseSchema,
    MetricsResponseSchema,
)

router = APIRouter(prefix="/participants", tags=["participants"])


@router.post(
    "/",
    response_model=ParticipantResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_participant(
    schema: ParticipantCreateSchema,
    repo: ParticipantRepository = Depends(get_participant_repo),
    current_user: User = Depends(get_current_user),
):
    dto = CreateParticipantDTO(
        subject_id=schema.subject_id,
        study_group=schema.study_group,
        enrollment_date=schema.enrollment_date,
        status=schema.status,
        age=schema.age,
        gender=schema.gender,
    )
    use_case = CreateParticipant(repo)
    try:
        participant = await use_case.execute(dto)
        return participant
    except DuplicateSubjectIdError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get("/", response_model=List[ParticipantResponseSchema])
async def list_participants(
    repo: ParticipantRepository = Depends(get_participant_repo),
    current_user: User = Depends(get_current_user),
):
    use_case = ListParticipants(repo)
    return await use_case.execute()


@router.get("/metrics", response_model=MetricsResponseSchema)
async def get_metrics(
    repo: ParticipantRepository = Depends(get_participant_repo),
    current_user: User = Depends(get_current_user),
):
    use_case = GetParticipantMetrics(repo)
    return await use_case.execute()


@router.get("/{participant_id}", response_model=ParticipantResponseSchema)
async def get_participant(
    participant_id: UUID,
    repo: ParticipantRepository = Depends(get_participant_repo),
    current_user: User = Depends(get_current_user),
):
    use_case = GetParticipant(repo)
    participant = await use_case.execute(participant_id)
    if participant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Participant with ID {participant_id} not found",
        )
    return participant


@router.put("/{participant_id}", response_model=ParticipantResponseSchema)
async def update_participant(
    participant_id: UUID,
    schema: ParticipantUpdateSchema,
    repo: ParticipantRepository = Depends(get_participant_repo),
    current_user: User = Depends(get_current_user),
):
    dto = UpdateParticipantDTO(
        subject_id=schema.subject_id,
        study_group=schema.study_group,
        enrollment_date=schema.enrollment_date,
        status=schema.status,
        age=schema.age,
        gender=schema.gender,
    )
    use_case = UpdateParticipant(repo)
    try:
        updated = await use_case.execute(participant_id, dto)
        return updated
    except ParticipantNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.delete("/{participant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_participant(
    participant_id: UUID,
    repo: ParticipantRepository = Depends(get_participant_repo),
    current_user: User = Depends(get_current_user),
):
    use_case = DeleteParticipant(repo)
    await use_case.execute(participant_id)
    return

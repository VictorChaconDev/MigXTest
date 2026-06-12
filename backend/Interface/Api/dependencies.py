from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Ports.auth_service import AuthService, InvalidTokenError
from Application.Ports.participant_repository import ParticipantRepository
from Application.Ports.user_repo import UserRepository
from Domain.Entities.user import User
from Infrastructure.Auth.jwt_service import JwtAuthService
from Infrastructure.database import get_session
from Infrastructure.Persistence.sqlalchemy_participant_repo import SqlaParticipantRepo
from Infrastructure.Persistence.sqlalchemy_user_repo import SqlaUserRepo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_auth_service() -> AuthService:
    return JwtAuthService()


def get_user_repo(session: AsyncSession = Depends(get_session)) -> UserRepository:
    return SqlaUserRepo(session)


def get_participant_repo(
    session: AsyncSession = Depends(get_session),
) -> ParticipantRepository:
    return SqlaParticipantRepo(session)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
    user_repo: UserRepository = Depends(get_user_repo),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        username = auth_service.decode_token(token)
    except InvalidTokenError:
        raise credentials_exception

    user = await user_repo.get_by_username(username)
    if user is None:
        raise credentials_exception
    return user

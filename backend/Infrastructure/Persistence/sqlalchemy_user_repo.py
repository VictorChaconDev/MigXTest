from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Ports.user_repo import UserRepository
from Domain.Entities.user import User
from Infrastructure.Persistence.models import UserModel


class SqlaUserRepo(UserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, user: User) -> None:
        model = UserModel(
            user_id=user.user_id,
            username=user.username,
            hashed_password=user.hashed_password,
        )
        self._session.add(model)
        await self._session.commit()

    async def get_by_username(self, username: str) -> User | None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def get_by_id(self, user_id: UUID) -> User | None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.user_id == user_id)
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    @staticmethod
    def _to_domain(model: UserModel) -> User:
        return User(
            user_id=model.user_id,
            username=model.username,
            hashed_password=model.hashed_password,
        )

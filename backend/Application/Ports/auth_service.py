# application/ports/auth_service.py

from abc import ABC, abstractmethod
from Domain.Entities.user import User


class AuthService(ABC):
    @abstractmethod
    def hash_password(self, plain_password: str) -> str: ...

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool: ...

    @abstractmethod
    def create_access_token(self, user: User) -> str: ...

    @abstractmethod
    def decode_token(self, token: str) -> str: ...


class InvalidTokenError(Exception):
    pass
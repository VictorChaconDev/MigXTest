# domain/entities/user.py

from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class User:
    username: str
    hashed_password: str
    user_id: UUID = field(default_factory=uuid4)
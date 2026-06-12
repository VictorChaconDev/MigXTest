# infrastructure/auth/jwt_service.py

from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError
from passlib.context import CryptContext

from Application.Ports.auth_service import AuthService, InvalidTokenError
from Domain.Entities.user import User
from core.config import settings

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JwtAuthService(AuthService):
    def __init__(self, secret_key: str = settings.SECRET_KEY, algorithm: str = "HS256"):
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    def hash_password(self, plain_password: str) -> str:
        return _pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return _pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, user: User) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=self._expire_minutes)
        payload = {"sub": user.username, "exp": expire}
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def decode_token(self, token: str) -> str:
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            username = payload.get("sub")
            if username is None:
                raise InvalidTokenError("Token missing subject")
            return username
        except JWTError as exc:
            raise InvalidTokenError("Could not validate token") from exc
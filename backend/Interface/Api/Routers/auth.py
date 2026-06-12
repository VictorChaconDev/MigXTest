from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from Application.Ports.auth_service import AuthService
from Application.Ports.user_repo import UserRepository
from Domain.Entities.user import User
from Interface.Api.dependencies import get_auth_service, get_user_repo
from Interface.Api.Schemas.auth import Token, UserRegisterSchema

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(
    schema: UserRegisterSchema,
    auth_service: AuthService = Depends(get_auth_service),
    user_repo: UserRepository = Depends(get_user_repo),
):
    existing = await user_repo.get_by_username(schema.username)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    hashed_pwd = auth_service.hash_password(schema.password)
    user = User(username=schema.username, hashed_password=hashed_pwd)
    await user_repo.save(user)

    access_token = auth_service.create_access_token(user)
    return Token(access_token=access_token, token_type="bearer")


@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
    user_repo: UserRepository = Depends(get_user_repo),
):
    user = await user_repo.get_by_username(form_data.username)
    if user is None or not auth_service.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth_service.create_access_token(user)
    return Token(access_token=access_token, token_type="bearer")
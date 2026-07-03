from fastapi import APIRouter, HTTPException, Response, status

from app.core.schemes.user import UserCreateScheme, UserPrivateScheme
from app.infostructure.dependencies.services import UserServiceDep


router = APIRouter(tags=["auth"])


@router.post("/register", response_model=UserPrivateScheme, status_code=status.HTTP_201_CREATED)
async def register(user_create_scheme: UserCreateScheme, user_service: UserServiceDep):
    existing_user = await user_service.get_existing_user(
        username=user_create_scheme.username,
        email=user_create_scheme.email
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with that name or email already exists"
        )

    user: UserPrivateScheme = await user_service.create_user(user_create_scheme)

    return user


@router.post("/login")
async def token():
    ...


@router.post("/logout")
async def logout():
    ...


from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette import status

from containers import Container
from user.application.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


class CreateUserBody(BaseModel):
    name: str
    email: str
    password: str


class UpdateUser(BaseModel):
    name: str | None = None
    password: str | None = None


@router.post("", status_code=status.HTTP_201_CREATED)
@inject
def create_user(user: CreateUserBody,
                user_service: UserService = Depends(
                    Provide[Container.user_service])):
    created_user = user_service.create_user(
        name=user.name,
        email=user.email,
        password=user.password
    )
    return created_user


@router.put("/{user_id}")
@inject
def update_user(user_id: str,
                user: UpdateUser,
                user_service: UserService = Depends(
                    Provide[Container.user_service])):
    user = user_service.update_user(
        user_id=user_id,
        name=user.name,
        password=user.password
    )

    return user


@router.get("")
@inject
def get_users(
        user_service: UserService = Depends(Provide[Container.user_service])):
    users = user_service.get_users()
    return users

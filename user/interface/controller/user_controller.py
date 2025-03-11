from fastapi import APIRouter, Depends
from starlette import status
from pydantic import BaseModel

from user.application.user_service import UserService

from dependency_injector.wiring import inject, Provide
from containers import Container

router = APIRouter(prefix="/users", tags=["users"])


class CreateUserBody(BaseModel):
    name: str
    email: str
    password: str


@router.post("", status_code=status.HTTP_201_CREATED)
@inject
def create_user(user: CreateUserBody,
                user_service: UserService = Depends(Provide[Container.user_service])):
    created_user = user_service.create_user(
        name=user.name,
        email=user.email,
        password=user.password
    )
    return created_user

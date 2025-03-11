from fastapi import HTTPException, Depends
from containers import Container
from ulid import ULID
from datetime import datetime
from dependency_injector.wiring import inject, Provide

from user.domain.repository.user_repo import IUserRepository
from user.domain.user import User, Profile
from user.infra.repository.user_repo import UserRepository
from utils.crypto import Crypto


class UserService:
    @inject
    def __init__(self,
                 user_repo: IUserRepository = Depends(Provide[Container.user_repo])):
        self.user_repo = user_repo
        self.ulid = ULID()
        self.crypto = Crypto()

    def create_user(self, name: str, email: str, password: str):
        _user = None

        try:
            _user = self.user_repo.find_by_email(email)
        except HTTPException as e:
            if e.status_code != 422:
                raise e

        if _user:
            raise HTTPException(status_code=422)

        now = datetime.now()
        user: User = User(
            id=self.ulid.generate(),
            profile=Profile(
                name=name,
                email=email,
            ),
            password=self.crypto.encrypt(password),
            created_at=now,
            updated_at=now
        )
        self.user_repo.save(user)

        return user

from dataclasses import asdict
from datetime import datetime
from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from common.auth import CurrentUser
from common.auth import get_current_user
from containers import Container
from note.application.note_service import NoteService

router = APIRouter(prefix="/notes", tags=["note"])


class NoteResponse(BaseModel):
    id: str
    user_id: str
    title: str
    content: str
    memo_date: str
    tags: list[str]
    created_at: datetime
    updated_at: datetime


class CreateNoteBody(BaseModel):
    title: str = Field(min_length=1, max_length=64)
    content: str = Field(min_length=1)
    memo_date: str = Field(min_length=8, max_length=8)
    tags: list[str] | None = Field(default=None, min_length=1, max_length=32)


@router.post("", status_code=201, response_model=NoteResponse)
@inject
def create_note(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    body: CreateNoteBody,
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    note = note_service.create_note(
        user_id=current_user.id,
        title=body.title,
        content=body.content,
        memo_date=body.memo_date,
        tag_names=body.tags if body.tags else [],
    )

    response = asdict(note)
    response.update({"tags": [tag.name for tag in note.tags]})

    return response

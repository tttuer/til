from dataclasses import dataclass
from datetime import datetime


@dataclass
class Tag:
    id: str
    name: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Note:
    id: str
    title: str
    content: str
    user_id: str
    memo_date: str
    tags: list[Tag]
    created_at: datetime
    updated_at: datetime

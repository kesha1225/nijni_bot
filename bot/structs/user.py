from dataclasses import dataclass
from typing import Self

from aiogram.types import Message


@dataclass
class UserStruct:
    tg_id: int
    language_code: str
    username: str | None
    first_name: str | None
    last_name: str | None

    @classmethod
    def from_aiogram_event(cls, event: Message) -> Self:
        return cls(
            tg_id=event.from_user.id,
            language_code=event.from_user.language_code,
            username=event.from_user.username,
            first_name=event.from_user.first_name,
            last_name=event.from_user.last_name,
        )

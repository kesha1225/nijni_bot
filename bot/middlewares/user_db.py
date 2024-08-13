from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from bot.structs.user import UserStruct
from services.userdb.crud import get_middleware_user, ensure_user


class DbUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        user_data = UserStruct.from_aiogram_event(event=event)
        meta_user = await get_middleware_user(user_data=user_data)
        meta_user = await ensure_user(user_data=user_data, user=meta_user)
        data["current_user"] = meta_user
        return await handler(event, data)

from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from bot.constants.commands import TextCommand


class ClearStateMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:

        text = event.text
        state = data["state"]
        if (
            text
            in (
                TextCommand.command_call,
                TextCommand.share_news,
                TextCommand.send_issue,
                TextCommand.suggest_idea,
                TextCommand.start,
            )
            and await state.get_state() is not None
        ):
            await state.clear()

        return await handler(event, data)

from aiogram.filters import Filter
from aiogram.types import Message

from bot_config import BotConfig


class OnlyAdminMessageFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in BotConfig.admins

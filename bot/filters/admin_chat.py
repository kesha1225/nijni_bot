from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from bot_config import BotConfig


class AdminChatMessageFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.id == BotConfig.admin_chat_id


class AdminChatCallbackFilter(Filter):
    async def __call__(self, callback_query: CallbackQuery) -> bool:
        return callback_query.message.chat.id == BotConfig.admin_chat_id

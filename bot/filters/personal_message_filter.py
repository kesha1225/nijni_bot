from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery


class OnlyPersonalMessageFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.id > 0


class OnlyPersonalCallbackFilter(Filter):
    async def __call__(self, callback_query: CallbackQuery) -> bool:
        return callback_query.message.chat.id > 0

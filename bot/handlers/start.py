from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.filters.any_state import AnyStateClearMessageFilter
from bot.filters.personal_message_filter import OnlyPersonalMessageFilter
from bot.keyboards.action import get_first_action_keyboard
from bot.middlewares.user_db import DbUserMiddleware

router = Router(name=__name__)
router.message.outer_middleware(DbUserMiddleware())
router.message.filter(OnlyPersonalMessageFilter())


@router.message(CommandStart(), AnyStateClearMessageFilter())
async def start_handler(message: Message) -> None:
    temp_i18n = "Что вы хотите сделать?"

    await message.answer(
        text=temp_i18n,
        reply_markup=(get_first_action_keyboard()),
        parse_mode=ParseMode.HTML,
    )

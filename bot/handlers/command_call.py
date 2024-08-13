from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.constants.commands import TextCommand
from bot.filters.any_state import AnyStateClearMessageFilter, StateMessageFilter
from bot.filters.personal_message_filter import OnlyPersonalMessageFilter
from bot.fsm.state_group import CallCommandForm
from bot.middlewares.user_db import DbUserMiddleware
from bot.send_to_admin_chat import forward_to_admin_chat
from bot_config import BotConfig

router = Router(name=__name__)
router.message.outer_middleware(DbUserMiddleware())
router.message.filter(OnlyPersonalMessageFilter())


@router.message(F.text == TextCommand.command_call, AnyStateClearMessageFilter())
async def command_call_handler(message: Message, state: FSMContext) -> None:
    temp_i18n = "Изложите свое предложение к команде в свободной форме."

    await state.set_state(CallCommandForm.message)
    await message.answer(text=temp_i18n)


@router.message(CallCommandForm.message, StateMessageFilter())
async def command_call_message_handler(message: Message, state: FSMContext) -> None:
    temp_i18n = "Предложение успешно передано!"

    await message.answer(text=temp_i18n)

    await state.clear()

    await forward_to_admin_chat(
        message=message,
        message_thread_id=BotConfig.command_call_topic_id,
        text=f"Пользователь {message.from_user.id} @{message.from_user.username} передал сообщение команде:",
    )

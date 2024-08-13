from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.constants.commands import TextCommand
from bot.filters.any_state import AnyStateClearMessageFilter, StateMessageFilter
from bot.filters.personal_message_filter import OnlyPersonalMessageFilter
from bot.fsm.state_group import SendNewsForm
from bot.middlewares.user_db import DbUserMiddleware
from bot.send_to_admin_chat import forward_to_admin_chat
from bot_config import BotConfig

router = Router(name=__name__)
router.message.outer_middleware(DbUserMiddleware())
router.message.filter(OnlyPersonalMessageFilter())


@router.message(F.text == TextCommand.share_news, AnyStateClearMessageFilter())
async def share_news_handler(message: Message, state: FSMContext) -> None:
    temp_i18n = "Отправьте одно сообщение с новостью и любыми вложениями (фото/видео). Я передам его администраторам."

    await state.set_state(SendNewsForm.message)
    await message.answer(text=temp_i18n)


@router.message(SendNewsForm.message, StateMessageFilter())
async def share_news_message_handler(message: Message, state: FSMContext) -> None:
    temp_i18n = "Сообщение успешно отправлено!"

    await message.answer(text=temp_i18n)

    await state.clear()

    await forward_to_admin_chat(
        message=message,
        message_thread_id=BotConfig.share_news_topic_id,
        text=f"Пользователь {message.from_user.id} @{message.from_user.username} поделился новостью:",
    )

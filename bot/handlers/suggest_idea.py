from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.constants.commands import TextCommand
from bot.filters.any_state import AnyStateClearMessageFilter, StateMessageFilter
from bot.filters.personal_message_filter import OnlyPersonalMessageFilter
from bot.fsm.state_group import SuggestIdeaForm
from bot.middlewares.user_db import DbUserMiddleware
from bot.send_to_admin_chat import forward_to_admin_chat
from bot_config import BotConfig

router = Router(name=__name__)
router.message.outer_middleware(DbUserMiddleware())
router.message.filter(OnlyPersonalMessageFilter())


@router.message(F.text == TextCommand.suggest_idea, AnyStateClearMessageFilter())
async def suggest_idea_handler(message: Message, state: FSMContext) -> None:
    temp_i18n = "Как к вам обращаться? (Фамилия, Имя)"

    await state.set_state(SuggestIdeaForm.fio)
    await message.answer(text=temp_i18n)


@router.message(SuggestIdeaForm.fio, StateMessageFilter())
async def suggest_idea_idea_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(data={"fio": message.text})

    temp_i18n = "Опишите вашу идею."

    await message.answer(text=temp_i18n)
    await state.set_state(SuggestIdeaForm.idea)


@router.message(SuggestIdeaForm.idea, StateMessageFilter())
async def suggest_idea_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()

    await forward_to_admin_chat(
        message=message,
        message_thread_id=BotConfig.suggest_idea_topic_id,
        text=f"Пользователь {message.from_user.id} @{message.from_user.username} передал идею:\n\n"
        f"ФИО: {data['fio']}\n"
        f"Описание идеи:",
    )

    await state.clear()

    temp_i18n = "Идея успешно передана!"
    await message.answer(text=temp_i18n)

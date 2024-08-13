from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.constants.commands import TextCommand
from bot.filters.any_state import AnyStateClearMessageFilter, StateMessageFilter
from bot.filters.personal_message_filter import OnlyPersonalMessageFilter
from bot.fsm.state_group import SendIssueForm
from bot.middlewares.user_db import DbUserMiddleware
from bot.send_to_admin_chat import forward_to_admin_chat
from bot_config import BotConfig

router = Router(name=__name__)
router.message.outer_middleware(DbUserMiddleware())
router.message.filter(OnlyPersonalMessageFilter())


@router.message(F.text == TextCommand.send_issue, AnyStateClearMessageFilter())
async def send_issue_handler(message: Message, state: FSMContext) -> None:
    temp_i18n = "Как к вам обращаться? (Фамилия, Имя)"

    await state.set_state(SendIssueForm.fio)
    await message.answer(text=temp_i18n)


@router.message(SendIssueForm.fio, StateMessageFilter())
async def send_issue_location_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(data={"fio": message.text})

    temp_i18n = "Опишите адрес или местоположение проблемного объекта."

    await message.answer(text=temp_i18n)

    await state.set_state(SendIssueForm.place)


@router.message(SendIssueForm.place, StateMessageFilter())
async def send_issue_problem_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(data={"location": message.text})

    temp_i18n = "Опишите саму проблему одним сообщением. Вы можете приложить любые вложения (фото/видео)."

    await message.answer(text=temp_i18n)

    await state.set_state(SendIssueForm.problem)


@router.message(SendIssueForm.problem, StateMessageFilter())
async def send_issue_problem_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()

    await forward_to_admin_chat(
        message=message,
        message_thread_id=BotConfig.send_issue_topic_id,
        text=f"Пользователь {message.from_user.id} @{message.from_user.username} передал проблему:\n\n"
        f"ФИО: {data['fio']}\n"
        f"Местоположение: {data['location']}\n"
        f"Описание проблемы:",
    )

    await state.clear()

    temp_i18n = "Проблема успешно передана!"
    await message.answer(text=temp_i18n)

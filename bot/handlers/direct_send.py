from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.constants.commands import TextCommand
from bot.filters.admin_pm import OnlyAdminMessageFilter
from bot.filters.any_state import AnyStateClearMessageFilter, StateMessageFilter
from bot.filters.personal_message_filter import OnlyPersonalMessageFilter
from bot.fsm.state_group import DirectSendForm
from bot.middlewares.user_db import DbUserMiddleware

router = Router(name=__name__)
router.message.outer_middleware(DbUserMiddleware())
router.message.filter(OnlyPersonalMessageFilter())
router.message.filter(OnlyAdminMessageFilter())


@router.message(Command(TextCommand.send), AnyStateClearMessageFilter())
async def direct_send_handler(message: Message, state: FSMContext):
    try:
        tg_id = int(message.text.split()[-1])
    except ValueError:
        return await message.answer("Неверный id пользователя")

    try:
        await message.bot.send_chat_action(chat_id=tg_id, action="typing")
    except TelegramBadRequest:
        return await message.answer("Невозможно написать пользователю с таким id")

    await message.answer(f"Отправьте сообщение которое отправить пользователю {tg_id}:")
    await state.set_state(DirectSendForm.text)
    await state.set_data({"tg_id": tg_id})


@router.message(DirectSendForm.text, StateMessageFilter())
async def direct_send_text_handler(message: Message, state: FSMContext):
    tg_id = (await state.get_data())["tg_id"]

    try:
        await message.bot.send_message(
            chat_id=tg_id, text="Вам сообщение от админов бота:"
        )
        await message.copy_to(chat_id=(await state.get_data())["tg_id"])
    except TelegramBadRequest:
        return await message.answer("Не удалось переслать...")

    await state.clear()
    await message.answer("Успешно отправлено!")

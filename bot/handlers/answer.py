from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callback_data.admin import AdminCallbackData
from bot.filters.admin_chat import AdminChatMessageFilter, AdminChatCallbackFilter
from bot.filters.any_state import AnyStateClearMessageFilter, StateMessageFilter
from bot.fsm.state_group import AnswerForm
from bot.middlewares.user_db import DbUserMiddleware

router = Router(name=__name__)
router.message.outer_middleware(DbUserMiddleware())
router.message.filter(AdminChatMessageFilter())
router.callback_query.filter(AdminChatCallbackFilter())


@router.callback_query(
    F.data.startswith(AdminCallbackData.answer), AnyStateClearMessageFilter()
)
async def answer_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    temp_i18n = "Введите ответ пользователю:"

    await state.set_state(AnswerForm.text)

    await state.set_data({"tg_id": int(callback_query.data.split("_")[-1])})
    await callback_query.message.answer(text=temp_i18n)
    await callback_query.answer()


@router.message(AnswerForm.text, StateMessageFilter())
async def answer_text_handler(message: Message, state: FSMContext) -> None:
    text = message.text

    await message.bot.send_message(
        chat_id=(await state.get_data())["tg_id"],
        text="Вам пришел ответ от админов бота:",
    )
    await message.bot.send_message(chat_id=(await state.get_data())["tg_id"], text=text)
    await message.answer("Ответ успешно отправлен.")
    await state.clear()

from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from bot.callback_data.admin import AdminCallbackData
from bot.constants.commands import TextCommand


def get_first_action_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text=TextCommand.share_news)
    keyboard.button(text=TextCommand.command_call)
    keyboard.button(text=TextCommand.send_issue)
    keyboard.button(text=TextCommand.suggest_idea)

    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True)


def get_answer_keyboard(sender_tg_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.button(
        text="Ответить", callback_data=f"{AdminCallbackData.answer}{sender_tg_id}"
    )

    return keyboard.as_markup()

from aiogram.types import Message

from bot.keyboards.action import get_answer_keyboard
from bot_config import BotConfig


async def forward_to_admin_chat(message: Message, message_thread_id: int, text: str):
    await message.bot.send_message(
        chat_id=BotConfig.admin_chat_id,
        message_thread_id=message_thread_id,
        text=text,
    )
    await message.copy_to(
        chat_id=BotConfig.admin_chat_id,
        message_thread_id=message_thread_id,
        reply_markup=get_answer_keyboard(sender_tg_id=message.from_user.id),
    )

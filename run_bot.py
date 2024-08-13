import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.strategy import FSMStrategy
from aiogram.types import BotCommand

from bot.middlewares.clear_state import ClearStateMiddleware
from bot.middlewares.user_db import DbUserMiddleware
from bot_config import BotConfig
from db import init_db

from bot.handlers import (
    answer_router,
    start_router,
    share_news_router,
    command_call_router,
    send_issue_router,
    direct_send_router,
    suggest_idea_router,
)


async def main():
    dp = Dispatcher()
    dp.message.outer_middleware(DbUserMiddleware())
    dp.message.outer_middleware(ClearStateMiddleware())
    dp.include_routers(
        start_router,
        answer_router,
        share_news_router,
        command_call_router,
        send_issue_router,
        suggest_idea_router,
        direct_send_router,
    )
    bot = Bot(token=BotConfig.token)

    await init_db()
    print(await bot.get_me())

    await bot.set_my_commands(
        commands=[BotCommand(command="start", description="Начать")]
    )

    _log_format = "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    logging.basicConfig(level=logging.INFO, format=_log_format, encoding="utf-8")
    # And the run events dispatching
    await dp.start_polling(bot)


asyncio.run(main())

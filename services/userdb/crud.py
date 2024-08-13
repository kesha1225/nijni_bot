import logging

from bot.structs.user import UserStruct
from db.user import User


logger = logging.getLogger(__name__)


async def get_middleware_user(user_data: UserStruct) -> User:
    user, is_created = await User.get_or_create(
        tg_id=user_data.tg_id,
        defaults={
            "language_code": user_data.language_code,
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "username": user_data.username,
        },
    )
    if is_created:
        logger.info(f"New meta user created {user} (from {user_data})")
    return user


async def ensure_user(user_data: UserStruct, user: User) -> User:
    if user.username != user_data.username:
        user.username = user_data.username
    if user.first_name != user_data.first_name:
        user.first_name = user_data.first_name
    if user.last_name != user_data.last_name:
        user.last_name = user_data.last_name
    user.is_bot_blocked = False
    await user.save()
    return user

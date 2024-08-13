from tortoise import Tortoise

from bot_config import (
    DEFAULT_TORTOISE_CONNECTION,
)
from bot_config import PostgresConfig


TORTOISE_ORM = {
    "connections": {
        DEFAULT_TORTOISE_CONNECTION: PostgresConfig.url,
    },
    "apps": {
        "models": {
            "models": [
                "db.user",
                "aerich.models",
            ],
            "default_connection": DEFAULT_TORTOISE_CONNECTION,
        },
    },
}


async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)

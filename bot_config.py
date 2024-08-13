import os

from dotenv import load_dotenv

load_dotenv()


DEFAULT_TORTOISE_CONNECTION = "default"


class PostgresConfig:
    url = os.getenv("DB_URL")


class BotConfig:
    token = os.getenv("BOT_TOKEN")
    admin_chat_id = -1002144923292

    admins = (
        259687356,
        2109522499,
    )

    share_news_topic_id = 12

    command_call_topic_id = 13
    send_issue_topic_id = 6
    suggest_idea_topic_id = 7

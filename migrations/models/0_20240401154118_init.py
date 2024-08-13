from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "tg_id" BIGINT NOT NULL UNIQUE,
    "language_code" TEXT,
    "registration_date" TIMESTAMPTZ,
    "creation_date" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "username" TEXT,
    "first_name" TEXT,
    "last_name" TEXT,
    "is_bot_blocked" BOOL NOT NULL  DEFAULT False
);
CREATE INDEX IF NOT EXISTS "idx_user_tg_id_ba6243" ON "user" ("tg_id");
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """

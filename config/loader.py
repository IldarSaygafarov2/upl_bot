from dataclasses import dataclass

import environs


@dataclass
class BotConfig:
    token: str
    admin_chat_id: int | None = None

    @staticmethod
    def from_env(env: environs.Env) -> "BotConfig":
        return BotConfig(
            token=env.str('BOT_TOKEN'),
            admin_chat_id=env.int('ADMIN_CHAT_ID')
        )


@dataclass
class DbConfig:
    host: str
    port: int
    database: str
    user: str
    password: str

    @staticmethod
    def from_env(env: environs.Env) -> "DbConfig":
        return DbConfig(
            host=env.str('DB_HOST'),
            port=env.int('DB_PORT'),
            database=env.str('DB_NAME'),
            password=env.str('DB_PASSWORD'),
            user=env.str('DB_USER')
        )


@dataclass
class Config:
    db: DbConfig
    bot: BotConfig


from functools import lru_cache


@lru_cache()
def load_config(env_path: str | None = None) -> Config:
    env = environs.Env()
    env.read_env(env_path)

    db = DbConfig.from_env(env)
    bot = BotConfig.from_env(env)

    return Config(
        db=db,
        bot=bot
    )


settings = load_config()

# создать venv
# активировать его
# скачать библиотеки requests bs4 psycopg2 environs aiogram
# создать requirements.txt
import logging

import environs
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.client.default import DefaultBotProperties

from config.loader import settings
from handlers.user.text import router as user_router
from handlers.admin.text import router as admin_router

env = environs.Env()
env.read_env('.env')


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=settings.bot.token, default=DefaultBotProperties(
        parse_mode='HTML'))

    await bot.set_my_commands(
        commands=[
            BotCommand(command='start', description='Start bot'),
            BotCommand(command='some', description='Start bot some'),
        ]
    )
    dp = Dispatcher()
    dp.include_router(admin_router)
    dp.include_router(user_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())

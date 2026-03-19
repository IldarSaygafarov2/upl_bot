from aiogram import Router, types, F
from aiogram.filters.command import Command, CommandStart
from config.loader import settings
from keyboards.admin.reply import admin_start_kb
# /start

# Router - маршрутизатор

router = Router()
router.message.filter(lambda msg: msg.chat.id == settings.bot.admin_chat_id)

# CRUD - create read update delete


@router.message(CommandStart())
async def handle_start(message: types.Message):
    print(message.chat.id)
    await message.answer('ADMIN Добро пожаловать в бот upl.uz',
                         reply_markup=admin_start_kb())


@router.message(F.text == 'Все категории')
async def show_categories(message: types.Message):
    await message.answer('Все категории')


@router.message(F.text == 'Все статьи')
async def show_categories(message: types.Message):
    await message.answer('Все статьи')
# admin: Сделать обработку клика по второй кнопке
# user: сделать обработку для команд (/help, /about)




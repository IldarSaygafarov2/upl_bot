from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton


def admin_start_kb():
    kb = ReplyKeyboardBuilder()
    kb.add(
        KeyboardButton(text='Все категории'),
        KeyboardButton(text='Все статьи'),
    )
    return kb.as_markup(resize_keyboard=True)

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from database.connection import get_posts_by_category_id


def get_categories_kb(db_categories: list[tuple]):
    kb = InlineKeyboardBuilder()
    for category_id, category_name in db_categories:
        button = InlineKeyboardButton(text=category_name.title(),
                                      callback_data=f'category:{category_id}')
        kb.add(button)
    return kb.as_markup()


def posts_paginated_kb(category_id, start=0, finish=7, page=1):
    kb = InlineKeyboardBuilder()

    posts = get_posts_by_category_id(category_id)

    total_pages = round(len(posts) / 7) + 1

    posts = posts[start:finish]
    for id, title in posts:
        kb.add(
            InlineKeyboardButton(text=title[:30]+'...',
                                 callback_data=f'post:{id}')
        )
    kb.adjust(1)
    kb.row(
        InlineKeyboardButton(text='<', callback_data=f'prev:{category_id}:{start}:{finish}:{page}'),  # кнопка назад
        InlineKeyboardButton(text=f'{page}/{total_pages}', callback_data=f'page'),  # страница
        InlineKeyboardButton(text='>', callback_data=f'next:{category_id}:{start}:{finish}:{page}:{total_pages}')  # кнопка вперед
    )
    return kb.as_markup()


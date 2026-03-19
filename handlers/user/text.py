from aiogram import Router, types, F
from aiogram.filters.command import Command, CommandStart
from database.connection import insert_user, get_categories, get_post_by_id
from keyboards.user.inline import get_categories_kb, posts_paginated_kb

# /start

# Router - маршрутизатор

router = Router()

@router.message(CommandStart())
async def handle_start(message: types.Message):
    username = message.from_user.username
    chat_id = message.chat.id

    insert_user(username, chat_id)

    categories = get_categories()

    await message.answer('Добро пожаловать в бот upl.uz.\nВыберите категорию ⬇',
                         reply_markup=get_categories_kb(categories))


@router.message(Command('about'))
async def handle_about(message: types.Message):
    await message.answer('Данный бот несет информативный характер')


@router.message(Command('help'))
async def handle_help(message: types.Message):
    await message.answer(
        'Данный бот пока что не имеет тех.поддержку, дальше как нибудь сами')


@router.callback_query(F.data.startswith('category'))  # F.data == 'return_back'
async def get_category_posts(callback: types.CallbackQuery):
    await callback.answer()

    category_id = int(callback.data.split(':')[-1])

    await callback.message.edit_text(text='Выберите пост',
                                     reply_markup=posts_paginated_kb(category_id))

    # получить все посты с базы данных по
    # категории и вывести в консоль после нажатия на категорию


@router.callback_query(F.data.startswith('next'))
async def next_page(callback: types.CallbackQuery):
    # await callback.answer()

    _, category_id, start, finish, page, total_pages = callback.data.split(':')
    print(category_id)
    if int(page) == int(total_pages):
        return await callback.answer(text='Следующей страницы нет', show_alert=True)

    return callback.message.edit_reply_markup(
        reply_markup=posts_paginated_kb(
            category_id=int(category_id),
            start=int(start) + 7,
            finish=int(finish) + 7,
            page=int(page) + 1
        )
    )


@router.callback_query(F.data.startswith('prev'))
async def prev_page(callback: types.CallbackQuery):
    # await callback.answer()

    _, category_id, start, finish, page = callback.data.split(':')

    if int(page) == 1:
        return await callback.answer(text='Предыдущей страницы нет', show_alert=True)

    return callback.message.edit_reply_markup(
        reply_markup=posts_paginated_kb(
            category_id=int(category_id),
            start=int(start) - 7,
            finish=int(finish) - 7,
            page=int(page) - 1
        )
    )


@router.callback_query(F.data.startswith('post'))
async def get_post(callback: types.CallbackQuery):
    post_id = int(callback.data.split(':')[-1])

    _, title, description, date, img, href, _ = get_post_by_id(post_id)

    msg = f'''
<b>{title}</b>

<i>{description}</i>

Дата: {date}
Ссылка:
<a href='{href}'>Детально</a>
'''

    await callback.message.answer_photo(
        photo=img,
        caption=msg
    )


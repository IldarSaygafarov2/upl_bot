# сделать подключение к базе данных

import psycopg2

from config.loader import settings


def connect():
    connection = psycopg2.connect(
        host=settings.db.host,
        port=settings.db.port,
        database=settings.db.database,
        password=settings.db.password,
        user=settings.db.user
    )
    cursor = connection.cursor()
    return connection, cursor


def get_user_by_chat_id(chat_id: int) -> tuple | None:
    connection, cursor = connect()

    sql = 'SELECT * FROM users WHERE tg_chat_id = %s;'
    cursor.execute(sql, (chat_id,))
    user = cursor.fetchone()
    if user is None:
        return
    return user


def insert_user(tg_username: str, tg_chat_id: int) -> None:
    connection, cursor = connect()
    # unique constraint fail
    sql = '''
    INSERT INTO users(tg_username, tg_chat_id)
    VALUES (%(tg_username)s, %(tg_chat_id)s)
    ON CONFLICT(tg_chat_id) DO UPDATE
    SET tg_username = %(tg_username)s
    RETURNING *
    '''
    cursor.execute(sql, {
        'tg_username': tg_username,
        'tg_chat_id': tg_chat_id
    })
    connection.commit()
    user = cursor.fetchone()
    print('Registered: ', *user)


def insert_category(name: str) -> None:
    connection, cursor = connect()

    sql = 'INSERT INTO categories(name) VALUES (%s) ON CONFLICT (name) DO NOTHING RETURNING *;'
    cursor.execute(sql, (name,))
    connection.commit()
    category = cursor.fetchone()
    if category is not None:
        print('Added category: ', *category)
    else:
        print('Category already exists')


def get_category_id_by_name(name: str) -> int | None:
    connection, cursor = connect()

    sql = 'SELECT id FROM categories WHERE name = %s;'
    cursor.execute(sql, (name,))
    category = cursor.fetchone()
    if category is None:
        return
    return category[0]


def insert_post(title, description, date, img, href, category_id):
    connection, cursor = connect()

    sql = '''
    INSERT INTO posts(title,description,date,img,href,category_id)
    VALUES (%s,%s,%s,%s,%s,%s) RETURNING id, title
    '''
    cursor.execute(sql, (title,description,date,img,href,category_id))
    connection.commit()
    post = cursor.fetchone()
    print('added post: ', *post)


def get_categories() -> list[tuple]:
    connection, cursor = connect()
    sql = 'SELECT * FROM categories;'
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def get_posts_by_category_id(category_id: int) -> list:
    connection, cursor = connect()
    sql = 'SELECT id, title FROM posts WHERE category_id = %s;'
    cursor.execute(sql, (category_id,))
    return cursor.fetchall()


def get_post_by_id(post_id: int):
    connection, cursor = connect()
    sql = 'SELECT * FROM posts WHERE id = %s;'
    cursor.execute(sql, (post_id,))
    return cursor.fetchone()

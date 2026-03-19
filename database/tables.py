from database.connection import connect


def create_users_table():
    connection, cursor = connect()

    cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    tg_username VARCHAR(35) UNIQUE,
    tg_chat_id BIGINT UNIQUE
);
    ''')
    connection.commit()
    print('created users table')


# написать функцию для создания таблицы categories
# id, name


def create_categories_table():
    connection, cursor = connect()

    cursor.execute('''
CREATE TABLE IF NOT EXISTS categories(
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(100) UNIQUE
);
    ''')
    connection.commit()
    print('created categories table')


def create_posts_table():
    connection, cursor = connect()

    cursor.execute('''
CREATE TABLE IF NOT EXISTS posts(
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    title TEXT,
    description TEXT,
    date TEXT,
    img TEXT, 
    href TEXT,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories(id)
)
    ''')
    connection.commit()


create_users_table()
create_categories_table()
create_posts_table()

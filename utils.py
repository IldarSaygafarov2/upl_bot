from database import connection as con
import json


def read_json(file_path):
    with open(file_path, mode='r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


def fill_categories_from_json():
    data = read_json('data.json')

    for category in data.keys():
        con.insert_category(category)

def fill_posts():
    data = read_json('data.json')

    for category, pages in data.items():
        category_id = con.get_category_id_by_name(
            name=category
        )

        for posts in pages.values():
            for post in posts:
                con.insert_post(
                    title=post.get('title'),
                    description=post.get('text'),
                    date=post.get('time'),
                    href=post.get('href'),
                    img=post.get('img'),
                    category_id=category_id
                )

# fill_posts()
#
# fill_categories_from_json()
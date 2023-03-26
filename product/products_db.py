import sqlite3
from datetime import datetime
from product.images.product_images_db import insert_images_by_product_id
from product.images.product_images_db import update_images_by_product_id
from product.images.product_images_db import delete_images_by_product_id
from product.history_modification.product_modifications_db import insert_history_modification, delete_history_modification

PRODUCTS_TABLE = "products"

products_connection = sqlite3.connect("product/Products.db", check_same_thread=False)
products_cursor = products_connection.cursor()


def init_products_db_if_needed():
    products_cursor.execute(f"CREATE TABLE IF NOT EXISTS {PRODUCTS_TABLE}("
                            f"id INTEGER PRIMARY KEY AUTOINCREMENT, "
                            f"owner_email TEXT, "
                            f"title TEXT, "
                            f"description TEXT, "
                            f"created_at TEXT, "
                            f"edited_at TEXT, "
                            f"status INTEGER)")


def insert_product_in_db(owner_email, title, description, status, images):
    created_at = datetime.now()
    edited_at = created_at

    product = (owner_email, title, description, created_at, edited_at, status.value)

    products_cursor.execute(
        f"INSERT INTO "
        f"{PRODUCTS_TABLE}(owner_email, title, description, created_at, edited_at, status) "
        f"VALUES(?,?,?,?,?,?);",
        product)

    if images: insert_images_by_product_id(products_cursor.lastrowid, images)

    products_connection.commit()


def update_product_in_db(product_id, owner, title, description, status, images):
    edited_at = datetime.now()

    (owner_email, old_title, old_description, _, _, _) = get_product_by_id(product_id)

    if owner != owner_email: raise Exception("You cannot update another user's product")

    products_cursor.execute(f"UPDATE {PRODUCTS_TABLE} SET title='{title}', "
                            f"description='{description}', "
                            f"edited_at='{edited_at}', "
                            f"status={status.value} "
                            f"WHERE id={product_id}"
                            )
    products_connection.commit()

    if images: update_images_by_product_id(product_id, images)

    insert_history_modification(product_id, title, description)


def delete_product_from_db(product_id, owner):
    (owner_email, _, _, _, _, _) = get_product_by_id(product_id)
    if owner != owner_email: raise Exception("You cannot delete another user's product")

    delete_images_by_product_id(product_id)
    delete_history_modification(product_id)

    products_cursor.execute(f"DELETE FROM {PRODUCTS_TABLE} WHERE id={product_id};")
    products_connection.commit()


def get_product_by_id(product_id):
    return products_cursor.execute(
        f"SELECT owner_email, title, description, created_at, edited_at, status "
        f"FROM {PRODUCTS_TABLE} WHERE id={product_id};"
    ).fetchone()

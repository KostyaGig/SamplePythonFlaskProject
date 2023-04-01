import sqlite3
from datetime import datetime

PRODUCT_MODIFICATIONS_TABLE = "product_modification"

product_modifications_connection = sqlite3.connect("product/history_modification/ProductModifications.db",
                                                   check_same_thread=False)
product_modifications_cursor = product_modifications_connection.cursor()


def init_product_modifications_db_if_needed():
    product_modifications_cursor.execute(f"CREATE TABLE IF NOT EXISTS {PRODUCT_MODIFICATIONS_TABLE}("
                                         f"id INTEGER PRIMARY KEY AUTOINCREMENT, "
                                         f"product_id INTEGER, "
                                         f"title TEXT, "
                                         f"description TEXT, "
                                         f"edited_at TEXT)")


def insert_history_modification(product_id, title, description):
    edited_at = datetime.now()
    modification = (product_id, title, description, edited_at)
    product_modifications_cursor.execute(
        f"INSERT INTO "
        f"{PRODUCT_MODIFICATIONS_TABLE}(product_id, title, description, edited_at) "
        f"VALUES(?,?,?,?);",
        modification
    )
    product_modifications_connection.commit()


def delete_history_modification(product_id):
    product_modifications_cursor.execute(f"DELETE FROM {PRODUCT_MODIFICATIONS_TABLE} WHERE product_id={product_id}")
    product_modifications_connection.commit()


def get_product_by_history_modification_id(modification_id):
    product = product_modifications_cursor.execute(
        f"SELECT product_id, title, description, edited_at "
        f"FROM {PRODUCT_MODIFICATIONS_TABLE} WHERE id={modification_id};"
    ).fetchone()

    if product is None: raise Exception(f"product by {modification_id} modification id does not exist")
    return product

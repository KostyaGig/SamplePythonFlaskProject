import sqlite3

PRODUCT_IMAGES_TABLE = "product_images"

product_images_connection = sqlite3.connect("product/images/ProductImages.db", check_same_thread=False)
product_images_cursor = product_images_connection.cursor()


def init_product_images_db_if_needed():
    product_images_cursor.execute(f"CREATE TABLE IF NOT EXISTS {PRODUCT_IMAGES_TABLE}("
                                  f"id INTEGER PRIMARY KEY AUTOINCREMENT, "
                                  f"product_id INTEGER, "
                                  f"image TEXT)")


def insert_images_by_product_id(product_id, images):
    for image in images:
        insert(product_id, image)
    product_images_connection.commit()


def insert(product_id, image):
    product_and_image = (product_id, image)
    product_images_cursor.execute(
        f"INSERT INTO {PRODUCT_IMAGES_TABLE}"
        f"(product_id, image) VALUES(?,?);",
        product_and_image
    )

def update_images_by_product_id(product_id, images):
    delete_images_by_product_id(product_id)
    insert_images_by_product_id(product_id, images)

def delete_images_by_product_id(product_id):
    product_images_cursor.execute(f"DELETE FROM {PRODUCT_IMAGES_TABLE} WHERE product_id={product_id}")
    product_images_connection.commit()

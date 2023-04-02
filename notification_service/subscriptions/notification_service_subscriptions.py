import sqlite3

from authentication.users_db import USERS_TABLE
NOTIFICATION_SUBSCRIPTION_TABLE = "notification_subscriptions"

connection = sqlite3.connect("authentication/Users.db",
                             check_same_thread=False)
cursor = connection.cursor()


def init_notification_subscriptions_db_if_needed():
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {NOTIFICATION_SUBSCRIPTION_TABLE}("
                   f"id INTEGER PRIMARY KEY AUTOINCREMENT, "
                   f"subscriber_id INTEGER, "
                   f"subscription_id INTEGER"
                   f")")


def subscribe(subscriber_id, subscription_id):
    if subscriber_id == subscription_id: raise Exception("You cannot subscribe to yourself")

    subscription_from_db = cursor.execute(
        f"SELECT subscriber_id, subscription_id "
        f"FROM {NOTIFICATION_SUBSCRIPTION_TABLE} "
        f"WHERE subscription_id={subscription_id} AND subscriber_id={subscriber_id}"
    ).fetchone()
    if subscription_from_db: raise Exception("You're already subscribed to this user")

    subscription = (subscriber_id, subscription_id)
    cursor.execute(
        f"INSERT INTO "
        f"{NOTIFICATION_SUBSCRIPTION_TABLE}(subscriber_id, subscription_id) "
        f"VALUES(?,?);",
        subscription
    )
    connection.commit()


def unsubscribe(subscriber_id, subscription_id):
    print(subscriber_id, subscription_id)
    if subscriber_id == subscription_id: raise Exception("You cannot unsubscribe from yourself")

    subscription_from_db = cursor.execute(
        f"SELECT id, subscriber_id, subscription_id "
        f"FROM {NOTIFICATION_SUBSCRIPTION_TABLE} "
        f"WHERE subscription_id={subscription_id} AND subscriber_id={subscriber_id}"
    ).fetchone()
    if not subscription_from_db: raise Exception("You do not have a subscription to the user")

    (id, _, _) = subscription_from_db
    cursor.execute(
        f"DELETE FROM {NOTIFICATION_SUBSCRIPTION_TABLE} "
        f"WHERE subscriber_id={subscriber_id} AND subscription_id={subscription_id};",
    )
    connection.commit()


def get_subscriber_emails_by_user_id(id):
    return cursor.execute(
        f"SELECT {USERS_TABLE}.email "
        f"FROM {USERS_TABLE} "
        f"INNER JOIN {NOTIFICATION_SUBSCRIPTION_TABLE} "
        f"ON {USERS_TABLE}.id={NOTIFICATION_SUBSCRIPTION_TABLE}.subscriber_id "
        f"WHERE {NOTIFICATION_SUBSCRIPTION_TABLE}.subscription_id={id};"
    ).fetchall()

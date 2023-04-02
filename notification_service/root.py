from mail_service.root import send_message_to_admin_about_publishing_new_product, \
    send_message_to_user_about_approving_or_declining_the_product, \
    send_message_to_user_about_posting_new_product

from product.products_db import get_product_by_id

# todo think of this file and remove if it's redundant =>
#  => think of using mail service in notify_all_subscribers_about_publishing_product
from notification_service.subscriptions.notification_service_subscriptions import get_subscriber_emails_by_user_id


def notify_admin_about_publishing_new_product(publisher_email, product_id):
    (_, title, description, _, _, _) = get_product_by_id(product_id)
    send_message_to_admin_about_publishing_new_product(publisher_email, product_id, title, description)


def notify_user_about_approving_or_declining_the_product(owner, product, is_approved):
    send_message_to_user_about_approving_or_declining_the_product(owner, product, is_approved)


def notify_all_subscribers_about_publishing_product(owner_id, owner_email, product_id):
    subscribers = get_subscriber_emails_by_user_id(owner_id)
    (_, title, description, _, _, _) = get_product_by_id(product_id)
    for (subscriber,) in subscribers:
        send_message_to_user_about_posting_new_product(
            owner=owner_email,
            subscriber_email=subscriber,
            title=title,
            desc=description
        )

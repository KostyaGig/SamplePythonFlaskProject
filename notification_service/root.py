from mail_service.root import send_message_to_admin_about_publishing_new_product

def notify_admin_about_publishing_new_product(publisher_email, product_id):
    send_message_to_admin_about_publishing_new_product(publisher_email, product_id)

def notify_user_about_approving_or_declining_the_product(owner, product, is_approved):
    notify_user_about_approving_or_declining_the_product(owner, product, is_approved)

# todo create notification_subscription db |_id| subscriber_email | |subscription |
def subscribe_user_to_new_products_of(subscriber, subscription):
    pass

# todo find all subscribers by subscription_email and push messages to them
def notify_all_subscribers_about_publishing_product(owner):
    pass

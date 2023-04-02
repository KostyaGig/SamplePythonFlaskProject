from flask import *
from authentication.authentication import register_print, login_print
from authentication.users_db import init_users_db_if_needed
from authentication.activation import activation_print
from authentication.authorizationmiddleware import AuthorizationMiddleWare
from notification_service.routers import subscribe_to_user_changes, unsubscribe_from_user_changes
from notification_service.subscriptions.notification_service_subscriptions import \
    init_notification_subscriptions_db_if_needed
from product.event.product_publisher import subscribe_to_product_events

from product.products_db import init_products_db_if_needed
from product.images.product_images_db import init_product_images_db_if_needed
from product.history_modification.product_modifications_db import init_product_modifications_db_if_needed

from product.crud_product import post_product_print, delete_product_print, update_product_print, modify_product_print
app = Flask(__name__)


"""
    Set up auth
"""
app.wsgi_app = AuthorizationMiddleWare(app.wsgi_app)
app.register_blueprint(register_print)
app.register_blueprint(login_print)
app.register_blueprint(activation_print)

"""
    Set up products
"""
app.register_blueprint(post_product_print)
app.register_blueprint(update_product_print)
app.register_blueprint(delete_product_print)
app.register_blueprint(modify_product_print)

@app.route("/")
def root():
    return "Server is running..."

if __name__ == '__main__':
    init_users_db_if_needed()
    init_products_db_if_needed()
    init_product_images_db_if_needed()
    init_product_modifications_db_if_needed()
    subscribe_to_product_events()
    app.run(debug=True)

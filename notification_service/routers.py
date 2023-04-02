from flask import Blueprint, request, json

from authentication.authorizationmiddleware import require_auth
from authentication.token import get_email_by_token
from authentication.users_db import get_user_by_email, get_user_by_id
from notification_service.subscriptions.notification_service_subscriptions import subscribe, unsubscribe

subscribe_to_user_changes = Blueprint('subscribe_to_user_changes', __name__)


@require_auth("subscribe_to_user_changes/post_product")
@subscribe_to_user_changes.route("/subscribe_to_user_changes/post_product", methods=['POST'])
def subscribe_to_post_products():
    try:
        owner = get_email_by_token(request.headers)
        data = json.loads(request.form.get("json", {}))
        subscription_id = data.get("subscription_id", -1)
        (subscriber_id, _, _, _, _, _) = get_user_by_email(owner)

        if not(isinstance(subscription_id, int)) or subscription_id < 0: raise Exception(f"User id is not corrected")
        if get_user_by_id(subscription_id) is None: raise Exception(f"User by {subscription_id} cannot be found")
        subscribe(subscriber_id, subscription_id)
        return "OK"
    except Exception as e:
        return f"Error occurred {e}"


unsubscribe_from_user_changes = Blueprint('unsubscribe_from_user_changes', __name__)


@require_auth("unsubscribe_from_user_changes/post_product")
@unsubscribe_from_user_changes.route("/unsubscribe_from_user_changes/post_product", methods=['POST'])
def unsubscribe_from_post_products():
    try:
        owner = get_email_by_token(request.headers)
        data = json.loads(request.form.get("json", {}))
        subscription_id = data.get("subscription_id", -1)
        (subscriber_id, _, _, _, _, _) = get_user_by_email(owner)

        if get_user_by_id(subscription_id) is None: raise Exception(f"User by {subscription_id} cannot be found")
        unsubscribe(subscriber_id, subscription_id)
        return "OK"
    except Exception as e:
        return f"Error occurred {e}"

from flask import Blueprint
from flask import request
import json

from authentication.authorizationmiddleware import require_auth
from authentication.token import get_email_by_token
from authentication.users_db import get_user_by_email
from product.product_status import ProductStatus
from product.products_db import insert_product_in_db, update_product_in_db, delete_product_from_db
from product.validation import valid_post_product, valid_update_product, valid_delete_product
from product.images.image_service.service import upload_image

post_product_print = Blueprint('post', __name__)


@require_auth("/post")
@post_product_print.route("/post", methods=['POST'])
def post_product():
    try:
        data = json.loads(request.form.get("json", {}))

        owner = get_email_by_token(request.headers)
        user = get_user_by_email(owner)

        (_, _, _, is_active, _) = user
        if is_active == 0: return "Please, active your account to post the product"

        description = data.get('description', '')
        title = data.get('title', '')

        images = request.files.getlist("images")
        image_paths = []

        for image in images:
            if image:
                path = upload_image(image)
                image_paths.append(path)

        if valid_post_product(description, title):
            insert_product_in_db(owner, title, description, ProductStatus.ON_REVIEW, image_paths)
            return "OK"
        else:
            return "Description or title is empty"

    except Exception as e:
        return f"Error occurred {e}"


update_product_print = Blueprint('update', __name__)


@require_auth("/update")
@update_product_print.route("/update", methods=['POST'])
def update_product():
    try:
        data = json.loads(request.form.get("json", {}))

        owner = get_email_by_token(request.headers)
        product_id = data.get('product_id', -1)
        description = data.get('description', '')
        title = data.get('title', '')

        images = request.files.getlist("images")
        image_paths = []

        for image in images:
            if image:
                path = upload_image(image)
                image_paths.append(path)

        if valid_update_product(description, title, product_id):
            update_product_in_db(product_id, owner, title, description, ProductStatus.ON_REVIEW, image_paths)
            return "OK"
        else:
            return "Description, title, product id or status is not corrected"

    except Exception as e:
        return f"Error occurred {e}"


delete_product_print = Blueprint('delete', __name__)


@require_auth("/delete")
@delete_product_print.route("/delete", methods=['POST'])
def delete_product():
    try:
        data = json.loads(request.form.get("json", {}))
        owner = get_email_by_token(request.headers)
        product_id = data.get("product_id", -1)

        if valid_delete_product(product_id):
            delete_product_from_db(product_id, owner)
            return "OK"
        else:
            return "Product id is not corrected"
    except Exception as e:
        return f"Error occurred {e}"
from product.product_status import ProductStatus


def valid_post_product(description, title):
    return description and title


def valid_update_product(description, title, product_id):
    return valid_post_product(description, title) and product_id >= 0


def check_status(status):
    return status == ProductStatus.ON_REVIEW.value \
           or status == ProductStatus.APPROVED.value \
           or status == ProductStatus.DENIED.value


def valid_product_id_product(product_id):
    return product_id >= 0

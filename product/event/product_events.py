from abc import ABC
from enum import Enum


class ProductEventType(Enum):
    PUBLISHED = 0


class ProductEvent(ABC):

    def __init__(self, event_type: ProductEventType):
        self.event_type = event_type


class PostProductEvent(ProductEvent):

    def __init__(self, owner_email, owner_id, product_id):
        super().__init__(ProductEventType.PUBLISHED)
        self.owner_email = owner_email
        self.owner_id = owner_id
        self.product_id = product_id

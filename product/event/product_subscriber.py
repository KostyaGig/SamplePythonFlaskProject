from abc import ABC
from abc import abstractmethod

from product.event.product_events import ProductEvent


class ProductSubscriber(ABC):

    @abstractmethod
    def onEvent(self, event: ProductEvent): pass


class PublishProductSubscriber(ProductSubscriber):

    def onEvent(self, event: ProductEvent):
        print(f"PublishProductSubscriber -> {event} ")

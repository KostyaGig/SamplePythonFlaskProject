from abc import ABC
from abc import abstractmethod

from product.event.product_events import ProductEvent


class ProductEventSubscriber(ABC):

    @abstractmethod
    def onEvent(self, event: ProductEvent): pass

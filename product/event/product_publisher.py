from collections import defaultdict

from notification_service.product_notifier.publish_product_notifier import PublishProductNotifier
from product.event.product_events import ProductEvent, ProductEventType
from product.event.product_subscriber import ProductEventSubscriber


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ProductPublisher(metaclass=Singleton):

    def __init__(self):
        self.events_to_subscriber_dict = defaultdict()

    def subscribe(self, subscriber: ProductEventSubscriber, event: ProductEvent):
        subscribers_by_event = self.get_subscribers_by_event(event.event_type)
        subscribers_by_event.append(subscriber)
        self.events_to_subscriber_dict[event.event_type] = subscribers_by_event

    def send(self, event: ProductEvent):
        subscribers_by_event = self.get_subscribers_by_event(event.event_type)
        for subscriber in subscribers_by_event:
            subscriber.onEvent(event)

    def get_subscribers_by_event(self, event_type: ProductEventType) -> list:
        return self.events_to_subscriber_dict.get(event_type, [])

    def __str__(self):
        return str(self.events_to_subscriber_dict)


def subscribe_to_product_events():
    publisher = ProductPublisher()
    publisher.subscribe(PublishProductNotifier(), ProductEvent(ProductEventType.PUBLISHED))

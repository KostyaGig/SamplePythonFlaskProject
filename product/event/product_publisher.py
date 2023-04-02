from collections import defaultdict

from product.event.product_events import ProductEvent
from product.event.product_subscriber import ProductSubscriber

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class ProductPublisher(metaclass=Singleton):

    def __init__(self):
        self.events_to_subscriber_dict = defaultdict()

    def subscribe(self, subscriber: ProductSubscriber, event_type: ProductEvent):
        subscribers_by_event = self.get_subscribers_by_event(event_type)
        subscribers_by_event.append(subscriber)
        self.events_to_subscriber_dict[event_type] = subscribers_by_event

    def send(self, event: ProductEvent):
        subscribers_by_event = self.get_subscribers_by_event(event)
        for subscriber in subscribers_by_event:
            subscriber.onEvent(event)

    def get_subscribers_by_event(self, event: ProductEvent) -> list:
        return self.events_to_subscriber_dict.get(event, [])

    def __str__(self):
        return str(self.events_to_subscriber_dict)

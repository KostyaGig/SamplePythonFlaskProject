from product.event.product_events import ProductEvent, PostProductEvent
from product.event.product_subscriber import ProductEventSubscriber
from notification_service.root import *


class PublishProductNotifier(ProductEventSubscriber):

    def onEvent(self, event: ProductEvent):
        if isinstance(event, PostProductEvent):
            notify_admin_about_publishing_new_product(event.owner_email, event.product_id)
            notify_all_subscribers_about_publishing_product(
                owner_id=event.owner_id,
                owner_email=event.owner_email,
                product_id=event.product_id
            )

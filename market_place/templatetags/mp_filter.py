from django import template
from market_place.definitions import ItemStatus, OrderStatus

register = template.Library()


@register.filter(name='readable_item_status')
def readable_item_status(item_status_code: int):
    if isinstance(item_status_code, int):
        item_status = {_.value[0]: _.value[2] for _ in ItemStatus.__members__.values()}
        return item_status.get(item_status_code)
    else:
        return item_status_code


@register.filter(name='readable_order_status')
def readable_order_status(order_status_code: int) -> str:
    if isinstance(order_status_code, int):
        order_status = {_.value[0]: _.value[1] for _ in OrderStatus.__members__.values()}
        return order_status.get(order_status_code)
    else:
        return str(order_status_code)


@register.filter(name='order_progress_percentage')
def order_progress_percentage(order_status: int) -> int:
    if order_status == OrderStatus.Completed.value[0] or order_status == OrderStatus.Canceled.value[0]:
        return 100
    else:
        return int(order_status / (len(OrderStatus.__members__.values())-1) * 100)


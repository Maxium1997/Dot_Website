from django import template
from market_place.definitions import ItemStatus

register = template.Library()


@register.filter(name='readable_item_status')
def readable_item_status(code: int):
    if isinstance(code, int):
        item_status = {_.value[0]: _.value[2] for _ in ItemStatus.__members__.values()}
        return item_status.get(code)
    else:
        return code


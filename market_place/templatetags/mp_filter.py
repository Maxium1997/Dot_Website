from django import template
from market_place.definitions import CertificateUseFor

register = template.Library()


@register.filter(name='readable_use_for')
def readable_use_for(code: int):
    use_for = {_.value[0]: _.value[2] for _ in CertificateUseFor.__members__.values()}
    return use_for.get(code)

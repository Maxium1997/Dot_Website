from django import template
from organization.definitions import CBUnit, CPC4Unit

register = template.Library()


@register.filter(name='readable_CBUnit')
def readable_CBUnit(unit_code: int):
    cb_units = {_.value[0]: _.value[2] for _ in CBUnit.__members__.values()}
    return cb_units.get(unit_code)


@register.filter(name='readable_CPC4Unit')
def readable_CPC4Unit(unit_code: int):
    cpc4_units = {_.value[0]: _.value[2] for _ in CPC4Unit.__members__.values()}
    return cpc4_units.get(unit_code)

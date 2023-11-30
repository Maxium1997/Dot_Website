from django import template
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta
from business.definitions import CPC4Unit, StorageUnit, EquipmentType

register = template.Library()


@register.filter(name='readable_manage_unit')
def readable_manage_unit(unit_code: int):
    cpc4_units = {_.value[0]: _.value[2] for _ in CPC4Unit.__members__.values()}
    return cpc4_units.get(unit_code)


@register.filter(name='readable_storage_unit')
def readable_storage_unit(unit_code: int):
    storage_units = {_.value[0]: _.value[1] for _ in StorageUnit.__members__.values()}
    return storage_units.get(unit_code)


@register.filter(name='is_info_equip')
def is_info_equip(equip_code: int):
    if 1000 < equip_code < 2000:
        return True
    elif 2000 < equip_code < 3000:
        return False
    elif equip_code == 5000:
        return False
    else:
        return False

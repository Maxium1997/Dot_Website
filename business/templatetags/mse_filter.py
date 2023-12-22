from django import template
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta
from business.definitions import StorageUnit, EquipmentType
from organization.definitions import CBUnit, CPC4Unit, CPC4UnitVer2, ArmyCommission

register = template.Library()


@register.filter(name='readable_unit')
def readable_unit(unit_code: int):
    cpc4_units = {_.value[0]: _.value[2] for _ in CPC4Unit.__members__.values()}
    return cpc4_units.get(unit_code)


@register.filter(name='readable_cbunit')
def readable_cbunit(unit_code: int):
    cb_units = {_.value[0]: _.value[2] for _ in CBUnit.__members__.values()}
    return cb_units.get(unit_code)


@register.filter(name='readable_cpc4unit_ver2')
def readable_cpc4unit_ver2(unit_code: int):
    cpc4_units = {_.value[0]: _.value[2] for _ in CPC4UnitVer2.__members__.values()}
    return cpc4_units.get(unit_code)


@register.filter(name='readable_storage_unit')
def readable_storage_unit(unit_code: int):
    storage_units = {_.value[0]: _.value[1] for _ in StorageUnit.__members__.values()}
    return storage_units.get(unit_code)


@register.filter(name='is_info_equip')
def is_info_equip(equip_code: int):
    try:
        if 1000 < equip_code < 2000:
            return True
        elif 2000 < equip_code < 3000:
            return False
        elif equip_code == 5000:
            return False
        else:
            return False
    except:
        return False


@register.filter(name='readable_commission')
def readable_commission(commission_code):
    army_commission = {hex(_.value[0]): _.value[2] for _ in ArmyCommission.__members__.values()}
    try:
        hex_commission_code = hex(int(commission_code))
        return army_commission.get(hex_commission_code)
    except ValueError as e:
        print(f"Error: {e}")

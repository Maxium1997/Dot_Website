from django import template
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta
from business.definitions import StorageUnit, EquipmentType, CertificateUseFor
from organization.definitions import ArmyCommission

register = template.Library()


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


@register.filter(name='readable_use_for')
def readable_use_for(code: int):
    use_for = {_.value[0]: _.value[2] for _ in CertificateUseFor.__members__.values()}
    return use_for.get(code)

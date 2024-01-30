from django import template
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
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


@register.filter(name='readable_unit')
def readable_unit(serial_number: str) -> str:
    if serial_number is None:
        return str(None)
    else:
        try:
            if int(serial_number) == 0:
                return str("未選擇")
            else:
                pass
        except ValueError:
            return "Value Error."

    # Get the app configuration for the specified app
    app_config = apps.get_app_config('organization')
    # Get all models from the specified app
    app_models = app_config.get_models()
    # Name of the model to exclude
    model_to_exclude = 'BasicOrgInfo'
    # Filter models excluding the one specified
    filtered_models = [model for model in app_models if model.__name__ != model_to_exclude]

    for model in apps.get_app_config('organization').get_models():
        if model.__name__ == 'BasicOrgInfo':
            pass
        else:
            try:
                return model.objects.get(serial_number=serial_number)
            except ObjectDoesNotExist:
                pass

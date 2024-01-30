from datetime import datetime
from django import forms
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist

from .models import Order


class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

        # Get the app configuration for the specified app
        app_config = apps.get_app_config('organization')
        # Get all models from the specified app
        app_models = app_config.get_models()
        # Name of the model to exclude
        model_to_exclude = 'BasicOrgInfo'
        # Filter models excluding the one specified
        filtered_models = [model for model in app_models if model.__name__ != model_to_exclude]

        manage_unit_options = [(0, '請選擇單位')]
        for model in apps.get_app_config('organization').get_models():
            if model.__name__ == 'BasicOrgInfo':
                pass
            else:
                for item in model.objects.all():
                    if item.serial_number is None:
                        pass
                    else:
                        manage_unit_options.append((item.serial_number, item))

        self.fields['purchaser_unit'] = forms.ChoiceField(required=True,
                                                          choices=manage_unit_options,
                                                          widget=forms.Select(attrs={'class': 'form-control border-0'}))

        self.fields['purchaser'] = forms.CharField(required=True,
                                                   widget=forms.TextInput(attrs={'class': 'form-control border-0',
                                                                                 'placeholder': "Enter your name"}))
        self.fields['content'] = forms.CharField(required=True,
                                                 widget=forms.Textarea(attrs={'class': 'form-control'}))

    def save(self, commit=True):
        order = super(OrderForm, self).save(commit=False)

        if commit:
            order.save()
        return order

    class Meta:
        model = Order
        fields = ['purchaser_unit', 'purchaser', 'content']


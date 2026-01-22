import pytz
from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.views.generic import TemplateView
from django.db.models import Q

from .models import Item, Order, Record
from .definitions import ItemStatus, OrderStatus
# Create your views here.


class MarketPlaceView(TemplateView):
    template_name = 'market_place/index.html'


from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.db.models import Q

from .models import Item
from .definitions import ItemStatus
# Create your views here.


class MarketPlaceView(TemplateView):
    template_name = 'market_place/index.html'


class ItemIndexView(ListView):
    model = Item
    template_name = 'market_place/item/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemIndexView, self).get_context_data(object_list=None, **kwargs)
        items = list(set([_.name for _ in self.get_queryset()]))
        all_items = []

        for item in items:
            item_status_list = [item]
            for status in ItemStatus.__members__.values():
                criteria = Q(name__icontains=item) & Q(status__icontains=status.value[0])
                item_status_list.append(Item.objects.filter(criteria).count())
            all_items.append(item_status_list)

        context['item_status'] = ItemStatus.__members__.values()
        context['all_items'] = all_items

        return context

    def get_queryset(self):
        return Item.objects.all()


class ItemQueryView(ListView):
    model = Item
    template_name = 'market_place/item/query.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemQueryView, self).get_context_data(object_list=None, **kwargs)
        context['keyword'] = self.kwargs.get('item_name')
        context['query_items'] = self.get_queryset()
        return context

    def get_queryset(self):
        keyword = self.kwargs.get('item_name')
        return Item.objects.filter(name__icontains=keyword).order_by('category')


class ItemStatusQueryView(ListView):
    model = Item
    template_name = 'market_place/item/query.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemStatusQueryView, self).get_context_data(object_list=None, **kwargs)
        context['keyword'] = self.kwargs.get('item_status')
        context['query_items'] = self.get_queryset()
        return context

    def get_queryset(self):
        keyword = self.kwargs.get('item_status')
        return Item.objects.filter(status__icontains=keyword).order_by('category')

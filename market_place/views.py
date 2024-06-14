import pytz
from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView
from django.db.models import Q

from .models import Item, Order, Record
from .definitions import ItemStatus, OrderStatus
from .forms import OrderForm
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


class MaintenanceManagementView(TemplateView):
    template_name = 'market_place/MaintenanceManagement/index.html'


class OrderDashboardView(ListView):
    model = Order
    template_name = 'market_place/MaintenanceManagement/Order/dashboard.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OrderDashboardView, self).get_context_data(object_list=None, **kwargs)
        context['orders'] = self.get_queryset()
        return context

    def get_queryset(self):
        return Order.objects.all().order_by('status').order_by('-created_time')


class OrderDetailView(DetailView):
    model = Order
    template_name = 'market_place/MaintenanceManagement/Order/Detail.html'

    def get_object(self, queryset=None):
        serial_number = self.kwargs.get('serial_number')
        order = Order.objects.get(serial_number=serial_number)
        return order

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        order = self.get_object()
        context['order'] = order
        context['records'] = order.records.all()
        context['order_status'] = OrderStatus.__members__.values()
        return context


class ItemReportView(TemplateView):
    # model = Order
    template_name = 'market_place/Item/report.html'
    # fields = ['purchaser', 'content']
    # valid_message = "Successfully Reported."
    #
    # def get_form_class(self):
    #     return OrderForm
    #
    # def form_valid(self, form):
    #     today = datetime.now(pytz.timezone('Asia/Taipei'))
    #     get_today_order_nums = Order.objects.filter(created_time__year=today.year,
    #                                                 created_time__month=today.month,
    #                                                 created_time__day=today.day).count()
    #     serial_number = str(today.year) + '-' + str(today.month) + '-' + str(today.day) + '-' + \
    #                     str(get_today_order_nums+1).zfill(4)
    #
    #     form.instance.serial_number = serial_number
    #
    #     order = form.save()
    #
    #     Record.objects.create(
    #         content_type=ContentType.objects.get_for_model(order),
    #         object_id=order.id,
    #         content="Order created.",
    #         creator=order.serial_number,  # Set the creator information
    #     )
    #
    #     return super(ItemReportView, self).form_valid(form)


def order_confirm(request, serial_number):
    order = get_object_or_404(Order, serial_number=serial_number)

    if request.user.is_superuser:
        if order.status == OrderStatus.Pending.value[0]:
            order.status = OrderStatus.Confirmed.value[0]
            order.save()

            Record.objects.create(
                content_type=ContentType.objects.get_for_model(order),
                object_id=order.id,
                content="Order confirmed by {user}".format(user=request.user),
                creator=order.serial_number,  # Set the creator information
            )
            messages.success(request, "Order confirmed successfully.")
        else:
            messages.warning(request, "Order status is not pending, confirmed rejected.")
    else:
        messages.error(request, "Permission Denied.")
        # raise PermissionDenied

    return redirect('order_detail', serial_number=order.serial_number)


from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from learning_tree.models import Category, Subject
# Create your views here.


# class IndexView(TemplateView):
#     template_name = 'index.html'


class IndexView(ListView):
    template_name = 'index.html'
    model = Category

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data(object_list=None, **kwargs)
        context['categories'] = Category.objects.all()
        c_subjects = []
        for c in Category.objects.all():
            c_subjects.append([_ for _ in Subject.objects.filter(category=c)])
        context['c_subjects'] = c_subjects
        return context

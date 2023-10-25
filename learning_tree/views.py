from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DeleteView

from .models import Category, Subject

# Create your views here.


class CategoryView(ListView):
    model = Category
    template_name = 'learning_tree/category.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryView, self).get_context_data(object_list=None, **kwargs)
        category = get_object_or_404(Category, slug=self.kwargs.get('category_slug'))
        subjects = Subject.objects.filter(category=category,
                                          is_public=True)
        context['subjects'] = subjects
        context['categories'] = Category.objects.all()
        context['s_category'] = Category.objects.get(slug=self.kwargs.get('category_slug'))

        return context

    # def get_queryset(self):
        # category = get_object_or_404(Category, slug=self.kwargs.get('category_slug'))
        # return SubCategory.objects.filter(f=category)


class SubjectView(DeleteView):
    model = Subject
    template_name = 'learning_tree/subject.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SubjectView, self).get_context_data(object_list=None, **kwargs)
        context['subjects'] = Subject.objects.filter(category=self.get_object().category,
                                                     is_public=True)
        return context

    def get_object(self, queryset=None):
        subject = Subject.objects.get(slug=self.kwargs.get('subject_slug'))
        return subject

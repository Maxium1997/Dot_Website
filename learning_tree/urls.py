from django.urls import path, include

from .views import LearningTreeView, CategoryView, SubjectView

urlpatterns = [
    path('learning_tree', LearningTreeView.as_view(), name='learning_tree'),
    path('learning_tree/', include([
        path('<slug:category_slug>', CategoryView.as_view(), name='category'),
        path('<slug:category_slug>/', include([
            path('<slug:subject_slug>', SubjectView.as_view(), name='subject'),
        ])),
    ])),
]
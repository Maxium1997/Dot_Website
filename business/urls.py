from django.urls import path, include

from .views import BusinessView

urlpatterns = [
    path('business', BusinessView.as_view(), name='business'),
    # path('learning_tree/', include([
    #     path('<slug:category_slug>', CategoryView.as_view(), name='category'),
    #     path('<slug:category_slug>/', include([
    #         path('<slug:subject_slug>', SubjectView.as_view(), name='subject'),
    #     ])),
    # ])),
]
from django.urls import path
from django.views.generic import TemplateView
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('list-host/', views.HostListView.as_view()),
    path('list-vm/', views.VMListView.as_view()),
    path('list-storage/', views.StorageListView.as_view()),
    path('list-os/', views.OSListView.as_view()),
    path('add-host/', views.HostAddView.as_view()),
    path('add-vm/', views.VirtualAddView.as_view()),
    path('add-storage/', views.StorageAddView.as_view()),
    path('add-os/', views.OSAddView.as_view()),

    path('script-list-os', views.list, name='list'),
    path('', TemplateView.as_view(template_name='index.html')),
    path('script-add-os', views.add_row, name='add_row'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('list-host/', views.HostListView.as_view()),
    path('list-vm/', views.VMListView.as_view()),
    path('list-storage/', views.StorageListView.as_view()),
    path('list-os/', views.OSListView.as_view()),
    path('add-storage/', views.StorageAddView.as_view()),
    path('add-os/', views.OSAddView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
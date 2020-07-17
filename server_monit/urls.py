from django.urls import path
from django.views.generic import TemplateView
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('list-host/', views.HostListView.as_view()),
    path('list-vm/', views.VMListView.as_view()),
    path('list-storage/', views.StorageListView.as_view()),
    path('list-os/', views.OSListView.as_view()),
    path('list-type-storage/', views.TypeStorageListView.as_view()),
    path('list-host-storage/', views.HostListStorageView.as_view()),
    path('list-select-host/', views.HostSelectView.as_view()),
    path('list-family/', views.FamilyListView.as_view()),
    path('list-capacity/', views.CapacityListView.as_view()),
    path('host/<int:pk>', views.HostDetailView.as_view()),
    path('vm/<int:pk>', views.VMDetailView.as_view()),
    path('add-host/', views.HostAddView.as_view()),
    path('add-vm/', views.VirtualAddView.as_view()),
    path('add-storage/', views.StorageAddView.as_view()),
    path('add-os/', views.OSAddView.as_view()),
    path('update-host/<int:pk>', views.HostEditView.as_view()),
    path('update-vm/<int:pk>', views.VMEditView.as_view()),
    path('update-storage/<int:pk>', views.StorageEditView.as_view()),
    path('update-os/<int:pk>', views.OSEditView.as_view()),
    path('delete-host/<int:pk>', views.HostDeleteView.as_view()),
    path('delete-vm/<int:pk>', views.VirtualDeleteView.as_view()),
    path('delete-storage/<int:pk>', views.StorageDeleteView.as_view()),
    path('delete-os/<int:pk>', views.OSDeleteView.as_view()),
    path('script-list-os/', views.list, name='list'),
    path('', TemplateView.as_view(template_name='index.html')),
    path('script-add-os/', views.add_row, name='add_row'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

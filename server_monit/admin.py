from django.contrib import admin
from .models import (TypeStorageModel,
                     StorageModel,
                     HostModel,
                     VirtualModel,
                     CapacityModel,
                     OSModel,
                     FamilyOSModel,)

@admin.register(TypeStorageModel)
class TypeStorageAdmin(admin.ModelAdmin):
    list_display = ('type_storage',)


@admin.register(StorageModel)
class StorageAdmin(admin.ModelAdmin):
      list_display = ('model', 'type_storage', 'size_storage', 'inv', 'date_install')
      search_fields = ('model', 'inv', 'date_install')
      list_filter = ('model', 'type_storage', 'size_storage')


@admin.register(HostModel)
class HostAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip', 'os',  'cpu', 'memory')
    search_fields = ('name', 'ip')
    list_filter = ('cpu', 'memory')


@admin.register(VirtualModel)
class VirtualAdmin(admin.ModelAdmin):
    list_display = ('host', 'name', 'ip', 'os', 'cores', 'threads', 'memory', 'storage_size')
    search_fields = ('name', 'ip', 'host')
    list_filter = ('host', 'cores', 'threads', 'memory', 'storage_size')


@admin.register(CapacityModel)
class CapacityAdmin(admin.ModelAdmin):
    list_display = ('bit',)


@admin.register(FamilyOSModel)
class FamilyOSAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(OSModel)
class OSAdmin(admin.ModelAdmin):
    list_display = ('family', 'os', 'capacity')
    list_filter = ('family', 'capacity')
    search_fields = ('os',)


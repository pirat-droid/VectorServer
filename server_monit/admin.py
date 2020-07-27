from django.contrib import admin
from .models import (TypeStorageModel,
                     StorageModel,
                     HostModel,
                     VirtualModel,
                     CapacityModel,
                     OSModel,
                     FamilyOSModel,
                     CPUModel,
                     RAIDModel, )


@admin.register(CPUModel)
class AmtCPUAdmin(admin.ModelAdmin):
    list_display = ('amt_cpu',)


@admin.register(RAIDModel)
class AmtCPUAdmin(admin.ModelAdmin):
    list_display = ('type_raid',)


@admin.register(TypeStorageModel)
class TypeStorageAdmin(admin.ModelAdmin):
    list_display = ('type_storage',)

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.user = request.user
        obj.save()


@admin.register(StorageModel)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('model', 'type_storage', 'size_storage', 'inv', 'date_install')
    search_fields = ('model', 'inv', 'date_install')
    list_filter = ('model', 'type_storage', 'size_storage')


def save_model(self, request, obj, form, change):
    if getattr(obj, 'author', None) is None:
        obj.user = request.user
    obj.save()


@admin.register(HostModel)
class HostAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip', 'os', 'cpu', 'memory')
    search_fields = ('name', 'ip')
    list_filter = ('cpu', 'memory')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.user = request.user
        obj.save()


@admin.register(VirtualModel)
class VirtualAdmin(admin.ModelAdmin):
    list_display = ('host', 'name', 'ip', 'os', 'cores', 'threads', 'memory', 'storage_size')
    search_fields = ('name', 'ip', 'host')
    list_filter = ('host', 'cores', 'threads', 'memory', 'storage_size')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.user = request.user
        obj.save()


@admin.register(CapacityModel)
class CapacityAdmin(admin.ModelAdmin):
    list_display = ('bit',)

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.user = request.user
        obj.save()


@admin.register(FamilyOSModel)
class FamilyOSAdmin(admin.ModelAdmin):
    list_display = ('name',)

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.user = request.user
        obj.save()


@admin.register(OSModel)
class OSAdmin(admin.ModelAdmin):
    list_display = ('id', 'family', 'os', 'capacity')
    list_filter = ('family', 'capacity')
    search_fields = ('os',)

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.user = request.user
        obj.save()

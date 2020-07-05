from .models import TypeStorageModel, StorageModel, HostModel, VirtualModel
from rest_framework import serializers

class ListHostSerializer(serializers.ModelSerializer):
    """Сериализаия списка хостов"""
    class Meta:
        model = HostModel
        fields = ['name', 'ip', 'os']


class listVirtualSerializer(serializers.ModelSerializer):
    """Сериализация списка виртуалок"""
    class Meta:
        models = VirtualModel
        fields = ['name', 'ip', 'host', 'os']
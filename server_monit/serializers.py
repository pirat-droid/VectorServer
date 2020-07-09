from .models import (TypeStorageModel,
                     StorageModel,
                     HostModel,
                     VirtualModel,
                     OSModel,)
from rest_framework import serializers


class ListHostSerializer(serializers.ModelSerializer):
    """Сериализаия списка хостов"""
    os = serializers.CharField(source='os.__str__')

    class Meta:
        model = HostModel
        fields = ('id',
                  'name',
                  'ip',
                  'os',)


class DetailHostSerializer(serializers.ModelSerializer):
    """Сериализатор детального описания хоста"""

    class Meta:
        model = HostModel
        exclude = ['user', 'date_create']


class AddHostSerializer(serializers.ModelSerializer):
    """Сериализация добавления хоста"""
    date_create = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = HostModel
        fields = '__all__'


class ListVirtualSerializer(serializers.ModelSerializer):
    """Сериализация списка виртуалок"""
    os = serializers.CharField(source='os.__str__')
    host = serializers.CharField(source='host.name')

    class Meta:
        model = VirtualModel
        fields = ('name',
                  'ip',
                  'host',
                  'os',)


class DetailVirtualSerializer(serializers.ModelSerializer):
    """Сериализатор детального описания виртуальной машины"""

    class Meta:
        model = VirtualModel
        exclude = ['user', 'date_create']


class AddVirtualSerializer(serializers.ModelSerializer):
    """Сериализация добавления виртуальной машины"""
    date_create = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = VirtualModel
        fields = '__all__'


class ListStorageSerializer(serializers.ModelSerializer):
    """Сериализация списка накопителей"""
    type_storage = serializers.CharField(source='type_storage.type_storage')

    class Meta:
        model = StorageModel
        exclude = ['user', 'date_create']


class AddStorageSerializer(serializers.ModelSerializer):
    """Сериализация добавления накопителя"""
    date_create = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = StorageModel
        fields = '__all__'


class ListOSSerializer(serializers.ModelSerializer):
    """Сериализация спска операционных систем"""
    family = serializers.CharField(source='family.name')
    capacity = serializers.CharField(source='capacity.bit')

    class Meta:
        model = OSModel
        exclude = ['user', 'date_create']


class AddOSSerializer(serializers.ModelSerializer):
    """Сериализация добавление операционной системы"""
    date_create = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = OSModel
        fields = '__all__'
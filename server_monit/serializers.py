from .models import (TypeStorageModel,
                     StorageModel,
                     HostModel,
                     VirtualModel,
                     OSModel,
                     FamilyOSModel,
                     CapacityModel,)
from rest_framework import serializers


class ListStorageSerializer(serializers.ModelSerializer):
    """Сериализация списка накопителей"""
    type_storage = serializers.CharField(source='type_storage.type_storage')

    class Meta:
        model = StorageModel
        fields = ['id',
                  'model',
                  'inv',
                  'size_storage',
                  'type_storage',
                  'date_install',
                  'description',
                  'host']


class ListVirtualInHostSerializer(serializers.ModelSerializer):
    """Сериализация списка виртуальных машин в хосте"""
    os = serializers.CharField(source='os.__str__')

    class Meta:
        model = VirtualModel
        fields = ('id',
                  'name',
                  'ip',
                  'cores',
                  'threads',
                  'storage_size',
                  'memory',
                  'os',
                  'description',)


class ListHostSerializer(serializers.ModelSerializer):
    """Сериализаия списка хостов"""
    # storage = ListStorageSerializer(read_only=True, many=True)
    os = serializers.CharField(source='os.__str__')
    amt_cpu = serializers.IntegerField(source='amt_cpu.amt_cpu')

    class Meta:
        model = HostModel
        fields = '__all__'

class ListSelectHostSerializer(serializers.ModelSerializer):
    """Сериализаия списка хостов при добавлении или изменении виртуальной машины"""
    os = serializers.CharField(source='os.__str__')

    class Meta:
        model = HostModel
        fields = ['id',
                  'name',
                  'os',
                  'ip',
                  ]


class DetailHostSerializer(serializers.ModelSerializer):
    """Сериализатор детального описания хоста"""
    storage = ListStorageSerializer(read_only=True, many=True)
    os = serializers.CharField(source='os.__str__')
    virtuals = ListVirtualInHostSerializer(read_only=True, many=True)
    amt_cpu = serializers.IntegerField(source='amt_cpu.amt_cpu')

    class Meta:
        model = HostModel
        fields = '__all__'


class AddHostSerializer(serializers.ModelSerializer):
    """Сериализация добавления хоста"""

    class Meta:
        model = HostModel
        fields = '__all__'


class ListVirtualSerializer(serializers.ModelSerializer):
    """Сериализация списка виртуалок"""
    os = serializers.CharField(source='os.__str__')
    host = serializers.CharField(source='host.name')

    class Meta:
        model = VirtualModel
        fields = '__all__'


# class DetailVirtualSerializer(serializers.ModelSerializer):
#     """Сериализатор детального описания виртуальной машины"""
#     os = serializers.CharField(source='os.__str__')
#     host = serializers.CharField(source='host.name')
#
#     class Meta:
#         model = VirtualModel
#         exclude = ['user', 'date_create']


class AddVirtualSerializer(serializers.ModelSerializer):
    """Сериализация добавления виртуальной машины"""

    class Meta:
        model = VirtualModel
        fields = '__all__'


class ListTypeStorageSerializer(serializers.ModelSerializer):
    """Сериализация списка типов накопителей"""

    class Meta:
        model = TypeStorageModel
        fields = ['id', 'type_storage']

class AddStorageSerializer(serializers.ModelSerializer):
    """Сериализация добавления накопителя"""

    class Meta:
        model = StorageModel
        fields = '__all__'


class ListOSSerializer(serializers.ModelSerializer):
    """Сериализация спска операционных систем"""
    family = serializers.CharField(source='family.name')
    capacity = serializers.CharField(source='capacity.bit')

    class Meta:
        model = OSModel
        fields = '__all__'


class ListFamilySerializer(serializers.ModelSerializer):
    """Сериализация списка семейств ос"""

    class Meta:
        model = FamilyOSModel
        fields = '__all__'


class ListCapacitySerializer(serializers.ModelSerializer):
    """Сериализация списка разрядности ос"""

    class Meta:
        model = CapacityModel
        fields = '__all__'


class AddOSSerializer(serializers.ModelSerializer):
    """Сериализация добавление операционной системы"""

    class Meta:
        model = OSModel
        fields = '__all__'


class ListHostStorageSerializer(serializers.ModelSerializer):
    """Сериализация выбора хоста при добавлении или редактировании накопителя !!!!!!!!11"""

    class Meta:
        model = HostModel
        fields = ['id',
                  'name']
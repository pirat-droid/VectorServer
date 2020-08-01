from django.db import models
from django.contrib.auth.models import User


class ClusterModel(models.Model):
    name = models.CharField('Название кластера', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Кластер'
        verbose_name_plural = 'Кластеры'


class RAIDModel(models.Model):
    type_raid = models.CharField('Тип RAID массива', max_length=10)

    def __str__(self):
        return self.type_raid

    class Meta:
        verbose_name = 'RAID'
        verbose_name_plural = 'RAIDs'


class CapacityModel(models.Model):
    bit = models.CharField('Разрядность ОС', max_length=10)

    def __str__(self):
        return self.bit

    class Meta:
        verbose_name = 'Разрядность'
        verbose_name_plural = 'Разрядность'


class FamilyOSModel(models.Model):
    name = models.CharField('Имя семейства операциооной системы', max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Семейство'
        verbose_name_plural = 'Семейство'


class OSModel(models.Model):
    os = models.CharField('Назваание операционной системы', max_length=50)
    capacity = models.ForeignKey(CapacityModel, verbose_name='Разрядность ОС', on_delete=models.CASCADE)
    family = models.ForeignKey(FamilyOSModel, on_delete=models.CASCADE, verbose_name='Семейство операционной системы')

    def __str__(self):
        return f"{self.family} {self.os} {self.capacity}"

    class Meta:
        verbose_name = 'Операционная система'
        verbose_name_plural = 'Операционные системы'


class TypeStorageModel(models.Model):
    type_storage = models.CharField('Тип накопителя', max_length=50)

    def __str__(self):
        return self.type_storage

    class Meta:
        verbose_name = 'Тип накопителя'
        verbose_name_plural = 'Типы накопителей'


class CPUModel(models.Model):
    amt_cpu = models.PositiveSmallIntegerField('Количество процессоров на материнской плате')

    def __str__(self):
        return f"{self.amt_cpu}"

    class Meta:
        verbose_name = 'Количество процессоров'
        verbose_name_plural = 'Количество процессоров'


class HostModel(models.Model):
    name = models.CharField('Название хоста', max_length=50)
    os = models.ForeignKey(OSModel, on_delete=models.CASCADE, verbose_name='Операционная система')
    ip = models.CharField('IP адрес хоста', max_length=15)
    description = models.CharField('Описание хоста', max_length=500)
    cpu = models.CharField('Процессор', max_length=50)
    amt_cpu = models.ForeignKey(CPUModel, on_delete=models.CASCADE, default=1,
                                verbose_name='Количество процессоров на материнской плате')
    raid_controller = models.CharField('RAID контроллер', max_length=100)
    cluster = models.ForeignKey('self', verbose_name="Кластер", on_delete=models.SET_NULL, blank=True, null=True,
                                related_name="children")
    total_storage = models.PositiveSmallIntegerField('Общий объём накопителей', default=0)
    free_storage = models.PositiveSmallIntegerField('Свободное место на накопители', default=0, null=True)
    inv = models.CharField('Инвентарный номер', max_length=50, default='-')
    memory = models.PositiveSmallIntegerField('Объём оперативной памяти в гигабайтах')
    free_memory = models.PositiveSmallIntegerField('Свободный объём оперативной памяти', default=0, null=True)
    cluster = models.ForeignKey(ClusterModel, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Кластер')

    def __str__(self):
        return f"{self.name} - {self.ip} - {self.os}"

    class Meta:
        verbose_name = 'Хост'
        verbose_name_plural = 'Хосты'


class StorageModel(models.Model):
    model = models.CharField('Модель накопителя', max_length=50)
    serial_number = models.CharField('s/n', max_length=50)
    host = models.ForeignKey(HostModel, verbose_name='На каком хосте размещен', on_delete=models.CASCADE,
                             related_name='storage')
    size_storage = models.PositiveSmallIntegerField('Объём накопителя в гигабайтах', )
    type_storage = models.ForeignKey(TypeStorageModel, on_delete=models.CASCADE, verbose_name='Тип накопителя')
    date_install = models.DateField('Дата установки', null=True, blank=True)
    description = models.CharField('Пометки', max_length=500, null=True, blank=True)
    raid = models.ForeignKey(RAIDModel, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='RAID массив',
                             related_name='children')

    def __str__(self):
        return f"{self.model} - {self.size_storage}"

    class Meta:
        verbose_name = 'Накопитель'
        verbose_name_plural = 'Накопители'


class VirtualModel(models.Model):
    name = models.CharField('Название виртуального сервера', max_length=50)
    host = models.ForeignKey(HostModel, verbose_name='На каком хосте размещен', on_delete=models.CASCADE,
                             related_name='virtuals')
    ip = models.CharField('IP адрес виртуального сервера', max_length=15)
    os = models.ForeignKey(OSModel, on_delete=models.CASCADE, verbose_name='Операционная система')
    description = models.CharField('Описание виртуального сервера', max_length=500)
    cores = models.PositiveSmallIntegerField('Колличество ядер')
    threads = models.PositiveSmallIntegerField('Колличество потоков')
    memory = models.PositiveSmallIntegerField('Объём оперативной памяти в гигабайтах')
    storage_size = models.PositiveSmallIntegerField('Объём накопителя в гигабайтах')
    type_raid = models.ForeignKey('RAIDModel', null=True, blank=True, on_delete=models.CASCADE,
                                  verbose_name='Тип RAID массива')

    def __str__(self):
        return f"{self.name} - {self.ip} - {self.os}"

    class Meta:
        verbose_name = 'Виртуальный сервер'
        verbose_name_plural = 'Виртуальные сервера'

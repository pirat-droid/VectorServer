from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class CapacityModel(models.Model):
    bit = models.CharField('Разрядность ОС', max_length=10)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_create = models.DateTimeField('Дата создания', auto_now=True, blank=True)

    def __str__(self):
        return self.bit

    class Meta:
        verbose_name = 'Разрядность'
        verbose_name_plural = 'Разрядность'


class FamilyOSModel(models.Model):
    name = models.CharField('Имя семейства операциооной системы', max_length=20)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_create = models.DateTimeField('Дата создания', auto_now=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Семейство'
        verbose_name_plural = 'Семейство'


class OSModel(models.Model):
    os = models.CharField('Назваание операционной системы', max_length=50)
    capacity = models.ForeignKey(CapacityModel, verbose_name='Разрядность ОС', on_delete=models.CASCADE)
    family = models.ForeignKey(FamilyOSModel, on_delete=models.CASCADE, verbose_name='Семейство операционной системы')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_create = models.DateTimeField('Дата создания', auto_now=True, blank=True)

    def __str__(self):
        return f"{self.family} {self.os} {self.capacity}"

    class Meta:
        verbose_name = 'Операционная система'
        verbose_name_plural = 'Операционные системы'


class TypeStorageModel(models.Model):
    type_storage = models.CharField('Тип накопителя', max_length=50)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_create = models.DateTimeField('Дата создания', auto_now=True, blank=True)

    def __str__(self):
        return self.type_storage

    class Meta:
        verbose_name = 'Тип накопителя'
        verbose_name_plural = 'Типы накопителей'


class StorageModel(models.Model):
    model = models.CharField('Модель накопителя', max_length=50)
    inv = models.CharField('Инв. №', max_length=50)
    size_storage = models.PositiveSmallIntegerField('Объём накопителя в гигабайтах', )
    type_storage = models.ForeignKey(TypeStorageModel, on_delete=models.CASCADE, verbose_name='Тип накопителя')
    date_install = models.DateField('Дата установки', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_create = models.DateTimeField('Дата создания', auto_now=True, blank=True)

    def __str__(self):
        return f"{self.model} - {self.size_storage}"

    class Meta:
        verbose_name = 'Накопитель'
        verbose_name_plural = 'Накопители'


class HostModel(models.Model):
    name = models.CharField('Название хоста', max_length=50)
    os = models.ForeignKey(OSModel, on_delete=models.CASCADE, verbose_name='Операционная система')
    ip = models.CharField('IP адрес хоста', max_length=15)
    description = models.CharField('Описание хоста', max_length=500)
    cpu = models.CharField('Процессор', max_length=50)
    memory = models.PositiveSmallIntegerField('Объём оперативной памяти в гигабайтах')
    storage = models.ManyToManyField(StorageModel, verbose_name='Накопители')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_create = models.DateTimeField('Дата создания', auto_now=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.ip} - {self.os}"

    class Meta:
        verbose_name = 'Хост'
        verbose_name_plural = 'Хосты'


class VirtualModel(models.Model):
    name = models.CharField('Название виртуального сервера', max_length=50)
    host = models.ForeignKey(HostModel, verbose_name='На каком хосте размещен', on_delete=models.CASCADE)
    ip = models.CharField('IP адрес виртуального сервера', max_length=15)
    os = models.ForeignKey(OSModel, on_delete=models.CASCADE, verbose_name='Операционная система')
    description = models.CharField('Описание виртуального сервера', max_length=500)
    cores = models.PositiveSmallIntegerField('Колличество ядер')
    threads = models.PositiveSmallIntegerField('Колличество потоков')
    memory = models.PositiveSmallIntegerField('Объём оперативной памяти в гигабайтах')
    storage_size = models.PositiveSmallIntegerField('Объём накопителя в гигабайтах')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_create = models.DateTimeField('Дата создания', auto_now=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.ip} - {self.os}"

    class Meta:
        verbose_name = 'Виртуальный сервер'
        verbose_name_plural = 'Виртуальные сервера'

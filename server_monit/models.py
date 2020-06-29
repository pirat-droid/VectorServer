from django.db import models
from django.conf import settings

class TypeStorageModel(models.Model):
    type_storage =  models.CharField('Тип накопителя', max_length=50)

    def __str__(self):
        return self.type_storage

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'


class StorageModel(models.Model):
    model = models.CharField('Модель накопителя', max_length=50)
    inv = models.CharField('Инв. №', max_length=50)
    size_storage = models.PositiveSmallIntegerField('Объём накопителя в гигабайтах',)
    type_storage = models.ManyToManyField(TypeStorageModel, verbose_name='Тип накопителя')
    date_install = models.DateField('Дата установки')

    def __str__(self):
        return {self.model - self.type_storage - self.size_storage}

    class Meta:
        verbose_name = 'Накопитель'
        verbose_name_plural = 'Накопители'


class HostModel(models.Model):
    name = models.CharField('Название хоста', max_length=50)
    ip = models.CharField('IP адрес хоста', max_length=15)
    description = models.CharField('Описание хоста', max_length=500)
    cpu = models.CharField('Процессор', max_length=50)
    memory = models.PositiveSmallIntegerField('Объём оперативной памяти в гигабайтах')
    storage = models.ManyToManyField(StorageModel, verbose_name='Накопители')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    date_create = models.DateTimeField('Дата создания', auto_now=True, blank=True)

    def __str__(self):
        return {self.name - self.ip}

    class Meta:
        verbose_name = 'Хост'
        verbose_name_plural = 'Хосты'

class VirtualModel(models.Model):
    name = models.CharField('Название виртуального сервера', max_length=50)
    ip = models.CharField('IP адрес виртуального сервера', max_length=15)
    description = models.CharField('Описание виртуального сервера', max_length=500)
    cores = models.PositiveSmallIntegerField('Колличество ядер')
    threads = models.PositiveSmallIntegerField('Колличество потоков')
    memory = models.PositiveSmallIntegerField('Объём оперативной памяти в гигабайтах')
    storage_size = models.PositiveSmallIntegerField('Объём накопителя в гигабайтах')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    date_create = models.DateTimeField('Дата создания', auto_now=True, blank=True)

    def __str__(self):
        return {self.name - self.ip}

    class Meta:
        verbose_name = 'Виртуальный сервер'
        verbose_name_plural = 'Виртуальные сервера'
from django.shortcuts import render
from datetime import datetime
from .models import (TypeStorageModel,
                     StorageModel,
                     HostModel,
                     VirtualModel,
                     CapacityModel,
                     OSModel,
                     FamilyOSModel, )
from .serializers import (ListHostSerializer,
                          ListVirtualSerializer,
                          ListStorageSerializer,
                          ListOSSerializer,
                          AddStorageSerializer,
                          AddOSSerializer,)
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class HostListView(APIView):

    """Вывод списка всех хостов"""
    def get(self, request):
        list = HostModel.objects.all()
        serializer = ListHostSerializer(list, many=True)
        return Response(serializer.data)


class VMListView(APIView):

    """Вывод списока всех виртуальных машин"""
    def get(self, request):
        list = VirtualModel.objects.all()
        serializer = ListVirtualSerializer(list, many=True)
        return Response(serializer.data)


class StorageListView(APIView):

    """Вывод списка накопителей"""
    def get(self, request):
        list = StorageModel.objects.all()
        serializer = ListStorageSerializer(list, many=True)
        return Response(serializer.data)


class StorageAddView(APIView):

    """Добавление накопителя"""
    def post(self, request):
        serializer = AddStorageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OSListView(APIView):

    """Вывод списка операционных систем"""
    def get(self, request):
        list = OSModel.objects.all()
        serializer = ListOSSerializer(list, many=True)
        return Response(serializer.data)


class OSAddView(APIView):

    """Добавление операционной системы"""
    def post(self, request):
        serializer = AddOSSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



"""
добавление накопителей, ос, виртуалок и хостов
тоже самое только на изменение и удаление
Добавить вывод виртуальных машин по хосту
"""

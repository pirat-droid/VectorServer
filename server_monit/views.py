import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from .parsing import parsing_hw
from .report import create_report

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
                          AddOSSerializer,
                          AddHostSerializer,
                          AddVirtualSerializer,
                          DetailHostSerializer,
    # DetailVirtualSerializer,
                          ListTypeStorageSerializer,
                          ListHostStorageSerializer,
                          ListFamilySerializer,
                          ListCapacitySerializer,
                          ListSelectHostSerializer)
from django.http import Http404, HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
import sqlite3
import xlsxwriter
from django.views.generic import View
import io


class MyView(View):

    def get(self, request):
        create_report()


class SearchStorage(View):
    """Поиск жестких дисков и RAID массивов"""

    def get(self, request):
        parsing_hw()
        return render(request, 'test.html')


def list(request):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    sql = 'SELECT * FROM server_monit_osmodel'
    cursor.execute(sql)
    sql = cursor.fetchall()
    data = {'data': sql}
    return render(request, 'test.html', context=data)


def add_row(request):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    sql = 'SELECT id FROM server_monit_osmodel ORDER BY id DESC LIMIT 1'
    cursor.execute(sql)
    sql = cursor.fetchall()
    id = sql[0]
    id = int(id[0]) + 1
    sql = "INSERT INTO server_monit_osmodel VALUES (" + str(id) + ", 'script', 1, 3, datetime('now'), 1)"
    cursor.execute(sql)
    # sql = cursor.fetchall()
    sql = 'SELECT * FROM server_monit_osmodel'
    cursor.execute(sql)
    conn.commit()
    sql = cursor.fetchall()
    conn.close()
    data = {'data': sql}
    return render(request, 'test.html', context=data)


class HostListView(APIView):
    """Вывод списка всех хостов"""

    def get(self, request):
        list = HostModel.objects.all()
        serializer = ListHostSerializer(list, many=True)
        return Response(serializer.data)


class HostAddView(APIView):
    """Добавление хоста"""

    def post(self, request):
        serializer = AddHostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HostDetailView(APIView):
    """Детальное описание хоста"""

    def get_object(self, pk):
        try:
            return HostModel.objects.get(pk=pk)
        except HostModel.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        detail = self.get_object(pk)
        serializer = DetailHostSerializer(detail)
        return Response(serializer.data)


class HostEditView(APIView):
    """Изменение хоста"""

    def get_object(self, pk):
        try:
            return HostModel.objects.get(pk=pk)
        except HostModel.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        edit = self.get_object(pk)
        serializer = AddHostSerializer(edit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HostDeleteView(APIView):
    """Удаление хоста"""

    def get_object(self, pk):
        try:
            return HostModel.objects.get(pk=pk)
        except HostModel.DoesNotExist:
            raise Http404

    def delete(self, request, pk):
        delete = self.get_object(pk)
        delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VMListView(APIView):
    """Вывод списока всех виртуальных машин"""

    def get(self, request):
        list = VirtualModel.objects.all()
        serializer = ListVirtualSerializer(list, many=True)
        return Response(serializer.data)


class VMDetailView(APIView):
    """Детальное описание виртуальной машины"""

    def get_object(self, pk):
        try:
            return VirtualModel.objects.get(pk=pk)
        except VirtualModel.DoesNotExist:
            raise Http404

    # def get(self, request, pk):
    #     detail = self.get_object(pk)
    #     serializer = DetailVirtualSerializer(detail)
    #     return Response(serializer.data)


class VMEditView(APIView):
    """Изменение виртуальной машины"""

    def get_object(self, pk):
        try:
            return VirtualModel.objects.get(pk=pk)
        except VirtualModel.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        edit = self.get_object(pk)
        serializer = AddVirtualSerializer(edit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VirtualAddView(APIView):
    """Добавление виртуальной машины"""

    def post(self, request):
        serializer = AddVirtualSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VirtualDeleteView(APIView):
    """Удаление виртуальной машины"""

    def get_object(self, pk):
        try:
            return VirtualModel.objects.get(pk=pk)
        except VirtualModel.DoesNotExist:
            raise Http404

    def delete(self, request, pk):
        delete = self.get_object(pk)
        delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StorageEditView(APIView):
    """Изменение накопителя"""

    def get_object(self, pk):
        try:
            return StorageModel.objects.get(pk=pk)
        except StorageModel.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        edit = self.get_object(pk)
        serializer = AddStorageSerializer(edit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StorageDeleteView(APIView):
    """Удаление накопителя"""

    def get_object(self, pk):
        try:
            return StorageModel.objects.get(pk=pk)
        except StorageModel.DoesNotExist:
            raise Http404

    def delete(self, request, pk):
        delete = self.get_object(pk)
        delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OSListView(APIView):
    """Вывод списка операционных систем"""

    def get(self, request):
        # conn = sqlite3.connect('db.sqlite3')
        # cursor = conn.cursor()
        # sql = 'SELECT id FROM server_monit_osmodel ORDER BY id DESC LIMIT 1'
        # cursor.execute(sql)
        # sql = cursor.fetchall()
        # id = sql[0]
        # id = int(id[0]) + 1
        # sql = "INSERT INTO server_monit_osmodel VALUES (" + str(id) + ", 'script', 1, 3, datetime('now'), 1)"
        # cursor.execute(sql)
        # # sql = cursor.fetchall()
        # sql = 'SELECT * FROM server_monit_osmodel'
        # cursor.execute(sql)
        # conn.commit()
        # sql = cursor.fetchall()
        # conn.close()

        list = OSModel.objects.all()
        serializer = ListOSSerializer(list, many=True)
        return Response(serializer.data)


class OSAddView(APIView):
    """Добавление операционной системы"""

    def post(self, request):
        serializer = AddOSSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OSEditView(APIView):
    """Изменение операционной системы"""

    def get_object(self, pk):
        try:
            return OSModel.objects.get(pk=pk)
        except OSModel.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        edit = self.get_object(pk)
        serializer = AddOSSerializer(edit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OSDeleteView(APIView):
    """Удаление операционной системы"""

    def get_object(self, pk):
        try:
            return OSModel.objects.get(pk=pk)
        except OSModel.DoesNotExist:
            raise Http404

    def delete(self, request, pk):
        delete = self.get_object(pk)
        delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TypeStorageListView(APIView):
    """Вывод списка типов накопителей"""

    def get(self, request):
        list = TypeStorageModel.objects.all()
        serializer = ListTypeStorageSerializer(list, many=True)
        return Response(serializer.data)


class HostListStorageView(APIView):
    """Вывод списка хостов при добавлении или изменении информации о накопителе"""

    def get(self, request):
        list = HostModel.objects.all()
        serializer = ListHostStorageSerializer(list, many=True)
        return Response(serializer.data)


class FamilyListView(APIView):
    """Вывод списка семейства ос"""

    def get(self, request):
        list = FamilyOSModel.objects.all()
        serializer = ListFamilySerializer(list, many=True)
        return Response(serializer.data)


class CapacityListView(APIView):
    """Вывод списка разрядности ос"""

    def get(self, request):
        list = CapacityModel.objects.all()
        serializer = ListCapacitySerializer(list, many=True)
        return Response(serializer.data)


class HostSelectView(APIView):
    """Вывод списка имени хостов"""

    def get(self, request):
        list = HostModel.objects.all()
        serializer = ListSelectHostSerializer(list, many=True)
        return Response(serializer.data)

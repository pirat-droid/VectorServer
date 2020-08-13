import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from datetime import datetime

import xlsxwriter
from django.http import HttpResponse
import io
from server_monit.models import StorageModel, VirtualModel, HostModel
from datetime import datetime

from .parsing import parsing_hw
from .report import create_report

from .models import (TypeStorageModel,
                     StorageModel,
                     HostModel,
                     VirtualModel,
                     CapacityModel,
                     OSModel,
                     FamilyOSModel,
                     CPUModel, )
from .serializers import (ListHostSerializer,
                          ListVirtualSerializer,
                          ListStorageSerializer,
                          ListOSSerializer,
                          AddStorageSerializer,
                          AddOSSerializer,
                          AddHostSerializer,
                          AddVirtualSerializer,
                          DetailHostSerializer,
                          ListCPUSerializer,
                          ListTypeStorageSerializer,
                          ListHostStorageSerializer,
                          ListFamilySerializer,
                          ListCapacitySerializer,
                          ListSelectHostSerializer,
                          HostVMSerializer)
from django.http import Http404, HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
import sqlite3
import xlsxwriter
from django.views.generic import View
import io



def get_simple_table_host():
    return ['№',
            'Название',
            'Процессор',
            'Кол-во процессоров',
            'RAID контроллер',
            'Объём накопителей',
            'Объём озу',
            'Операционная система',
            'IP адрес',
            'Инв.№',
            'Описание']

def get_simple_table_vm():
    return ['№',
            'Название',
            'Кол-во ядер',
            'Кол-во потоков',
            'Объём озу',
            'Операционная система',
            'IP адрес',
            'Объём накопителей',
            'Описание']

def get_simple_table_storage():
    return ['№',
            'Модель',
            'Тип',
            'Объём',
            'Дата установки',
            'Инв.№',
            'Описание']

def get_name_row_host():
    return ['name',
            'cpu',
            'amt_cpu',
            'raid',
            'memory',
            'os_id',
            'ip',
            'serial_number',
            'description']

def report(self):
    output = io.BytesIO()

    workbook = xlsxwriter.Workbook(output)

    workbook.set_properties({
        'title': 'This is the server hardware report',
        'subject': 'With document properties',
        'author': 'Pirate',
        'manager': 'Filibusters leader',
        'company': 'Tortuga',
        'category': 'Server',
        'keywords': 'Server, Virtual machine, Storage, Host',
        'created': datetime.now(),
        'comments': 'Designed for host and virtual machine inventory'})

    worksheet = workbook.add_worksheet()

    row = 0
    col = 0

    data = HostModel.objects.values_list('id',
                                         'name',
                                         'cpu',
                                         'amt_cpu',
                                         'raid_controller',
                                         'total_storage',
                                         'memory',
                                         'os_id',
                                         'ip',
                                         'inv',
                                         'description')

    data_host = get_simple_table_host()
    data_vm = get_simple_table_vm()
    data_storage = get_simple_table_storage()

    host_format = workbook.add_format({'bold': True})
    host_format.set_bg_color('green')

    description_row_host_format = workbook.add_format({'bold': True})
    description_row_host_format.set_bg_color('#81e781')
    description_row_host_format.set_text_wrap()

    number_description_row_host_format = workbook.add_format({'bold': True})
    number_description_row_host_format.set_bg_color('#81e781')
    number_description_row_host_format.set_text_wrap()
    number_description_row_host_format.set_align('center')
    number_description_row_host_format.set_align('vcenter')

    vm_format = workbook.add_format({'bold': True})
    vm_format.set_bg_color('#fdfd5a')

    description_row_vm_format = workbook.add_format({'bold': True})
    description_row_vm_format.set_bg_color('yellow')
    description_row_vm_format.set_text_wrap()

    description_number_row_vm_format = workbook.add_format({'bold': True})
    description_number_row_vm_format.set_bg_color('yellow')
    description_number_row_vm_format.set_text_wrap()
    description_number_row_vm_format.set_align('center')
    description_number_row_vm_format.set_align('vcenter')

    storage_format = workbook.add_format({'bold': True})
    storage_format.set_bg_color('red')

    description_row_storage_format = workbook.add_format({'bold': True})
    description_row_storage_format.set_bg_color('#fa4343')

    description_number_row_storage_format = workbook.add_format({'bold': True})
    description_number_row_storage_format.set_bg_color('#fa4343')
    description_number_row_storage_format.set_align('center')
    description_number_row_storage_format.set_align('vcenter')

    row_format = workbook.add_format()
    row_format.set_text_wrap()
    row_format.set_align('center')
    row_format.set_align('vcenter')

    worksheet.set_column('A:A', 3)
    worksheet.set_column('B:B', 10)
    worksheet.set_column('C:C', 15)
    worksheet.set_column('D:D', 15)
    worksheet.set_column('E:E', 17)
    worksheet.set_column('F:F', 19)
    worksheet.set_column('G:G', 10)
    worksheet.set_column('H:H', 15)
    worksheet.set_column('I:I', 15)
    worksheet.set_column('J:J', 25)
    worksheet.set_column('K:K', 30)

    # worksheet.set_row(2, 60)
    # worksheet.set_row(1, 30)

    s_n_host = 1
    s_n_vm = 1
    s_n_storage = 1

    for (id, name, cpu, amt_cpu, raid_controller, total_storage, memory, os_id, ip, inv, description) in (data):
        col = 0
        worksheet.merge_range(row, col, row, col + 10, 'Host', host_format)
        row += 1
        for row_name in data_host:
            worksheet.set_row(row, 30)
            worksheet.write(row, col, row_name, description_row_host_format)
            col += 1
        row += 1
        col = 0
        os_id = OSModel.objects.get(id=os_id)
        worksheet.set_row(row, 60)
        worksheet.write(row, col, s_n_host, number_description_row_host_format)
        worksheet.write(row, col + 1, name, row_format)
        worksheet.write(row, col + 2, cpu, row_format)
        worksheet.write(row, col + 3, amt_cpu, row_format)
        worksheet.write(row, col + 4, raid_controller, row_format)
        worksheet.write(row, col + 5, str(total_storage) + ' GB', row_format)
        worksheet.write(row, col + 6, str(memory) + ' GB', row_format)
        worksheet.write(row, col + 7, str(os_id), row_format)
        worksheet.write(row, col + 8, ip, row_format)
        worksheet.write(row, col + 9, inv, row_format)
        worksheet.write(row, col + 10, description, row_format)
        row += 1
        s_n_host += 1

        vm = VirtualModel.objects.filter(host=id).values_list('name', 'cores', 'threads', 'memory', 'os_id', 'ip',
                                                              'storage_size', 'description')

        if vm:
            worksheet.merge_range(row, col + 2, row, col + 10, 'Виртуальные машины', vm_format)

            row += 1
            col = 2
            worksheet.set_row(row, 30)
            for row_name in data_vm:
                worksheet.write(row, col, row_name, description_row_vm_format)
                col += 1

            row += 1

            for (name, cores, threads, memory, os, ip, storage_size, description) in vm:
                col = 0
                os = OSModel.objects.get(id=os)
                worksheet.set_row(row, 60)
                worksheet.write(row, col + 2, s_n_vm, description_number_row_vm_format)
                worksheet.write(row, col + 3, name, row_format)
                worksheet.write(row, col + 4, cores, row_format)
                worksheet.write(row, col + 5, threads, row_format)
                worksheet.write(row, col + 6, str(memory)+' GB', row_format)
                worksheet.write(row, col + 7, str(os), row_format)
                worksheet.write(row, col + 8, ip, row_format)
                worksheet.write(row, col + 9, str(storage_size)+' GB', row_format)
                worksheet.write(row, col + 10, description, row_format)
                row += 1
                s_n_vm += 1

        s_n_vm = 1
        storage = StorageModel.objects.filter(host=id).values_list('model', 'serial_number', 'size_storage',
                                                                   'type_storage',
                                                                   'date_install', 'description')

        if storage:
            col = 0
            worksheet.merge_range(row, col + 4, row, col + 10, 'Накопители', storage_format)
            row += 1
            col = 4

            for row_name in data_storage:
                worksheet.set_row(row, 30)
                worksheet.write(row, col, row_name, description_row_storage_format)
                col += 1

            row += 1

            for (model, serial_number, size_storage, type_storage, date_install, description) in storage:
                col = 0
                type_storage = TypeStorageModel.objects.get(id=type_storage)
                worksheet.set_row(row, 30)
                worksheet.write(row, col + 4, s_n_storage, description_number_row_storage_format)
                worksheet.write(row, col + 5, model, row_format)
                worksheet.write(row, col + 6, str(type_storage), row_format)
                worksheet.write(row, col + 7, str(size_storage) + ' GB', row_format)
                worksheet.write(row, col + 8, date_install, row_format)
                worksheet.write(row, col + 9, serial_number, row_format)
                worksheet.write(row, col + 10, description, row_format)
                s_n_storage += 1
                row += 1

        s_n_storage = 1

    workbook.close()

    output.seek(0)
    filename = 'Server_report.xlsx'

    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response


class SearchStorage(View):
    """Поиск жестких дисков и RAID массивов"""

    def get(self, request):
        parsing_hw()
        # host = HostModel.objects.filter(os=(OSModel.objects.filter(family=ily=1)))
        # print(host)
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


class CPUListView(APIView):
    """Вывод списка количества CPU"""

    def get(self, request):
        list = CPUModel.objects.all()
        serializer = ListCPUSerializer(list, many=True)
        return Response(serializer.data)


class HostAddView(APIView):
    """Добавление хоста"""

    def post(self, request):
        serializer = AddHostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HostVMView(APIView):
    """Список виртуальных машин хоста"""

    def get_object(self, pk):
        try:
            return HostModel.objects.get(pk=pk)
        except HostModel.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        detail = self.get_object(pk)
        serializer = HostVMSerializer(detail)
        return Response(serializer.data)


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

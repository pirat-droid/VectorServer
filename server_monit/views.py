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


def get_simple_table_host():
    return ['№',
            'название',
            'процессор',
            'Кол-во процессоров',
            'raid controller',
            'объём накопителей',
            'объём озу',
            'операционная система',
            'ip адрес',
            'Инв.№',
            'описание']


def get_simple_table_vm():
    return ['№',
            'название',
            'Кол-во ядер',
            'Кол-во потоков',
            'объём озу',
            'операционная система',
            'ip адрес',
            'объём накопителей',
            'описание']


def get_simple_table_storage():
    return ['№',
            'модель',
            'Тип',
            'Объём',
            'дата установки',
            'Инв.№',
            'описание']


def get_name_row_host():
    return ['name',
            'cpu',
            'amt_cpu',
            'raid',
            'memory',
            'os_id',
            'ip',
            'inv',
            'description']


class MyView(View):

    def get(self, request):

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
        print(data)

        data_host = get_simple_table_host()
        data_vm = get_simple_table_vm()
        data_storage = get_simple_table_storage()
        print(data_host)
        print(data_vm)
        print(data_storage)

        host_format = workbook.add_format({'bold': True})
        host_format.set_bg_color('green')
        description_row_host_format = workbook.add_format({'bold': True})
        description_row_host_format.set_bg_color('#81e781')
        vm_format = workbook.add_format({'bold': True})
        vm_format.set_bg_color('#fdfd5a')
        description_row_vm_format = workbook.add_format({'bold': True})
        description_row_vm_format.set_bg_color('yellow')
        storage_format = workbook.add_format({'bold': True})
        storage_format.set_bg_color('red')
        description_row_storage_format = workbook.add_format({'bold': True})
        description_row_storage_format.set_bg_color('#fa4343')

        s_n_host = 1
        s_n_vm = 1
        s_n_storage = 1

        for (id, name, cpu, amt_cpu, raid_controller, total_storage, memory, os_id, ip, inv, description) in (data):
            col = 0
            worksheet.merge_range(row, col, row, col + 10, 'Host', host_format)
            row += 1
            for row_name in data_host:
                worksheet.write(row, col, row_name, description_row_host_format)
                col += 1
            row += 1
            col = 0
            worksheet.write(row, col, s_n_host, description_row_host_format)
            worksheet.write(row, col + 1, name)
            worksheet.write(row, col + 2, cpu)
            worksheet.write(row, col + 3, amt_cpu)
            worksheet.write(row, col + 4, raid_controller)
            worksheet.write(row, col + 5, total_storage)
            worksheet.write(row, col + 6, memory)
            worksheet.write(row, col + 7, os_id)
            worksheet.write(row, col + 8, ip)
            worksheet.write(row, col + 9, inv)
            worksheet.write(row, col + 10, description)
            row += 1
            s_n_host += 1

            vm = VirtualModel.objects.filter(host=id).values_list('name', 'cores', 'threads', 'memory', 'os_id', 'ip', 'storage_size', 'description')

            if vm:
                worksheet.merge_range(row, col + 2, row, col + 10, 'Виртуальные машины', vm_format)

                row += 1
                col = 2

                for row_name in data_vm:
                    worksheet.write(row, col, row_name, description_row_vm_format)
                    col += 1

                row += 1

                for (name, cores, threads, memory, os, ip, storage_size, description) in vm:
                    col = 0
                    worksheet.write(row, col + 2, s_n_vm, description_row_vm_format)
                    worksheet.write(row, col + 3, name)
                    worksheet.write(row, col + 4, cores)
                    worksheet.write(row, col + 5, threads)
                    worksheet.write(row, col + 6, memory)
                    worksheet.write(row, col + 7, os)
                    worksheet.write(row, col + 8, ip)
                    worksheet.write(row, col + 9, storage_size)
                    worksheet.write(row, col + 10, description)
                    row += 1
                    s_n_vm += 1

            s_n_vm = 1
            storage = StorageModel.objects.filter(host=id).values_list('model', 'inv', 'size_storage', 'type_storage', 'date_install', 'description')

            if storage:
                col = 0
                worksheet.merge_range(row, col + 4, row, col + 10, 'Накопители', storage_format)
                row += 1
                col = 4

                for row_name in data_storage:
                    worksheet.write(row, col, row_name, description_row_storage_format)
                    col += 1

                row += 1

                for (model, inv, size_storage, type_storage, date_install, description) in storage:
                    col = 0
                    worksheet.write(row, col + 4, s_n_storage, description_row_storage_format)
                    worksheet.write(row, col + 5, model)
                    worksheet.write(row, col + 6, type_storage)
                    worksheet.write(row, col + 7, size_storage)
                    worksheet.write(row, col + 8, date_install)
                    worksheet.write(row, col + 9, inv)
                    worksheet.write(row, col + 10, description)
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

    def get(self, request, pk):
        detail = self.get_object(pk)
        serializer = DetailVirtualSerializer(detail)
        return Response(serializer.data)


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

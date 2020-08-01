import xlsxwriter
from django.http import HttpResponse
import io
from server_monit.models import StorageModel, VirtualModel, HostModel
from datetime import datetime


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
            'serial_number',
            'description']

def create_report():
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

            vm = VirtualModel.objects.filter(host=id).values_list('name', 'cores', 'threads', 'memory', 'os_id', 'ip',
                                                                  'storage_size', 'description')

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
            storage = StorageModel.objects.filter(host=id).values_list('model', 'serial_number', 'size_storage', 'type_storage',
                                                                       'date_install', 'description')

            if storage:
                    col = 0
                    worksheet.merge_range(row, col + 4, row, col + 10, 'Накопители', storage_format)
                    row += 1
                    col = 4

                    for row_name in data_storage:
                            worksheet.write(row, col, row_name, description_row_storage_format)
                            col += 1

                    row += 1

                    for (model, serial_number, size_storage, type_storage, date_install, description) in storage:
                            col = 0
                            worksheet.write(row, col + 4, s_n_storage, description_row_storage_format)
                            worksheet.write(row, col + 5, model)
                            worksheet.write(row, col + 6, type_storage)
                            worksheet.write(row, col + 7, size_storage)
                            worksheet.write(row, col + 8, date_install)
                            worksheet.write(row, col + 9, serial_number)
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
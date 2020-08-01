from server_monit.models import StorageModel
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import sqlite3
import logging

logging.basicConfig(level=logging.INFO, filename='Log.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def search_delete(value, page, sought):
    if sought is True:
        index = page.find(value)
        return page[:index]
    else:
        lenght = len(value)
        index = page.find(value)
        return page[index + lenght:]


def sql_connection():
    try:
        conn = sqlite3.connect('db.sqlite3')
        logging.info('DB open')
        return conn
    except:
        logging.error('DB not open')
        pass


def parsing_hw():
    # Подключаемся к базе данных
    conn = sql_connection()
    cursor = conn.cursor()
    # находим все хосты с операционной системой windows
    sql_host = '''SELECT ip, id FROM server_monit_hostmodel WHERE server_monit_hostmodel.os_id =
     (SELECT id FROM server_monit_osmodel WHERE server_monit_osmodel.family_id = 1)'''
    cursor.execute(sql_host)
    sql_host = cursor.fetchall()
    lenght_host = len(sql_host)
    logging.info('Найдено %s хостов', str(lenght_host))
    host_i = 0

    while host_i < lenght_host:
        sql_i = sql_host[host_i]
        # Извлекаем ip адрес
        host_ip = sql_i[0]
        # Извлекаем id
        host_id = sql_i[1]
        logging.info('IP адрес хоста - %s', host_ip)
        logging.info('ID хоста - %s', host_ip)
        host_i += 1

        url = 'https://' + host_ip + ':8444/SuperDoctor5/'
        # options = Options()
        # options.headless = True
        driver = webdriver.Chrome('/home/pirat/selenium/chromedriver')
        logging.info('Подключение драйвера chromium')
        # driver.maximize_window()
        # Авторизация
        driver.get(url + 'login')
        logging.info('Переход на сайт по адресу - https:// $s :8444/SuperDoctor5/login', url)
        time.sleep(1)
        driver.find_element_by_id("details-button").click()
        logging.info('Нажимаем на кнопку "Детали"')
        time.sleep(1)
        driver.find_element_by_id("proceed-link").click()
        logging.info('Подтверждаем переход')
        time.sleep(1)
        driver.find_element_by_name("username").send_keys('')
        driver.find_element_by_name("password").send_keys('')
        driver.find_element_by_name("signIn").click()
        logging.info('Вводим логин и парольб нажимаем на авторизацию')
        time.sleep(1)
        page = driver.page_source
        page = search_delete('<fieldset class="ok">', page, False)
        page = search_delete('<span class="legendSubTitle">', page, False)
        raid_controller = search_delete('<', page, True)
        logging.info('Имя RAID контролера - %s', raid_controller)
        # Ищем тип RAID массива
        page = search_delete('Raid Level:RAID ', page, False)
        raid_type = page[:1]
        logging.info('RAID контролер имеет тип - %s', raid_type)

        # Ищем жесткие диски
        driver.get(url + 'systemInfo')
        logging.info('Переходим по ссылки - %s \systeminfo', url)
        time.sleep(1)
        driver.find_element_by_xpath("//span[text()='Drives']").click()
        logging.info('Нажимаем на Drives')
        time.sleep(4)
        page = driver.page_source

        #     Начало ищем плюс для открытия списка, id постоянно меняется
        page = search_delete(
            '<th class="spec" style="width: 15px; text-align: center; vertical-align: middle" scope="col">', page, False)
        page = search_delete('<img id="', page, False)
        plus = search_delete('" src', page, True)
        logging.info('Имя кнопки - %s', plus)
        # Закончили искать плюс

        driver.find_element_by_id(plus).click()
        logging.info('Нажимаем на кнопку для разварачивания всех накопителей')
        time.sleep(4)
        page = driver.page_source
        page = search_delete('<th class="spec" scope="col" style="width: 25%;white-space: nowrap">Size</th>', page, False)

        value = '<td style="width: 15px; text-align: center; vertical-align: middle">'
        count: int = page.count(value)
        logging.info('Найденно %s накопителей', count)
        i = 0

        while i < count:
            page = search_delete('<td style="width: 15px; text-align: center; vertical-align: middle">', page, False)
            page = search_delete('<td><span>', page, False)
            page = search_delete('<td><span>', page, False)
            storage_model = search_delete('</span></td>', page, True)
            logging.info('Модель накопителя - %s', storage_model)
            page = search_delete('</span></td>', page, False)
            page = search_delete('<td><span>', page, False)
            storage_sn = search_delete('</span></td>', page, True)
            logging.info('Серийный номер накопителя - %s', storage_sn)
            page = search_delete('</span></td>', page, False)
            page = search_delete('<td style="white-space: nowrap">', page, False)
            storage_size = search_delete(' TB</td>', page, True)
            storage_size = storage_size.replace('.', '')
            logging.info('Размер накопителя - %s', storage_size)
            page = search_delete(' TB</td>', page, False)
            page = search_delete('<th scope="row" class="spec" width="30%"><span>Media Type</span>&nbsp;</th>', page, False)
            page = search_delete('<td><span>', page, False)
            storage_type = search_delete('</span>&nbsp;</td>', page, True)
            logging.info('Тип накопителя - %s', storage_type)
            page = search_delete('</span>&nbsp;</td>', page, False)

            if storage_type == 'SSD':
                storage_type = 1
            elif storage_type == 'HDD':
                storage_type = 2
            logging.info('Типу накопителя присвоен внешний ключ - %s', str(storage_type))

            if raid_type == 6:
                raid_type = 6
            elif raid_type == 0:
                raid_type = 1
            elif raid_type == 1:
                raid_type = 2
            elif raid_type == 3:
                raid_type = 3
            elif raid_type == 4:
                raid_type = 4
            elif raid_type == 0:
                raid_type = 1
            elif raid_type == '':
                raid_type = 5
            logging.info('Типу RAID массива присвоен внешний ключ - %s', str(raid_type))

            sql = StorageModel.objects.filter(serial_number=storage_sn)
            lenght = len(sql)
            if lenght == 0:
                sql = '''INSERT INTO server_monit_storagemodel(model, serial_number, host_id, size_storage,
                 type_storage_id, raid_id) VALUES (?,?,?,?,?,?)'''
                cursor.execute(sql, (storage_model, storage_sn, host_id, storage_size, storage_type, raid_type))
                conn.commit()
                logging.info('Добавлена новая запись')
            else:
                logging.info('Запись уже имеется в базе данных')
            i += 1

        #   Ищем общий объём и свободное место на диске
        driver.find_element_by_xpath("//span[text()='Onboard Controller']").click()
        logging.info('Нажимаем на "Onboard Controller"')
        time.sleep(4)
        page = driver.page_source
        page = search_delete('<div id="deviceTitle">Onboard Controller</div>', page, False)

        # Удаляем локальный диск 'C'
        page = search_delete('<td><span>Локальный несъемный диск</span></td>', page, False)
        page = search_delete('<td><span>Локальный несъемный диск</span></td>', page, False)
        logging.info('Удаляем локальный диск "c:/"')
        # Ищем локальные диски и складываем их

        value = 'Capacity: <span>'
        count: int = page.count(value)
        logging.info('Найденно %s локальных дисков', str(count))

        i = 0
        while i < count:
            # ищем обчий объём места на диске
            page = search_delete('Capacity: <span>', page, False)
            storage_size = search_delete(' GB<', page, True)
            logging.info('Объём локального диска - %s', storage_size)
            page = search_delete(' GB<', page, False)
            # Округляем до целых
            value = '.'
            index = storage_size.find(value)
            if index > 0:
                storage_size = storage_size[:index]
                logging.info('Локальный диск округлен до гигабайт - %s', storage_size)
            # total_size_storage += storage_size

            # ищем объём свободного места на диске
            page = search_delete('Free space: <span>', page, False)
            storage_free_size = search_delete(' GB<', page, True)
            logging.info('Найденно свободное место на локальном диске - %s', storage_free_size)
            page = search_delete(' GB<', page, False)
            # Округляем до целых
            value = '.'
            index = storage_free_size.find(value)
            if index > 0:
                storage_free_size = storage_free_size[:index]
                logging.info('Свободное место округленно до гигабайт - %s', storage_free_size)
            # total_storage_free_size = total_storage_free_size + storage_free_size

            i += 1

        # Ищем общий объём оперативной памятиы
        driver.find_element_by_xpath("//span[text()='Memory']").click()
        logging.info('Нажимаем "Memory"')
        time.sleep(4)
        page = driver.page_source
        page = search_delete('<th scope="row" class="spec">Total Physical Memory:</th>', page, False)
        page = search_delete('<td>', page, False)
        memory = search_delete(' GB<', page, True)
        logging.info('Объём оперативной памяти - %s', memory)
        # Закончили искать общий объём оперативной памяти

        sql = '''UPDATE server_monit_hostmodel
                 SET total_storage = ?,
                 free_storage = ?,
                 raid_controller = ?,
                 memory = ?
                 WHERE id = ?'''
        cursor.execute(sql, (storage_size, storage_free_size, raid_controller, memory, host_id))
        conn.commit()
        logging.info('Обновили данные по хосту')

    cursor.close()

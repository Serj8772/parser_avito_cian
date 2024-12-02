import zipfile

import fake_useragent
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import fake_useragent
import telebot
import csv

from settings1 import token, id_channel, link_avito

# настройка бота
bot = telebot.TeleBot(token)


# # вводим прокси
# PROXY_HOST = '185.111.24.31'
# PROXY_PORT = '8000'
# PROXY_USER = 'fdyrQf'
# PROXY_PASS = 'G7eMxA'

# подменяем user-agent
user_agent = fake_useragent.UserAgent(min_percentage=1.2).random

opts = webdriver.ChromeOptions()
opts.add_argument(user_agent)
opts.add_argument("--disable-blink-features=AutomationControlled")

opts.add_argument('--headless') # запуск в фоновом режиме

driver = webdriver.Chrome(options=opts)


while True:

    # загружаем ссылки из csv
    filename = 'links1.csv'
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        existing_rows = list(reader)

    try:
        driver.implicitly_wait(10)          # ожидание появление элемента в секундах

        # проверить анонимность:
        # driver.get("https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html")
        # driver.get("https://2ip.ru/")
        # time.sleep(200)

        #  ссылка на страницу поиска
        driver.get(link_avito) # заходим на сайт
        time.sleep(5)

        #https://www.avito.ru/lobnya/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?context=H4sIAAAAAAAA_wEjANz_YToxOntzOjg6ImZyb21QYWdlIjtzOjc6ImNhdGFsb2ciO312FITcIwAAAA
        #https://www.avito.ru/lobnya/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?context=H4sIAAAAAAAA_wEjANz_YToxOntzOjg6ImZyb21QYWdlIjtzOjc6ImNhdGFsb2ciO312FITcIwAAAA&f=ASgBAgICA0SSA8gQ8AeQUrCzFP6hjwM&s=104

        # ищем объявления
        ssilki = driver.find_elements(By.CLASS_NAME, value='iva-item-title-CdRXl')

        for ssilka in ssilki:
            link = ssilka.find_element(By.TAG_NAME, 'a')


            # проверяем есть ли строка в файле, если нет то записываем ссылку
            def write_to_csv(filename, data):

                if [data] not in existing_rows:
                    with open(filename, mode='a', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow(data)
                    print(data)
                    bot.send_message(id_channel, text=data) # отправляем через бота в канал

                else:
                    print('строка уже существует')


            data = link.get_attribute('href')
            write_to_csv('links1.csv', data)


    except Exception as ex:
        print(ex)

    time.sleep(30 * 60) # обновление данных каждые 30 минут
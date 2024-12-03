import zipfile

import fake_useragent
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import fake_useragent
import telebot
import csv

from settings import token, id_channel, link_avito, delay


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
    filename = 'links.csv'
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        existing_rows = list(reader)

    try:
        driver.implicitly_wait(5)          # ожидание появление элемента в секундах

        # проверить анонимность:
        # driver.get("https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html")
        # driver.get("https://2ip.ru/")
        # time.sleep(200)

        #  ссылка на страницу поиска
        driver.get(link_avito) # заходим на сайт
        time.sleep(5)
        driver.save_screenshot(f'screenshots/screenshot'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'.png')
        bot.send_message(id_channel, text=f'⚡️⚡️⚡️ СТАРТ ⚡️⚡️⚡️\n{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')

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
                        writer.writerow([data])
                    print(data, '--', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    bot.send_message(id_channel, text=data) # отправляем через бота в канал
                    time.sleep(5)

                else:
                    print('строка уже существует', '--', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


            data = link.get_attribute('href')
            write_to_csv(filename, data)


    except Exception as ex:
        print(ex)
        bot.send_message(id_channel, text=f'⚡️⚡️⚡️ Ошибка ⚡️⚡️⚡️\n{ex}')

    time.sleep(delay * 60)
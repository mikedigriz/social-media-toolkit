import csv
import random
import time
from time import sleep

import uiautomator2 as u2

# Автоматизация подсчета подписчиков страниц Instagram через телефон.
# Этот способ более безопасен, но лучше использовать аккаунт который не жалко потерять.
# У меня не было блокировок и ограничений, когда я использовал этот метод 1 раз в месяц на 100 аккаунтов.

# TODO На больших цифрах нужно будет приводить к единому формату данных

# USB - Connection
d = u2.connect('R58M31BXMNT')  # get name from "adb devices"
# WiFi - Connection
# d = u2.connect('192.168.1.130:5555')
file_time = time.strftime('_%m-%d %H-%M-%S')

account_list = [
    'mtb.woody',
    'metal',
    'wearepixelartworks'
]


def get_followers_count():
    followers_count_id = "com.instagram.android:id/row_profile_header_textview_followers_count"
    with open('Стата_соц_сеток_inst' + f'{file_time}.csv', 'w', encoding='utf8', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for account in account_list:
            try:
                d.open_url("https://instagram.com/" + account)
                sleep(random.uniform(0.3, 0.8))
                # Значение подписчиков
                followers = d(resourceId=followers_count_id).get_text()
                print(f'{account} подписано: {followers}')
                writer.writerow([account, followers])
            except Exception as ex:
                print(ex)
                print(f'{account} ошибка!')
                writer.writerow([account, ''])
                continue


start_time = time.time()
get_followers_count()
print("--- %s минут ---" % ((time.time() - start_time) / 60))

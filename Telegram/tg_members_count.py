import csv
import time
from time import sleep

import requests

# Считает кол-во подписчиков канала в TG, записывает в файлик

# Токен вида bot1234567890:Abcdifghijklmnopqrstuvwxyz123456789
token = "bot**********:***********************************"

# Список пабликов для подсчета
channel_list = ["@tass_agency",
                "@bazabazon",
                "@radiogovoritmsk",
                "@karaulny",
                "@breakingmash",
                ]

# Задержка в сек. между запросами
delay = 2

file_time = time.strftime('_%m-%d %H-%M-%S')

with open('Каналы в TG от' + f'{file_time}.csv', 'w', newline='', encoding='utf8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Каналы TG и кол-во подписчиков:'])

    for channel in channel_list:
        try:
            if channel != "null":
                sleep(delay)
                get_members_count = requests.get(
                    f'https://api.telegram.org/{token}/getChatMemberCount?chat_id={channel}').json()
                print(channel + " " + f"{get_members_count['result']}")
                writer.writerow([channel, get_members_count['result']])
            else:
                writer.writerow([channel])
        except Exception as e:
            writer.writerow([channel, "Ошибка"])
            print([channel], e)

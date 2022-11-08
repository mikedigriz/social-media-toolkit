import csv
import time
from time import sleep

import vk

# Возвращает список участников сообщества.

# TODO зачем мне сторонняя библиотека, когда есть requests? Переписать.

# Как получить access_token:
# https://oauth.vk.com/authorize?client_id=******&display=page&scope=friends&response_type=token&v=5.131
# client_id это id приложения VK. Лучше создать свое приложение или использовать чужой client_id, например KateMobile.

# Параметры:
access_token = ''
v = '5.131'

# Подключение к VK API
session = vk.Session(access_token=access_token)
api = vk.API(session, v=v)

group = 'progrocknews'


def vk_user_in_group():
    offset = 0
    with open('vk_user_in_group.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        while True:
            vk_group_get_user = api.groups.getMembers(group_id=group, sort='time_asc', count=1000, offset=offset)
            sleep(0.5)
            for ids in vk_group_get_user['items']:
                print(ids)
                writer.writerow([ids])
            offset += 1000
            # задать количество подписчиков для остановки
            if offset >= 3000:
                break


start_time = time.time()
vk_user_in_group()
print("--- %s минут ---" % ((time.time() - start_time) / 60))

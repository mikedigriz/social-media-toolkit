import csv
import time
from time import sleep

import vk

# Подсчет участников в сообществах VK

# Как получить access_token:
# https://oauth.vk.com/authorize?client_id=******&display=page&scope=friends&response_type=token&v=5.131
# client_id это id приложения VK. Лучше создать свое приложение или использовать чужой client_id, например KateMobile.

# Параметры:
access_token = ''
v = '5.131'
file_time = time.strftime('_%m-%d %H-%M-%S')

# Подключение к VK API
session = vk.Session(access_token=access_token)
api = vk.API(session, v=v)

group_list = [
    'page1', 'page2'
]


def vk_groups_count_members():
    with open('Стата_соц_сеток_VK' + f'{file_time}.csv', 'w', newline='', encoding='utf8') as csv_file:
        writer = csv.writer(csv_file)
        for group in group_list:
            sleep(0.4)
            try:
                vk_groups = api.groups.getMembers(group_id=group, count=0)
                print(group, vk_groups['count'])
                writer.writerow([group, vk_groups['count']])
            except vk.exceptions.VkAPIError:
                print(f'Проблема с id: {group}')
                writer.writerow([group, ''])
                continue


start_time = time.time()
vk_groups_count_members()
print("--- %s минут ---" % ((time.time() - start_time) / 60))

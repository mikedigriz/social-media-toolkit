import csv
import time
from time import sleep

import vk

# Преобразование ника в id VK

# client_id это id приложения VK. Лучше создать свое приложение или использовать чужой client_id, например KateMobile.
# https://oauth.vk.com/authorize?client_id=******&display=page&scope=friends&response_type=token&v=5.131
access_token = ''
v = '5.131'
file_time = time.strftime('_%m-%d %H-%M-%S')

# Подключение к VK API
session = vk.Session(access_token=access_token)
api = vk.API(session, v=v)

id_list = [
    'durov',
    'mikedigriz'
]


def get_real_id():
    with open('vk_ids' + f'{file_time}.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for user in id_list:
            sleep(0.5)
            try:
                vk_users = api.users.get(user_ids=user)[0]
                get_id = vk_users['id']
                writer.writerow([user, get_id])
                print(get_id)
            except vk.exceptions.VkAPIError and Exception:
                print(f'Проблема с id: {user}')
                writer.writerow([user, ''])
                continue


get_real_id()
